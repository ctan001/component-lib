# cc1101-e07-m1101d-sma — CC1101 433MHz RF收發模組

**類別**：module/rf  
**介面**：SPI（4-wire）  
**工作電壓**：1.8V – 3.6V（建議 3.3V）  
**邏輯電平**：3.3V  

## 描述

Chengdu Ebyte E07-M1101D-SMA：基於 TI CC1101 的 433MHz ISM 頻段 RF 收發模組。
DIP 封裝，SMA-K 天線接頭，工業級設計（-40~85°C），
支援多種調製模式，空曠地帶通訊距離可達 1km。

## 主要規格

| 項目 | 規格 |
|:--|:--|
| 頻率 | 433 MHz（可調 387–464 MHz） |
| 最大發射功率 | 10 dBm（10 mW） |
| 接收靈敏度 | -110 dBm（@ 1.2kbps） |
| 空中速率 | 0.6k – 500kbps |
| 調製模式 | OOK、ASK、GFSK、2-FSK、4-FSK、MSK |
| FIFO | 64 Byte TX + 64 Byte RX |
| 通訊距離 | 最遠 1km（空曠地，5dBi 天線） |
| 工作電壓 | 1.8V – 3.6V |
| TX 電流 | 100 mA（瞬時） |
| RX 電流 | 20 mA |
| 睡眠電流 | 2 µA |
| 尺寸 | 15 × 30 mm |

## 接腳定義

| Pin | 名稱 | 方向 | 說明 |
|:--|:--|:--|:--|
| 1 | GND | — | 接地 |
| 2 | VCC | input | 電源 1.8V–3.6V |
| 3 | GDO0 | output | 通用數位輸出（封包同步/carrier detect） |
| 4 | CSN | input | SPI 片選（低電平有效） |
| 5 | SCK | input | SPI 時鐘 |
| 6 | MOSI | input | SPI 主機輸出 |
| 7 | MISO/GDO1 | output | SPI 主機輸入 |
| 8 | GDO2 | output | 通用數位輸出（通常設為 IRQ） |
| 9 | GND | — | 接地 |
| 10 | GND | — | 接地 |

## 連接 MCU（基本電路）

```
MCU              E07-M1101D
SPI_NSS  ───────  CSN  (Pin 4)
SPI_SCK  ───────  SCK  (Pin 5)
SPI_MOSI ───────  MOSI (Pin 6)
SPI_MISO ───────  MISO (Pin 7)
GPIO_IRQ ───────  GDO2 (Pin 8)   ← 外部中斷
3.3V     ───────  VCC  (Pin 2)
GND      ───────  GND  (Pin 1/9/10)
```

## 重要注意事項

> ⚠️ **最高耐壓 3.6V，超過將永久損毀！不可直接接 5V！**

- 5V TTL 邏輯需串接 1k-5.1k 電阻降壓（仍有風險，建議用電平轉換器）
- GDO2 建議設為 IRQ，使用 MCU 外部中斷處理，不要用 SPI 輪詢
- 從 IDLE/Sleep 模式恢復後，建議重新初始化功率配置表
- 空中速率越高，通訊距離越短（500kbps 下距離遠不及 1.2kbps）
- 天線必須外露，垂直向上；不得安裝於金屬殼內
- 供電需穩定，電壓波動大會導致誤碼率升高

## 程式設計要點

- 讀寫暫存器透過 SPI；時序參考原廠 CC1101 datasheet
- GDO0 為通用 I/O 腳，用途由暫存器設定
- GDO2 通常設為封包接收中斷（IRQ）
- 支援 RSSI（信號強度）和 LQI（鏈路品質）讀取

## Datasheet

[CC1101-E07-M1101D-SMA_Usermanual.pdf](datasheet/CC1101-E07-M1101D-SMA_Usermanual.pdf) — Chengdu Ebyte v1.30

## 驗證狀態

⏳ pending
