# mosfet-switch-f5305s — F5305S 隔離型 MOSFET 開關模組（HW-548）

**類別**：actuator
**介面**：GPIO / PWM
**輸入電壓**：3.0–20.0 V（trigger側）／輸出：5–36V（負載側）
**邏輯**：pwm

## 描述

PC817 光耦合器隔離的 F5305S 功率 MOSFET 開關模組，input/output 完全隔離。數位高低電位或
PWM 訊號觸發 optocoupler LED，驅動 MOSFET 導通/截止，可控制高功率 DC 負載（heater/馬達/LED等）。

板上 silkscreen 印 **HW-548**（常見公板 clone，多個賣場都有賣，非單一品牌獨有）。

## 接腳定義

板子本身**沒有印任何 +/- 或 IN/OUT 文字標示**（[photos/hw548_board.jpg](photos/hw548_board.jpg) 可對照，
另外交叉比對 makerselectronics.com、otronic.nl 兩個獨立賣場的產品照片，都同樣沒有標示）。

| 端子座 | 功能 | 方向 |
|:--|:--|:--|
| 左側 2-pin | Trigger輸入：3-20V數位電位或PWM，約5mA，接PC817 LED端 | input |
| 右側 4-pin(2x2) | 負載輸出：5-36V，連續電流<5A(超過需散熱片，上限20A) | output |

**⚠️ Trigger輸入極性未知**：兩顆screw孔沒有標示哪個是LED陽極/陰極。這是安全的不確定性——
接反的後果只是LED不亮、MOSFET不導通，不會燒毀任何東西。實接時如果沒反應，對調兩條線即可。

## 規格來源

makerselectronics.com/product/f5305s-mosfet-module-hw-548/ 與 otronic.nl/en/mosfet-3v-24v-electronic-switch-f5305s.html
兩個獨立賣場的規格表數字一致：Input Voltage 3-20V／Input Current ~5mA／Output Voltage 5-36V／
Continuous Output Current ≤5A／Peak ≤20A(需散熱片)。

## MicroPython 使用（GPIO trigger測試片段）

```python
from machine import Pin
import time

heater1 = Pin(6, Pin.OUT, value=0)  # 對應本專案的Heater1
heater2 = Pin(7, Pin.OUT, value=0)  # 對應本專案的Heater2

heater1.value(1)
heater2.value(1)
time.sleep(5)
heater1.value(0)
heater2.value(0)
```

正式PWM調功率的driver尚未寫，目前只有GPIO on/off的trigger訊號驗證。

## 使用於

[[project_312_heat_module]] — 每支40W/24V cartridge heater各配一顆本模組獨立驅動，
GP6→Heater1、GP7→Heater2。

## 外殼設計

`100_Projects/active/長期維護_ETC/3D設計/樂高盒/HW548_FET模組盒/project.md`
——AI 3D Printing Pipeline 的第一個真實驗證案例，待 Jerry 量測尺寸後開始設計。

## 驗證狀態

⏳ pending — 2026-08-13：GPIO trigger訊號smoke test通過（24V負載電源未開，僅驗證訊號送達），
PWM調功率與24V實際負載驅動尚未測試。
