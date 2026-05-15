from obstacle_avoidance import ObstacleSensor
import time

sensor = ObstacleSensor(14)   # 信號端 S 接 GPIO14

print("開始偵測 避障，Ctrl+C 停止...")
while True:
    if sensor.is_blocked():
        print("is_blocked: True")
    time.sleep_ms(100)
