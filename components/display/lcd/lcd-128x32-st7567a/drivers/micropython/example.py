from lcd_128x32_st7567a import LCD128x32
import time

# SDA=GP4 (pin6), SCL=GP5 (pin7), V=3V3, G=GND
lcd = LCD128x32(sda=4, scl=5)

# 畫邊框
for x in range(128):
    lcd.pixel(x, 0, 1)
    lcd.pixel(x, 31, 1)
for y in range(32):
    lcd.pixel(0, y, 1)
    lcd.pixel(127, y, 1)
lcd.show()
time.sleep(3)
lcd.clear()
lcd.show()
