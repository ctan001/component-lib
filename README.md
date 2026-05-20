# component-lib

感應器與周邊元件知識庫，適用於 YD-RP2040（MicroPython）。

每個元件獨立一個資料夾，內含：
- `README.md`：接腳定義、規格摘要、使用說明
- `component.json`：機器可讀的結構化規格（含驗證狀態旗標）
- `datasheet/`：本地 PDF 備份
- `drivers/micropython/`：MicroPython driver + 可直接跑的 example.py
- `drivers/circuitpython/`、`drivers/arduino/`：預留（日後補充）

## 元件清單

完整清單見 [index.md](index.md)。

## 使用方式

1. 找到需要的元件資料夾（參考 index.md）
2. 讀 `README.md` 確認接腳與邏輯
3. 把 `drivers/micropython/<name>.py` 複製進你的專案
4. 跑 `example.py` 確認硬體正常
5. 驗證通過後說「XXX 驗證完成」更新驗證旗標
6. 執行 `python sync_index.py` 同步 index.md

## 新增元件 SOP

說「新增元件 XXX」→ AI 搜尋 Mouser/DigiKey datasheet → 建立目錄 + 寫 driver → 執行 `python sync_index.py`

## index.md 維護

index.md **不要手動編輯**，永遠由 `sync_index.py` 生成：

```
# 重新生成
python sync_index.py

# 只檢查差異，不寫入
python sync_index.py --check
```

每次更新 component.json（驗證完成、新增元件）後執行一次即可。

## 硬體

- 板子：YD-RP2040 V1.1（源地工作室）
- MCU：RP2040，Dual Cortex-M0+ @ 133 MHz
- Flash：16 MB QSPI

## 參考資料

- [docs/schema.md](docs/schema.md)：component.json 欄位定義
- [docs/categories.md](docs/categories.md)：分類說明
- [pico-drivers](../pico-drivers/)：底層介面 driver（GPIO/I2C/SPI/UART/ADC…）
