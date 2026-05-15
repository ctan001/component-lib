from capacitive_touch import CapTouch
import time

sensor = CapTouch(14)   # 信號端 S 接 GPIO14

print("開始偵測 電容觸摸，Ctrl+C 停止...")
while True:
    if sensor.is_touched():
        print("is_touched: True")
    time.sleep_ms(100)
