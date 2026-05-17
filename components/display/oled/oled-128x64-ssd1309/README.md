# oled-128x64-ssd1309 — 2.42" OLED 128x64 顯示模組

**類別**：display/oled
**介面**：I2C
**工作電壓**：3.0–5.0 V
**邏輯**：protocol

## 描述

2.42 吋 128×64 像素 OLED 顯示模組，SSD1309 驅動晶片，I2C 介面。
SSD1309 指令集與 SSD1306 完全相容，可直接使用 MicroPython 內建 `ssd1306` 函式庫。
顯示顏色：白 / 藍 / 黃綠（購買時選定，固定）。

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| GND | 接地 | input |
| VDD | 電源 3V–5V | input |
| SCL | I2C 時鐘 | input |
| SDA | I2C 數據 | input |

## I2C 地址

| SA0 | 地址 |
|:--|:--|
| 0（預設） | 0x3C |
| 1 | 0x3D |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/oled_ssd1309.py
# 依賴：MicroPython 內建 ssd1306 模組（micropython-lib）
```

```python
from oled_ssd1309 import OLED

oled = OLED(sda=4, scl=5)   # SDA=GP4, SCL=GP5
oled.fill(0)
oled.text("Hello!", 0, 0)
oled.show()
```

完整範例見 `drivers/micropython/example.py`。

## 重要注意事項

- **SoftI2C 優先**：部分 Pico 板的 Hardware I2C 與此模組有相容性問題（EIO 錯誤），建議使用 SoftI2C。
- 模組使用 **OLED**（自發光），無需背光，對比度高，適合顯示小字與圖示。
- `oled.fill(0)` 清除畫面後必須 `oled.show()` 才會更新到實體顯示器。
- **殘影問題**：SSD1309 上電後 GDDRAM 可能有硬體殘留，`ssd1306` 函式庫只清一次不夠；`oled_ssd1309.py` 已在 `__init__` 中加入第二次 `fill(0)+show()` 修正此問題。

## Datasheet

`datasheet/SSD1309.pdf`

## 驗證狀態

✅ verified — 2026-05-17，micropython-pico，SDA=GP4 / SCL=GP5 / VDD=3.3V
