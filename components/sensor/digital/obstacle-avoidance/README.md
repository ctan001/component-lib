# obstacle-avoidance — 避障传感器

**類別**：sensor/digital
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-low

## 描述

NE555+IR 避障感應，有障礙物時 S=LOW，無障礙 S=HIGH，兩個電位器可調距離

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/obstacle_avoidance.py
```

請將 `obstacle_avoidance.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
