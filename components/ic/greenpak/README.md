# GreenPAK（TSSOP / "G" 封裝）選料資料庫

Renesas GreenPAK 是可規劃混合訊號 IC（Configurable Mixed-Signal Matrix）：用 GUI 工具「Go Configure Software Hub」拖拉配置 LUT/正反器/振盪器/類比比較器等巨集單元，燒錄進 NVM，不寫韌體。

**這份資料庫只收錄 TSSOP 封裝（現行命名後綴 "G"，Dialog 時代舊稱 "AG"）的型號** —— 這個封裝腳距 0.65mm，比其餘 STQFN/MSTQFN（0.4mm pitch）好手焊/好 rework，是本專案刻意鎖定的封裝條件。詳見 [[project_pai_system]] 的 GreenPAK 分類說明。

## 資料來源

- 型號清單：Renesas 官方 [GreenPAK Portfolio Brochure](https://www.renesas.com/en/document/bro/greenpak-configurable-mixed-signal-matrix-family-overview)（Doc No. R11CP0004EU0104，2026年版）「Alternate Package Type and Size」欄位
- 庫存/價格/datasheet 連結：DigiKey KeywordSearch API + Mouser SearchByPartNumber API（透過 [bom-sourcing skill](../../../../../000_Agent/skills/bom-sourcing/) 官方 API，查詢日期見各 component.json 的 `updated`）

⚠️ Portfolio brochure 是行銷整理文件，標註「*more packages available」，不保證完全窮舉。之後若發現遺漏的 TSSOP 型號，比照同樣流程（DigiKey/Mouser API 查證）補充。

## 家族比較表（2026-08-15 已對照各自 datasheet Pinout + Table 5 逐一核實）

| MPN | 對應 QFN 型號 | 車規/一般 | 狀態 | IO腳位 | ADC | 比較器 | LUT | Counters/Delays | DFF/Latch | PWM | 通訊介面 | 供電範圍 | 特殊功能 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [slg46620g](slg46620g/) | SLG46620 | 一般 | ✅ Active | 18 GPIO（單電源） | 8-bit SAR ×1(含PGA) | 6 | 26 | 10 | 12 | 3 | SPI | 1.8–5.5V | 2xDAC |
| [slg46824g](slg46824g/) | SLG46824 | 一般 | ✅ Active | 15 IO（Dual Supply） | – | 2(ACMPxL) | 19 | 8 | 17 | – | I²C | VDD 2.3–5.5V／VDD2 1.71–5.5V | – |
| [slg46826g](slg46826g/) | SLG46826 | 一般 | ✅ Active | 15 IO（Dual Supply） | – | 4(2xACMPxH+2xACMPxL) | 19 | 8 | 17 | – | I²C | VDD 2.3–5.5V／VDD2 1.71–5.5V | 類比溫度感測器、2-kbit I²C EEPROM模擬 |
| [slg46620-ag](slg46620-ag/) | SLG46620-A | 車規(-40~105°C) | ⚠️ 兩邊缺貨 | 18 GPIO（單電源，⚠️只有TSSOP無STQFN選項） | 8-bit SAR ×1(含PGA) | 6 | 26 | 10 | 12 | 3 | SPI | 1.71–3.6V | 2xDAC，AEC-Q100 |
| [slg46827-ag](slg46827-ag/) | SLG46827-A | 車規(-40~105°C) | ⛔ DigiKey判NFND停產 | 15 IO（Dual Supply，⚠️只有TSSOP無STQFN選項） | – | 4(2xACMPxH+2xACMPxL) | 19 | 8 | 17 | – | I²C | VDD 2.3–5.5V／VDD2 1.71–5.5V | 類比溫度感測器、In-System Debug，AEC-Q100 |

**Dual Supply（雙電源域）說明：** SLG46824G/SLG46826G/SLG46827-AG 都有獨立的 VDD2 pin，讓一部分 IO 可以吃不同電壓（例如部分IO配合3.3V邏輯、部分配合1.8V邏輯），常見於需要跨電壓域接口的設計。SLG46620系列（G版與AG版）沒有這個功能，是單電源設計。

**車規版封裝提醒：** SLG46620-AG 和 SLG46827-AG 的官方 datasheet「Packages Available」只列出 TSSOP，沒有 STQFN 選項——不像一般版 SLG46620/SLG46826 兩種封裝都有。

## 選料建議（依現貨狀況，2026-08-15 查證）

- **一般設計首選：SLG46620G** —— 唯一有 8-bit ADC + SPI + 最多 LUT/Counter 的款式，DigiKey/Mouser 現貨都充足（5.5k+/9k+ 顆）
- **只需 I²C + 比較器、不需 ADC**：SLG46826G（4 顆 ACMP）優於 SLG46824G（2 顆 ACMP），現貨也較多
- **車規需求**：SLG46620-AG 目前兩邊都缺貨，SLG46827-AG 已被 DigiKey 標記 NFND（Not For New Designs）——新設計不建議選用，若既有設計要維護才考慮 Mouser 尚存的庫存
