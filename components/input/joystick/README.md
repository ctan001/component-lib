# joystick — 遥感模块

**類別**：input
**介面**：ADC, GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：analog

## 描述

搖桿模組，X/Y 軸各一個 ADC 電位器，Z 軸按鈕（按下=HIGH，與一般按鍵相反）

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| X | X 軸類比輸出 | output |
| Y | Y 軸類比輸出 | output |
| B | Z 軸按鈕（按下=HIGH, active-high） | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/joystick.py
```

請將 `joystick.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
