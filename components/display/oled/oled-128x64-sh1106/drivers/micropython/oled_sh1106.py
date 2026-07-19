"""
oled_sh1106.py — 1.3" SH1106 128x64 OLED driver for MicroPython (Pico)

SH1106 差異（依原廠 Sino Wealth datasheet 確認）：
  - charge pump: 0xAD,0x8B (內供VCC/內部DC-DC ON)，跟SSD1306內建的0x8D,0x14不相容
  - GDDRAM是132欄寬，但面板只顯示中間128欄 → 每次寫入前欄位起始位址須設為2，
    不是0，否則畫面會偏移/跑版

show() 用 Page Addressing Mode，每個page寫入前都明確設定page+欄位(含2欄offset)。

接線 (I2C，硬體I2C，不用SoftI2C):
  GND → GND
  VCC → 3.3V
  SCL → e.g. GP5
  SDA → e.g. GP4

用法:
  from oled_sh1106 import OLED
  oled = OLED(sda=4, scl=5)
  oled.text("Hello!", 0, 0)
  oled.show()
"""

from machine import Pin, I2C
import ssd1306

I2C_ADDR = 0x3C   # 0x3D 如果 D/C# 接 VDD（依原廠datasheet p.16）
WIDTH    = 128
HEIGHT   = 64
_COL_OFFSET = 2   # SH1106 GDDRAM是132欄，面板只顯示中間128欄

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
        _t.sleep_ms(100)  # 冷開機等待VDD穩定
        super().__init__(width, height, i2c, addr=addr)

    def init_display(self):
        for cmd in (
            0xAE,                    # display off
            0xD5, 0x80,              # clock divide/osc freq
            0xA8, self.height - 1,   # multiplex ratio (63 for 64-row)
            0xD3, 0x00,              # display offset = 0
            0x40,                    # display start line = 0
            0xAD, 0x8B,              # charge pump: 內供VCC(internal DC-DC ON)
            0xA1,                    # segment remap
            0xC8,                    # COM scan direction (remapped)
            0xDA, 0x12,              # COM pins config
            0x81, 0xFF,              # contrast（內供VCC時原廠範例用0xFF）
            0xD9, 0x1F,              # pre-charge period
            0xDB, 0x40,              # VCOMH deselect level
            0xA4,                    # output follows RAM（避免軟重啟殘留A5全亮狀態）
            0xA6,                    # normal (non-inverted) display
            0xAF,                    # display on
        ):
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def show(self):
        # SH1106 Page Addressing Mode + 2欄offset(132欄GDDRAM只顯示中間128欄)
        for page in range(self.pages):
            self.write_cmd(0xB0 + page)                    # set page address (B0-B7)
            self.write_cmd(0x00 | (_COL_OFFSET & 0x0F))     # column start lower nibble
            self.write_cmd(0x10 | (_COL_OFFSET >> 4))       # column start upper nibble
            offset = page * self.width
            self.write_data(self.buffer[offset:offset + self.width])
