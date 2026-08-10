# component-lib 元件索引

> 更新時間：2026-08-10
> 元件總數：53

| 元件 | 中文名 | 類別 | 介面 | MicroPython Driver | 驗證狀態 |
|:--|:--|:--|:--|:--|:--|
| [raspberry-pi-pico](components/board/mcu/raspberry-pi-pico/) | Raspberry Pi Pico（非Wi-Fi官方板，RP2040） | board/mcu | USB, GPIO, ADC, PWM, I2C, SPI, UART, PIO | ❌ | ✅ |
| [bjt-mmbt3904](components/actuator/bjt-mmbt3904/) | NPN 通用晶體 MMBT3904 | actuator | GPIO | ❌ | ⏳ |
| [bjt-mmbt3906](components/actuator/bjt-mmbt3906/) | PNP 通用晶體 MMBT3906 | actuator | GPIO | ❌ | ⏳ |
| [buzzer-active](components/actuator/buzzer-active/) | 有源蜂鸣器 | actuator | GPIO | ✅ | ⏳ |
| [ir-emitter-tsal](components/actuator/ir-emitter-tsal/) | 红外发射模块 TSAL6100/6200 + BJT 驱动 | actuator | GPIO, PWM | ❌ | ⏳ |
| [motor-130](components/actuator/motor-130/) | 130电机模块 | actuator | GPIO | ✅ | ⏳ |
| [servo](components/actuator/servo/) | 伺服舵机 | actuator | PWM | ✅ | ⏳ |
| [speaker-8002b](components/actuator/speaker-8002b/) | 8002B功放喇叭模块 | actuator | PWM | ✅ | ⏳ |
| [tm1650](components/display/7seg/tm1650/) | TM1650四位数码管模块 | display/7seg | I2C | ✅ | ⏳ |
| [lcd-128x32-st7567a](components/display/lcd/lcd-128x32-st7567a/) | LCD 128x32 DOT模块 | display/lcd | I2C | ✅ | ✅ |
| [lcd-2004-i2c](components/display/lcd/lcd-2004-i2c/) | I2C 2004 LCD 字元顯示模組 | display/lcd | I2C | ✅ | ✅ |
| [rgb-3color](components/display/led/rgb-3color/) | 3色LED模块 | display/led | GPIO | ✅ | ⏳ |
| [rgb-plugin](components/display/led/rgb-plugin/) | 插件RGB | display/led | GPIO | ✅ | ⏳ |
| [sk6812](components/display/led/sk6812/) | SK6812 RGB模块 | display/led | PIO | ✅ | ⏳ |
| [ht16k33-8x8](components/display/matrix/ht16k33-8x8/) | HT16K33 8X8点阵模块 | display/matrix | I2C | ✅ | ⏳ |
| [oled-128x64-sh1106](components/display/oled/oled-128x64-sh1106/) | 1.3" OLED 128x64 顯示模組 | display/oled | I2C | ✅ | ✅ |
| [oled-128x64-ssd1309](components/display/oled/oled-128x64-ssd1309/) | 2.42" OLED 128x64 顯示模組 | display/oled | I2C | ✅ | ✅ |
| [adc-button-5way](components/input/adc-button-5way/) | 五路AD按键 | input | ADC | ✅ | ⏳ |
| [ir-receiver](components/input/ir-receiver/) | 红外遥控接收器 | input | GPIO | ✅ | ✅ |
| [joystick](components/input/joystick/) | 遥感模块 | input | ADC, GPIO | ✅ | ⏳ |
| [rotary-encoder](components/input/rotary-encoder/) | 旋转编码器 | input | GPIO | ✅ | ⏳ |
| [mfrc522](components/module/rfid/mfrc522/) | RFID刷卡模块 | module/rfid | SPI | ✅ | ⏳ |
| [ds1307](components/module/rtc/ds1307/) | 实时时钟DS1307 | module/rtc | I2C | ✅ | ⏳ |
| [ds18b20](components/sensor/1wire/ds18b20/) | DS18B20温度传感器 | sensor/1wire | 1-Wire | ✅ | ⏳ |
| [ntc-temperature](components/sensor/analog/ntc-temperature/) | 模拟温度传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [photoresistor](components/sensor/analog/photoresistor/) | 光敏电阻传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [potentiometer](components/sensor/analog/potentiometer/) | 旋转电位器 | sensor/analog | ADC | ✅ | ⏳ |
| [pressure-film](components/sensor/analog/pressure-film/) | 薄膜压力传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [sound](components/sensor/analog/sound/) | 声音传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [uv](components/sensor/analog/uv/) | 太阳光紫外线传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [water-steam](components/sensor/analog/water-steam/) | 水滴水蒸气传感器 | sensor/analog | ADC | ✅ | ⏳ |
| [button](components/sensor/digital/button/) | 按键 | sensor/digital | GPIO | ✅ | ⏳ |
| [capacitive-touch](components/sensor/digital/capacitive-touch/) | 电容触摸传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [collision](components/sensor/digital/collision/) | 碰撞传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [hall](components/sensor/digital/hall/) | 霍尔传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [line-following](components/sensor/digital/line-following/) | 巡线传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [obstacle-avoidance](components/sensor/digital/obstacle-avoidance/) | 避障传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [photointerrupter](components/sensor/digital/photointerrupter/) | 光折断模块 | sensor/digital | GPIO | ✅ | ⏳ |
| [pir](components/sensor/digital/pir/) | 人体红外热传感器 | sensor/digital | GPIO | ✅ | ⏳ |
| [reed-switch](components/sensor/digital/reed-switch/) | 干簧管模块 | sensor/digital | GPIO | ✅ | ⏳ |
| [tilt](components/sensor/digital/tilt/) | 倾斜模块 | sensor/digital | GPIO | ✅ | ⏳ |
| [flame](components/sensor/dual/flame/) | 火焰传感器 | sensor/dual | ADC, GPIO | ✅ | ⏳ |
| [mq2-smoke](components/sensor/dual/mq2-smoke/) | MQ-2烟雾传感器 | sensor/dual | ADC, GPIO | ✅ | ⏳ |
| [mq3-alcohol](components/sensor/dual/mq3-alcohol/) | MQ-3酒精传感器 | sensor/dual | ADC, GPIO | ✅ | ✅ |
| [ens160](components/sensor/gas/ens160/) | ENS160 數位空氣品質感應器 | sensor/gas | I2C | ✅ | ✅ |
| [aht21](components/sensor/humidity/aht21/) | AHT21 溫濕度感應器 | sensor/humidity | I2C | ✅ | ✅ |
| [xht11](components/sensor/humidity/xht11/) | XHT11温湿度传感器 | sensor/humidity | DHT | ✅ | ✅ |
| [adxl345](components/sensor/imu/adxl345/) | ADXL345加速度传感器 | sensor/imu | I2C, SPI | ✅ | ⏳ |
| [hc-sr04](components/sensor/ultrasonic/hc-sr04/) | 超声波传感器 | sensor/ultrasonic | GPIO | ✅ | ⏳ |
| [PMS5003](components/sensor/particle/pms5003/) |  | sensor/particle | U, A, R, T | ❌ | ⏳ |
| [cc1101-e07-m1101d-sma](components/module/rf/cc1101-e07-m1101d-sma/) | CC1101 433MHz RF收發模組（E07-M1101D-SMA） | module/rf | SPI | ❌ | ⏳ |
| [esp32-cam](components/module/camera/esp32-cam/) | ESP32-CAM WiFi攝像頭模組 | module/camera | UART, WiFi, Bluetooth, SDMMC, GPIO | ❌ | ⏳ |
| [xiao-vision-ai](components/module/camera/xiao-vision-ai/) | XIAO Vision AI 攝像頭（邊緣 AI 視覺套件） | module/camera | USB-C, WiFi, Bluetooth, I2C, UART, SPI, CSI | ❌ | ⏳ |

---

驗證狀態：⏳ pending | ✅ verified | ❌ failed
