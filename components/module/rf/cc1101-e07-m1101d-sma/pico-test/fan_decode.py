"""
fan_decode.py — CC1101 接收 303.875 MHz OOK，即時解碼風扇遙控器按鈕

接線：
  CC1101 Pin5  SCK   → Pico GP2
  CC1101 Pin6  MOSI  → Pico GP3
  CC1101 Pin7  MISO  → Pico GP4
  CC1101 Pin4  CSN   → Pico GP5
  CC1101 Pin3  GDO0  → Pico GP6   ← OOK demodulated output
  CC1101 Pin2  VCC   → 3.3V
  CC1101 Pin1  GND   → GND

原理：
  CC1101 async RX 模式下，GDO0 輸出解調後的 OOK 訊號
  Pico 用 time_pulse_us() 量每個 pulse 的寬度
  T≈320μs（短）、2T≈630μs（長）、sync gap >9500μs

已知按鈕 bit pattern（F=模糊位，不參與比對）:
  高速:    F1111FFF0000
  （其他按鈕待補完）

使用方法：
  mpremote run fan_decode.py
  然後按遙控器按鈕，終端機顯示接收到的指令
"""

from machine import SPI, Pin, time_pulse_us
import time
import sys

# ── 把 cc1101.py driver import 進來 ─────────────────────────
sys.path.append('/lib')  # 若 cc1101.py 在 /lib 下
try:
    from cc1101 import CC1101
except ImportError:
    # 直接 inline 最小需要的部分
    SRES = 0x30; SCAL = 0x33; SRX = 0x34; SIDLE = 0x36
    SFRX = 0x3A
    OOK_CONFIG = [
        (0x00, 0x0B),(0x02, 0x0D),(0x03, 0x47),(0x06, 0xFF),
        (0x07, 0x04),(0x08, 0x32),(0x0A, 0x00),(0x0B, 0x06),
        (0x0C, 0x00),(0x0D, 0x0B),(0x0E, 0xB0),(0x0F, 0x00),
        (0x10, 0x65),(0x11, 0x83),(0x12, 0x34),(0x13, 0x22),
        (0x14, 0xF8),(0x15, 0x00),(0x16, 0x07),(0x17, 0x20),
        (0x18, 0x18),(0x19, 0x16),(0x1A, 0x6C),(0x1B, 0x43),
        (0x1C, 0x40),(0x1D, 0x91),(0x21, 0x56),(0x22, 0x11),
        (0x23, 0xE9),(0x24, 0x2A),(0x25, 0x00),(0x26, 0x1F),
        (0x2C, 0x81),(0x2D, 0x35),(0x2E, 0x09),
    ]

    class CC1101:
        def __init__(self):
            self._spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
                            sck=Pin(2), mosi=Pin(3), miso=Pin(4))
            self._cs = Pin(5, Pin.OUT, value=1)
            self._reset()
            for addr, val in OOK_CONFIG:
                self._write(addr, val)
            self._write_burst(0x3E, bytes([0xC0,0,0,0,0,0,0,0]))

        def _strobe(self, cmd):
            self._cs(0); time.sleep_us(2)
            b = bytearray(1)
            self._spi.write_readinto(bytes([cmd]), b)
            self._cs(1)

        def _write(self, addr, val):
            self._cs(0); time.sleep_us(2)
            self._spi.write(bytes([addr & 0x3F, val]))
            self._cs(1)

        def _write_burst(self, addr, data):
            self._cs(0); time.sleep_us(2)
            self._spi.write(bytes([addr | 0x40]) + bytes(data))
            self._cs(1)

        def _read_status(self, addr):
            self._cs(0); time.sleep_us(2)
            self._spi.write(bytes([addr | 0xC0]))
            r = bytearray(1); self._spi.readinto(r)
            self._cs(1); return r[0]

        def _reset(self):
            cs = self._cs
            cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
            cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
            cs(1); time.sleep_us(200); self._strobe(SRES); time.sleep_ms(10)

        def rx(self):
            self._strobe(SIDLE); self._strobe(SFRX); self._strobe(SRX)

        @property
        def version(self): return self._read_status(0x31)

