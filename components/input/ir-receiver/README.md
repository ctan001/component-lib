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

搭配 OLED 顯示：`example_oled.py`（需同時複製 `oled_ssd1309.py`，SDA=GP4, SCL=GP5）

## 按鍵碼表（NEC 協議，address=0x00）

| 按鍵 | CMD (hex) | | 按鍵 | CMD (hex) |
|:--|:--|:--|:--|:--|
| 1 | 0x16 | | UP | 0x46 |
| 2 | 0x19 | | DOWN | 0x15 |
| 3 | 0x0D | | LEFT | 0x44 |
| 4 | 0x0C | | RIGHT | 0x43 |
| 5 | 0x18 | | OK | 0x40 |
| 6 | 0x5E | | * | 0x42 |
| 7 | 0x08 | | # | 0x4A |
| 8 | 0x1C |
| 9 | 0x5A |
| 0 | 0x52 |

> 長按發送重複碼，奇偶校驗失敗（cmd ^ ~cmd ≠ 0xFF），driver 忽略或標記為 HOLD。

## Datasheet

待補充

## 驗證狀態

✅ verified — 2026-05-17，micropython-pico，S=GP15 / V=3.3V / G=GND

NEC 協議 address=0x00，17鍵遙控器按鍵碼實測對應。`example_oled.py` 搭配 SSD1309 OLED 顯示確認正常。
