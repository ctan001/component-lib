/*
 * ESP32-CAM 拍照儲存到 microSD 卡
 * 完成後進入深度睡眠
 *
 * Arduino IDE: Tools > Board > AI-Thinker ESP32-CAM
 * 燒錄時 GPIO0 接 GND，燒錄完移除跳線再按 RESET
 *
 * Source: HandsOn Technology / handsontec.com
 */

#include "esp_camera.h"
#include "Arduino.h"
#include "FS.h"
#include "SD_MMC.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "driver/rtc_io.h"
#include <EEPROM.h>

#define EEPROM_SIZE 1

// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM   32
#define RESET_GPIO_NUM  -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM   26
#define SIOC_GPIO_NUM   27
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

int pictureNumber = 0;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // 停用欠壓重置

  Serial.begin(115200);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size   = FRAMESIZE_UXGA;  // 1600x1200
    config.jpeg_quality = 10;
    config.fb_count     = 2;
  } else {
    config.frame_size   = FRAMESIZE_SVGA;  // 800x600
    config.jpeg_quality = 12;
    config.fb_count     = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x\n", err);
    return;
  }

  if (!SD_MMC.begin()) {
    Serial.println("SD Card Mount Failed");
    return;
  }

  if (SD_MMC.cardType() == CARD_NONE) {
    Serial.println("No SD Card attached");
    return;
  }

  // 拍照
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  EEPROM.begin(EEPROM_SIZE);
  pictureNumber = EEPROM.read(0) + 1;

  String path = "/picture" + String(pictureNumber) + ".jpg";
  fs::FS &fs  = SD_MMC;
  Serial.printf("Saving to: %s\n", path.c_str());

  File file = fs.open(path.c_str(), FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file");
  } else {
    file.write(fb->buf, fb->len);
    Serial.printf("Saved %u bytes\n", fb->len);
    EEPROM.write(0, pictureNumber);
    EEPROM.commit();
  }
  file.close();
  esp_camera_fb_return(fb);

  // 關閉 Flash LED
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  rtc_gpio_hold_en(GPIO_NUM_4);

  delay(2000);
  Serial.println("Going to deep sleep...");
  delay(2000);
  esp_deep_sleep_start();
}

void loop() {
  // 不會執行到這裡（深度睡眠後 setup 重新執行）
}