# ── 按鈕 bit pattern 對照表 ──────────────────────────────────
# F = don't care（模糊位，略過比對）
# 格式：(名稱, bit_pattern)
BUTTONS = {
    # 從 Flipper Zero 捕捉解碼，F=ambiguous（don't care）
    # 結構：F [1111 固定頭] F [6-bit 指令碼]
    # 指令碼規律：FF 對在不同位置移動（one-hot 式）
    'HIGH_SPEED' : 'F1111FFF0000',   # FF 在 bit 6-7
    'MID_SPEED'  : 'F1111F0FF000',   # FF 在 bit 7-8
    'LOW_SPEED'  : 'F1111F00FF00',   # FF 在 bit 8-9
    'REVERSE'    : 'F1111F000FF0',   # FF 在 bit 9-10
    'STOP'       : 'F1111F0000FF',   # FF 在 bit 10-11
    'LIGHT_TOP'  : 'F1111F00FF0F',   # FF 在 bit 8-9 + bit 11
    'LIGHT_BOT'  : 'F1111F00000F',   # F  在 bit 11 only
}

# ── Timing 參數（從 Flipper raw 分析） ───────────────────────
T_SHORT  = 320     # μs（short pulse）
T_LONG   = 630     # μs（long pulse）
T_MID    = 450     # 分界點
T_SYNC   = 9500    # sync gap 下限 μs
MAX_FRAME= 30      # 最多幾個 pulse-pair 一個 frame

def match_button(bits):
    """比對 bit string 到按鈕名稱，F = don't care"""
    for name, pattern in BUTTONS.items():
        if len(bits) != len(pattern):
            continue
        match = all(
            p == 'F' or b == p
            for b, p in zip(bits, pattern)
        )
        if match:
            return name
    return None

def capture_frame(gdo0, timeout_ms=200):
    """
    在 sync gap 之後捕捉一個完整 frame。
    回傳 list of (high_us, low_us) 或 None。
    """
    # 等 sync gap（GDO0 低電平 > T_SYNC μs）
    # 先等訊號變低
    deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
    while gdo0.value() == 1:
        if time.ticks_diff(deadline, time.ticks_ms()) < 0:
            return None

    # 量低電平寬度（timeout = T_SYNC*3 μs）
    low_us = time_pulse_us(gdo0, 0, T_SYNC * 3)
    if low_us < T_SYNC:
        return None  # 不夠長，不是 sync

    # Sync 確認！開始量 frame
    pairs = []
    for _ in range(MAX_FRAME):
        high_us = time_pulse_us(gdo0, 1, 5000)
        if high_us < 0:
            break
        low_us = time_pulse_us(gdo0, 0, 15000)
        if low_us < 0:
            break
        if low_us > T_SYNC:
            # 下一個 sync，frame 結束
            break
        pairs.append((high_us, low_us))

    return pairs if len(pairs) >= 6 else None

def decode_pairs(pairs):
    """將 (high, low) pair list 轉成 bit string"""
    bits = ''
    for h, l in pairs:
        if   h > T_MID and l <= T_MID: bits += '1'
        elif h <= T_MID and l > T_MID: bits += '0'
        else:                           bits += 'F'
    return bits

# ── 主程式 ───────────────────────────────────────────────────
print('=' * 40)
print('CC1101 風扇遙控器解碼器')
print('頻率: 303.875 MHz  OOK async')
print('=' * 40)

radio = CC1101()
print(f'CC1101 VERSION: 0x{radio.version:02X}', '✅' if radio.version == 0x14 else '❌')

gdo0 = Pin(6, Pin.IN)
radio.rx()
print('進入 RX 模式，等待訊號...')
print('（對著 CC1101 按遙控器按鈕）')
print()

last_bits = ''
last_time = 0

while True:
    pairs = capture_frame(gdo0, timeout_ms=500)
    if pairs is None:
        continue

    bits = decode_pairs(pairs)
    now = time.ticks_ms()

    # 去重（同一個按鈕連發時只顯示一次）
    if bits != last_bits or time.ticks_diff(now, last_time) > 800:
        name = match_button(bits)
        if name:
            print(f'>>> {name}  ({bits})')
        else:
            print(f'    UNKNOWN  ({bits})  {len(pairs)} pairs')
        last_bits = bits
        last_time = now
