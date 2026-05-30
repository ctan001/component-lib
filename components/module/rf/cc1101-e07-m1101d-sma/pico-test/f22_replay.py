"""
f22_replay.py — 直接重放 F22.sub 原始波形測試
按 GP15 → 用 F22 的精確時序發射 3 次，測試是否能控制風扇
"""
from machine import SPI, Pin
import time

# ── CC1101 Init ──────────────────────────────────────────────
SRES=0x30; STX=0x35; SIDLE=0x36; SRX=0x34; SFRX=0x3A

OOK_CONFIG = [
    (0x00,0x0B),(0x02,0x0D),(0x03,0x47),(0x06,0xFF),(0x07,0x04),(0x08,0x32),
    (0x0A,0x00),(0x0B,0x06),(0x0C,0x00),(0x0D,0x10),(0x0E,0xB1),(0x0F,0x3B),
    (0x10,0xC8),(0x11,0x93),(0x12,0x30),(0x13,0x22),(0x14,0xF8),(0x15,0x00),
    (0x16,0x07),(0x17,0x20),(0x18,0x18),(0x19,0x16),(0x1A,0x6C),(0x1B,0x43),
    (0x1C,0x40),(0x1D,0x91),(0x21,0x56),(0x22,0x11),(0x23,0xE9),(0x24,0x2A),
    (0x25,0x00),(0x26,0x1F),(0x2C,0x81),(0x2D,0x35),(0x2E,0x09),
]

spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs  = Pin(5, Pin.OUT, value=1)

def strobe(cmd):
    cs(0); time.sleep_us(2)
    b=bytearray(1); spi.write_readinto(bytes([cmd]),b); cs(1)

def write_reg(addr, val):
    cs(0); time.sleep_us(2); spi.write(bytes([addr&0x3F,val])); cs(1)

def read_status(addr):
    cs(0); time.sleep_us(2); spi.write(bytes([addr|0xC0]))
    r=bytearray(1); spi.readinto(r); cs(1); return r[0]

cs(1); time.sleep_us(5); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(41); cs(0); time.sleep_us(10)
cs(1); time.sleep_us(200); strobe(SRES); time.sleep_ms(10)
for addr,val in OOK_CONFIG:
    write_reg(addr, val)
write_reg(0x22, 0x11)
spi.write(bytes([0x3E|0x40,0x00,0xC0,0,0,0,0,0,0]))

ver = read_status(0x31)
print(f'CC1101 VERSION: 0x{ver:02X}', '✅' if ver==0x14 else '❌')

# ── F22 精確波形（Flipper 實測原廠遙控）──────────────────────
# Format: [pre_H, pre_L, ...×11pairs, header_L, data_H, data_L, ...×65, trailing_H]
F22_WAVE = [323, 478, 323, 474, 323, 476, 321, 476, 323, 476, 321, 480, 323, 476, 321, 476, 321, 478, 323, 476, 355, 444, 5244, 785, 426, 367, 816, 799, 400, 787, 396, 795, 408, 393, 824, 379, 816, 805, 382, 415, 780, 811, 388, 801, 396, 797, 408, 811, 380, 413, 814, 775, 416, 377, 818, 799, 402, 393, 790, 411, 820, 357, 832, 775, 408, 815, 388, 411, 778, 807, 416, 773, 420, 387, 814, 385, 814, 383, 816, 777, 418, 779, 414, 809, 386, 809, 384, 805, 418, 779, 416, 773, 420, 783, 416, 801, 420, 355, 808, 419, 780, 811, 388, 805, 394, 401, 816, 379, 806, 415, 780, 411, 810, 385, 814, 383, 812, 777, 416, 387, 804, 417, 780, 381, 840, 777, 414, 779, 416, 805, 386, 811, 382, 817, 420, 777, 384, 805, 420, 777, 418, 383, 816, 785, 426, 757, 416, 797, 426, 367, 814, 403, 788, 379]
# idx 0-21  = preamble (11 pairs of H,L)
# idx 22    = header LOW duration
# idx 23..  = data (65 pairs of H,L = 130 values)
# last      = trailing HIGH

PRE_COUNT = 11   # 11 preamble pairs
INTER_MS  = 26   # inter-frame gap

def replay_f22(p):
    w = F22_WAVE
    idx = 0
    # Preamble
    for _ in range(PRE_COUNT):
        p(1); time.sleep_us(w[idx]);   idx+=1
        p(0); time.sleep_us(w[idx]);   idx+=1
    # Header
    p(0); time.sleep_us(w[idx]);       idx+=1
    # 65 data pairs
    for _ in range(65):
        p(1); time.sleep_us(w[idx]);   idx+=1
        p(0); time.sleep_us(w[idx]);   idx+=1
    # Trailing HIGH
    p(1); time.sleep_us(w[idx])
    p(0)

# ── 主程式 ──────────────────────────────────────────────────
btn = Pin(15, Pin.IN, Pin.PULL_UP)
print('GP15 按下 → 用 F22 精確波形發射 3 次')

while True:
    if btn.value() == 0:
        time.sleep_ms(30)
        if btn.value() == 0:
            print('TX: F22 exact waveform × 3...')
            strobe(SIDLE); time.sleep_ms(2)
            strobe(STX);   time.sleep_ms(5)
            gdo0 = Pin(6, Pin.OUT, value=0)

            # Carrier burst（模擬 F22 前段的 long HIGH，讓接收器 AGC 準備）
            p = gdo0
            p(1); time.sleep_ms(10)   # 10ms carrier HIGH
            p(0); time.sleep_ms(5)    # 5ms LOW
            p(1); time.sleep_ms(8)    # 8ms carrier HIGH
            p(0); time.sleep_ms(5)    # 5ms LOW

            for i in range(3):
                replay_f22(gdo0)
                time.sleep_ms(INTER_MS)

            gdo0(0)
            strobe(SIDLE)
            gdo0 = Pin(6, Pin.IN)
            print('TX done')
            while btn.value() == 0:
                time.sleep_ms(10)
    time.sleep_ms(50)
