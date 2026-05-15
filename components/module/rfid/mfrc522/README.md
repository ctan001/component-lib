# mfrc522 — RFID刷卡模块

**類別**：module/rfid
**介面**：SPI
**工作電壓**：3.3–3.3 V
**邏輯**：protocol

## 描述

MFRC522 RFID 讀卡器，SPI 介面，13.56MHz，支援 MIFARE 1K/4K，讀寫 UID 及資料

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SCK | SPI 時鐘 | input |
| MOSI | SPI 主機到從機 | input |
| MISO | SPI 從機到主機 | output |
| SDA | SPI 片選（CS） | input |
| RST | 硬體重置（LOW=重置） | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/mfrc522.py
```

請將 `mfrc522.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

[MFRC522.pdf](https://www.mouser.com/datasheet/2/302/MF1S50YYX_V1-1278395.pdf)

## 驗證狀態

⏳ pending
