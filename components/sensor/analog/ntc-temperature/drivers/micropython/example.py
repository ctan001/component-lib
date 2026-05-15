from ntc_temperature import NTCTemperature
import time

sensor = NTCTemperature(26)   # 信號端 S 接 ADC GPIO26

print("開始讀取 NTC 類比溫度，Ctrl+C 停止...")
while True:
    c = sensor.read_celsius()
    f = sensor.read_fahrenheit()
    if c is not None:
        print(f"溫度：{c:.2f}°C  /  {f:.2f}°F")
    else:
        print("讀取失敗")
    time.sleep(1)
