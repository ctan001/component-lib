# ht16k33-8x8 — HT16K33 8X8点阵模块

**類別**：display/matrix
**介面**：I2C
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

HT16K33 8×8 LED 點陣驅動，I2C 地址 0x70（A0/A1/A2 全接 GND），最大 16×8 矩陣

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SDA | I2C 數據線 | bidirectional |
| SCL | I2C 時鐘線 | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/ht16k33_8x8.py
```

請將 `ht16k33_8x8.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

[HT16K33.pdf](https://www.mouser.com/datasheet/2/198/DA00-HT16K33v120-1143516.pdf)

## 驗證狀態

⏳ pending
