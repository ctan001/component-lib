# tm1650 — TM1650四位数码管模块

**類別**：display/7seg
**介面**：I2C
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

TM1650 四位七段數碼管，I2C-like 協議，顯示地址 0x34-0x37，控制地址 0x24-0x27

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| SDA | 數據線（I2C-like） | bidirectional |
| SCL | 時鐘線 | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/tm1650.py
```

請將 `tm1650.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
