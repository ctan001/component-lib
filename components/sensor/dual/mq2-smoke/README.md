# mq2-smoke — MQ-2烟雾传感器

**類別**：sensor/dual
**介面**：ADC, GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-low

## 描述

MQ-2 煙霧/可燃氣體感應，A0 類比濃度（越濃越大），D0 active-low 閾值警報（電位器調整）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| A0 | 類比信號端（氣體濃度越高值越大） | output |
| D0 | 數位信號端（超過閾值時LOW） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/mq2_smoke.py
```

請將 `mq2_smoke.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
