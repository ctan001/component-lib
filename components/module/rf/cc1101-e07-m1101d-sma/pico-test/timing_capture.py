"""
timing_capture.py — 精確量測 Keeloq 遙控器脈衝寬度
等 header LOW > 2ms，然後印出每個 HIGH/LOW 的 µs 數值
"""
from machine import SPI, Pin, time_pulse_us
import time

SRES = 0x30; SRX = 0x34; SIDLE = 0x36; SFRX = 0x3A

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
cs = Pin(5, Pin.OUT, value=1)

def strobe(cmd):
    cs(0); time.sleep_us(2)
    b = bytearray(1); spi.write_readinto(bytes([cmd]), b)
    cs(1)

def write_reg(addr, val):
    cs(0); time.sleep_us(2); spi.write(bytes([addr & 0x3F, val])); cs(1)

def read_status(addr):
    cs(0); time.sleep_us(2); spi.write(bytes([addr | 0xC0]))
    r = bytearray(1); spi.readinto(r); cs(1); return r[0]

cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(200); strobe(SRES); time.sleep_ms(10)

for addr, val in OOK_CONFIG:
    write_reg(addr, val)

ver = read_status(0x31)
print(f'CC1101 VERSION: 0x{ver:02X}', '✅' if ver == 0x14 else '❌')
strobe(SIDLE); strobe(SFRX); strobe(SRX)

gdo0 = Pin(6, Pin.IN)
print('按遙控器按鈕（任意一個），量測脈衝寬度')
print()

captures = 0
while captures < 3:
    # 等 header LOW > 2ms
    low = time_pulse_us(gdo0, 0, 20000)
    if low < 2000:
        continue

    print(f'--- Frame {captures+1}  header_low={low}µs ---')
    print('  #   HIGH(µs)  LOW(µs)')

    for i in range(80):
        h = time_pulse_us(gdo0, 1, 3000)
        if h <= 0 or h > 2000:
            print(f'  END (h={h})')
            break
        l = time_pulse_us(gdo0, 0, 5000)
        if l <= 0:
            print(f'  END (l={l})')
            break
        bit = '1' if h >= 600 else '0'
        print(f'  {i:2d}  {h:6d}    {l:6d}   bit={bit}')
        if l > 2000:
            print(f'  (next_header={l}µs)')
            break

    print()
    captures += 1
