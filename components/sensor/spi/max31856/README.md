# max31856 — MAX31856 高精度熱電偶數位轉換器（含線性化）

**類別**：sensor/spi
**介面**：SPI（可讀寫暫存器，非 MAX31855 的唯讀架構）
**工作電壓**：AVDD/DVDD 各 3.0–3.6 V
**邏輯**：protocol
**Package**：14-pin TSSOP（MPN: `MAX31856MUD+`，datasheet p.29 Ordering Information 確認）
**狀態**：評估中，尚未購買/實測（見下方背景）

## 描述

Precision Thermocouple to Digital Converter with Linearization，19-bit SPI，
0.0078125°C 解析度，支援 B/E/J/K/N/R/S/T 型熱電偶，±0.15% 精度。

## 跟 MAX31855 的關鍵差異（本案評估重點）

| | MAX31855 | MAX31856 |
|:--|:--|:--|
| 解析度 | 14-bit, 0.25°C | 19-bit, 0.0078125°C |
| 熱電偶類型 | 單一型號對應單一TC類型 | 一顆晶片SPI設定切換8種類型 |
| **數位雜訊濾波** | 無，只能靠外部類比電容 | **內建50Hz/60Hz陷波濾波，Noise Rejection 91dB**（datasheet p.5） |
| 建議差動電容(T+/T-) | 10nF | **100nF**（datasheet p.27，數值不同，注意別直接沿用MAX31855的10nF） |
| 輸入保護 | 無特別規格 | ±45V input protection |
| SPI介面 | 唯讀(24-bit輸出) | 可讀寫暫存器 |
| Package | SOIC-8 | 14-pin TSSOP |

**評估背景**：312-heat-module 專案的 MAX31855 breakout 板上已內建 datasheet 建議的 T+/T- 差動電容（實測 9.4nF）+ VCC-GND 旁路電容，但實際跑 PID 迴路時仍觀察到間歇性 SHORT/error fault，且發生頻率與運作中的 duty/電流正相關。既然 MAX31855 建議的類比濾波電容已到位仍有雜訊，評估換用內建數位陷波濾波的 MAX31856 是否能解決。**待實測驗證，此表格是 datasheet 規格對照，不是效果保證。**

## 接腳定義

**已下單，2026-08-20 預計到貨**（`photos/max31856_breakout_board.jpg` 是賣場商品照，2026-08-19 用戶提供，非實拍；到貨後要換成實拍照片重新核對）。這是仿 Adafruit MAX31856 breakout 命名慣例的板子，跟下方原廠裸晶片 datasheet pin 名稱**不是逐一對應**，以 silkscreen 實際印字為準（賣場商品照上可讀到的字，到貨後仍需拿實體再核對一次，賣場照片解析度/角度可能誤讀）：

| Breakout板 silkscreen | 對應裸晶片 pin（datasheet p.10） | 功能 | 方向 |
|:--|:--|:--|:--|
| VIN | — (板上regulator輸入) | 電源輸入，經板上regulator降壓 | input |
| 3Vo | — (板上regulator輸出) | 3.3V輸出，疑似可對外供電，待查證 | output? |
| GND | AGND+DGND(板上應已短接) | 接地 | input |
| SDO | SDO | SPI資料輸出(MISO) | output |
| SCK | SCK | SPI序列時脈輸入 | input |
| SDI | SDI | SPI資料輸入(MOSI) | input |
| CS | CS | 晶片選擇(active low) | input |
| FLT | FAULT | 故障輸出 | output |
| DRDY | DRDY | Data Ready輸出(active low) | output |
| 板上方 "+"/"-" 兩個焊接孔 | T+ / T- | 熱電偶輸入，需自行焊上照片裡附的綠色2-pin端子座 | input |

板子隨附但**未焊接**：一顆綠色2-pin端子座(TC線用)、一排排針(9pin，焊到SPI/電源那排腳位用)，都要使用者自己焊接才能用。

⚠️ 板上IC標示為 `MAX31856MUD +506`，跟 datasheet Ordering Information 的 `MAX31856MUD+` 一致，但 **VIN/3Vo/GND 這三隻腳背後的板上電路(regulator)沒有原廠schematic可查證**，待之後有需要再深入。

## Datasheet

[MAX31856.pdf](datasheet/MAX31856.pdf)（原廠 analog.com PDF，透過 DigiKey API 查 MPN `MAX31856MUD+T` 取得 `datasheet_url` 欄位後下載，2026-08-19，見 `feedback_datasheet_source_official`）

## Driver

尚未撰寫，待硬體到貨後開始。

## 驗證狀態

❌ not_verified — 尚未購買硬體，此條目目前只有 datasheet 規格研究，無實測資料。
