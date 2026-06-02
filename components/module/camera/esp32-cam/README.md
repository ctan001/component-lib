# esp32-cam — ESP32-CAM WiFi攝像頭模組

**類別**：module/camera  
**介面**：UART（燒錄）/ WiFi / Bluetooth / SDMMC / GPIO  
**工作電壓**：3.3V 或 5V  
**邏輯電平**：3.3V  

## 描述

AI-Thinker ESP32-CAM：ESP32-S 核心 + OV2640 2MP 攝像頭 + WiFi + Bluetooth，
內建閃光燈（GPIO 4），microSD 插槽（最高 4GB），4MB PSRAM。
支援影像串流、拍照存 SD 卡、人臉辨識、深度睡眠。

## 主要規格

| 項目 | 規格 |
|:--|:--|
| WiFi | 802.11 b/g/n |
| Bluetooth | BT 4.2 + BLE |
| Camera | OV2640 2MP |
| RAM | 512KB SRAM + 4MB PSRAM |
| Storage | microSD 最高 4GB |
| Flash LED | GPIO 4 |
| 尺寸 | 40.5 × 27 × 4.5 mm |
| 工作電流（閃光關） | 180 mA @ 5V |
| 工作電流（閃光最亮） | 310 mA @ 5V |
| 深度睡眠電流 | 低至 6 mA @ 5V |

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
| 5V | 電源輸入（或 3.3V） | input |
| GND | 接地 | input |
| 3.3V | 3.3V 輸出（P_OUT） | output |
| GPIO 0 | CSI_MCLK / **燒錄：接 GND** | I/O |
| GPIO 1 | U0TXD（UART TX） | output |
| GPIO 3 | U0RXD（UART RX） | input |
| GPIO 4 | Flash LED（高電平亮） | output |
| GPIO 16 | U2RXD | input |

## 攝像頭 GPIO 對應（Arduino define）

```c
#define PWDN_GPIO_NUM   32
#define RESET_GPIO_NUM  -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM   26   // Camera I2C SDA
#define SIOC_GPIO_NUM   27   // Camera I2C SCL
#define Y9_GPIO_NUM     35
#define Y8_GPIO_NUM     34
#define Y7_GPIO_NUM     39
#define Y6_GPIO_NUM     36
#define Y5_GPIO_NUM     21
#define Y4_GPIO_NUM     19
#define Y3_GPIO_NUM     18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM  25
#define HREF_GPIO_NUM   23
#define PCLK_GPIO_NUM   22
```

## 燒錄方式（FTDI）

1. FTDI 設為 **3.3V**
2. 接線：`3.3V↔VCC`、`GND↔GND`、`TX↔GPIO3`、`RX↔GPIO1`
3. **GPIO 0 接 GND** → 進入 Flash 模式
4. Arduino IDE：Tools > Board > **AI-Thinker ESP32-CAM**
5. 燒錄完成後移除 GPIO0-GND 跳線，按 RESET

## Arduino Driver

```cpp
// drivers/arduino/esp32cam_snapshot.ino
// 功能：拍照儲存到 microSD 卡，完成後進入深度睡眠
#include "esp_camera.h"
#include "SD_MMC.h"
#include <EEPROM.h>

// （詳見 drivers/arduino/esp32cam_snapshot.ino）
```

## 重要注意事項

- 有 PSRAM 時最高支援 `FRAMESIZE_UXGA`（1600×1200）
- 無 PSRAM 最高 `FRAMESIZE_SVGA`（800×600）
- Flash LED 使用 `rtc_gpio_hold_en(GPIO_NUM_4)` 可在深度睡眠中保持狀態
- 供電需充足（最大 310mA），電源不穩容易導致當機

## 技術文件

| 文件 | 說明 |
|:-----|:-----|
| [ESP32-CAM.pdf](datasheet/ESP32-CAM.pdf) | HandsOn Technology 模組 Datasheet（pin map、電路圖、燒錄方式） |
| [esp_camera API Reference](docs/esp_camera_api_reference.md) | Espressif esp32-camera v2.1.6 完整 API（struct/enum/function） |
| [OV2640 Register Map](docs/ov2640_register_map.md) | OV2640 雙 bank register 完整定義（DSP + Sensor） |
| [ESP32 Camera FAQ](docs/esp32_camera_faq.md) | 常見問題、效能調校、troubleshooting |

**外部來源**:
- [espressif/esp32-camera GitHub](https://github.com/espressif/esp32-camera) — 官方 driver 原始碼
- [Arduino CameraWebServer 範例](https://github.com/espressif/arduino-esp32/tree/master/libraries/ESP32/examples/Camera/CameraWebServer) — WiFi 影像串流範例
- [ESP Component Registry](https://components.espressif.com/components/espressif/esp32-camera) — 最新版本 v2.1.6

## 驗證狀態

⏳ pending
