from tilt import TiltSensor
import time

sensor = TiltSensor(14)   # 信號端 S 接 GPIO14

print("開始偵測 傾斜，Ctrl+C 停止...")
while True:
    if sensor.is_tilted():
        print("is_tilted: True")
    time.sleep_ms(100)
