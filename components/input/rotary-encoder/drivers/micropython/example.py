from rotary_encoder import RotaryEncoder
import time

# CLK 接 GPIO14，DT 接 GPIO15，SW 接 GPIO16（可選）
enc = RotaryEncoder(clk_pin=14, dt_pin=15, sw_pin=16)

print("旋轉編碼器測試，Ctrl+C 停止...")
last = None
while True:
    val = enc.value
    if val != last:
        print(f"計數：{val}")
        last = val
    if enc.is_pressed():
        enc.reset()
        print("按下按鈕，計數重置為 0")
        time.sleep_ms(300)
    time.sleep_ms(10)
