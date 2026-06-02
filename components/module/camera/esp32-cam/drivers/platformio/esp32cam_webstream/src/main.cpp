#include "esp_camera.h"
#include "WiFi.h"
#include "esp_http_server.h"
#include "esp_timer.h"
#include "img_converters.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

// ----- WiFi -----
const char *ssid     = "JerryHome-5G";
const char *password = "jena0915";

// ----- AI-Thinker ESP32-CAM pin map -----
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
#define FLASH_GPIO_NUM   4

httpd_handle_t stream_httpd = NULL;
httpd_handle_t camera_httpd = NULL;

#define PART_BOUNDARY "123456789000000000000987654321"
static const char *STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char *STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char *STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\nX-Timestamp: %d.%06d\r\n\r\n";

// ----- Single capture handler: /capture -----
static esp_err_t capture_handler(httpd_req_t *req) {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        httpd_resp_send_500(req);
        return ESP_FAIL;
    }
    httpd_resp_set_type(req, "image/jpeg");
    httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    esp_err_t res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
    esp_camera_fb_return(fb);
    return res;
}

// ----- MJPEG stream handler: /stream -----
static esp_err_t stream_handler(httpd_req_t *req) {
    esp_err_t res = ESP_OK;
    char part_buf[128];

    res = httpd_resp_set_type(req, STREAM_CONTENT_TYPE);
    if (res != ESP_OK) return res;

    httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
    httpd_resp_set_hdr(req, "X-Framerate", "60");

    while (true) {
        camera_fb_t *fb = esp_camera_fb_get();
        if (!fb) {
            res = ESP_FAIL;
            break;
        }

        struct timeval tv = fb->timestamp;
        size_t hlen = snprintf(part_buf, sizeof(part_buf),
                               STREAM_PART, fb->len, (int)tv.tv_sec, (int)tv.tv_usec);

        res = httpd_resp_send_chunk(req, STREAM_BOUNDARY, strlen(STREAM_BOUNDARY));
        if (res == ESP_OK)
            res = httpd_resp_send_chunk(req, part_buf, hlen);
        if (res == ESP_OK)
            res = httpd_resp_send_chunk(req, (const char *)fb->buf, fb->len);

        esp_camera_fb_return(fb);

        if (res != ESP_OK) break;
    }
    return res;
}

// ----- Flash LED control: /flash?state=on|off -----
static esp_err_t flash_handler(httpd_req_t *req) {
    char buf[32];
    int len = httpd_req_get_url_query_len(req) + 1;
    if (len > 1 && len < (int)sizeof(buf)) {
        httpd_req_get_url_query_str(req, buf, len);
        char val[8];
        if (httpd_query_key_value(buf, "state", val, sizeof(val)) == ESP_OK) {
            digitalWrite(FLASH_GPIO_NUM, strcmp(val, "on") == 0 ? HIGH : LOW);
        }
    }
    httpd_resp_set_type(req, "text/plain");
    httpd_resp_sendstr(req, "OK");
    return ESP_OK;
}

