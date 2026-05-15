from adxl345 import ADXL345
import time

# SDA 接 GPIO4，SCL 接 GPIO5，SDO 接 GND（地址 0x53）
acc = ADXL345(sda=4, scl=5)

print("ADXL345 加速度計測試，Ctrl+C 停止...")
while True:
    x, y, z = acc.read_xyz()
    print(f"X={x:+.3f}g  Y={y:+.3f}g  Z={z:+.3f}g")
    time.sleep_ms(200)
