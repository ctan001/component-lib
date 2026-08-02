# raspberry-pi-pico — Raspberry Pi Pico（非Wi-Fi官方板，RP2040）

**類別**：board/mcu
**介面**：USB / GPIO / ADC / PWM / I2C / SPI / UART / PIO
**工作電壓**：VSYS 1.8–5.5V（VBUS 5V±10%，板上SMPS產生3.3V）
**邏輯**：protocol（MCU開發板本身，非單一協議週邊）

## 描述

Raspberry Pi 官方 RP2040 微控制器開發板，**Non-Wi-Fi 原版**（無 CYW43439 無線晶片）。
Pico 系列目前有多款板子，命名與分類刻意標明「非Wi-Fi」以區分：

| 型號 | Wi-Fi | 晶片 |
|:--|:--|:--|
| **Raspberry Pi Pico（本款）** | 無 | RP2040 |
| Raspberry Pi Pico W | 有(CYW43439) | RP2040 |
| Raspberry Pi Pico 2 | 無 | RP2350 |
| Raspberry Pi Pico 2 W | 有(CYW43439) | RP2350 |

本專案（電子手指精準點擊控制，COM7）實際使用的就是這款。

## 機構尺寸

| 項目 | 數值 | 來源/信心度 |
|:--|:--|:--|
| 板外框 | 21 × 51 mm，厚1mm | 官方datasheet p.6 文字直接標明 |
| 鎖孔 | 4× Ø2.1mm（±0.05mm） | 官方Figure 3圖上直接標註 |
| 鎖孔水平間距(中心距) | 17.78 mm | 官方Figure 3圖上直接標註 |
| 鎖孔垂直間距(中心距) | 48.26 mm | 官方Figure 3圖上直接標註 |
| 鎖孔到左右邊緣內縮 | 1.61 mm | 圖上直接標註，且與(21-17.78)/2計算值一致，**已交叉驗證** |
| 鎖孔到上下邊緣內縮 | 1.37 mm | 推算值=(51-48.26)/2，圖上未直接印出，信心度中等 |
| 主排針間距 | 2.54mm(0.1")，孔徑1mm | 官方文字段落，相容breadboard/veroboard |
| Micro-USB位置 | 懸空於頂邊外 | 官方文字段落；確切開口尺寸待補(圖上標註不夠清楚) |

機構圖來源：`datasheet/RP-008307-DS-2-pico-datasheet.pdf`，Chapter 2 Mechanical specification, **Figure 3**（p.6，"The dimensions of the Raspberry Pi Pico Rev3 board"）。
因該圖是嵌入圖片，文字轉檔會遺失標註，改用 PyMuPDF 對該頁做4倍率渲染後逐區裁切放大讀取數字（比對「PDF高解析度zoom驗證技巧」方法）。

## 系統腳位（非GPIO）

| 腳位 | 功能 | 方向 |
|:--|:--|:--|
| VBUS | Micro-USB輸入電壓 | input |
| VSYS | 主系統電源輸入 | input |
| 3V3_EN | SMPS enable(內部拉高) | input |
| 3V3 | 板上3.3V輸出(建議<300mA) | output |
| ADC_VREF | ADC參考電壓 | input/output |
| AGND | 類比接地 | input |
| GND | 數位接地 | input |
| RUN | 重置腳(內部上拉，拉低重置) | input |

完整40-pin GPIO功能對照見 `200_Reference/Hardware/Pico/RP2040_Datasheet_摘要.md`（晶片層級）或本datasheet Figure 2/4。

## 訂購資訊

| 型號 | Order Code | 備註 |
|:--|:--|:--|
| Raspberry Pi Pico | SC0915 / SC0916 | 無排針版(本款) |
| Raspberry Pi Pico H | SC0917 | 已焊排針，非本款 |

## 這個元件為什麼沒有 driver

此元件是 host MCU開發板本身（執行 MicroPython 韌體的主體），不是被驅動的週邊元件，
故 `drivers/micropython` 留空。板子的實際應用邏輯見各專案的 `firmware/` 資料夾
（例如 `100_Projects/active/Microcontroller/電子手指精準點擊控制/firmware/finger_clicker_main.py`）。

## Datasheet

`datasheet/RP-008307-DS-2-pico-datasheet.pdf`（Raspberry Pi Ltd 官方文件，經
datasheets.raspberrypi.com → pip-assets.raspberrypi.com 轉址取得）

## 驗證狀態

✅ verified — 2026-07-19，此板(COM7)在「電子手指精準點擊控制」專案長期實機運行驗證
(BJT driver GP17 / OLED I2C0 GP4-GP5 / 按鍵GP15-16)，功能面已確認正常。
機構圖數據為官方datasheet讀取值，尚未拿卡尺對實體板複驗。
