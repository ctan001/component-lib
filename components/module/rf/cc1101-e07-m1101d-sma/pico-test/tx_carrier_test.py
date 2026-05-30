"""
tx_carrier_test.py — CC1101 持續載波測試
按 GP15 → 發射純載波 2 秒（不帶資料），確認 CC1101 TX 硬體是否正常
"""

from machine import SPI, Pin
import time

SRES = 0x30; STX = 0x35; SIDLE = 0x36; SFRX = 0x3A; SRX = 0x34

OOK_CONFIG = [
    (0x00, 0x0B),(0x02, 0x0D),(0x03, 0x47),(0x06, 0xFF),
    (0x07, 0x04),(0x08, 0x32),(0x0A, 0x00),(0x0B, 0x06),
    (0x0C, 0x00),(0x0D, 0x10),(0x0E, 0xB1),(0x0F, 0x3B),
    (0x10, 0xC8),(0x11, 0x93),(0x12, 0x30),(0x13, 0x22),
    (0x14, 0xF8),(0x15, 0x00),(0x16, 0x07),(0x17, 0x20),
    (0x18, 0x18),(0x19, 0x16),(0x1A, 0x6C),(0x1B, 0x43),
    (0x1C, 0x40),(0x1D, 0x91),(0x21, 0x56),(0x22, 0x11),
    (0x23, 0xE9),(0x24, 0x2A),(0x25, 0x00),(0x26, 0x1F),
    (0x2C, 0x81),(0x2D, 0x35),(0x2E, 0x09),
]

spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5, Pin.OUT, value=1)

def strobe(cmd):
    cs(0); time.sleep_us(2)
    b = bytearray(1); spi.write_readinto(bytes([cmd]), b)
    cs(1); return b[0]

def write_reg(addr, val):
    cs(0); time.sleep_us(2)
    spi.write(bytes([addr & 0x3F, val])); cs(1)

def write_burst(addr, data):
    cs(0); time.sleep_us(2)
    spi.write(bytes([addr | 0x40]) + bytes(data)); cs(1)

def read_status(addr):
    cs(0); time.sleep_us(2)
    spi.write(bytes([addr | 0xC0]))
    r = bytearray(1); spi.readinto(r); cs(1)
    return r[0]

# Reset
cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(200); strobe(SRES); time.sleep_ms(10)

for addr, val in OOK_CONFIG:
    write_reg(addr, val)
write_burst(0x3E, bytes([0x00, 0xC0, 0, 0, 0, 0, 0, 0]))

ver = read_status(0x31)
print(f'CC1101 VERSION: 0x{ver:02X}', '✅' if ver == 0x14 else '❌')
print('GP15 按下 → 發射純載波 2 秒')
print()

btn = Pin(15, Pin.IN, Pin.PULL_UP)

while True:
    if btn.value() == 0:
        time.sleep_ms(20)  # debounce
        if btn.value() == 0:
            print('TX: 發射純載波 2 秒...')

            # 進入 TX 模式
            strobe(SIDLE); time.sleep_ms(2)
            strobe(STX);   time.sleep_ms(5)

            # 讀 MARCSTATE 確認 TX 狀態
            marcstate = read_status(0x35) & 0x1F
            print(f'  MARCSTATE = 0x{marcstate:02X}', '(TX ✅)' if marcstate == 0x13 else f'(期望 0x13!)')

            # GDO0 持續 HIGH → 持續發射載波
            gdo0 = Pin(6, Pin.OUT, value=1)
            time.sleep_ms(2000)

            # 停止
            gdo0(0)
            strobe(SIDLE); time.sleep_ms(5)
            print(f'  TX 完成')
            gdo0 = Pin(6, Pin.IN)

            # 等按鍵放開
            while btn.value() == 0:
                time.sleep_ms(10)

    time.sleep_ms(50)
