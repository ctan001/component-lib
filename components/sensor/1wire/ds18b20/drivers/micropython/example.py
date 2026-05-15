from ds18b20 import DS18B20
import time

# DQ 接 GPIO14，DQ 和 VCC 之間接 4.7K 上拉電阻
sensor = DS18B20(14)
print(f"發現 {sensor.device_count} 個 DS18B20")

while True:
    c = sensor.read_celsius()
    f = sensor.read_fahrenheit()
    print(f"溫度：{c:.2f}°C  /  {f:.2f}°F")
    time.sleep(1)
