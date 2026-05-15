from adc_button_5way import ADCButton5Way
import time

btn = ADCButton5Way(26)   # 信號端 S 接 ADC GPIO26

print("五路按鍵測試，Ctrl+C 停止...")
last = None
while True:
    key = btn.read()
    if key != last:
        if key:
            print(f"按下 SW{key}  (raw={btn.read_raw()})")
        else:
            print("無按鍵")
        last = key
    time.sleep_ms(50)
