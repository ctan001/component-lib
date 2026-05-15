# rgb-plugin — 插件RGB

**類別**：display/led
**介面**：GPIO
**工作電壓**：3.3–5.0 V
**邏輯**：active-high

## 描述

直插式 RGB LED（共陰），R/G/B 三腳分別限流電阻控制，高電平亮起

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| R | 紅色陽極（含限流電阻） | input |
| G | 綠色陽極（含限流電阻） | input |
| B | 藍色陽極（含限流電阻） | input |
| GND | 共陰接地 | input |

## MicroPython Driver

```python
# driver 路徑：drivers/micropython/rgb_plugin.py
```

請將 `rgb_plugin.py` 複製到 Pico，再執行 `example.py`。

## Datasheet

待補充

## 驗證狀態

⏳ pending
