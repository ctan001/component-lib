# lcd-128x32-st7567a — LCD 128x32 DOT模块

**類別**：display/lcd
**介面**：SPI
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

128×32 像素 LCD，ST7567A 驅動晶片，SPI 介面，頁式定址模式

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SCK | SPI 時鐘 | input |
| SDA | SPI MOSI 數據 | input |
| RS | 指令/數據選擇（LOW=指令，HIGH=數據） | input |
| RST | 硬體重置（LOW=重置） | input |
| CS | SPI 片選（LOW=選中） | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/lcd_128x32_st7567a.py
```

請將 `lcd_128x32_st7567a.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
