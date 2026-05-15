# ds1307 — 实时时钟DS1307

**類別**：module/rtc
**介面**：I2C
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

DS1307 I2C 實時時鐘（RTC），地址 0x68，BCD 格式，含電池備份，精度 ±2ppm

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SDA | I2C 數據線 | bidirectional |
| SCL | I2C 時鐘線 | input |
| SQW | 方波輸出（可選） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/ds1307.py
```

請將 `ds1307.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

[DS1307.pdf](https://www.mouser.com/datasheet/2/256/DS1307-1203167.pdf)

## 驗證狀態

⏳ pending
