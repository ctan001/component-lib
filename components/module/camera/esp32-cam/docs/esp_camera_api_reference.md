# esp_camera API Reference

**Source**: [espressif/esp32-camera](https://github.com/espressif/esp32-camera) v2.1.6  
**License**: Apache-2.0  
**Supported SoC**: ESP32, ESP32-S2, ESP32-S3

---

## Supported Sensors (15)

OV2640, OV3660, OV5640, OV7670, OV7725, GC032A, GC0308, GC2145,
BF3005, BF20A6, SC101IOT, SC030IOT, SC031GS, NT99141, HM0360, HM1055

---

## Enums

### pixformat_t

| Value | Description |
|:------|:------------|
| PIXFORMAT_RGB565 | 16-bit RGB |
| PIXFORMAT_YUV422 | YCbCr 4:2:2 |
| PIXFORMAT_YUV420 | YCbCr 4:2:0 |
| PIXFORMAT_GRAYSCALE | 8-bit gray |
| PIXFORMAT_JPEG | JPEG compressed |
| PIXFORMAT_RGB888 | 24-bit RGB |
| PIXFORMAT_RAW | RAW Bayer |
| PIXFORMAT_RGB444 | 12-bit RGB |
| PIXFORMAT_RGB555 | 15-bit RGB |

### framesize_t

| Value | Resolution | Notes |
|:------|:-----------|:------|
| FRAMESIZE_96X96 | 96x96 | |
| FRAMESIZE_QQVGA | 160x120 | |
| FRAMESIZE_QCIF | 176x144 | |
| FRAMESIZE_HQVGA | 240x176 | |
| FRAMESIZE_240X240 | 240x240 | |
| FRAMESIZE_QVGA | 320x240 | |
| FRAMESIZE_CIF | 400x296 | |
| FRAMESIZE_HVGA | 480x320 | |
| FRAMESIZE_VGA | 640x480 | |
| FRAMESIZE_SVGA | 800x600 | |
| FRAMESIZE_XGA | 1024x768 | |
| FRAMESIZE_HD | 1280x720 | |
| FRAMESIZE_SXGA | 1280x1024 | |
| FRAMESIZE_UXGA | 1600x1200 | OV2640 max |
| FRAMESIZE_FHD | 1920x1080 | |
| FRAMESIZE_QXGA | 2048x1536 | |
| FRAMESIZE_QHD | 2560x1440 | |
| FRAMESIZE_WQXGA | 2560x1600 | |
| FRAMESIZE_QSXGA | 2592x1944 | 5MP sensors |

### camera_grab_mode_t

| Value | Description |
|:------|:------------|
| CAMERA_GRAB_WHEN_EMPTY | Fills buffers when available (may be stale) |
| CAMERA_GRAB_LATEST | Keeps most recent frame in queue |

### camera_fb_location_t

| Value | Description |
|:------|:------------|
| CAMERA_FB_IN_PSRAM | Frame buffer in external PSRAM |
| CAMERA_FB_IN_DRAM | Frame buffer in internal DRAM |

### gainceiling_t

2X, 4X, 8X, 16X, 32X, 64X, 128X

---

## Structs

### camera_config_t

```c
typedef struct {
    // Pin assignments
    int pin_pwdn;       // Power down pin (-1 = unused)
    int pin_reset;      // Reset pin (-1 = unused)
    int pin_xclk;       // External clock pin
    int pin_sccb_sda;   // I2C SDA (camera control)
    int pin_sccb_scl;   // I2C SCL (camera control)
    int pin_d7;         // Data bit 7 (MSB)
    int pin_d6;
    int pin_d5;
    int pin_d4;
    int pin_d3;
    int pin_d2;
    int pin_d1;
    int pin_d0;         // Data bit 0 (LSB)
    int pin_vsync;      // Vertical sync
    int pin_href;       // Horizontal reference
    int pin_pclk;       // Pixel clock

    // Clock
    int xclk_freq_hz;          // Typically 20000000 (20 MHz)
    ledc_timer_t ledc_timer;
    ledc_channel_t ledc_channel;

    // Image format
    pixformat_t pixel_format;
    framesize_t frame_size;
    int jpeg_quality;          // 0-63 (lower = better quality)

    // Buffer
    size_t fb_count;           // 1 = single, 2+ = continuous
    camera_fb_location_t fb_location;
    camera_grab_mode_t grab_mode;
    int sccb_i2c_port;         // I2C port (-1 = auto)
} camera_config_t;
```

### camera_fb_t

```c
typedef struct {
    uint8_t *buf;              // Pointer to image data
    size_t len;                // Length of image data
    size_t width;              // Width in pixels
    size_t height;             // Height in pixels
    pixformat_t format;        // Image format
    struct timeval timestamp;  // Capture timestamp
} camera_fb_t;
```

---

## Functions

| Function | Description |
|:---------|:------------|
| `esp_err_t esp_camera_init(const camera_config_t* config)` | Initialize camera |
| `esp_err_t esp_camera_deinit(void)` | Deinitialize camera |
| `camera_fb_t* esp_camera_fb_get(void)` | Get frame buffer (blocks until available) |
| `void esp_camera_fb_return(camera_fb_t* fb)` | Return frame buffer to driver |
| `sensor_t* esp_camera_sensor_get(void)` | Get sensor control handle |
| `esp_err_t esp_camera_save_to_nvs(const char* key)` | Save config to NVS |
| `esp_err_t esp_camera_load_from_nvs(const char* key)` | Load config from NVS |
| `void esp_camera_return_all(void)` | Return all frame buffers |
| `bool esp_camera_available_frames(void)` | Check if frames available |
| `esp_err_t esp_camera_reconfigure(const camera_config_t* config)` | Reconfigure camera |

---

## Error Codes

| Code | Meaning |
|:-----|:--------|
| ESP_ERR_CAMERA_NOT_DETECTED | No sensor found on I2C |
| ESP_ERR_CAMERA_FAILED_TO_SET_FRAME_SIZE | Resolution not supported |
| ESP_ERR_CAMERA_FAILED_TO_SET_OUT_FORMAT | Format not supported |
| ESP_ERR_CAMERA_NOT_SUPPORTED | Feature not available |

---

## sensor_t Function Pointers (via esp_camera_sensor_get)

```c
sensor_t *s = esp_camera_sensor_get();

// Image quality
s->set_framesize(s, FRAMESIZE_VGA);
s->set_quality(s, 10);              // 0-63
s->set_brightness(s, 0);            // -2 to 2
s->set_contrast(s, 0);              // -2 to 2
s->set_saturation(s, 0);            // -2 to 2
s->set_sharpness(s, 0);             // OV2640: unsupported

// Exposure & gain
s->set_exposure_ctrl(s, 1);         // 0=manual, 1=auto
s->set_aec2(s, 0);                  // Night mode
s->set_ae_level(s, 0);              // -2 to 2
s->set_aec_value(s, 300);           // 0-1200
s->set_gain_ctrl(s, 1);             // 0=manual, 1=auto
s->set_agc_gain(s, 0);              // 0-30
s->set_gainceiling(s, GAINCEILING_2X);

// White balance
s->set_whitebal(s, 1);              // 0=off, 1=auto
s->set_awb_gain(s, 1);
s->set_wb_mode(s, 0);               // 0=Auto, 1=Sunny, 2=Cloudy, 3=Office, 4=Home

// DSP features
s->set_raw_gma(s, 1);               // Gamma correction
s->set_lenc(s, 1);                   // Lens correction
s->set_dcw(s, 1);                    // Downsize enable
s->set_bpc(s, 0);                    // Black pixel correction
s->set_wpc(s, 1);                    // White pixel correction

// Mirror/flip
s->set_hmirror(s, 0);
s->set_vflip(s, 0);

// Special effects
s->set_special_effect(s, 0);         // 0=None, 1=Negative, 2=Grayscale,
                                     // 3=Red, 4=Green, 5=Blue, 6=Sepia

// Test
s->set_colorbar(s, 0);              // 0=off, 1=test pattern
```

---

## Important Notes

1. **PSRAM Required**: JPEG above CIF or any RGB/YUV above QVGA needs PSRAM
2. **PCLK Limit**: ESP32 max 8 MHz, ESP32-S3 max 40 MHz
3. **WiFi + Camera**: YUV/RGB + WiFi may cause data corruption; use JPEG
4. **fb_count=1**: Waits for VSYNC; fb_count=2+: continuous capture
5. **Power**: ESP32-CAM needs stable 5V, 310mA peak (flash on)

---

## Installation

```
# ESP-IDF
idf.py add-dependency "espressif/esp32-camera"

# PlatformIO
lib_deps = esp32-camera

# Arduino IDE
# Pre-installed with arduino-esp32 core
```
