# PMS5003 — 雷射粒子濃度感應器

**類別**：sensor/particle  
**廠商**：PLANTOWER  
**介面**：UART（9600 bps）  
**工作電壓**：5V（data pin TTL 3.3V）  
**尺寸**：50×38×21 mm

## 量測範圍

| 粒徑 | 說明 |
|------|------|
| PM1.0 | 標準 / 大氣環境（μg/m³）|
| PM2.5 | 標準 / 大氣環境（μg/m³）|
| PM10  | 標準 / 大氣環境（μg/m³）|
| 粒子數 | 0.3 / 0.5 / 1.0 / 2.5 / 5.0 / 10.0 μm per 0.1L |

**有效量測範圍（PM2.5）**：0–500 μg/m³  
**解析度**：1 μg/m³  
**最小粒徑**：0.3 μm  
**單次回應時間**：< 1s

## 接腳

| PIN | 說明 |
|-----|------|
| 1 VCC  | 5V 電源 |
| 2 GND  | 接地 |
| 3 SET  | Sleep 控制，HIGH/懸空 = 正常，LOW = sleep |
| 4 RX   | 串列接收（3.3V TTL）|
| 5 TX   | 串列發送（3.3V TTL）|
| 6 RESET| 模組重置，LOW = reset |
| 7/8 NC | 不接 |

> **注意**：FAN 需要 5V 驅動；data pin 是 3.3V TTL，若 MCU 是 5V 需加電位轉換。

## 接線（Pico）

| PMS5003 | Pico |
|---------|------|
| VCC | 5V（VBUS） |
| GND | GND |
| TX  | GP1（UART0 RX）|
| RX  | GP0（UART0 TX）|
| SET | 懸空（正常模式）|
| RESET | 懸空 |

## 通訊協議（Active Mode，預設）

- Baud：9600，無 parity，1 stop bit
- 自動每 ~2.3s 輸出一筆（低濃度穩定模式）
- Frame：32 bytes

```
Byte 0-1 : 0x42 0x4D (header)
Byte 2-3 : Frame length = 28
Byte 4-5 : PM1.0 std (μg/m³)
Byte 6-7 : PM2.5 std (μg/m³)
Byte 8-9 : PM10  std (μg/m³)
Byte 10-11: PM1.0 atm (μg/m³)
Byte 12-13: PM2.5 atm (μg/m³)
Byte 14-15: PM10  atm (μg/m³)
Byte 16-17: >0.3μm count per 0.1L
Byte 18-19: >0.5μm count per 0.1L
Byte 20-21: >1.0μm count per 0.1L
Byte 22-23: >2.5μm count per 0.1L
Byte 24-25: >5.0μm count per 0.1L
Byte 26-27: >10μm count per 0.1L
Byte 28-29: Reserved
Byte 30-31: Checksum (sum of bytes 0..29)
```

## MicroPython 基本讀取（待補充）

```python
from machine import UART
import struct

uart = UART(0, baudrate=9600, tx=0, rx=1)

def read_pms5003():
    buf = uart.read(32)
    if not buf or len(buf) < 32: return None
    if buf[0] != 0x42 or buf[1] != 0x4D: return None
    chk = sum(buf[0:30])
    if chk != (buf[30] << 8 | buf[31]): return None
    return {
        'pm1':   (buf[4] << 8) | buf[5],
        'pm2_5': (buf[6] << 8) | buf[7],
        'pm10':  (buf[8] << 8) | buf[9],
    }
```

## Passive Mode 指令

| 功能 | CMD | DATA |
|------|-----|------|
| 讀取 | 0xE2 | - |
| 切換 active | 0xE1 | 0x01 |
| 切換 passive | 0xE1 | 0x00 |
| Sleep | 0xE4 | 0x00 |
| Wakeup | 0xE4 | 0x01 |

## 注意事項

- Sleep 喚醒後需等 ≥30s 才能讀到穩定資料（風扇啟動時間）
- 不建議用於廚房、浴室、水霧環境、戶外長期使用
- 金屬外殼接 GND，安裝時注意不要與其他電路短路
