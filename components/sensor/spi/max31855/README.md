# max31855 — MAX31855 K型熱電偶數位轉換器

**類別**：sensor/spi
**介面**：SPI（唯讀）
**工作電壓**：3.0–3.6 V（絕對最大 4.0V，不可接 5V）
**邏輯**：protocol

## 描述

Cold-Junction Compensated Thermocouple-to-Digital Converter，14-bit SPI 輸出，
支援 K/J/N/T/S/R/E 型熱電偶（本案用 K 型），0.25°C 解析度。

## 接腳定義（依實際購入 breakout 板 silkscreen，非裸晶片）

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| Vin | 電源輸入 3.0–3.6V（不可接5V） | input |
| GND | 接地 | input |
| CLK | SPI SCK | input |
| DO  | SPI 資料輸出（MISO） | output |
| CS  | 晶片選擇（active low） | input |
| 3V0 | 未知用途（疑似板上regulator輸出腳，本案未接），照片見 `photos/` | ? |

板上另有一個 2-pin 端子座接 K-type 熱電偶線，標示 `Red -` / `Ye +`（依 ANSI MC96.1 K-type 色碼）。

實際板子照片見 [`photos/`](photos/)。

## MicroPython Driver

```python
from max31855 import MAX31855

sensor = MAX31855(sck=2, mosi=3, miso=0, cs=1)  # 依實際接線調整；spi_id預設0，可傳spi_id=1改用SPI1
tc, cj, fault, scv, scg, oc = sensor.read()
# tc = 熱電偶(case)溫度°C, cj = 冷端(晶片內部)溫度°C
# fault = 任一故障旗標, scv = 短路到VCC, scg = 短路到GND, oc = 熱電偶斷路
```

驅動路徑：`drivers/micropython/max31855.py`
Smoke test：`drivers/micropython/example.py`（含 `self_test()`，用 datasheet Table 4/5 已知數值驗證解碼正確；已在 312-heat-module 專案的 Pico + ApexTester1 上實測跑通）

## Datasheet

[MAX31855.pdf](datasheet/MAX31855.pdf)（官方 analog.com PDF）

## 協定重點（完整說明存於 Claude memory，此處僅摘要）

- 32-bit frame，MSB(D31) first，SPI mode 0（CPOL=0, CPHA=0）
- D[31:18] = 14-bit 熱電偶溫度（0.25°C/LSB），D16 = fault flag，D[15:4] = 12-bit 冷端溫度（0.0625°C/LSB）
- D2/D1/D0 = SCV/SCG/OC 個別故障旗標

## 驗證狀態

✅ verified — 2026-08-13，platform: micropython-pico（透過 ApexTester1 執行）
實測：接線正確時 case(TC)≈20.5°C / internal(CJ)≈25.6°C，讀值穩定、fault=False。
熱電偶端子斷路時會正確回報 OC fault（railed 2047.75°C，與 datasheet 描述吻合）。
