"""
oled_ssd1309.py — 2.42" SSD1309 128x64 OLED driver for MicroPython (Pico)

SSD1309 shares most SSD1306 commands but has a different charge pump:
  SSD1306: 0x8D, 0x14  (internal charge pump)
  SSD1309: 0xAD, 0x8B  (internal DC-DC ON)

show() uses Page Addressing Mode (SSD1309 cold-boot default) — writes each
of the 8 pages with an explicit column-reset command before the 128-byte
data payload. This avoids the horizontal-mode addressing-command timing
race that causes random garbling after a cold power cycle.

Wiring (I2C):
  GND → GND
  VDD → 3.3V
  SCL → e.g. GP5
  SDA → e.g. GP4

Usage:
  from oled_ssd1309 import OLED
  oled = OLED(sda=4, scl=5)
  oled.text("Hello!", 0, 0)
  oled.show()
"""

from machine import Pin, I2C
import ssd1306

I2C_ADDR = 0x3C
WIDTH    = 128
HEIGHT   = 64

# Hardware I2C bus mapping on Pico (RP2040):
#   I2C0: SDA=GP0/GP4/GP8/GP12/GP16/GP20  SCL=GP1/GP5/GP9/GP13/GP17/GP21
#   I2C1: SDA=GP2/GP6/GP10/GP14/GP18/GP26  SCL=GP3/GP7/GP11/GP15/GP19/GP27
_SDA_TO_BUS = {0:0, 4:0, 8:0, 12:0, 16:0, 20:0,
               2:1, 6:1, 10:1, 14:1, 18:1, 26:1}


class OLED(ssd1306.SSD1306_I2C):
    def __init__(self, sda: int, scl: int, addr: int = I2C_ADDR,
                 width: int = WIDTH, height: int = HEIGHT):
        import time as _t
        bus = _SDA_TO_BUS.get(sda, 0)
        i2c = I2C(bus, sda=Pin(sda), scl=Pin(scl), freq=400_000)
        _t.sleep_ms(100)  # wait for VDD to stabilize on cold boot
        super().__init__(width, height, i2c, addr=addr)

    def init_display(self):
        for cmd in (
            0xAE,                    # display off
            0x40,                    # display start line = 0
            0xA1,                    # seg remap: col 127 → SEG0
            0xA8, self.height - 1,   # multiplex ratio (63 for 64-row)
            0xC8,                    # COM scan: remapped (bottom-up)
            0xD3, 0x00,              # display offset = 0
            0xDA, 0x12,              # COM pins: alternative, no LR remap
            0xD5, 0x80,              # clock: divider=1, osc=8
            0xD9, 0x22,              # pre-charge: phase1=2, phase2=2
            0xDB, 0x34,              # VCOMH deselect = 0.83 × Vcc
            0x81, 0xCF,              # contrast
            0xA4,                    # output follows RAM
            0xA6,                    # normal (non-inverted) display
            0xAD, 0x8B,              # DC-DC control: internal ON (SSD1309)
            0xAF,                    # display on
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def show(self):
        # Page Addressing Mode: explicitly set page + column=0 before each
        # 128-byte write. No reliance on multi-byte addressing commands that
        # can be lost during cold-boot I2C timing.
        for page in range(self.pages):
            self.write_cmd(0xB0 + page)  # set page address (B0-B7)
            self.write_cmd(0x00)          # column start lower nibble = 0
            self.write_cmd(0x10)          # column start upper nibble = 0
            offset = page * self.width
            self.write_data(self.buffer[offset:offset + self.width])
