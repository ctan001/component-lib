"""
oled_ssd1309.py — 2.42" SSD1309 128x64 OLED driver for MicroPython (Pico)

SSD1309 shares most SSD1306 commands but has a different charge pump:
  SSD1306: 0x8D, 0x14  (internal charge pump)
  SSD1309: 0xAD, 0x8B  (internal DC-DC ON)
Sending the ssd1306 command to SSD1309 leaves the panel voltage unregulated,
causing persistent vertical stripe artifacts. This class overrides init_display()
with the correct SSD1309 sequence.

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

from machine import Pin, SoftI2C
import ssd1306

I2C_ADDR = 0x3C
WIDTH    = 128
HEIGHT   = 64


class OLED(ssd1306.SSD1306_I2C):
    def __init__(self, sda: int, scl: int, addr: int = I2C_ADDR,
                 width: int = WIDTH, height: int = HEIGHT):
        i2c = SoftI2C(sda=Pin(sda), scl=Pin(scl))
        super().__init__(width, height, i2c, addr=addr)

    def init_display(self):
        for cmd in (
            0xAE,                    # display off
            0x20, 0x00,              # horizontal addressing mode
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
