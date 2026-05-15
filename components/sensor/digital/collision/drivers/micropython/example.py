from collision import CollisionSensor
import time

sensor = CollisionSensor(14)   # 信號端 S 接 GPIO14

print("開始偵測 碰撞，Ctrl+C 停止...")
while True:
    if sensor.is_hit():
        print("is_hit: True")
    time.sleep_ms(100)
