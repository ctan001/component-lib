from sound import SoundSensor
import time

sensor = SoundSensor(26)   # 信號端 S 接 ADC GPIO26

print("開始讀取 聲音感應器，Ctrl+C 停止...")
print("提示：讀取值越大代表聲音越響")
while True:
    raw = sensor.read_raw()
    voltage = sensor.read_voltage()
    percent = sensor.read_percent()
    print(f"raw={raw:5d}  voltage={voltage:.3f}V  {percent:.1f}%")
    time.sleep_ms(200)
