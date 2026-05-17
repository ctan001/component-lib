# MQ-3 酒精感應器 — I2C 2004 LCD 顯示
# 接線：
#   MQ-3 VCC → VBUS (pin 40, 5V)
#   MQ-3 GND → GND
#   MQ-3 A0  → GPIO26 (ADC0)
#   LCD  VCC → VBUS (5V)
#   LCD  GND → GND
#   LCD  SDA → GPIO4
#   LCD  SCL → GPIO5
#
# mg/L 換算說明：
#   Rs = RL × (Vcc - Vout) / Vout      RL=1.5kΩ, Vcc=5V（模組電路）
#   Ro = Rs_air / 4                     啟動時清潔空氣校準，Rs_air/Ro 典型 ≈ 4
#   C  = 0.4 × (Ro/Rs)^1.667           datasheet 冪次法則 α=0.6
#   台灣酒測法規：0.15 mg/L=法規上限, 0.25 mg/L=公共危險

from machine import ADC, Pin, I2C
from lcd_2004_i2c import LCD2004I2C
import time

# --- 常數 ---
VCC          = 5.0
RL           = 1500
VREF         = 3.3
WARMUP_S     = 30
CALIB_S      = 15
RS_AIR_RATIO = 4.0

# --- 硬體 ---
adc = ADC(Pin(26))
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
lcd = LCD2004I2C(i2c, addr=0x27)

# --- 工具函數 ---
def read_v():
    raw = adc.read_u16()
    return raw, raw / 65535 * VREF

def v_to_rs(v):
    if v < 0.001:
        return 9_999_999
    return max(1, int(VCC * RL / v - RL))

def rs_to_mgl(rs, ro):
    if rs <= 0 or ro <= 0:
        return 0.0
    ratio = ro / rs
    if ratio < 0.001:
        return 0.0
    return 0.4 * (ratio ** (1 / 0.6))

def mgl_status(mgl):
    if   mgl < 0.15:  return "PASS "
    elif mgl < 0.25:  return "LIMIT"
    else:             return "CRIME"

# --- 預熱 ---
for i in range(WARMUP_S, 0, -1):
    _, v = read_v()
    lcd.clear()
    lcd.set_cursor(0, 0); lcd.print("MQ-3 Warmup")
    lcd.set_cursor(0, 1); lcd.print(f"Heating {i:2d}s")
    lcd.set_cursor(0, 2); lcd.print("Keep clean air")
    lcd.set_cursor(0, 3); lcd.print(f"V:{v:.4f}V")
    time.sleep(1)

# --- 清潔空氣校準 ---
lcd.clear()
lcd.set_cursor(0, 0); lcd.print("Calibrating Ro")
lcd.set_cursor(0, 1); lcd.print("Clean air only!")
samples = []
for i in range(CALIB_S):
    _, v = read_v()
    rs = v_to_rs(v)
    samples.append(rs)
    lcd.set_cursor(0, 3); lcd.print(f"Rs:{rs//1000:5d}k {i+1:2d}/{CALIB_S}")
    time.sleep(1)

rs_air = sum(samples) / len(samples)
ro = rs_air / RS_AIR_RATIO
lcd.set_cursor(0, 2); lcd.print(f"Ro:{ro//1000:.0f}k OK")
time.sleep(2)
print(f"[CAL] Rs_air={rs_air:.0f}  Ro={ro:.0f}")

# --- 讀取迴圈 ---
BREATH_DETECT = 0.06
BREATH_END    = 0.025

state      = "sensing"
peak_mgl   = 0.0
result_end = 0

while True:
    raw, v = read_v()
    rs  = v_to_rs(v)
    mgl = rs_to_mgl(rs, ro)

    if state == "sensing":
        st = mgl_status(mgl)
        lcd.clear()
        lcd.set_cursor(0, 0); lcd.print(f"{st} {mgl:.3f}mg/L")
        lcd.set_cursor(0, 1); lcd.print(f"V:{v:.3f} Rs:{rs//1000:4d}k")
        lcd.set_cursor(0, 2); lcd.print(f"Rs:{rs:7d} Ohm")
        lcd.set_cursor(0, 3); lcd.print(f"Lim:0.15|DUI:0.25")
        print(f"raw={raw:5d}  V={v:.3f}  Rs={rs:7d}  {mgl:.3f}mg/L  {st}")
        if mgl > BREATH_DETECT:
            state    = "breath"
            peak_mgl = mgl

    elif state == "breath":
        if mgl > peak_mgl:
            peak_mgl = mgl
        st = mgl_status(mgl)
        lcd.clear()
        lcd.set_cursor(0, 0); lcd.print(">> BLOWING <<")
        lcd.set_cursor(0, 1); lcd.print(f"Now:{mgl:.3f}mg/L")
        lcd.set_cursor(0, 2); lcd.print(f"Peak:{peak_mgl:.3f}mg/L")
        lcd.set_cursor(0, 3); lcd.print(f"Status:{st}")
        print(f"BREATH peak={peak_mgl:.3f}  now={mgl:.3f}mg/L")
        if mgl < BREATH_END:
            state      = "result"
            result_end = time.ticks_ms() + 3000

    elif state == "result":
        st = mgl_status(peak_mgl)
        lcd.clear()
        lcd.set_cursor(0, 0); lcd.print(f"RESULT: {st}")
        lcd.set_cursor(0, 1); lcd.print(f"{peak_mgl:.3f} mg/L")
        lcd.set_cursor(0, 2); lcd.print(f"Lim:0.15|DUI:0.25")
        lcd.set_cursor(0, 3); lcd.print(f"Back in 3s...")
        print(f"RESULT {peak_mgl:.3f}mg/L  {st}")
        if time.ticks_diff(time.ticks_ms(), result_end) >= 0:
            state    = "sensing"
            peak_mgl = 0.0

    time.sleep_ms(200)
