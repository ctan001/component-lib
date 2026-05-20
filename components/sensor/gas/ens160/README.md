# ENS160 — 數位空氣品質感應器

**類別**：sensor/gas  
**介面**：I2C（0x52 / 0x53）  
**工作電壓**：模組 VIN 5V（板載穩壓至 1.8V）

## AQI 等級

| AQI | 等級 |
|:--|:--|
| 1 | Excellent |
| 2 | Good |
| 3 | Moderate |
| 4 | Poor |
| 5 | Unhealthy |

## 接線（ENS160+AHT21 combo 板，Pico）

| 模組 | Pico |
|:--|:--|
| VIN | 5V（VBUS）或 3.3V |
| GND | GND |
| SCL | GP5 |
| SDA | GP4 |

> **I2C 地址**：combo 板 ADDR 接 VDD → 使用 **0x53**

## MicroPython 使用

```python
from machine import Pin, SoftI2C
from ens160 import ENS160

i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
ens = ENS160(i2c)
ens.set_compensation(25.0, 50.0)   # 先餵 T/RH 補償
aqi, tvoc, eco2 = ens.read()
print(f"AQI={aqi}  TVOC={tvoc}ppb  eCO2={eco2}ppm")
```

## 注意事項
- 首次上電後需暖機數分鐘才穩定
- 每次讀取前呼叫 `set_compensation()` 可提升精度
- combo 板上 AHT21 固定 0x38，ENS160 固定 0x53

## 驗證狀態

⏳ unverified — Driver 根據 datasheet 撰寫，待實機驗證
