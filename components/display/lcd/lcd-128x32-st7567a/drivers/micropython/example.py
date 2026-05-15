from lcd_128x32_st7567a import LCD128x32
import time

# SCK=GPIO2, SDA=GPIO3, RS=GPIO4, RST=GPIO5, CS=GPIO6
lcd = LCD128x32(sck=2, sda=3, rs=4, rst=5, cs=6)

print("LCD 128×32 測試...")
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
print("完成")
