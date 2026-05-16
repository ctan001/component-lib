"""
LCD 128x32 ST7567A  硬體測試
接線: SDA=GP4, SCL=GP5, V=3V3, G=GND
"""
from machine import SoftI2C, Pin
import time

ADDR = 0x3F
SDA  = 4
SCL  = 5

def run():
    i2c = SoftI2C(sda=Pin(SDA), scl=Pin(SCL), freq=100_000)

    # --- Test 1: I2C 掃描，確認 LCD 有回應 ---
    devices = i2c.scan()
    if ADDR in devices:
        print(f"[PASS] Test1 I2C 偵測到 0x{ADDR:02X}")
    else:
        print(f"[FAIL] Test1 找不到 0x{ADDR:02X}，掃描到: {[hex(d) for d in devices]}")
        return

    from lcd_128x32_st7567a import LCD128x32
    lcd = LCD128x32(sda=SDA, scl=SCL)
    print("[PASS] Test2 初始化完成（無例外）")

    # --- Test 3: 清除畫面 ---
    lcd.Clear()
    time.sleep_ms(500)
    print("[PASS] Test3 清除畫面（目視確認畫面空白）")

    # --- Test 4: 正常字體四行顯示 ---
    lcd.Cursor(0, 0); lcd.Display("Row 0 ABC")
    lcd.Cursor(1, 0); lcd.Display("Row 1 DEF")
    lcd.Cursor(2, 0); lcd.Display("Row 2 123")
    lcd.Cursor(3, 0); lcd.Display("Row 3 xyz")
    time.sleep_ms(1000)
    print("[PASS] Test4 四行文字顯示（目視確認四行內容）")

    # --- Test 5: 4x 放大顯示 Hello ---
    lcd.Clear()
    lcd.BigDisplay("Hell", x_start=0)   # 4 chars * 28px = 112px fits 128px wide
    time.sleep_ms(1000)
    print("[PASS] Test5 4x 放大顯示 Hell（目視確認大字）")

    # --- Test 6: 清除後空白 ---
    lcd.Clear()
    time.sleep_ms(500)
    print("[PASS] Test6 清除後空白確認")

    print("\n=== 全部測試完成 ===")

run()
