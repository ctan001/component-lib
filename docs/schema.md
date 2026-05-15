# component.json Schema 定義

每個元件目錄下的 `component.json` 遵循以下結構：

```json
{
  "name": "元件英文名（資料夾名稱）",
  "name_zh": "元件中文名",
  "manufacturer": "製造商（不明填 unknown）",
  "part_number": "型號",
  "category": "sensor/digital",
  "description": "一句話功能描述",
  "interface": ["GPIO"],
  "voltage": {"min": 3.3, "max": 5.0, "unit": "V"},
  "pins": [
    {"name": "VCC", "function": "電源", "direction": "input"},
    {"name": "GND", "function": "接地",  "direction": "input"},
    {"name": "S",   "function": "信號端", "direction": "output"}
  ],
  "logic": "active-low",
  "datasheet": {
    "filename": null,
    "source": null,
    "url": null,
    "downloaded": false
  },
  "drivers": {
    "micropython": "drivers/micropython/<name>.py",
    "circuitpython": null,
    "arduino": null
  },
  "verification": {
    "status": "pending",
    "platform": null,
    "date": null,
    "notes": ""
  },
  "added": "YYYY-MM-DD",
  "updated": "YYYY-MM-DD"
}
```

## 欄位說明

| 欄位 | 說明 |
|:--|:--|
| `logic` | `active-high` / `active-low` / `analog` / `pwm` / `protocol` |
| `verification.status` | `pending` / `verified` / `failed` |
| `verification.platform` | 驗證平台，e.g. `micropython-pico` |
| `datasheet.source` | `mouser` / `digikey` / `manufacturer` / `other` |
