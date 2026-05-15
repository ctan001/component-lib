# xht11 — XHT11温湿度传感器

**類別**：sensor/humidity
**介面**：DHT
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

XHT11 數位溫濕度感應（DHT11 相容），單線協議，溫度精度 ±2°C，濕度精度 ±5%RH

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 單線數據（DHT 協議） | bidirectional |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/xht11.py
```

請將 `xht11.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
