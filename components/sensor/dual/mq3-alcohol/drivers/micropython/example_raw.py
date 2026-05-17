from machine import ADC, Pin
import time

# LCD 可選：有接就顯示，沒接就只印 serial
try:
    from lcd_128x32_st7567a import LCD128x32
    lcd = LCD128x32(sda=4, scl=5)
    has_lcd = True
except Exception:
    has_lcd = False

adc = ADC(Pin(26))

print("MQ-3 Raw Monitor — Ctrl+C to stop")
while True:
    raw = adc.read_u16()
    v   = raw / 65535 * 3.3

    if has_lcd:
        lcd.Clear()
        lcd.Cursor(0, 0); lcd.Display("MQ-3 Raw Monitor")
        lcd.Cursor(1, 0); lcd.Display(f"Raw: {raw}")
        lcd.Cursor(2, 0); lcd.Display(f"V:   {v:.4f}V")
        lcd.Cursor(3, 0); lcd.Display("Warming up...")

    print(f"raw={raw}  V={v:.4f}")
    time.sleep_ms(500)
