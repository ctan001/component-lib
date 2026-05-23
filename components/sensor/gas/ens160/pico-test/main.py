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
from machine import Pin, I2C
from aht21 import AHT21
from ens160 import ENS160
from oled_ssd1309 import OLED

OLED_SDA = 4
OLED_SCL = 5
SENSOR_SDA = 6
SENSOR_SCL = 7
READ_INTERVAL = 2000  # ms

# OLED: 硬體 I2C0（GP4/GP5）
oled = OLED(sda=OLED_SDA, scl=OLED_SCL)

# 感應器: 硬體 I2C1（GP6/GP7）
i2c = I2C(1, sda=Pin(SENSOR_SDA), scl=Pin(SENSOR_SCL), freq=400_000)
aht = AHT21(i2c)
ens = ENS160(i2c)

oled.fill(0)
oled.text("Initializing...", 0, 28)
oled.show()
time.sleep_ms(2000)  # ENS160 暖機


# validity flag → 顯示用標籤
_VALIDITY_LABEL = ("OK", "WarmUp", "Init..", "ERR")

def draw(temp, rh, aqi, tvoc, eco2, validity):
    oled.fill(0)

    # Line 0: T and RH
    oled.text("T:{:.1f}C  H:{:.0f}%".format(temp, rh), 0, 0)

    # Divider
    oled.hline(0, 10, 128, 1)

    label = ("", "Excellent", "Good", "Moderate", "Poor", "Unhealthy")
    aqi_str = label[aqi] if 1 <= aqi <= 5 else "?"

    if validity == 1:
        # Warm-Up: only ~3 min, block display
        oled.text("Warming up...", 0, 14)
        oled.text("Wait ~3 min", 0, 26)
    elif validity == 3:
        # Invalid output: hardware issue
        oled.text("Sensor ERR", 0, 14)
        oled.text("Check wiring", 0, 26)
    else:
        # validity=0 (Normal) or validity=2 (Init, approx data) — show data
        oled.text("AQI:{} {}".format(aqi, aqi_str), 0, 14)
        oled.text("CO2: {} ppm".format(eco2), 0, 26)
        oled.text("TVOC:{} ppb".format(tvoc), 0, 38)

    # Bottom: status bar
    oled.hline(0, 52, 128, 1)
    v_tag = _VALIDITY_LABEL[validity] if validity < 4 else "ERR"
    oled.text("ENS160 [{}]".format(v_tag), 8, 55)

    oled.show()


print("Starting ENS160+AHT21 monitor...")

while True:
    # Step 1: Read AHT21
    temp, rh = aht.read()

    # Step 2: Feed compensation to ENS160
    ens.set_compensation(temp, rh)

    # Step 3: Read ENS160 — None means no new data this cycle (NEWDAT=0)
    result = ens.read()
    if result is None:
        time.sleep_ms(READ_INTERVAL)
        continue  # skip display/log, wait for next sample

    aqi, tvoc, eco2, validity = result

    # Step 4: Display
    draw(temp, rh, aqi, tvoc, eco2, validity)

    # Step 5: Serial log (validity 一起印出)
    v_str = _VALIDITY_LABEL[validity] if validity < 4 else "ERR"
    print("T={:.1f}C  H={:.0f}%  AQI={}  TVOC={}ppb  eCO2={}ppm  [{}]".format(
        temp, rh, aqi, tvoc, eco2, v_str))

    time.sleep_ms(READ_INTERVAL)
