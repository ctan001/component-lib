from water_steam import WaterSensor
import time

sensor = WaterSensor(26)   # 信號端 S 接 ADC GPIO26

print("開始讀取 水滴/水蒸氣感應器，Ctrl+C 停止...")
print("提示：讀取值越大代表水量越多或濕度越高")
while True:
    raw = sensor.read_raw()
    voltage = sensor.read_voltage()
    percent = sensor.read_percent()
    print(f"raw={raw:5d}  voltage={voltage:.3f}V  {percent:.1f}%")
    time.sleep_ms(200)