// ----- Index page: / -----
static const char INDEX_HTML[] = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ESP32-CAM Stream</title>
  <style>
    body { font-family: Arial, sans-serif; text-align: center; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }
    h1 { color: #e94560; }
    img { max-width: 100%; border: 2px solid #e94560; border-radius: 8px; margin: 10px 0; }
    .btn { display: inline-block; padding: 12px 24px; margin: 8px; border: none; border-radius: 6px;
           font-size: 16px; cursor: pointer; color: #fff; text-decoration: none; }
    .btn-stream { background: #0f3460; }
    .btn-capture { background: #533483; }
    .btn-flash { background: #e94560; }
    .btn:hover { opacity: 0.85; }
    .info { color: #aaa; font-size: 14px; margin-top: 16px; }
    select { padding: 8px; font-size: 14px; border-radius: 4px; margin: 8px; }
  </style>
</head>
<body>
  <h1>ESP32-CAM</h1>
  <div>
    <button class="btn btn-stream" onclick="startStream()">Start Stream</button>
    <button class="btn btn-stream" onclick="stopStream()">Stop Stream</button>
    <button class="btn btn-capture" onclick="capture()">Capture</button>
    <button class="btn btn-flash" onclick="toggleFlash()">Flash Toggle</button>
  </div>
  <div>
    <label>Resolution: </label>
    <select id="res" onchange="setResolution()">
      <option value="13">UXGA (1600x1200)</option>
      <option value="12">SXGA (1280x1024)</option>
      <option value="11">HD (1280x720)</option>
      <option value="10">XGA (1024x768)</option>
      <option value="9" selected>SVGA (800x600)</option>
      <option value="8">VGA (640x480)</option>
      <option value="6">CIF (400x296)</option>
      <option value="5">QVGA (320x240)</option>
    </select>
  </div>
  <div><img id="viewer" src=""></div>
  <p class="info" id="status">Ready</p>

  <script>
    var flashOn = false;
    var baseUrl = window.location.origin;

    function startStream() {
      document.getElementById('viewer').src = baseUrl + ':81/stream';
      document.getElementById('status').innerText = 'Streaming...';
    }
    function stopStream() {
      document.getElementById('viewer').src = '';
      document.getElementById('status').innerText = 'Stopped';
    }
    function capture() {
      document.getElementById('viewer').src = baseUrl + '/capture?' + Date.now();
      document.getElementById('status').innerText = 'Captured';
    }
    function toggleFlash() {
      flashOn = !flashOn;
      fetch(baseUrl + '/flash?state=' + (flashOn ? 'on' : 'off'));
      document.getElementById('status').innerText = 'Flash ' + (flashOn ? 'ON' : 'OFF');
    }
    function setResolution() {
      var val = document.getElementById('res').value;
      fetch(baseUrl + '/control?var=framesize&val=' + val)
        .then(function() { document.getElementById('status').innerText = 'Resolution changed'; });
    }
  </script>
</body>
</html>
)rawliteral";

static esp_err_t index_handler(httpd_req_t *req) {
    httpd_resp_set_type(req, "text/html");
    return httpd_resp_send(req, INDEX_HTML, strlen(INDEX_HTML));
}

// ----- Control handler: /control?var=framesize&val=N -----
static esp_err_t control_handler(httpd_req_t *req) {
    char buf[64];
    int len = httpd_req_get_url_query_len(req) + 1;
    if (len > 1 && len < (int)sizeof(buf)) {
        httpd_req_get_url_query_str(req, buf, len);
        char var[16], val[8];
        if (httpd_query_key_value(buf, "var", var, sizeof(var)) == ESP_OK &&
            httpd_query_key_value(buf, "val", val, sizeof(val)) == ESP_OK) {
            sensor_t *s = esp_camera_sensor_get();
            int v = atoi(val);
            if (strcmp(var, "framesize") == 0) {
                if (s->pixformat == PIXFORMAT_JPEG) {
                    s->set_framesize(s, (framesize_t)v);
                }
            } else if (strcmp(var, "quality") == 0) {
                s->set_quality(s, v);
            } else if (strcmp(var, "brightness") == 0) {
                s->set_brightness(s, v);
            } else if (strcmp(var, "contrast") == 0) {
                s->set_contrast(s, v);
            } else if (strcmp(var, "hmirror") == 0) {
                s->set_hmirror(s, v);
            } else if (strcmp(var, "vflip") == 0) {
                s->set_vflip(s, v);
            }
        }
    }
    httpd_resp_set_type(req, "text/plain");
    httpd_resp_sendstr(req, "OK");
    return ESP_OK;
}

// ----- Start web servers -----
void startCameraServer() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    config.max_uri_handlers = 8;

    // Port 80: index, capture, flash, control
    if (httpd_start(&camera_httpd, &config) == ESP_OK) {
        httpd_uri_t index_uri = { .uri = "/", .method = HTTP_GET, .handler = index_handler };
        httpd_uri_t capture_uri = { .uri = "/capture", .method = HTTP_GET, .handler = capture_handler };
        httpd_uri_t flash_uri = { .uri = "/flash", .method = HTTP_GET, .handler = flash_handler };
        httpd_uri_t control_uri = { .uri = "/control", .method = HTTP_GET, .handler = control_handler };
        httpd_register_uri_handler(camera_httpd, &index_uri);
        httpd_register_uri_handler(camera_httpd, &capture_uri);
        httpd_register_uri_handler(camera_httpd, &flash_uri);
        httpd_register_uri_handler(camera_httpd, &control_uri);
    }

    // Port 81: MJPEG stream
    config.server_port = 81;
    config.ctrl_port += 1;
    if (httpd_start(&stream_httpd, &config) == ESP_OK) {
        httpd_uri_t stream_uri = { .uri = "/stream", .method = HTTP_GET, .handler = stream_handler };
        httpd_register_uri_handler(stream_httpd, &stream_uri);
    }
}

void setup() {
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
    Serial.begin(115200);
    Serial.println("\n\n=== ESP32-CAM Web Stream ===");

    // Flash LED off
    pinMode(FLASH_GPIO_NUM, OUTPUT);
    digitalWrite(FLASH_GPIO_NUM, LOW);

    // Camera config
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
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn     = PWDN_GPIO_NUM;
    config.pin_reset    = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.grab_mode    = CAMERA_GRAB_LATEST;

    if (psramFound()) {
        Serial.println("PSRAM found");
        config.frame_size   = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count     = 2;
        config.fb_location  = CAMERA_FB_IN_PSRAM;
    } else {
        Serial.println("No PSRAM");
        config.frame_size   = FRAMESIZE_VGA;
        config.jpeg_quality = 15;
        config.fb_count     = 1;
        config.fb_location  = CAMERA_FB_IN_DRAM;
    }

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init FAILED: 0x%x\n", err);
        return;
    }
    Serial.println("Camera init OK");

    // Default sensor tweaks
    sensor_t *s = esp_camera_sensor_get();
    s->set_brightness(s, 1);
    s->set_saturation(s, 0);

    // WiFi connect
    WiFi.begin(ssid, password);
    WiFi.setSleep(false);
    Serial.print("Connecting to WiFi");
    int retry = 0;
    while (WiFi.status() != WL_CONNECTED && retry < 30) {
        delay(500);
        Serial.print(".");
        retry++;
    }

    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("\nWiFi FAILED");
        return;
    }

    Serial.println("");
    Serial.println("WiFi connected!");
    Serial.print("  IP: http://");
    Serial.println(WiFi.localIP());
    Serial.print("  Stream: http://");
    Serial.print(WiFi.localIP());
    Serial.println(":81/stream");

    startCameraServer();
    Serial.println("Web server started");
}

void loop() {
    delay(10000);
}
