# photoresistor — 光敏电阻传感器

**類別**：sensor/analog
**介面**：ADC
**工作電壓**：3.3–5.0 V
**邏輯**：analog

## 描述

光敏電阻分壓電路，光越強電阻越小，S 電壓越高，ADC 值越大

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/photoresistor.py
```

請將 `photoresistor.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
