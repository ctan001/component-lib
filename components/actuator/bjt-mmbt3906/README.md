# bjt-mmbt3906 — PNP 通用晶體 MMBT3906

**類別**：actuator（離散半導體）
**製造商**：onsemi
**封裝**：SOT-23（SMD，= 2N3906 貼片版）
**互補對**：MMBT3904（NPN）

## 描述

PNP 通用放大/開關晶體。常用於高端開關（high-side switch，射極接電源、base 拉低導通）或小訊號放大。是 MMBT3904 的互補件。

## 最大額定（onsemi datasheet）

| 參數 | 符號 | 值 |
|:--|:--|:--|
| 集-射極電壓 | VCEO | −40 V |
| 集-基極電壓 | VCBO | −40 V |
| 射-基極電壓 | VEBO | −5.0 V |
| 集極電流（連續） | IC | −200 mA |
| 集極電流（峰值） | ICM | −800 mA |
| 功耗 @25°C (FR-5) | PD | 225 mW |
| 接面溫度 | TJ | −55 ~ +150 °C |

## 關鍵特性

| 參數 | 條件 | 值 |
|:--|:--|:--|
| 直流增益 hFE | IC=10mA | 100 ~ 300 |
| 直流增益 hFE | IC=100mA | **≥ 30**（min） |
| 飽和壓降 VCE(sat) | IC=50mA, IB=5mA（forced β=10） | 0.4 V max |
| 基-射飽和 VBE(sat) | IC=50mA, IB=5mA | 0.95 V max |

> ⚠️ PNP 電壓/電流方向為負。要保證飽和同樣需 `|IB| ≥ |IC|/10`。

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

> 腳位與 MMBT3904 (NPN) 完全相同；差別在 PNP 的電流方向與導通邏輯（base 拉低導通）。

## Datasheet

[`datasheet/MMBT3906LT1.pdf`](datasheet/MMBT3906LT1.pdf) — onsemi 官方，[線上連結](https://www.onsemi.com/download/data-sheet/pdf/mmbt3906lt1-d.pdf)

## 驗證狀態

⏳ pending（被動離散元件，無 driver）
