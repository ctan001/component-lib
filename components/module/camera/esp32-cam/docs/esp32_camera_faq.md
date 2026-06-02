# ESP32 Camera FAQ & Troubleshooting

**Source**: [Espressif Camera Application FAQ](https://docs.espressif.com/projects/esp-faq/en/latest/application-solution/camera-application.html)

---

## PCLK Frequency Limits

| SoC | Max PCLK |
|:----|:---------|
| ESP32 | 8 MHz |
| ESP32-S2 | 32 MHz |
| ESP32-S3 | 40 MHz |

---

## PSRAM Requirements

- JPEG above CIF (400x296): **requires PSRAM**
- RGB/YUV above QVGA (320x240): **requires PSRAM**
- ESP32-CAM 標配 4MB PSRAM，所以 UXGA JPEG 沒問題

---

## Frame Rate vs Format

JPEG 比 YUV/RGB 快很多，因為資料量小：
- UXGA JPEG ~100KB vs UXGA RGB565 ~3.7MB
- WiFi 串流建議一律用 JPEG

---

## Common Issues

### Camera Not Detected
1. 檢查 XCLK, SIOC (SCL), SIOD (SDA) 接線
2. 確認 xclk_freq_hz 設定正確（通常 20MHz）
3. 檢查電源穩定性（ESP32-CAM 需 5V 穩定供電）
4. 多個 I2C 裝置可能衝突 → 固定 camera ID bypass polling

### Image Distortion / FB-OVF
- 降低 PCLK 頻率
- 減小 frame size
- fb_count=2 可以用連續模式避免丟幀
- WiFi + YUV/RGB 容易 data corruption → 改用 JPEG

### Startup Delay
- ESP32-S2: 移除 esp_camera_init 中多餘的 delay
- 或將 SCCB clock 調到 400,000 Hz

---

## Performance Tips

1. **WiFi 串流**: 用 JPEG + SVGA(800x600) 平衡畫質和速度
2. **拍照存檔**: 用 JPEG + UXGA(1600x1200) 取最高畫質
3. **fb_count**: 串流用 2（連續），拍照用 1（省記憶體）
4. **grab_mode**: CAMERA_GRAB_LATEST 取最新幀（減少延遲）
5. **TCP bandwidth**: ESP32 WiFi 理論 20 MB/s

---

## Video Encoding

- ESP32 **無** 硬體 H.264/H.265 encoder
- 只能輸出 MJPEG（逐幀 JPEG）
- 如需 H.264 → 傳到外部設備用 FFmpeg / x264 編碼

---

## Multiple Cameras

| SoC | Support |
|:----|:--------|
| ESP32 | 1 camera only |
| ESP32-S3 | 2 SPI cameras |
| ESP32-P4 | Multiple (DVP + MIPI-CSI) |
