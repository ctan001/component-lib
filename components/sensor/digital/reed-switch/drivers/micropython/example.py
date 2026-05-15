from reed_switch import ReedSwitch
import time

sensor = ReedSwitch(14)   # 信號端 S 接 GPIO14

print("開始偵測 乾簧管，Ctrl+C 停止...")
while True:
    if sensor.is_closed():
        print("is_closed: True")
    time.sleep_ms(100)
