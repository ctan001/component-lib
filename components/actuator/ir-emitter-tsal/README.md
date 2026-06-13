# ir-emitter-tsal — 红外发射模块 TSAL6100/6200 + BJT 驱动

**類別**：actuator
**介面**：GPIO / PWM
**工作電壓**：**5 V**（⚠️ LED 驅動用，SIG 邏輯為 3.3V）
**邏輯**：active-high（SIG=HIGH → 發射）

## 描述

940nm 高功率紅外 LED 發射模組，含 **MMBT3904 NPN 低端開關驅動線路**。tr/tf=15ns，適合 38kHz NEC 調制遙控發射。本 entry 只記錄**硬體驅動方式與線路**；NEC 編碼、遙控碼表、coding 留各專案。

## ⚠️ 使用前必讀

1. **VCC 必須接 5V**（不是 3.3V）——LED 經 39Ω 在 5V 下才有足夠電流/射程。
2. **脈衝/調制專用**：設計電流 ~88–99mA 接近 LED 連續額定 100mA。SIG **不可長期維持 HIGH**，否則 LED 與 R1 會在上限附近連續工作；高溫環境再降額。
3. **R1 是 through-hole 1/2W**，不是 0603（功率 0.3–0.38W 超過 SMD 0603 與 1/4W）。

## TSAL6100 vs TSAL6200（Vishay datasheet）

| 項目 | TSAL6100 | TSAL6200 | 共通 |
|:--|:--|:--|:--|
| 半強度角 φ | **±10°**（窄、長距） | **±17°**（廣、覆蓋大） | — |
| Ie @100mA (min/typ/max) | 80 / 170 / 400 mW/sr | 40 / 72 / 200 mW/sr | — |
| 波長 λp | | | 940 nm |
| Vf @100mA | | | 1.35 typ / 1.6 max V |
| If 連續 / IFM 峰值 / IFSM | | | 100mA / 200mA / 1.5A |
| tr / tf | | | 15 ns |
| 封裝 | | | T-1¾ 5mm 藍灰 |

選型：**對準式長距遙控用 6100；大範圍近距用 6200**。兩者腳位/電氣相同，可直接互換。

## 線路圖

見 [`circuit.svg`](circuit.svg)（向量圖，可當接線前對照檢查）。

```
   5V ──[ R1 39Ω 1/2W TH ]──►|── LED(TSAL6100/6200) ──┐
                            (A)            (K)         │ C
   SIG(3.3V)──[ R2 220Ω 0603 ]── B   Q1 MMBT3904(NPN) │
                                 E ────────────────────┴── GND
```

## BOM（驅動線路）

| 編號 | 元件 | 值 | 封裝 | 說明 |
|:--|:--|:--|:--|:--|
| LED | [TSAL6100/6200](datasheet/) | 940nm | T-1¾ 5mm | 短腳/凸緣平邊 = Cathode (−) |
| Q1 | [MMBT3904](../bjt-mmbt3904/) | NPN | SOT-23 | Pin1=B / Pin2=E / Pin3=C |
| R1 | 限流電阻 | **39 Ω** | **TH 1/2W** | 串 LED，P≈0.38W（⚠️非 0603） |
| R2 | 基極電阻 | **220 Ω** | 0603 | Ib≈10.7mA，保證飽和 |

## 設計計算

- **R1 = 39Ω**：`(5−Vf−Vce(sat))/Ic`，標稱 ~88mA、最壞容差 ~99mA ≤ 100mA 連續上限。功率 I²R≈0.38W → **TH 1/2W**。
- **R2 = 220Ω**：保證飽和需 forced β=10 → Ib=Ic/10=10mA；`(3.3−0.95)/0.01≈220Ω`，Ib≈10.7mA、forced β≈9.4 < hFE_min(30) ✅。
- **MCU 注意**：base 電流 ~10.7mA，RP2040 該 GPIO 需設 12mA drive strength。

## 接腳定義（模組 3 腳）

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 **5V** | input |
| GND | 接地 | input |
| SIG | 訊號輸入 3.3V（active-high，HIGH→發射） | input |

## Driver / Coding

**無 driver 檔**。NEC 38kHz 調制發射方法與遙控碼表屬各專案，不放資料庫
（見記憶 `feedback_protocol_in_project_not_db`）。配對接收端見 [`input/ir-receiver`](../../input/ir-receiver/)。

## Datasheet

- [`datasheet/TSAL6100.pdf`](datasheet/TSAL6100.pdf) — [Vishay](https://www.vishay.com/docs/81009/tsal6100.pdf)
- [`datasheet/TSAL6200.pdf`](datasheet/TSAL6200.pdf) — [Vishay](https://www.vishay.com/docs/81010/tsal6200.pdf)

## 驗證狀態

⏳ pending — 待硬體接好後，用 `input/ir-receiver` 收回自身發射的 NEC 碼確認。
