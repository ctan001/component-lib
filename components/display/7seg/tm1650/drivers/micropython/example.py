from tm1650 import TM1650
import time

# SDA 接 GPIO4，SCL 接 GPIO5
display = TM1650(sda=4, scl=5)

print("TM1650 四位數碼管測試...")
for i in range(100):
    display.show_number(i)
    time.sleep_ms(100)

display.show("HELLO"[:4])
time.sleep(2)
display.clear()
print("完成")
