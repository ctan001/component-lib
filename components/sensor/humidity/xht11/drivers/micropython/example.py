from xht11 import XHT11
import time

sensor = XHT11(14)   # 信號端 S 接 GPIO14

print("開始讀取 XHT11 溫濕度，Ctrl+C 停止...")
while True:
    temp, humi = sensor.read()
    print(f"溫度：{temp}°C  濕度：{humi}%RH")
    time.sleep(2)
