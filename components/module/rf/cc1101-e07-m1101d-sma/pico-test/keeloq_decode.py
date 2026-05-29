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
SN        = 0xF1B15E9D
LIGHT_CODE = 0x0E60199F  # 28-bit code for 燈
STAT_BITS  = 0xF          # 4-bit stat

CODE_MAP = {
    0xE60199F: ('燈',     'LIGHT'),
    0x7F8819F: ('風扇開關', 'FAN ON/OFF'),
    0xF70099F: ('風扇加速', 'FAN FASTER'),
    0xF68099F: ('風扇減速', 'FAN SLOWER'),
}

# ── TX 功能 ───────────────────────────────────────────────────
Te = 350  # µs（原廠~380µs，補償 python 呼叫開銷 ~30µs）

def _build_frame():
    bits = []
    for i in range(32): bits.append((SN >> i) & 1)
    for i in range(28): bits.append((LIGHT_CODE >> i) & 1)
    for i in range(4):  bits.append((STAT_BITS >> i) & 1)
    return bits

def _tx_frame(p, bits):
    """Bit-bang 一個 Keeloq frame，直接呼叫減少 Python overhead"""
    Te2 = Te * 2

    # Preamble: 12 × (Te HIGH + Te LOW)
    for _ in range(12):
        p(1); time.sleep_us(Te)
        p(0); time.sleep_us(Te)

    # Header: long LOW（實測遙控器 = 14058µs）
    p(0); time.sleep_us(14000)

    # 64 data bits
    for b in bits:
        if b:
            p(1); time.sleep_us(Te2)
            p(0); time.sleep_us(Te)
        else:
            p(1); time.sleep_us(Te)
            p(0); time.sleep_us(Te2)

    p(0); time.sleep_us(Te * 4)

def transmit_light(radio, oled):
    bits = _build_frame()

    # 先進入 TX 模式等 PLL 穩定（GDO0 暫時保持 Low）
    radio.start_tx()                  # SIDLE → STX + 5ms wait
    gdo0_out = Pin(6, Pin.OUT, value=0)  # TX 穩定後才接管 GDO0

    oled.fill(0)
    oled.text('** TX **', 24, 0)
    oled.text('>> LIGHT', 0, 20)
    oled.text('Max Power 0xC0', 0, 36)
    oled.show()
    print('TX: 發射「燈」訊號 × 3')

    for _ in range(5):          # 連發 5 次提高可靠性
        _tx_frame(gdo0_out, bits)
        time.sleep_ms(20)       # inter-frame gap

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

# GP15 按鍵（Internal Pull-up，按下=LOW）
tx_flag = False
def _btn_irq(pin):
    global tx_flag
    tx_flag = True
btn = Pin(15, Pin.IN, Pin.PULL_UP)
btn.irq(trigger=Pin.IRQ_FALLING, handler=_btn_irq)

gdo0 = Pin(6, Pin.IN)
radio.rx()
print('GP15 按下 → 發射燈訊號')
print('等待 RX 或 TX...')

oled.fill(0)
oled.text('Keeloq RX+TX', 0, 0)
oled.text('GP15=TX LIGHT', 0, 16)
oled.text('Waiting...', 0, 32)
oled.show()

last_code = -1
last_time = 0
count = 0

while True:
    if tx_flag:
        tx_flag = False
        transmit_light(radio, oled)
        gdo0 = Pin(6, Pin.IN)
        radio.rx()
        oled.fill(0)
        oled.text('TX Done!', 0, 0)
        oled.text('Back to RX...', 0, 20)
        oled.show()
        time.sleep_ms(500)
        continue

    result = decode_keeloq(gdo0, attempts=30)
    if result is None:
        continue

    serial, code, stat = result
    now = time.ticks_ms()
    if code != last_code or time.ticks_diff(now, last_time) > 1000:
        count += 1
        zh, en = CODE_MAP.get(code, ('?', f'{code:07X}'))
        print(f'RX [{zh}] {en}  Code=0x{code:07X}  #{count}')
        oled.fill(0)
        oled.text('Keeloq RX+TX', 0, 0)
        oled.text(f'SN:{serial:08X}', 0, 12)
        oled.text(f'>> {en}', 0, 28)
        oled.text(f'{code:07X}', 0, 40)
        oled.text(f'#{count}', 0, 52)
        oled.show()
        last_code = code
        last_time = now
