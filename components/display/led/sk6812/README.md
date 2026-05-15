# sk6812 — SK6812 RGB模块

**類別**：display/led
**介面**：PIO
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

SK6812 可定址 RGB LED，單線歸零碼協議（24-bit GRB），多顆串聯，PIO 實作

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| DIN | 串行數據輸入（單線） | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/sk6812.py
```

請將 `sk6812.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
