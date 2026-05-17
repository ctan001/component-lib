"""
I2C 2004 LCD 使用範例 (YD-RP2040 / Pico)
SDA=GP4, SCL=GP5, VCC=5V, GND=GND
I2C 地址: 0x3F (PCF8574AT 預設)
"""

from machine import I2C, Pin
from lcd_2004_i2c import LCD2004I2C
import time

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
lcd = LCD2004I2C(i2c, addr=0x27)

lcd.set_cursor(0, 0); lcd.print("Hello, World!")
lcd.set_cursor(0, 1); lcd.print("I2C 2004 LCD")
lcd.set_cursor(0, 2); lcd.print("MicroPython Pico")
lcd.set_cursor(0, 3); lcd.print("20x4 Display")

time.sleep(3)

# 掃描確認 I2C 地址
print("I2C scan:", [hex(a) for a in i2c.scan()])
