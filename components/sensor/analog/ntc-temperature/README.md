# ntc-temperature — 模拟温度传感器

**類別**：sensor/analog
**介面**：ADC
**工作電壓**：3.3–5.0 V
**邏輯**：analog

## 描述

NTC-MF52AT 熱敏電阻（10kΩ@25°C，B=3950），串聯 10kΩ 分壓，Steinhart-Hart 轉換溫度

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/ntc_temperature.py
```

請將 `ntc_temperature.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
