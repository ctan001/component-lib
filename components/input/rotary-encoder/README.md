# rotary-encoder — 旋转编码器

**類別**：input
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

增量式旋轉編碼器，20 脈衝/轉，CLK 下降沿時 DT=HIGH→順時針，DT=LOW→逆時針

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| CLK | 時鐘信號 | output |
| DT | 方向信號 | output |
| SW | 按鈕（active-low） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/rotary_encoder.py
```

請將 `rotary_encoder.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
