# bjt-mmbt3904 — NPN 通用晶體 MMBT3904

**類別**：actuator（離散半導體）
**製造商**：onsemi
**封裝**：SOT-23（SMD，= 2N3904 貼片版）
**互補對**：MMBT3906（PNP）

## 描述

NPN 通用放大/開關晶體。常用於 MCU GPIO 驅動 LED / 繼電器 / 小負載的低端開關，或小訊號放大。

## 最大額定（onsemi datasheet）

| 參數 | 符號 | 值 |
|:--|:--|:--|
| 集-射極電壓 | VCEO | 40 V |
| 集-基極電壓 | VCBO | 60 V |
| 射-基極電壓 | VEBO | 6.0 V |
| 集極電流（連續） | IC | 200 mA |
| 集極電流（峰值） | ICM | 900 mA |
| 功耗 @25°C (FR-5) | PD | 225 mW |
| 接面溫度 | TJ | −55 ~ +150 °C |

## 關鍵特性

| 參數 | 條件 | 值 |
|:--|:--|:--|
| 直流增益 hFE | IC=10mA | 100 ~ 300 |
| 直流增益 hFE | IC=100mA | **≥ 30**（min） |
| 飽和壓降 VCE(sat) | IC=50mA, IB=5mA（forced β=10） | 0.3 V max |
| 基-射飽和 VBE(sat) | IC=50mA, IB=5mA | 0.95 V max |

> ⚠️ **設計開關時**：datasheet 的 VCE(sat) 是在 **forced β=10** 條件量測。要保證飽和，base 電流應給到 `IB ≥ IC/10`，**不要**用線性區的 hFE_min(30) 反推。

## SOT-23 腳位（頂視，onsemi 官方）

```
        3 (C)
        │
     ┌──┴──┐
     │     │
     └─┬─┬─┘
       1 2
   (B)   (E)
```

| Pin | 腳位 | 說明 |
|:--|:--|:--|
| 1 | **B** | Base（底面左下） |
| 2 | **E** | Emitter（底面右下） |
| 3 | **C** | Collector（單腳側） |

> 單腳那一側 = Pin 3 = Collector。MMBT3906 (PNP) 腳位相同。

## 應用範例

IR LED 5V 低端驅動見 [`actuator/ir-emitter-tsal`](../ir-emitter-tsal/)（circuit.svg）。

## Datasheet

[`datasheet/MMBT3904LT1.pdf`](datasheet/MMBT3904LT1.pdf) — onsemi 官方，[線上連結](https://www.onsemi.com/download/data-sheet/pdf/mmbt3904lt1-d.pdf)

## 驗證狀態

⏳ pending（被動離散元件，無 driver）
