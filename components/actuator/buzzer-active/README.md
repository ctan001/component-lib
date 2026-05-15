# buzzer-active — 有源蜂鸣器

**類別**：actuator
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-high

## 描述

有源蜂鳴器，S=HIGH 三極管導通蜂鳴，S=LOW 靜音（active-high）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/buzzer_active.py
```

請將 `buzzer_active.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
