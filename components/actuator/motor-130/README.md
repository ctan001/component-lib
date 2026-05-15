# motor-130 — 130电机模块

**類別**：actuator
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-high

## 描述

130 DC 馬達 + HR1124S H 橋驅動，IN+=HIGH/IN-=LOW 正轉，反之反轉，兩者同 LOW 滑行停止

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| IN+ | 馬達控制端正 | input |
| IN- | 馬達控制端負 | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/motor_130.py
```

請將 `motor_130.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
