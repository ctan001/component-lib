from mq3_alcohol import MQ3Alcohol
import time

sensor = MQ3Alcohol(a0_pin=26, d0_pin=14)   # A0 接 GPIO26（ADC），D0 接 GPIO14

print("開始讀取 MQ-3 酒精感應器，Ctrl+C 停止...")
print("提示：A0 類比值越大表示酒精濃度越高")
while True:
    raw = sensor.read_analog()
    voltage = sensor.read_voltage()
    alarm = sensor.is_alarm()
    print(f"raw={raw:5d}  {voltage:.3f}V  alarm={alarm}")
    time.sleep_ms(200)
