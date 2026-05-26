"""
test_oled.py — 驗證 SSD1309 OLED 接線正確（GP10=SDA, GP11=SCL）

上傳到 Pico 前，確認 oled_ssd1309.py 已在 Pico 根目錄。
"""
from oled_ssd1309 import OLED
import time

print("初始化 OLED (GP10/GP11, I2C1)...")
oled = OLED(sda=10, scl=11)

oled.fill(0)
oled.text("=== OLED TEST ===", 0, 0)
oled.text("SDA: GP10", 0, 16)
oled.text("SCL: GP11", 0, 24)
oled.text("I2C1 / 0x3C", 0, 32)
oled.text("128x64 SSD1309", 0, 48)
oled.show()

print("OLED 初始化完成，請確認螢幕有顯示文字。")
print("若螢幕空白或有垂直條紋 → 檢查接線或 I2C 位址")
