from flame import FlameSensor
import time

sensor = FlameSensor(a0_pin=26, d0_pin=14)   # A0 接 GPIO26（ADC），D0 接 GPIO14

print("開始讀取 火焰感應器，Ctrl+C 停止...")
print("提示：A0 類比值越小表示火焰越強（IR 越強）")
while True:
    raw = sensor.read_analog()
    voltage = sensor.read_voltage()
    alarm = sensor.is_flame_detected()
    print(f"raw={raw:5d}  {voltage:.3f}V  alarm={alarm}")
    time.sleep_ms(200)
