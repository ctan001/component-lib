# adc-button-5way — 五路AD按键

**類別**：input
**介面**：ADC
**工作電壓**：3.3–5.0 V
**邏輯**：analog

## 描述

五個按鍵共用一個 ADC 腳，電阻分壓產生不同電壓，16-bit ADC 區分各鍵

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/adc_button_5way.py
```

請將 `adc_button_5way.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
