from hc_sr04 import HCSR04
import time

# TRIG 接 GPIO14，ECHO 接 GPIO15
# 注意：HC-SR04 使用 5V 供電，ECHO 輸出為 5V，需分壓後接 Pico GPIO
sensor = HCSR04(trig_pin=14, echo_pin=15)

print("開始超聲波測距，Ctrl+C 停止...")
while True:
    d = sensor.distance_cm()
    if d is not None:
        print(f"距離：{d:.1f} cm")
    else:
        print("超出測距範圍（>400cm）或無回波")
    time.sleep_ms(200)
