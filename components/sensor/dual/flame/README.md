# flame — 火焰传感器

**類別**：sensor/dual
**介面**：ADC, GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-low

## 描述

偵測 700–1000nm 紅外光（最佳 880nm），D0 active-low 數位警報，A0 類比強度（越亮值越小）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| A0 | 類比信號端（外界IR越強值越小） | output |
| D0 | 數位信號端（偵測到火焰時LOW） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/flame.py
```

請將 `flame.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
