"""
ENS160 + AHT21 + SSD1309 OLED 空氣品質監測
兩條獨立 I2C bus：
  OLED   → GP4(SDA) / GP5(SCL)  addr 0x3C
  感應器 → GP6(SDA) / GP7(SCL)  AHT21=0x38, ENS160=0x53

上傳順序：
  mpremote cp aht21.py :aht21.py
  mpremote cp ens160.py :ens160.py
  mpremote cp oled_ssd1309.py :oled_ssd1309.py
  mpremote cp main.py :main.py
"""

import time
from machine import Pin, SoftI2C
from aht21 import AHT21
from ens160 import ENS160
from oled_ssd1309 import OLED

OLED_SDA = 4
OLED_SCL = 5
SENSOR_SDA = 6
SENSOR_SCL = 7
READ_INTERVAL = 2000  # ms

# OLED 獨立 I2C bus（GP4/GP5）
oled = OLED(sda=OLED_SDA, scl=OLED_SCL)

# 感應器獨立 I2C bus（GP6/GP7）
i2c = SoftI2C(sda=Pin(SENSOR_SDA), scl=Pin(SENSOR_SCL))
aht = AHT21(i2c)
ens = ENS160(i2c)

oled.fill(0)
oled.text("Initializing...", 0, 28)
oled.show()
time.sleep_ms(2000)  # ENS160 暖機


def draw(temp, rh, aqi, tvoc, eco2):
    oled.fill(0)

    # Line 0: T and RH
    oled.text("T:{:.1f}C  H:{:.0f}%".format(temp, rh), 0, 0)

    # Divider
    oled.hline(0, 10, 128, 1)

    # Line 1: AQI with label
    label = ("", "Excellent", "Good", "Moderate", "Poor", "Unhealthy")
    aqi_str = label[aqi] if 1 <= aqi <= 5 else "?"
    oled.text("AQI:{} {}".format(aqi, aqi_str), 0, 14)

    # Line 2: eCO2
    oled.text("CO2: {} ppm".format(eco2), 0, 26)

    # Line 3: TVOC
    oled.text("TVOC:{} ppb".format(tvoc), 0, 38)

    # Bottom: status bar
    oled.hline(0, 52, 128, 1)
    oled.text("ENS160+AHT21", 8, 55)

    oled.show()


print("Starting ENS160+AHT21 monitor...")

while True:
    # Step 1: Read AHT21
    temp, rh = aht.read()

    # Step 2: Feed compensation to ENS160
    ens.set_compensation(temp, rh)

    # Step 3: Read ENS160
    aqi, tvoc, eco2 = ens.read()

    # Step 4: Display
    draw(temp, rh, aqi, tvoc, eco2)

    # Step 5: Serial log
    print("T={:.1f}C  H={:.0f}%  AQI={}  TVOC={}ppb  eCO2={}ppm".format(
        temp, rh, aqi, tvoc, eco2))

    time.sleep_ms(READ_INTERVAL)
