# hc-sr04 — 超声波传感器

**類別**：sensor/ultrasonic
**介面**：GPIO
**工作電壓**：4.5–5.5 V
**邏輯**：protocol

## 描述

HC-SR04 超聲波測距，量程 2-400cm，精度 3mm，TRIG 拉高 10μs 觸發，ECHO 高電平持續時間正比距離

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| TRIG | 觸發端（輸出 10μs 高電平） | input |
| ECHO | 回波端（高電平持續時間 = 往返時間） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/hc_sr04.py
```

請將 `hc_sr04.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
