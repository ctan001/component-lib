from rgb_plugin import PluginRGB
import time

# R 接 GPIO12，G 接 GPIO13，B 接 GPIO14
led = PluginRGB(r_pin=12, g_pin=13, b_pin=14)

colors = [
    ("紅", 1, 0, 0),
    ("綠", 0, 1, 0),
    ("藍", 0, 0, 1),
    ("白", 1, 1, 1),
    ("關", 0, 0, 0),
]
for name, r, g, b in colors:
    print(f"  {name}")
    led.set_color(r, g, b)
    time.sleep(1)
