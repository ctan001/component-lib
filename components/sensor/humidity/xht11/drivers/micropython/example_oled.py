"""
example_oled.py — XHT11 溫濕度 + SSD1309 OLED 顯示

接線：
  XHT11: S=GP14, V=3.3V, G=GND
  OLED:  SDA=GP4, SCL=GP5, VDD=3.3V
"""

from xht11 import XHT11
from oled_ssd1309 import OLED
import time

sensor = XHT11(14)
oled   = OLED(sda=4, scl=5)


def draw(temp, humi):
    oled.fill(0)

    # 標題列
    oled.text("XHT11 Monitor", 0, 0)
    oled.hline(0, 10, 128, 1)

    # 溫度
    oled.text("Temp", 0, 18)
    oled.text(f"{temp} C", 60, 18)

    # 濕度
    oled.text("Humi", 0, 32)
    oled.text(f"{humi} %", 60, 32)

    # 底部橫線 + 提示
    oled.hline(0, 53, 128, 1)
    oled.text("GP14 DHT11", 16, 56)

    oled.show()


print("XHT11 + OLED 啟動，Ctrl+C 停止...")

while True:
    try:
        temp, humi = sensor.read()
        draw(temp, humi)
        print(f"T={temp}°C  H={humi}%RH")
    except Exception as e:
        oled.fill(0)
        oled.text("Read error", 16, 28)
        oled.show()
        print("Error:", e)
    time.sleep(2)
