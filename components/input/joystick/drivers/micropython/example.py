from joystick import Joystick
import time

# X 接 GPIO26，Y 接 GPIO27，B（Z軸按鈕）接 GPIO14
js = Joystick(x_pin=26, y_pin=27, btn_pin=14)

print("搖桿測試，Ctrl+C 停止...")
while True:
    x, y = js.read_xy()
    pressed = js.is_pressed()
    print(f"X={x:5d}  Y={y:5d}  按鈕={'按下' if pressed else '未按'}")
    time.sleep_ms(100)
