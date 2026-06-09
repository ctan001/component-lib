# xiao-vision-ai — XIAO Vision AI 攝像頭（邊緣 AI 視覺套件）

**類別**：module/camera
**製造商**：Seeed Studio（SKU 104990982）
**介面**：USB-C / WiFi / Bluetooth / I2C / UART / SPI / CSI
**工作電壓**：5V（USB Type-C）
**價格**：USD $26.99（10+ 顆 $24.99）
**狀態**：Early Build（beta 產品，3D 列印外殼，軟體持續演進）

## 描述

XIAO Vision AI Camera 是一個整合式邊緣 AI 視覺套件，三大核心：

1. **Grove Vision AI Module V2** — AI 運算核心，採用 Himax WiseEye2 HX6538（雙核 Arm Cortex-M55 + Ethos-U55 NPU）
2. **XIAO ESP32-C3** — 主控制器，提供 2.4GHz WiFi / Bluetooth 5.0
3. **OV5647 5MP 攝像頭** — 影像輸入

全部封裝於客製 3D 列印外殼內。支援 TensorFlow / PyTorch，相容 Arduino IDE。最大特色是透過
[SenseCraft AI](https://sensecraft.seeed.cc/ai/#/model) 平台**無需寫程式**即可選模型、訓練、一鍵部署，
並在網頁即時可視化推論結果。

## 主要規格

### 攝像頭（OV5647）

| 項目 | 規格 |
|:--|:--|
| Sensor | OmniVision OV5647 |
| 靜態解析度 | 2592 × 1944（5 MP） |
| 視角（FoV） | 62° |
| 影片模式 | 1080p @ 30fps；720p @ 60fps |
| 像素尺寸 | 1.4 µm × 1.4 µm |
| 焦距 | 3.4 mm（可調） |
| 光圈 | F/2.8 |
| CMOS 尺寸 | 1/4″ |

### 主控制器 — XIAO ESP32-C3

| 項目 | 規格 |
|:--|:--|
| 無線 | 2.4GHz WiFi / Bluetooth 5.0 |
| 處理器 | RISC-V 單核 32-bit，四級管線，最高 160 MHz |
| 記憶體 | 400KB SRAM + 4MB Flash |

### AI 運算 — Grove Vision AI V2（Himax WiseEye2 HX6538）

| 項目 | 規格 |
|:--|:--|
| CPU | 雙核 Arm Cortex-M55 @ 400MHz & 150MHz |
| NPU | Arm Ethos-U55 microNPU @ 400MHz |
| SRAM | 可配置最高 2432 KB；64 KB Boot ROM |
| 介面 | CSI 攝像頭連接器、Grove I²C/UART/SPI |
| 儲存 | microSD 卡槽（DS mode，最高 25MHz SDIO） |
| 麥克風 | 內建 PDM 麥克風 |

### 系統

| 項目 | 規格 |
|:--|:--|
| 電源 | 5V via USB Type-C |
| Baud Rate | 115200 bps |
| 工作溫度 | −20°C ～ 70°C |
| 外殼尺寸 | 31 × 49 × 32 mm |
| 外殼材質 | PLA（白色，3D 列印） |
| AI 框架 | TensorFlow / PyTorch |
| 內建模型 | MobileNet V1/V2、EfficientNet-Lite、YOLO v5/v8 |

## 五大特色

1. **強大 AI 運算** — Grove Vision AI V2 的 WiseEye2 HX6538（Cortex-M55 + Ethos-U55 NPU）。
2. **無程式碼 AI 模型部署與可視化** — 透過 SenseCraft AI 選用內建模型或上傳自訂資料集，
   「Quick Training」或「Image Collection Training」訓練完一鍵部署，網頁即時看推論結果。
3. **WiFi 智慧視覺** — 借 XIAO ESP32-C3 的 WiFi 變身智慧 IP 攝像頭，無線串流偵測結果，
   可整合 Home Assistant 等平台做遠端監控。
4. **本地閉環自動化 + Home Assistant** — 部署模型後燒 ESPHome，於 HA 自動化編輯器中以偵測事件
   （跌倒、物件偵測等）觸發其他裝置或通知，完全本地的「視覺→動作」閉環。
5. **完全開源** — 所有程式碼、設計檔、電路圖皆可修改使用；外殼開源於 Thingiverse。
   亦提供 ODM 客製服務（iot[at]seeed.cc）。

## 接腳 / 連接

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| USB Type-C | 5V 電源 + 燒錄/序列（XIAO ESP32-C3） | input |
| Grove I2C | 對外 I2C（與主控/感測器溝通） | I/O |
| Grove UART | 對外 UART（baud 115200） | I/O |
| Grove SPI | 對外 SPI | I/O |
| CSI（內部） | OV5647 攝像頭連接器 | input |
| microSD | Grove Vision AI V2 卡槽（最高 25MHz SDIO） | I/O |
| PDM MIC | Grove Vision AI V2 內建麥克風 | input |

## 應用場景（Application）

- **工業自動化**：品質檢測、預測性維護、語音控制等
- **智慧城市**：設備監控、能源管理等
- **交通運輸**：狀態監控、位置追蹤等
- **智慧農業**：環境監測等
- **行動 IoT 裝置**：穿戴式、手持式裝置等

## 如何使用

1. 用 USB-C 連接，到 [SenseCraft AI](https://sensecraft.seeed.cc/ai/#/model) 連接裝置
2. 選擇內建模型（或上傳自訂資料集訓練）
3. 一鍵部署，網頁即時可視化辨識結果
4. （進階）燒 ESPHome → 整合 Home Assistant 做本地閉環自動化

## 燒錄方式（背面兩個 USB-C）

⚠️ 背面那兩個 Type-C **不是備援，是兩塊不同板子各自的口**，要燒的東西、用的工具都不同，
**不能用同一個口燒兩邊**。

| | **USB ① — Grove Vision AI V2 的口** | **USB ② — XIAO ESP32-C3 的口** |
|:--|:--|:--|
| 屬於哪塊板 | AI 運算板（WiseEye2 HX6538） | 主控板（ESP32-C3） |
| 燒什麼 | **AI 模型**（如 Person Detection） | **Arduino 韌體**（讀結果 + 應用邏輯） |
| 用什麼工具 | **SenseCraft AI 網頁**（Chrome/Edge，WebSerial） | **Arduino IDE**（`Seeed_Arduino_SSCMA`） |
| 驅動 | 需裝 **CH343** USB 序列驅動（VID 1a86） | ESP32-C3 原生 USB，Win11 通常免裝 |
| 進入燒錄 | 接上 → 網頁按 Connect → 選「USB Single Serial」 | 一般直接燒；卡住時按住 **BOOT** 再接 USB |

### 怎麼分辨哪個口

插上電腦看裝置管理員：
- 出現 **CH343 / USB-SERIAL（VID 1a86）** → 是 **Grove Vision AI V2（USB ①）**
- 出現 **ESP32-C3 原生序列裝置（Espressif）** → 是 **XIAO（USB ②）**

### 運作原理（為什麼要分兩個口）

```
影像 → OV5647 →（CSI）→ Grove Vision AI V2 本地推論
                              │ 辨識結果（box / class / score）
                              │ 經 I2C（位址 0x62）
                              ▼
                         XIAO ESP32-C3 → 應用（WiFi / 序列輸出…）
```

模型推論**全在 Grove 板上本地完成**，只把「結果」透過 I2C（0x62）餵給 XIAO。
所以模型燒 Grove 板（①）、應用程式燒 XIAO（②）。

### 建議順序

1. **先燒模型**（USB ①，SenseCraft）→ 在瀏覽器即時預覽，先確認模型抓得到目標。
2. **再燒韌體**（USB ②，Arduino）→ 燒自己的 sketch。
3. 執行時任一 USB-C 供電即可（或兩個都插，一個供電一個看 log）。

### 坑

- SenseCraft 裝置清單只列 **XIAO ESP32-S3 / Grove Vision AI V2 / SenseCAP A1102**，
  **沒有列 ESP32-C3**。但模型是把 Grove 板當「獨立模組」直接燒（清單裡的
  「Grove Vision AI V2 / XIAO Vision AI Camera」就是它），不經過 C3，所以不影響。

## 技術文件（Documents）

| 文件 | 說明 |
|:-----|:-----|
| [XIAO-Vision-AI-Camera_product.pdf](datasheet/XIAO-Vision-AI-Camera_product.pdf) | Seeed 官方產品 PDF（規格、特色、應用） |
| [HX6538_datasheet.pdf](datasheet/HX6538_datasheet.pdf) | Himax WiseEye2 HX6538 AI 處理器 Datasheet |

**外部來源**：
- [產品頁面](https://www.seeedstudio.com/XIAO-Vision-AI-Camera-p-6450.html) — Seeed Studio 官方
- [SenseCraft AI 平台](https://sensecraft.seeed.cc/ai/#/model) — 無程式碼模型訓練/部署
- [Grove Vision AI V2 Wiki](https://wiki.seeedstudio.com/grove_vision_ai_v2/) — AI 模組詳細教學
- [Himax 官方範例（GitHub）](https://github.com/HimaxWiseEyePlus/Seeed_Grove_Vision_AI_Module_V2) — Seeed Grove Vision AI V2 範例
- [WiseEye2 HX6538 產品頁](https://www.himax.com.tw/products/intelligent-sensing/always-on-smart-sensing/wiseeye2-ai-processor/)
- [3D 外殼（Thingiverse）](https://www.thingiverse.com/thing:6989378) — 可摺疊支架/外殼開源檔
- [ESPHome Ready-Made Projects](https://esphome.io/projects/) — 瀏覽器燒錄、Home Assistant 整合

## 認證

| 項目 | 值 |
|:--|:--|
| HSCODE | 9031809090 |
| US HSCODE | 9031808085 |
| EU HSCODE | 9013101000 |
| COO | CHINA |

## 驗證狀態

⏳ pending（尚未實機測試）
