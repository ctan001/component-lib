# I2C 2004 LCD 字元顯示模組

20×4 字元 LCD，HD44780 相容控制器（S6A0069），配 PCF8574A I2C 背包轉接板。

## 規格

| 項目 | 值 |
|:--|:--|
| 顯示格式 | 20 列 × 4 行，5×8 點字元 |
| LCD 面板 | GDM2004D-FL-YBW（廈門歐卡） |
| LCD 控制器 | S6A0069（HD44780 相容） |
| I2C 轉接晶片 | PCF8574AT（預設）或 PCF8574T |
| I2C 地址 | **0x3F**（PCF8574AT，A0-A2 全開）/ 0x27（PCF8574T） |
| 電源 | 5V |
| 背光 | 黃綠色 LED，可軟體控制 |
| 對比調節 | 板上可變電阻 |
| 尺寸 | 98×60 mm |

## 接線（YD-RP2040 / Pico）

| LCD 模組 | MCU |
|:--|:--|
| GND | GND |
| VCC | 5V |
| SDA | GP4（或任意 SDA） |
| SCL | GP5（或任意 SCL） |

> **注意**：必須接 5V，3.3V 供電可能導致顯示不穩或背光暗淡。

## I2C 地址選擇

背板上有 A0、A1、A2 三個焊點：
- 焊點**開路**（預設）→ 對應 bit = 1
- 焊點**短接**→ 對應 bit = 0

| A2 | A1 | A0 | 地址（PCF8574AT） |
|:--:|:--:|:--:|:--:|
| 開 | 開 | 開 | **0x3F**（出廠預設） |
| 開 | 開 | 短 | 0x3E |
| 短 | 短 | 短 | 0x38 |

## MicroPython 使用

```python
from machine import I2C, Pin
from lcd_2004_i2c import LCD2004I2C

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
lcd = LCD2004I2C(i2c, addr=0x3F)

lcd.set_cursor(0, 0)
lcd.print("Hello!")
```

## DDRAM 位址對照

| 行 | 起始位址 |
|:--:|:--:|
| 0 | 0x00 |
| 1 | 0x40 |
| 2 | 0x14 |
| 3 | 0x54 |

## 踩坑提醒

- 若 I2C scan 找不到，先確認 A0-A2 焊點設定，用 0x27 也試試
- 字元顯示但亂碼 → 調板上對比電阻
- 背光不亮 → 確認 BL 跳線未被拔除
