"""
fan_decode.py — CC1101 接收 303.875 MHz OOK，即時解碼 CAME12 風扇遙控器按鈕

接線：
  CC1101 Pin5  SCK   → Pico GP2
  CC1101 Pin6  MOSI  → Pico GP3
  CC1101 Pin7  MISO  → Pico GP4
  CC1101 Pin4  CSN   → Pico GP5
  CC1101 Pin3  GDO0  → Pico GP6   ← OOK demodulated output
  CC1101 Pin2  VCC   → 3.3V
  CC1101 Pin1  GND   → GND

CAME12 bit 編碼（看 LOW pulse 長短，THRESHOLD = 425µs）：
  "0" = SHORT LOW + LONG HIGH
  "1" = LONG  LOW + SHORT HIGH
  Sync gap = LOW > 5000µs

已知按鈕 Key（12-bit hex）：
  0x05F = 高速, 0x06F = 中速, 0x077 = 低速, 0x07F = 放開按鍵
  反轉 / 停止 / 上燈 / 下燈 Key 待補

使用方法：
  mpremote run fan_decode.py
  對著模組按遙控器按鈕，終端機顯示接收到的指令
"""

from machine import SPI, Pin, time_pulse_us
import time

SRES = 0x30; SCAL = 0x33; SRX = 0x34; SIDLE = 0x36; SFRX = 0x3A

OOK_CONFIG = [
    (0x00, 0x0B),  # IOCFG2
    (0x02, 0x0D),  # IOCFG0: async serial data output on GDO0
    (0x03, 0x47),  # FIFOTHR
    (0x06, 0xFF),  # PKTLEN
    (0x07, 0x04),  # PKTCTRL1
    (0x08, 0x32),  # PKTCTRL0: async serial mode, infinite length
    (0x0A, 0x00),  # CHANNR
    (0x0B, 0x06),  # FSCTRL1
    (0x0C, 0x00),  # FSCTRL0
    (0x0D, 0x0B),  # FREQ2
    (0x0E, 0xB0),  # FREQ1  → 303.875 MHz
    (0x0F, 0x00),  # FREQ0
    (0x10, 0x2C),  # MDMCFG4: BW ~542 kHz，AM650 規格需要寬帶寬（原 0x65=271kHz 太窄）
    (0x11, 0x83),  # MDMCFG3
    (0x12, 0x30),  # MDMCFG2: OOK, SYNC_MODE=0，不找 sync word（原 0x34=SYNC_MODE=4 導致 GDO0 無輸出）
    (0x13, 0x22),  # MDMCFG1
    (0x14, 0xF8),  # MDMCFG0
    (0x15, 0x00),  # DEVIATN
    (0x16, 0x07),  # MCSM2
    (0x17, 0x20),  # MCSM1
    (0x18, 0x18),  # MCSM0
    (0x19, 0x16),  # FOCCFG
    (0x1A, 0x6C),  # BSCFG
    (0x1B, 0x43),  # AGCCTRL2
    (0x1C, 0x40),  # AGCCTRL1
    (0x1D, 0x91),  # AGCCTRL0
    (0x21, 0x56),  # FREND1
    (0x22, 0x11),  # FREND0
    (0x23, 0xE9),  # FSCAL3
    (0x24, 0x2A),  # FSCAL2
    (0x25, 0x00),  # FSCAL1
    (0x26, 0x1F),  # FSCAL0
    (0x2C, 0x81),  # TEST2
    (0x2D, 0x35),  # TEST1
    (0x2E, 0x09),  # TEST0
]


class CC1101:
    def __init__(self):
        self._spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
                        sck=Pin(2), mosi=Pin(3), miso=Pin(4))
        self._cs = Pin(5, Pin.OUT, value=1)
        self._reset()
        for addr, val in OOK_CONFIG:
            self._write(addr, val)
        self._write_burst(0x3E, bytes([0xC0, 0, 0, 0, 0, 0, 0, 0]))

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
        self._cs(1)
        return r[0]

    def _reset(self):
        cs = self._cs
        cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(200); self._strobe(SRES); time.sleep_ms(10)

    def rx(self):
        self._strobe(SIDLE); self._strobe(SFRX); self._strobe(SRX)

    @property
    def version(self):
        return self._read_status(0x31)


# ── CAME12 按鈕對照表 ─────────────────────────────────────────
# Key = 12-bit int（bit[0..4]=Device Code, bit[5..11]=Function Code）
BUTTON_KEYS = {
    0x05F: 'HIGH_SPEED',   # 000001011111
    0x06F: 'MID_SPEED',    # 000001101111
    0x077: 'LOW_SPEED',    # 000001110111
    0x07F: 'KEY_END',      # 000001111111（任何按鈕放開時發送）
    # 待補：REVERSE, STOP, LIGHT_TOP, LIGHT_BOT
}

THRESHOLD = 425   # µs：短/長脈衝分界
SYNC_MIN  = 5000  # µs：sync gap 最小長度


def decode_came12(gdo0, attempts=200):
    """
    等 sync gap（LOW > SYNC_MIN µs）→ 跳過 preamble HIGH → 讀 12 個 (LOW, HIGH) bit pair
    SHORT LOW + LONG HIGH = 0 / LONG LOW + SHORT HIGH = 1
    成功回傳 12-bit int，失敗回傳 None
    """
    for _ in range(attempts):
        low = time_pulse_us(gdo0, 0, 15000)
        if low < SYNC_MIN:
            continue
        pre = time_pulse_us(gdo0, 1, 2000)
        if not (100 < pre < 800):
            continue
        bits = []
        ok = True
        for _ in range(12):
            l = time_pulse_us(gdo0, 0, 2000)
            h = time_pulse_us(gdo0, 1, 2000)
            if l < 0 or h < 0:
                ok = False; break
            if   l < THRESHOLD and h >= THRESHOLD: bits.append(0)
            elif l >= THRESHOLD and h < THRESHOLD: bits.append(1)
            else:                                  ok = False; break
        if ok and len(bits) == 12:
            return int(''.join(str(b) for b in bits), 2)
    return None


# ── 主程式 ───────────────────────────────────────────────────
print('=' * 40)
print('CC1101 風扇遙控器解碼器 (CAME12)')
print('頻率: 303.875 MHz  OOK async')
print('=' * 40)

radio = CC1101()
print(f'CC1101 VERSION: 0x{radio.version:02X}', '✅' if radio.version == 0x14 else '❌')

gdo0 = Pin(6, Pin.IN)
radio.rx()
print('進入 RX 模式，等待訊號...')
print()

last_key = -1
last_time = 0

while True:
    key = decode_came12(gdo0)
    if key is None:
        continue
    now = time.ticks_ms()
    if key != last_key or time.ticks_diff(now, last_time) > 800:
        name = BUTTON_KEYS.get(key, f'UNKNOWN_0x{key:03X}')
        print(f'Key=0x{key:03X}  {name}')
        last_key = key
        last_time = now
