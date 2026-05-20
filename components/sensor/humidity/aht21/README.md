# AHT21 — 溫濕度感應器

**類別**：sensor/humidity  
**介面**：I2C（固定地址 0x38）  
**工作電壓**：2.2–5.5V  

## 規格

| 項目 | 值 |
|:--|:--|
| 溫度精度 | ±0.3°C (typical) |
| 濕度精度 | ±2%RH (typical) |
| 量測範圍 | -40~120°C / 0~100%RH |
| 採集週期 | 建議 ≥2 秒（自發熱影響） |

## 接線（Pico）

| AHT21 | Pico |
|:--|:--|
| VDD | 3.3V |
| GND | GND |
| SCL | GP5（建議） |
| SDA | GP4（建議） |

## MicroPython 使用

```python
from machine import Pin, SoftI2C
from aht21 import AHT21

i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
sensor = AHT21(i2c)
temp, rh = sensor.read()
print(f"T={temp:.1f}°C  RH={rh:.1f}%")
```

## 驗證狀態

⏳ unverified — Driver 根據 datasheet 撰寫，待實機驗證
