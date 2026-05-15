from rgb_3color import RGB3LED
import time

# R 接 GPIO12，Y 接 GPIO13，G 接 GPIO14
led = RGB3LED(r_pin=12, y_pin=13, g_pin=14)

print("三色 LED 測試...")
for color, fn in [("紅", led.red), ("黃", led.yellow), ("綠", led.green)]:
    print(f"  {color}色")
    fn()
    time.sleep(1)

led.off()
print("完成")
