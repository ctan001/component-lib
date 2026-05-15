from pir import PIRSensor
import time

sensor = PIRSensor(14)   # 信號端 S 接 GPIO14

print("開始偵測 PIR 人體紅外，Ctrl+C 停止...")
while True:
    if sensor.is_detected():
        print("is_detected: True")
    time.sleep_ms(100)
