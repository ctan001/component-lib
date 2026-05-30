"""
keeloq_decode.py — CC1101 Keeloq 64-bit RX + TX

CC1101 接線：
  SCK→GP2  MOSI→GP3  MISO→GP4  CSN→GP5  GDO0→GP6

OLED（SSD1309 2.42"）：  SDA→GP10  SCL→GP11

按鍵（TX 觸發）：  GP15，Internal Pull-up，按下接 GND

TX 功能：GP15 按下 → 發射「燈」訊號，最大功率（PATABLE=0xC0）
"""

from machine import SPI, Pin, time_pulse_us
from oled_ssd1309 import OLED
import time

# ── CC1101 Strobes ────────────────────────────────────────────
SRES = 0x30; STX = 0x35; SIDLE = 0x36
SRX  = 0x34; SFRX = 0x3A

OOK_CONFIG = [
    (0x00, 0x0B),  # IOCFG2
    (0x02, 0x0D),  # IOCFG0: async serial data (GDO0)
    (0x03, 0x47),  # FIFOTHR
    (0x06, 0xFF),  # PKTLEN
    (0x07, 0x04),  # PKTCTRL1
    (0x08, 0x32),  # PKTCTRL0: async serial mode
    (0x0A, 0x00),  # CHANNR
    (0x0B, 0x06),  # FSCTRL1
    (0x0C, 0x00),  # FSCTRL0
    (0x0D, 0x10),  # FREQ2  → 433.92 MHz
    (0x0E, 0xB1),  # FREQ1
    (0x0F, 0x3B),  # FREQ0
    (0x10, 0xC8),  # MDMCFG4: BW ≈102 kHz
    (0x11, 0x93),  # MDMCFG3
    (0x12, 0x30),  # MDMCFG2: OOK, SYNC_MODE=0
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
    (0x22, 0x11),  # FREND0: PA_POWER=1 → 使用 PATABLE[1] 作為 OOK '1' 功率
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
        # PATABLE[0]=0x00（OOK off），PATABLE[1]=0xC0（最大功率 ~+10dBm）
        self._write_burst(0x3E, bytes([0x00, 0xC0, 0, 0, 0, 0, 0, 0]))

    def _strobe(self, cmd):
        self._cs(0); time.sleep_us(2)
        b = bytearray(1); self._spi.write_readinto(bytes([cmd]), b)
        self._cs(1)

    def _write(self, addr, val):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr & 0x3F, val])); self._cs(1)

    def _write_burst(self, addr, data):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr | 0x40]) + bytes(data)); self._cs(1)

    def _read_status(self, addr):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr | 0xC0]))
        r = bytearray(1); self._spi.readinto(r); self._cs(1)
        return r[0]

    def _reset(self):
        cs = self._cs
        cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(200); self._strobe(SRES); time.sleep_ms(10)

    def rx(self):
        self._strobe(SIDLE); self._strobe(SFRX); self._strobe(SRX)

    def start_tx(self):
        self._strobe(SIDLE)
        time.sleep_ms(2)
        self._strobe(STX)
        time.sleep_ms(5)   # PLL 校準需要 ~800µs，等 5ms 保險

    def idle(self):
        self._strobe(SIDLE)

    @property
    def version(self):
        return self._read_status(0x31)


# ── 固定碼資料 ────────────────────────────────────────────────
SN = 0xF1B15E9D

# 按鍵清單：(28-bit code, stat 4-bit, 中文, OLED英文)
# Stat 依 Flipper 實測：燈/加速=0xF，風扇開關/減速=0x7
BUTTONS = [
    (0x0E60199F, 0xF, '燈',     'Light'),
    (0x07F8819F, 0x7, '風扇開關', 'Fan On/Off'),
    (0x0F70099F, 0xF, '風扇加速', 'Fan Faster'),
    (0x0F68099F, 0x7, '風扇減速', 'Fan Slower'),
]

CODE_MAP = {code & 0xFFFFFFF: (zh, en) for code, stat, zh, en in BUTTONS}

# ── TX 功能 ───────────────────────────────────────────────────
# p(1) overhead ~12µs，p(0) overhead ~7µs → 需分開補償
# 原廠實測：SHORT HIGH=391, SHORT LOW=406, LONG HIGH=793, LONG LOW=807
Te_h  = 379  # sleep → 379+12 = 391µs (SHORT HIGH)
Te_l  = 399  # sleep → 399+ 7 = 406µs (SHORT LOW)
Te2_h = 781  # sleep → 781+12 = 793µs (LONG  HIGH)
Te2_l = 800  # sleep → 800+ 7 = 807µs (LONG  LOW)

def _build_frame(code, stat):
    bits = []
    for i in range(32): bits.append((SN >> i) & 1)
    for i in range(28): bits.append((code >> i) & 1)
    for i in range(4):  bits.append((stat >> i) & 1)
    return bits

def _tx_frame(p, bits):
    # Preamble: 12 × (SHORT HIGH + SHORT LOW)
    for _ in range(12):
        p(1); time.sleep_us(Te_h)
        p(0); time.sleep_us(Te_l)

    # Header
    p(0); time.sleep_us(5200)

    # 64 data bits
    for b in bits:
        if b:
            p(1); time.sleep_us(Te2_h)   # LONG  HIGH
            p(0); time.sleep_us(Te_l)    # SHORT LOW
        else:
            p(1); time.sleep_us(Te_h)    # SHORT HIGH
            p(0); time.sleep_us(Te2_l)   # LONG  LOW

    # Stop bit
    p(1); time.sleep_us(Te2_h)
    p(0); time.sleep_us(Te_l)

    # Trailing HIGH（切斷 stop LOW 與 inter-frame 合併）
    p(1); time.sleep_us(Te_h)
    p(0)

