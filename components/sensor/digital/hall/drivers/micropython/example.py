from hall import HallSensor
import time

sensor = HallSensor(14)   # 信號端 S 接 GPIO14

print("開始偵測 霍爾，Ctrl+C 停止...")
while True:
    if sensor.is_magnet():
        print("is_magnet: True")
    time.sleep_ms(100)
