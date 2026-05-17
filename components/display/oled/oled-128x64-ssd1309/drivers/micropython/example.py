"""
example.py — SSD1309 OLED 基本範例

接線：
  GND → GND
  VDD → 3.3V
  SCL → GP5
  SDA → GP4
"""

from oled_ssd1309 import OLED
import time

oled = OLED(sda=4, scl=5)

# 清除畫面
oled.fill(0)

# 顯示文字
oled.text("SSD1309 OLED", 0, 0)
oled.text("128x64 I2C", 0, 16)
oled.text("Hello, Pico!", 0, 32)

# 畫橫線
oled.hline(0, 50, 128, 1)

oled.show()
time.sleep(3)

# 數字計數器
for i in range(10):
    oled.fill(0)
    oled.text(f"Count: {i}", 20, 28)
    oled.show()
    time.sleep(0.5)