def transmit(code, stat, zh, en, radio, oled):
    bits = _build_frame(code, stat)

    radio.start_tx()
    gdo0_out = Pin(6, Pin.OUT, value=0)

    oled.fill(0)
    oled.text('** TX **', 24, 0)
    oled.text(f'>> {en[:13]}', 0, 20)
    oled.text(f'   {zh[:13]}', 0, 36)
    oled.show()
    print(f'TX: [{zh}] {en}')

    for _ in range(3):
        _tx_frame(gdo0_out, bits)
        time.sleep_ms(25)

    gdo0_out(0)
    radio.idle()
    time.sleep_ms(5)
    print('TX 完成，切回 RX')

# ── RX 解碼 ──────────────────────────────────────────────────
THRESHOLD = 600
HDR_MIN   = 3500
BITS      = 64

def _lsb_to_int(bit_list):
    v = 0
    for i, b in enumerate(bit_list):
        v |= b << i
    return v

def decode_keeloq(gdo0, attempts=30):
    for _ in range(attempts):
        low = time_pulse_us(gdo0, 0, 20000)
        if low < HDR_MIN:
            continue
        bits = []
        ok = True
        for _ in range(BITS):
            h = time_pulse_us(gdo0, 1, 3000)
            if h <= 0 or h > 2500: ok = False; break
            l = time_pulse_us(gdo0, 0, 3000)
            if l <= 0: ok = False; break
            bits.append(0 if h < THRESHOLD else 1)
        if not ok or len(bits) != BITS:
            continue
        serial = _lsb_to_int(bits[0:32])
        code   = _lsb_to_int(bits[32:60])
        stat   = _lsb_to_int(bits[60:64])
        if serial == 0 or code == 0:
            continue
        return serial, code, stat
    return None

# ── 主程式 ───────────────────────────────────────────────────
print('=' * 44)
print('CC1101 Keeloq RX + TX')
print('433.92 MHz  Te=400µs  Max Power=0xC0')
print('=' * 44)

oled = OLED(sda=10, scl=11)
oled.fill(0); oled.text('Keeloq RX+TX', 0, 0); oled.text('Init...', 0, 20); oled.show()

radio = CC1101()
ver_ok = radio.version == 0x14
print(f'CC1101 VERSION: 0x{radio.version:02X}', '✅' if ver_ok else '❌')

# GP15 多次按鍵偵測
_press_count = 0
_last_press_ms = 0
_oled_dirty = False
_DEBOUNCE_MS = 60
_WINDOW_MS   = 500  # ms 無新按鍵後觸發發射

def _btn_irq(pin):
    global _press_count, _last_press_ms, _oled_dirty
    now = time.ticks_ms()
    if time.ticks_diff(now, _last_press_ms) > _DEBOUNCE_MS:
        _press_count += 1
        _last_press_ms = now
        _oled_dirty = True

btn = Pin(15, Pin.IN, Pin.PULL_UP)
btn.irq(trigger=Pin.IRQ_FALLING, handler=_btn_irq)

gdo0 = Pin(6, Pin.IN)
radio.rx()

def _show_idle(oled):
    oled.fill(0)
    oled.text('Keeloq RX+TX', 0, 0)
    oled.text('[1]Light [2]Fan', 0, 14)
    oled.text('[3]Fast  [4]Slow', 0, 26)
    oled.text('Waiting...', 0, 48)
    oled.show()

_show_idle(oled)
print('GP15: 1下=燈  2下=風扇開關  3下=加速  4下=減速')
print('等待 RX 或 TX...')

last_code = -1
last_time = 0
rx_count  = 0

while True:
    # ── 計數視窗更新 OLED ──
    if _oled_dirty and _press_count > 0:
        _oled_dirty = False
        n = min(_press_count, 4)
        _, _, zh, en = BUTTONS[n - 1]
        dots = '*' * n + ' ' * (4 - n)
        oled.fill(0)
        oled.text(f'[{dots}] {n}x', 0, 0)
        oled.text(f'>> {en[:13]}', 0, 18)
        oled.text(f'   {zh[:13]}', 0, 34)
        oled.text('...', 48, 52)
        oled.show()

    # ── 超時 → 發射 ──
    if _press_count > 0 and time.ticks_diff(time.ticks_ms(), _last_press_ms) > _WINDOW_MS:
        n = min(_press_count, 4)
        _press_count = 0
        code, stat, zh, en = BUTTONS[n - 1]
        transmit(code, stat, zh, en, radio, oled)
        gdo0 = Pin(6, Pin.IN)
        radio.rx()
        oled.fill(0)
        oled.text('TX Done!', 16, 0)
        oled.text(f'{en[:16]}', 0, 20)
        oled.show()
        time.sleep_ms(800)
        _show_idle(oled)
        continue

    result = decode_keeloq(gdo0, attempts=30)
    if result is None:
        continue

    serial, code, stat = result
    now = time.ticks_ms()
    if code != last_code or time.ticks_diff(now, last_time) > 1000:
        rx_count += 1
        zh, en = CODE_MAP.get(code, ('?', f'{code:07X}'))
        print(f'RX [{zh}] {en}  Code=0x{code:07X}  #{rx_count}')
        oled.fill(0)
        oled.text('RX:', 0, 0)
        oled.text(f'SN:{serial:08X}', 0, 12)
        oled.text(f'>> {en[:13]}', 0, 28)
        oled.text(f'{code:07X} #{rx_count}', 0, 44)
        oled.show()
        last_code = code
        last_time = now
