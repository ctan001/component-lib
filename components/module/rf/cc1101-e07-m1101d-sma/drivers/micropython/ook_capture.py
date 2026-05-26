"""
ook_capture.py — OOK pulse capture and decode for CC1101 async mode

Usage:
    from ook_capture import OOKCapture
    cap = OOKCapture(gdo0_pin=6)
    cap.start_rx()
    pulses = cap.wait_capture(timeout_ms=5000)
    result = cap.decode(pulses)
    cap.stop()

Result dict:
    {
      'raw':      [int, ...],   # pulse durations in µs (alternating hi/lo)
      'T_us':     int,          # base clock period
      'bits':     str,          # '0101...' bit string
      'hex':      str,          # '0xA3F2B4'
      'bit_count': int,
      'protocol': str,          # 'PT2262/EV1527' / 'HT6P20B' / 'Unknown'
      'repeats':  int,          # detected repetitions
    }
"""

from machine import Pin
import time
import array

_MAX_PULSES = 512   # max edges to capture


class OOKCapture:
    GAP_US = 8_000    # silence > 8ms → end of packet
    MIN_T  = 100      # ignore pulses shorter than 100µs (noise)

    def __init__(self, gdo0_pin: int = 6):
        self._pin_num = gdo0_pin
        self._pin = None
        self._buf  = array.array('i', [0] * _MAX_PULSES)
        self._idx  = 0
        self._last = 0

    # ── IRQ handler (kept minimal for timing accuracy) ────
    def _edge(self, pin):
        now  = time.ticks_us()
        dt   = time.ticks_diff(now, self._last)
        self._last = now
        if dt >= self.MIN_T and self._idx < _MAX_PULSES:
            self._buf[self._idx] = dt
            self._idx += 1

    # ── Public API ────────────────────────────────────────
    def start_rx(self):
        """Attach edge IRQ to GDO0 for pulse timing capture."""
        self._idx  = 0
        self._last = time.ticks_us()
        self._pin  = Pin(self._pin_num, Pin.IN)
        self._pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                      handler=self._edge)

    def stop(self):
        """Detach IRQ and release pin."""
        if self._pin:
            self._pin.irq(handler=None)
            self._pin = None

    def wait_capture(self, timeout_ms: int = 5000) -> list:
        """
        Wait until a gap of GAP_US µs is detected (end of OOK burst),
        or until timeout_ms is reached.
        Returns list of pulse durations (µs).
        """
        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        last_idx  = 0

        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            time.sleep_ms(20)
            cur_idx = self._idx
            if cur_idx > 0 and cur_idx == last_idx:
                # No new edges for 20ms → transmission ended
                break
            last_idx = cur_idx

        self.stop()
        return list(self._buf[:self._idx])

    # ── Decode ────────────────────────────────────────────
    @staticmethod
    def _find_T(pulses: list) -> int:
        """
        Find base clock period T.
        Strategy: use pulses in 200–2000µs window to exclude:
          - sub-200µs background noise (common at 303 MHz CAME band)
          - long sync/gap pulses (>2000µs)
        Then median of bottom third = 1T cluster.
        Works for both CAME (T≈300–350µs) and PWM-OOK (T≈500–600µs).
        Falls back to original bottom-third if window is empty.
        """
        if not pulses:
            return 0
        # Primary: noise-filtered window
        s = sorted(p for p in pulses if 200 <= p <= 2000)
        if len(s) < 3:
            # Fallback: original method (no window filter)
            s = sorted(p for p in pulses if p >= OOKCapture.MIN_T)
        if not s:
            return 0
        # Bottom third = 1T cluster (2T/3T+ pulses land in upper portions)
        n = max(1, len(s) // 3)
        cluster = s[:n]
        return int(sum(cluster) / len(cluster))

    @staticmethod
    def _quantize(val: int, T: int) -> int:
        """Round val to nearest multiple of T."""
        if T == 0:
            return 0
        return round(val / T)

    @staticmethod
    def _detect_protocol(bits: str, T: int,
                         pwm_style: bool = False,
                         pt2262_hi3: bool = False) -> str:
        """
        Fingerprint the protocol based on encoding style, bit count, and T.

        pwm_style   — True if any bit used fixed-mark (hi=1T, lo>=6T) encoding
        pt2262_hi3  — True if any bit used dual-width (hi=3T, lo=1T) encoding
        """
        n = len(bits)
        # CAME family: T≈250-400µs, dual-width encoding (1T+2T / 2T+1T)
        if pwm_style and not pt2262_hi3:
            if 200 <= T <= 450 and n in (12, 24):
                return 'CAME'
            # Fixed-mark variable-space: fan remotes, common Chinese 433 remotes
            return 'PWM-OOK'
        if 200 <= T <= 700 and pt2262_hi3:
            # Dual-width encoding with correct T range
            if n in (24, 25):
                return 'HT6P20B'
            if 24 <= n <= 72:
                return 'PT2262/EV1527'
        # Fallback: T/bit-count heuristic only
        if 200 <= T <= 700 and 24 <= n <= 72:
            return 'PT2262/EV1527'
        if n >= 8:
            return 'OOK-Unknown'
        return 'No signal'

    def decode(self, pulses: list) -> dict:
        """
        Decode raw pulse list into bit string + protocol ID.

        Supports two common 433 MHz OOK encodings:

        PT2262/EV1527 (dual-width):
            Bit 0 : 1T high + 3T low
            Bit 1 : 3T high + 1T low
            Float : 1T high + 1T low  (tri-state)
            Sync  : 1T high + 31T low

        PWM-OOK (fixed-mark variable-space, e.g. fan remotes):
            Bit 0 : 1T high + ~3-4T low
            Bit 1 : 1T high + ~7-8T low
            Sync  : long gap (> 10T)
        """
        result = {
            'raw':       pulses,
            'T_us':      0,
            'bits':      '',
            'hex':       '',
            'bit_count': 0,
            'protocol':  'No signal',
            'repeats':   0,
        }

        if len(pulses) < 6:
            return result

        T = self._find_T(pulses)
        if T < self.MIN_T:
            return result
        result['T_us'] = T

        # ── Find packet boundaries (sync gap >> 10T) ──────
        packets = []
        pkt = []
        for dur in pulses:
            q = self._quantize(dur, T)
            if q >= 10 and pkt:     # long gap = end of packet
                packets.append(pkt)
                pkt = []
            else:
                pkt.append((dur, q))
        if pkt:
            packets.append(pkt)

        if not packets:
            return result

        result['repeats'] = len(packets)

        # ── Pick the best packet (most decoded bits) ──────
        # Try both start offsets (0 and 1) for each packet; keep the best.
        def _try_decode_pkt(pk):
            """Return (bits_list, pwm_flag, pt2262_flag) for a single packet,
            trying start=0 and start=1 and returning whichever yields more bits."""
            best_bits, best_pwm, best_pt2 = [], False, False
            for s in (0, 1):
                b, p, q = [], False, False
                i = s
                while i + 1 < len(pk):
                    hq = pk[i][1]; lq = pk[i+1][1]
                    if hq == 1 and 2 <= lq <= 5:
                        b.append('0')            # PWM-bit0 OR CAME-bit0 (1T+2T)
                    elif hq == 1 and 6 <= lq <= 9:
                        b.append('1'); p = True  # PWM-bit1 (1T+7T)
                    elif hq == 2 and lq == 1:
                        b.append('1'); p = True  # CAME-bit1 (2T+1T)
                    elif hq == 3 and lq == 1:
                        b.append('1'); q = True  # PT2262-bit1 (3T+1T)
                    elif hq == 1 and lq == 1:
                        b.append('F')            # PT2262 tri-state
                    i += 2
                if len(b) > len(best_bits):
                    best_bits, best_pwm, best_pt2 = b, p, q
            return best_bits, best_pwm, best_pt2

        bits, pwm_style, pt2262_hi3 = [], False, False
        for pk in packets:
            b, p, q = _try_decode_pkt(pk)
            if len(b) > len(bits):
                bits, pwm_style, pt2262_hi3 = b, p, q

        bit_str = ''.join(bits)
        result['bits']      = bit_str
        result['bit_count'] = len(bit_str)

        # Convert to hex (treat F as 0 for numeric conversion)
        clean = bit_str.replace('F', '0')
        if clean:
            val = int(clean, 2)
            n_hex = (len(clean) + 3) // 4
            result['hex'] = '0x{:0{}X}'.format(val, n_hex)

        result['protocol'] = OOKCapture._detect_protocol(
            bit_str, T, pwm_style, pt2262_hi3)
        return result

    # ── TX replay ─────────────────────────────────────────
    @staticmethod
    def transmit(gdo0_pin: int, pulses: list, repeats: int = 3):
        """
        Replay captured pulse list on GDO0 (async TX).
        CC1101 must already be in TX mode before calling this.

        pulses: alternating [hi_us, lo_us, hi_us, lo_us, ...]
                first pulse is assumed HIGH.
        """
        if not pulses:
            return
        pin = Pin(gdo0_pin, Pin.OUT, value=0)
        for rep in range(repeats):
            level = 1
            for dur in pulses:
                pin.value(level)
                time.sleep_us(dur)
                level ^= 1
            pin.value(0)
            time.sleep_us(10_000)   # 10ms gap between repetitions
        pin.value(0)
        # Return pin to input for next RX
        Pin(gdo0_pin, Pin.IN)
