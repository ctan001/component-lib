# oled-128x64-sh1106 — 1.3" OLED 128x64 顯示模組

**類別**：display/oled
**介面**：I2C
**工作電壓**：1.65–3.3 V（VDD須等於MCU的I/O電壓）
**邏輯**：protocol

## 描述

1.3 吋 128×64 像素 OLED 顯示模組，SH1106 驅動晶片（Sino Wealth），I2C 介面。
SH1106 的 GDDRAM 是 132 欄寬，但面板只顯示中間 128 欄，直接沿用 MicroPython 內建
`ssd1306` 函式庫會造成畫面偏移，需要自訂 `init_display()` 與 `show()`。

## 機構尺寸

| 項目 | 數值 | 來源 |
|:--|:--|:--|
| 面板尺寸(含Cap) | 34.5 × 23.0 mm | 原廠datasheet |
| 可視顯示區域 | 29.42 × 14.7 mm | 原廠datasheet（與Amazon listing一致，交叉驗證） |
| 完整PCB模組尺寸(含接針) | 33.7 × 35.5 mm | Amazon listing |
| 像素間距 | 0.23 × 0.23 mm | 原廠datasheet |
| 重量 | 約10g | Amazon listing |
| 可視角度 | >160° | Amazon listing |
| 工作溫度 | -20℃~60℃（storage: -30℃~70℃） | Amazon listing |
| 供電電壓(模組) | 3.3V~5V | Amazon listing——晶片本身VDD邏輯電壓是1.65~3.3V，判斷板上有穩壓/電平轉換電路，待實測 |

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| GND | 接地 | input |
| VCC | 電源 3.3V | input |
| SCL | I2C 時鐘 | input |
| SDA | I2C 數據 | input |

## I2C 地址

| D/C# | 地址 |
|:--|:--|
| 接地（預設） | 0x3C |
| 接VDD | 0x3D |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/oled_sh1106.py
# 依賴：MicroPython 內建 ssd1306 模組（micropython-lib）
```

```python
from oled_sh1106 import OLED

oled = OLED(sda=4, scl=5)   # SDA=GP4, SCL=GP5
oled.fill(0)
oled.text("Hello!", 0, 0)
oled.show()
```

完整範例見 `drivers/micropython/example.py`。

## 重要注意事項

- **硬體I2C**：依 Pico I2C 已知坑（SoftI2C 被 GC 打斷導致顯示亂跳），一律用硬體 I2C，不用 SoftI2C。
- **132欄GDDRAM偏移**：SH1106 內部 GDDRAM 是 132 欄，面板只顯示中間 128 欄，`show()` 已內建 2 欄偏移修正，不可拿掉。
- **charge pump指令**：SH1106 用 `0xAD,0x8B`（內供VCC/內部DC-DC），跟 MicroPython 內建 `ssd1306` 預設的 `0x8D,0x14` 不相容，已在 `init_display()` override。
- **原廠datasheet內部矛盾**：datasheet 流程圖摘要與實際程式碼範例對 `0xAD` 後接 `0x8A`/`0x8B` 何者是內供/外供VCC的敘述方向相反；本driver採信程式碼+中文註解版本（`0x8B`=內供VCC），已通過 Codex review。
- `oled.fill(0)` 清除畫面後必須 `oled.show()` 才會更新到實體顯示器。

## Datasheet

`datasheet/SH1106.pdf`（Sino Wealth 官方，經 Sparkfun 代管取得）
`datasheet/Amazon_Listing.pdf`（Amazon賣場listing存檔，含規格表+買家評論——買家評論獨立確認為真正SH1106且不與SSD1306函式庫相容，佐證了本driver的設計方向）

## 驗證狀態

✅ verified — 2026-07-18，micropython-pico：Pico(COM7, I2C0 SDA=GP4/SCL=GP5)，driver上傳後執行文字渲染(3行文字+橫線)，實體螢幕顯示正常，無偏移/跑版/文字截斷，132欄offset處理正確。
