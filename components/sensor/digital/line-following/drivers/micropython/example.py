from line_following import LineSensor
import time

sensor = LineSensor(14)   # 信號端 S 接 GPIO14

print("開始巡線偵測，Ctrl+C 停止...")
while True:
    if sensor.is_black():
        print("偵測到黑線")
    elif sensor.is_white():
        print("偵測到白色")
    time.sleep_ms(50)
