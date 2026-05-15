# adxl345 — ADXL345加速度传感器

**類別**：sensor/imu
**介面**：I2C, SPI
**工作電壓**：2.0–3.6 V
**邏輯**：protocol

## 描述

ADXL345 三軸加速度計，支援 I2C/SPI，量程 ±2/4/8/16g，10-bit 解析度

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SDA/SDI | I2C SDA / SPI MOSI | bidirectional |
| SCL/SCK | I2C SCL / SPI SCK | input |
| SDO | SPI MISO / I2C地址選擇（GND=0x53, VCC=0x1D） | output |
| CS | SPI 片選（I2C 模式接 VCC） | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/adxl345.py
```

請將 `adxl345.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

[ADXL345.pdf](https://www.mouser.com/datasheet/2/609/ADXL345-1544506.pdf)

## 驗證狀態

⏳ pending
