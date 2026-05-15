# ir-receiver — 红外遥控接收器

**類別**：input
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：protocol

## 描述

38kHz NEC 協議 IR 接收，S 端接 4.7K 上拉，接收到信號時由 HIGH 轉 LOW

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| VCC | 電源 3.3V/5V | input |
| GND | 接地 | input |
| S | 信號端 | output |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/ir_receiver.py
```

請將 `ir_receiver.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
