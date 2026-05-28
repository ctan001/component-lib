"""
Pure OLED static text test — no sensors.
Each line = one page (y=0,8,16,24,32,40,48,56).
On cold boot, all 8 lines should appear correctly every time.
"""
from machine import Pin
from oled_ssd1309 import OLED
import time

oled = OLED(sda=4, scl=5)

oled.fill(0)
oled.text("Page0: HELLO", 0, 0)
oled.text("Page1: WORLD", 0, 8)
oled.text("Page2: 12345", 0, 16)
oled.text("Page3: ABCDE", 0, 24)
oled.text("Page4: FGHIJ", 0, 32)
oled.text("Page5: KLMNO", 0, 40)
oled.text("Page6: PQRST", 0, 48)
oled.text("Page7: UVWXY", 0, 56)
oled.show()

print("Static text shown. Reboot Pico and check if all 8 lines appear correctly.")
