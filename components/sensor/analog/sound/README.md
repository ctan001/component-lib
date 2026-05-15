# sound — 声音传感器

**類別**：sensor/analog
**介面**：ADC
**工作電壓**：3.3–5.0 V
**邏輯**：analog

## 描述

高感度麥克風 + LM386 放大（最大 200 倍），電位器調放大倍數，類比輸出聲音強度

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/sound.py
```

請將 `sound.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
