# reed-switch — 干簧管模块

**類別**：sensor/digital
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-low

## 描述

乾簧管磁場感應，有磁場時簧片吸合 S=LOW，LED 亮；無磁場 S=HIGH（上拉）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/reed_switch.py
```

請將 `reed_switch.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
