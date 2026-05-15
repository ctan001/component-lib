# pir — 人体红外热传感器

**類別**：sensor/digital
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-high

## 描述

PIR 人體紅外感應，偵測到人時 S=HIGH；無人 S=LOW，模組內建 3.3V 穩壓

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/pir.py
```

請將 `pir.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
