# servo — 伺服舵机

**類別**：actuator
**介面**：PWM
**工作電壓**：3.3–5.0 V
**邏輯**：pwm

## 描述

伺服舵機，PWM 50Hz（20ms 周期），脈寬 0.5ms-2.5ms 對應 0°-180°

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | PWM 信號端 | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/servo.py
```

請將 `servo.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
