"""批次生成所有元件的 component.json 和 README.md"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-05-14"

def comp_path(rel):
    return os.path.join(BASE, "components", rel.replace("/", os.sep))

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def gitkeep(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").close()

def make_comp(rel, name, name_zh, manufacturer, part_number, category, description,
              interface, voltage, pins, logic, driver_file, datasheet_url=None,
              datasheet_source=None, datasheet_filename=None, extra_pins=None):
    if extra_pins:
        pins = pins + extra_pins
    return {
        "name": name,
        "name_zh": name_zh,
        "manufacturer": manufacturer,
        "part_number": part_number,
        "category": category,
        "description": description,
        "interface": interface,
        "voltage": voltage,
        "pins": pins,
        "logic": logic,
        "datasheet": {
            "filename": datasheet_filename,
            "source": datasheet_source,
            "url": datasheet_url,
            "downloaded": False
        },
        "drivers": {
            "micropython": f"drivers/micropython/{driver_file}",
            "circuitpython": None,
            "arduino": None
        },
        "verification": {
            "status": "pending",
            "platform": None,
            "date": None,
            "notes": ""
        },
        "added": DATE,
        "updated": DATE
    }

VCC_GND_S = [
    {"name": "VCC", "function": "電源 3.3V/5V", "direction": "input"},
    {"name": "GND", "function": "接地", "direction": "input"},
    {"name": "S",   "function": "信號端", "direction": "output"}
]
VCC_GND = [
    {"name": "VCC", "function": "電源 3.3V/5V", "direction": "input"},
    {"name": "GND", "function": "接地", "direction": "input"}
]
V33_5 = {"min": 3.3, "max": 5.0, "unit": "V"}
V33 = {"min": 3.3, "max": 3.3, "unit": "V"}
V33_5V = {"min": 3.3, "max": 5.0, "unit": "V"}

COMPONENTS = [
    # --- sensor/digital ---
    ("sensor/digital/button", make_comp(
        "sensor/digital/button",
        "button", "按键", "unknown", "generic",
        "sensor/digital",
        "數位按鍵模組，未按 S=HIGH（4.7K 上拉），按下 S=LOW",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "button.py"
    )),
    ("sensor/digital/capacitive-touch", make_comp(
        "sensor/digital/capacitive-touch",
        "capacitive-touch", "电容触摸传感器", "unknown", "generic",
        "sensor/digital",
        "電容觸摸感應模組，觸摸時 S=HIGH，未觸摸 S=LOW",
        ["GPIO"], V33_5, VCC_GND_S, "active-high", "capacitive_touch.py"
    )),
    ("sensor/digital/obstacle-avoidance", make_comp(
        "sensor/digital/obstacle-avoidance",
        "obstacle-avoidance", "避障传感器", "unknown", "generic",
        "sensor/digital",
        "NE555+IR 避障感應，有障礙物時 S=LOW，無障礙 S=HIGH，兩個電位器可調距離",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "obstacle_avoidance.py"
    )),
    ("sensor/digital/line-following", make_comp(
        "sensor/digital/line-following",
        "line-following", "巡线传感器", "unknown", "generic",
        "sensor/digital",
        "LM393 比較器 IR 巡線，黑色/無物 S=HIGH，白色 S=LOW，檢測高度 0-3cm",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "line_following.py"
    )),
    ("sensor/digital/photointerrupter", make_comp(
        "sensor/digital/photointerrupter",
        "photointerrupter", "光折断模块", "unknown", "generic",
        "sensor/digital",
        "光電對射式開關，遮擋凹槽時 S=HIGH，未遮擋時 S=LOW（R2 下拉）",
        ["GPIO"], V33_5, VCC_GND_S, "active-high", "photointerrupter.py"
    )),
    ("sensor/digital/tilt", make_comp(
        "sensor/digital/tilt",
        "tilt", "倾斜模块", "unknown", "generic",
        "sensor/digital",
        "滾珠開關傾斜感應，傾斜導通時 S=LOW，LED 亮；直立時 S=HIGH（4.7K 上拉）",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "tilt.py"
    )),
    ("sensor/digital/collision", make_comp(
        "sensor/digital/collision",
        "collision", "碰撞传感器", "unknown", "generic",
        "sensor/digital",
        "輕觸開關碰撞感應，碰觸時 S=LOW，LED 亮；未碰觸 S=HIGH（4.7K 上拉）",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "collision.py"
    )),
    ("sensor/digital/hall", make_comp(
        "sensor/digital/hall",
        "hall", "霍尔传感器", "unknown", "A3144",
        "sensor/digital",
        "A3144 線性霍爾元件，偵測到磁場時 S=LOW（open-collector），無磁場 S=HIGH",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "hall.py"
    )),
    ("sensor/digital/reed-switch", make_comp(
        "sensor/digital/reed-switch",
        "reed-switch", "干簧管模块", "unknown", "generic",
        "sensor/digital",
        "乾簧管磁場感應，有磁場時簧片吸合 S=LOW，LED 亮；無磁場 S=HIGH（上拉）",
        ["GPIO"], V33_5, VCC_GND_S, "active-low", "reed_switch.py"
    )),
    ("sensor/digital/pir", make_comp(
        "sensor/digital/pir",
        "pir", "人体红外热传感器", "unknown", "generic",
        "sensor/digital",
        "PIR 人體紅外感應，偵測到人時 S=HIGH；無人 S=LOW，模組內建 3.3V 穩壓",
        ["GPIO"], V33_5, VCC_GND_S, "active-high", "pir.py"
    )),
    # --- sensor/analog ---
    ("sensor/analog/potentiometer", make_comp(
        "sensor/analog/potentiometer",
        "potentiometer", "旋转电位器", "unknown", "generic",
        "sensor/analog",
        "旋轉電位器，輸出 0–VCC 類比電壓，對應 ADC 0–65535",
        ["ADC"], V33_5, VCC_GND_S, "analog", "potentiometer.py"
    )),
    ("sensor/analog/water-steam", make_comp(
        "sensor/analog/water-steam",
        "water-steam", "水滴水蒸气传感器", "unknown", "generic",
        "sensor/analog",
        "裸露平行線偵測水量，水越多導電面積越大，ADC 值越大；也可偵測空氣水蒸氣",
        ["ADC"], V33_5, VCC_GND_S, "analog", "water_steam.py"
    )),
    ("sensor/analog/sound", make_comp(
        "sensor/analog/sound",
        "sound", "声音传感器", "unknown", "generic",
        "sensor/analog",
        "高感度麥克風 + LM386 放大（最大 200 倍），電位器調放大倍數，類比輸出聲音強度",
        ["ADC"], V33_5, VCC_GND_S, "analog", "sound.py"
    )),
    ("sensor/analog/photoresistor", make_comp(
        "sensor/analog/photoresistor",
        "photoresistor", "光敏电阻传感器", "unknown", "generic",
        "sensor/analog",
        "光敏電阻分壓電路，光越強電阻越小，S 電壓越高，ADC 值越大",
        ["ADC"], V33_5, VCC_GND_S, "analog", "photoresistor.py"
    )),
    ("sensor/analog/ntc-temperature", make_comp(
        "sensor/analog/ntc-temperature",
        "ntc-temperature", "模拟温度传感器", "unknown", "NTC-MF52AT",
        "sensor/analog",
        "NTC-MF52AT 熱敏電阻（10kΩ@25°C，B=3950），串聯 10kΩ 分壓，Steinhart-Hart 轉換溫度",
        ["ADC"], V33_5, VCC_GND_S, "analog", "ntc_temperature.py"
    )),
    ("sensor/analog/pressure-film", make_comp(
        "sensor/analog/pressure-film",
        "pressure-film", "薄膜压力传感器", "unknown", "generic",
        "sensor/analog",
        "薄膜壓力感應，壓力越大 ADC 值越小，類比輸出壓力強度",
        ["ADC"],
        {"min": 3.3, "max": 5.0, "unit": "V"},
        [
            {"name": "V", "function": "電源 VCC", "direction": "input"},
            {"name": "G", "function": "接地 GND", "direction": "input"},
            {"name": "S", "function": "信號端（類比）", "direction": "output"}
        ],
        "analog", "pressure_film.py"
    )),
    ("sensor/analog/uv", make_comp(
        "sensor/analog/uv",
        "uv", "太阳光紫外线传感器", "unknown", "generic",
        "sensor/analog",
        "UV 紫外線感應，輸出電流正比光照強度，模組電路已轉為電壓類比輸出",
        ["ADC"], V33_5, VCC_GND_S, "analog", "uv.py"
    )),
    # --- sensor/dual ---
    ("sensor/dual/flame", make_comp(
        "sensor/dual/flame",
        "flame", "火焰传感器", "unknown", "generic",
        "sensor/dual",
        "偵測 700–1000nm 紅外光（最佳 880nm），D0 active-low 數位警報，A0 類比強度（越亮值越小）",
        ["ADC", "GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "A0", "function": "類比信號端（外界IR越強值越小）", "direction": "output"},
            {"name": "D0", "function": "數位信號端（偵測到火焰時LOW）", "direction": "output"}
        ],
        "active-low", "flame.py"
    )),
    ("sensor/dual/mq2-smoke", make_comp(
        "sensor/dual/mq2-smoke",
        "mq2-smoke", "MQ-2烟雾传感器", "unknown", "MQ-2",
        "sensor/dual",
        "MQ-2 煙霧/可燃氣體感應，A0 類比濃度（越濃越大），D0 active-low 閾值警報（電位器調整）",
        ["ADC", "GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "A0", "function": "類比信號端（氣體濃度越高值越大）", "direction": "output"},
            {"name": "D0", "function": "數位信號端（超過閾值時LOW）", "direction": "output"}
        ],
        "active-low", "mq2_smoke.py"
    )),
    ("sensor/dual/mq3-alcohol", make_comp(
        "sensor/dual/mq3-alcohol",
        "mq3-alcohol", "MQ-3酒精传感器", "unknown", "MQ-3",
        "sensor/dual",
        "MQ-3 酒精蒸汽感應，A0 類比濃度（越濃越大），D0 active-low 閾值警報（電位器調整）",
        ["ADC", "GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "A0", "function": "類比信號端（酒精濃度越高值越大）", "direction": "output"},
            {"name": "D0", "function": "數位信號端（超過閾值時LOW）", "direction": "output"}
        ],
        "active-low", "mq3_alcohol.py"
    )),
    # --- sensor/1wire ---
    ("sensor/1wire/ds18b20", make_comp(
        "sensor/1wire/ds18b20",
        "ds18b20", "DS18B20温度传感器", "Maxim Integrated", "DS18B20",
        "sensor/1wire",
        "DS18B20 數位溫度感應，1-Wire 協議，精度 ±0.5°C，測量範圍 -55°C~+125°C",
        ["1-Wire"],
        V33_5,
        VCC_GND + [
            {"name": "DQ", "function": "單線數據（需 4.7K 上拉）", "direction": "bidirectional"}
        ],
        "protocol", "ds18b20.py",
        datasheet_url="https://www.mouser.com/datasheet/2/256/DS18B20-1203094.pdf",
        datasheet_source="mouser",
        datasheet_filename="DS18B20.pdf"
    )),
    # --- sensor/humidity ---
    ("sensor/humidity/xht11", make_comp(
        "sensor/humidity/xht11",
        "xht11", "XHT11温湿度传感器", "XHOSSEM", "XHT11",
        "sensor/humidity",
        "XHT11 數位溫濕度感應（DHT11 相容），單線協議，溫度精度 ±2°C，濕度精度 ±5%RH",
        ["DHT"],
        V33_5,
        VCC_GND + [
            {"name": "S", "function": "單線數據（DHT 協議）", "direction": "bidirectional"}
        ],
        "protocol", "xht11.py",
        datasheet_url=None,
        datasheet_source=None,
        datasheet_filename="XHT11.pdf"
    )),
    # --- sensor/imu ---
    ("sensor/imu/adxl345", make_comp(
        "sensor/imu/adxl345",
        "adxl345", "ADXL345加速度传感器", "Analog Devices", "ADXL345",
        "sensor/imu",
        "ADXL345 三軸加速度計，支援 I2C/SPI，量程 ±2/4/8/16g，10-bit 解析度",
        ["I2C", "SPI"],
        {"min": 2.0, "max": 3.6, "unit": "V"},
        VCC_GND + [
            {"name": "SDA/SDI", "function": "I2C SDA / SPI MOSI", "direction": "bidirectional"},
            {"name": "SCL/SCK", "function": "I2C SCL / SPI SCK", "direction": "input"},
            {"name": "SDO",     "function": "SPI MISO / I2C地址選擇（GND=0x53, VCC=0x1D）", "direction": "output"},
            {"name": "CS",      "function": "SPI 片選（I2C 模式接 VCC）", "direction": "input"}
        ],
        "protocol", "adxl345.py",
        datasheet_url="https://www.mouser.com/datasheet/2/609/ADXL345-1544506.pdf",
        datasheet_source="mouser",
        datasheet_filename="ADXL345.pdf"
    )),
    # --- sensor/ultrasonic ---
    ("sensor/ultrasonic/hc-sr04", make_comp(
        "sensor/ultrasonic/hc-sr04",
        "hc-sr04", "超声波传感器", "unknown", "HC-SR04",
        "sensor/ultrasonic",
        "HC-SR04 超聲波測距，量程 2-400cm，精度 3mm，TRIG 拉高 10μs 觸發，ECHO 高電平持續時間正比距離",
        ["GPIO"],
        {"min": 4.5, "max": 5.5, "unit": "V"},
        VCC_GND + [
            {"name": "TRIG", "function": "觸發端（輸出 10μs 高電平）", "direction": "input"},
            {"name": "ECHO", "function": "回波端（高電平持續時間 = 往返時間）", "direction": "output"}
        ],
        "protocol", "hc_sr04.py"
    )),
    # --- input ---
    ("input/adc-button-5way", make_comp(
        "input/adc-button-5way",
        "adc-button-5way", "五路AD按键", "unknown", "generic",
        "input",
        "五個按鍵共用一個 ADC 腳，電阻分壓產生不同電壓，16-bit ADC 區分各鍵",
        ["ADC"], V33_5, VCC_GND_S, "analog", "adc_button_5way.py"
    )),
    ("input/joystick", make_comp(
        "input/joystick",
        "joystick", "遥感模块", "unknown", "generic",
        "input",
        "搖桿模組，X/Y 軸各一個 ADC 電位器，Z 軸按鈕（按下=HIGH，與一般按鍵相反）",
        ["ADC", "GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "X",  "function": "X 軸類比輸出", "direction": "output"},
            {"name": "Y",  "function": "Y 軸類比輸出", "direction": "output"},
            {"name": "B",  "function": "Z 軸按鈕（按下=HIGH, active-high）", "direction": "output"}
        ],
        "analog", "joystick.py"
    )),
    ("input/rotary-encoder", make_comp(
        "input/rotary-encoder",
        "rotary-encoder", "旋转编码器", "unknown", "generic",
        "input",
        "增量式旋轉編碼器，20 脈衝/轉，CLK 下降沿時 DT=HIGH→順時針，DT=LOW→逆時針",
        ["GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "CLK", "function": "時鐘信號", "direction": "output"},
            {"name": "DT",  "function": "方向信號", "direction": "output"},
            {"name": "SW",  "function": "按鈕（active-low）", "direction": "output"}
        ],
        "protocol", "rotary_encoder.py"
    )),
    ("input/ir-receiver", make_comp(
        "input/ir-receiver",
        "ir-receiver", "红外遥控接收器", "unknown", "generic",
        "input",
        "38kHz NEC 協議 IR 接收，S 端接 4.7K 上拉，接收到信號時由 HIGH 轉 LOW",
        ["GPIO"], V33_5, VCC_GND_S, "protocol", "ir_receiver.py"
    )),
    # --- actuator ---
    ("actuator/buzzer-active", make_comp(
        "actuator/buzzer-active",
        "buzzer-active", "有源蜂鸣器", "unknown", "generic",
        "actuator",
        "有源蜂鳴器，S=HIGH 三極管導通蜂鳴，S=LOW 靜音（active-high）",
        ["GPIO"], V33_5, VCC_GND_S, "active-high", "buzzer_active.py"
    )),
    ("actuator/speaker-8002b", make_comp(
        "actuator/speaker-8002b",
        "speaker-8002b", "8002B功放喇叭模块", "unknown", "8002B",
        "actuator",
        "8002B 功放喇叭，小音頻信號放大約 8.5 倍，PWM 輸出不同頻率音調",
        ["PWM"],
        V33_5,
        VCC_GND + [
            {"name": "IN", "function": "音頻輸入（PWM 信號）", "direction": "input"}
        ],
        "pwm", "speaker_8002b.py"
    )),
    ("actuator/motor-130", make_comp(
        "actuator/motor-130",
        "motor-130", "130电机模块", "unknown", "HR1124S",
        "actuator",
        "130 DC 馬達 + HR1124S H 橋驅動，IN+=HIGH/IN-=LOW 正轉，反之反轉，兩者同 LOW 滑行停止",
        ["GPIO"],
        V33_5,
        VCC_GND + [
            {"name": "IN+", "function": "馬達控制端正", "direction": "input"},
            {"name": "IN-", "function": "馬達控制端負", "direction": "input"}
        ],
        "active-high", "motor_130.py"
    )),
    ("actuator/servo", make_comp(
        "actuator/servo",
        "servo", "伺服舵机", "unknown", "SG90",
        "actuator",
        "伺服舵機，PWM 50Hz（20ms 周期），脈寬 0.5ms-2.5ms 對應 0°-180°",
        ["PWM"], V33_5,
        VCC_GND + [
            {"name": "S", "function": "PWM 信號端", "direction": "input"}
        ],
        "pwm", "servo.py"
    )),
    # --- display/led ---
    ("display/led/rgb-3color", make_comp(
        "display/led/rgb-3color",
        "rgb-3color", "3色LED模块", "unknown", "generic",
        "display/led",
        "三色 LED 模組（紅/黃/綠），各腳高電平亮起對應顏色（active-high）",
        ["GPIO"], V33_5,
        VCC_GND + [
            {"name": "R", "function": "紅色 LED 控制（HIGH=亮）", "direction": "input"},
            {"name": "Y", "function": "黃色 LED 控制（HIGH=亮）", "direction": "input"},
            {"name": "G", "function": "綠色 LED 控制（HIGH=亮）", "direction": "input"}
        ],
        "active-high", "rgb_3color.py"
    )),
    ("display/led/rgb-plugin", make_comp(
        "display/led/rgb-plugin",
        "rgb-plugin", "插件RGB", "unknown", "generic",
        "display/led",
        "直插式 RGB LED（共陰），R/G/B 三腳分別限流電阻控制，高電平亮起",
        ["GPIO"], V33_5,
        [
            {"name": "R",   "function": "紅色陽極（含限流電阻）", "direction": "input"},
            {"name": "G",   "function": "綠色陽極（含限流電阻）", "direction": "input"},
            {"name": "B",   "function": "藍色陽極（含限流電阻）", "direction": "input"},
            {"name": "GND", "function": "共陰接地", "direction": "input"}
        ],
        "active-high", "rgb_plugin.py"
    )),
    ("display/led/sk6812", make_comp(
        "display/led/sk6812",
        "sk6812", "SK6812 RGB模块", "unknown", "SK6812",
        "display/led",
        "SK6812 可定址 RGB LED，單線歸零碼協議（24-bit GRB），多顆串聯，PIO 實作",
        ["PIO"], V33_5,
        VCC_GND + [
            {"name": "DIN", "function": "串行數據輸入（單線）", "direction": "input"}
        ],
        "protocol", "sk6812.py"
    )),
    # --- display/7seg ---
    ("display/7seg/tm1650", make_comp(
        "display/7seg/tm1650",
        "tm1650", "TM1650四位数码管模块", "Titan Micro", "TM1650",
        "display/7seg",
        "TM1650 四位七段數碼管，I2C-like 協議，顯示地址 0x34-0x37，控制地址 0x24-0x27",
        ["I2C"], V33_5,
        VCC_GND + [
            {"name": "SDA", "function": "數據線（I2C-like）", "direction": "bidirectional"},
            {"name": "SCL", "function": "時鐘線", "direction": "input"}
        ],
        "protocol", "tm1650.py",
        datasheet_url=None,
        datasheet_source=None,
        datasheet_filename="TM1650.pdf"
    )),
    # --- display/matrix ---
    ("display/matrix/ht16k33-8x8", make_comp(
        "display/matrix/ht16k33-8x8",
        "ht16k33-8x8", "HT16K33 8X8点阵模块", "Holtek", "HT16K33",
        "display/matrix",
        "HT16K33 8×8 LED 點陣驅動，I2C 地址 0x70（A0/A1/A2 全接 GND），最大 16×8 矩陣",
        ["I2C"], V33_5,
        VCC_GND + [
            {"name": "SDA", "function": "I2C 數據線", "direction": "bidirectional"},
            {"name": "SCL", "function": "I2C 時鐘線", "direction": "input"}
        ],
        "protocol", "ht16k33_8x8.py",
        datasheet_url="https://www.mouser.com/datasheet/2/198/DA00-HT16K33v120-1143516.pdf",
        datasheet_source="mouser",
        datasheet_filename="HT16K33.pdf"
    )),
    # --- display/lcd ---
    ("display/lcd/lcd-128x32-st7567a", make_comp(
        "display/lcd/lcd-128x32-st7567a",
        "lcd-128x32-st7567a", "LCD 128x32 DOT模块", "Sitronix", "ST7567A",
        "display/lcd",
        "128×32 像素 LCD，ST7567A 驅動晶片，SPI 介面，頁式定址模式",
        ["SPI"], V33_5,
        VCC_GND + [
            {"name": "SCK",  "function": "SPI 時鐘", "direction": "input"},
            {"name": "SDA",  "function": "SPI MOSI 數據", "direction": "input"},
            {"name": "RS",   "function": "指令/數據選擇（LOW=指令，HIGH=數據）", "direction": "input"},
            {"name": "RST",  "function": "硬體重置（LOW=重置）", "direction": "input"},
            {"name": "CS",   "function": "SPI 片選（LOW=選中）", "direction": "input"}
        ],
        "protocol", "lcd_128x32_st7567a.py",
        datasheet_url=None,
        datasheet_source=None,
        datasheet_filename="ST7567A.pdf"
    )),
    # --- module/rtc ---
    ("module/rtc/ds1307", make_comp(
        "module/rtc/ds1307",
        "ds1307", "实时时钟DS1307", "Maxim Integrated", "DS1307",
        "module/rtc",
        "DS1307 I2C 實時時鐘（RTC），地址 0x68，BCD 格式，含電池備份，精度 ±2ppm",
        ["I2C"], V33_5,
        VCC_GND + [
            {"name": "SDA", "function": "I2C 數據線", "direction": "bidirectional"},
            {"name": "SCL", "function": "I2C 時鐘線", "direction": "input"},
            {"name": "SQW", "function": "方波輸出（可選）", "direction": "output"}
        ],
        "protocol", "ds1307.py",
        datasheet_url="https://www.mouser.com/datasheet/2/256/DS1307-1203167.pdf",
        datasheet_source="mouser",
        datasheet_filename="DS1307.pdf"
    )),
    # --- module/rfid ---
    ("module/rfid/mfrc522", make_comp(
        "module/rfid/mfrc522",
        "mfrc522", "RFID刷卡模块", "NXP Semiconductors", "MFRC522",
        "module/rfid",
        "MFRC522 RFID 讀卡器，SPI 介面，13.56MHz，支援 MIFARE 1K/4K，讀寫 UID 及資料",
        ["SPI"], V33,
        VCC_GND + [
            {"name": "SCK",  "function": "SPI 時鐘", "direction": "input"},
            {"name": "MOSI", "function": "SPI 主機到從機", "direction": "input"},
            {"name": "MISO", "function": "SPI 從機到主機", "direction": "output"},
            {"name": "SDA",  "function": "SPI 片選（CS）", "direction": "input"},
            {"name": "RST",  "function": "硬體重置（LOW=重置）", "direction": "input"}
        ],
        "protocol", "mfrc522.py",
        datasheet_url="https://www.mouser.com/datasheet/2/302/MF1S50YYX_V1-1278395.pdf",
        datasheet_source="mouser",
        datasheet_filename="MFRC522.pdf"
    )),
]

def make_readme(rel, data):
    name = data["name"]
    name_zh = data["name_zh"]
    cat = data["category"]
    desc = data["description"]
    iface = ", ".join(data["interface"])
    v = data["voltage"]
    pins = data["pins"]
    logic = data["logic"]
    driver = data["drivers"]["micropython"]

    pin_rows = "\n".join(f"| {p['name']} | {p['function']} | {p['direction']} |" for p in pins)
    ds = data["datasheet"]
    ds_str = f"[{ds['filename']}]({ds['url']})" if ds.get("url") else "待補充"

    return f"""# {name} — {name_zh}

**類別**：{cat}
**介面**：{iface}
**工作電壓**：{v['min']}–{v['max']} {v['unit']}
**邏輯**：{logic}

## 描述

{desc}

## 接腳定義

| 接腳 | 功能 | 方向 |
|:--|:--|:--|
{pin_rows}

## MicroPython Driver

```python
# driver 路徑：{driver}
```

請將 `{os.path.basename(driver)}` 複製到 Pico，再執行 `example.py`。

## Datasheet

{ds_str}

## 驗證狀態

⏳ pending
"""

# --- write all ---
for rel, data in COMPONENTS:
    cp = comp_path(rel)
    # component.json
    write_json(os.path.join(cp, "component.json"), data)
    # README.md
    write_text(os.path.join(cp, "README.md"), make_readme(rel, data))
    # .gitkeep
    gitkeep(os.path.join(cp, "drivers", "circuitpython", ".gitkeep"))
    gitkeep(os.path.join(cp, "drivers", "arduino", ".gitkeep"))
    gitkeep(os.path.join(cp, "datasheet", ".gitkeep"))

print(f"Written {len(COMPONENTS)} components (component.json + README.md + .gitkeep)")
