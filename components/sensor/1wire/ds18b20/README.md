# ds18b20 — DS18B20温度传感器

**類別**：sensor/1wire
**介面**：1-Wire
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

DS18B20 數位溫度感應，1-Wire 協議，精度 ±0.5°C，測量範圍 -55°C~+125°C

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| DQ | 單線數據（需 4.7K 上拉） | bidirectional |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/ds18b20.py
```

請將 `ds18b20.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

[DS18B20.pdf](https://www.mouser.com/datasheet/2/256/DS18B20-1203094.pdf)

## 驗證狀態

⏳ pending
