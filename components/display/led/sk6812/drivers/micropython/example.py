from sk6812 import SK6812
import time

# DIN 接 GPIO14，共 4 顆 SK6812
leds = SK6812(pin=14, n=4)

print("SK6812 測試...")
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,0,0)]
for r, g, b in colors:
    leds.fill(r, g, b)
    leds.show()
    time.sleep_ms(500)

print("彩虹跑馬燈...")
rainbow = [(255,0,0),(255,128,0),(255,255,0),(0,255,0),(0,0,255),(128,0,255)]
for i in range(24):
    for j in range(4):
        r, g, b = rainbow[(i + j) % len(rainbow)]
        leds.set_pixel(j, r, g, b)
    leds.show()
    time.sleep_ms(100)

leds.fill(0,0,0)
leds.show()
print("完成")
