from button import Button
import time

sensor = Button(14)   # 信號端 S 接 GPIO14

print("開始偵測 按键，Ctrl+C 停止...")
while True:
    if sensor.is_pressed():
        print("is_pressed: True")
    time.sleep_ms(100)
