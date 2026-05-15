# rgb-3color — 3色LED模块

**類別**：display/led
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-high

## 描述

三色 LED 模組（紅/黃/綠），各腳高電平亮起對應顏色（active-high）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| R | 紅色 LED 控制（HIGH=亮） | input |
| Y | 黃色 LED 控制（HIGH=亮） | input |
| G | 綠色 LED 控制（HIGH=亮） | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/rgb_3color.py
```

請將 `rgb_3color.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
