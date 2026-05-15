"""批次生成所有元件的 MicroPython driver 和 example.py"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def drv_path(rel, filename):
    return os.path.join(BASE, "components", rel.replace("/", os.sep),
                        "drivers", "micropython", filename)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

# ─────────────────────────────────────────────
# Group 1: Simple GPIO digital input / output
# ─────────────────────────────────────────────

GPIO_SENSORS = [
    # (rel_path, driver_filename, class_name, name_zh, logic, method_name, active_state, description)
    ("sensor/digital/button",       "button.py",       "Button",
     "按键",       "active-low",  "is_pressed",  0, "按下=LOW（4.7K 上拉）"),
    ("sensor/digital/capacitive-touch", "capacitive_touch.py", "CapTouch",
     "電容觸摸",  "active-high", "is_touched",  1, "觸摸=HIGH"),
    ("sensor/digital/obstacle-avoidance", "obstacle_avoidance.py", "ObstacleSensor",
     "避障",       "active-low",  "is_blocked",  0, "有障礙物=LOW"),
    ("sensor/digital/line-following", "line_following.py", "LineSensor",
     "巡線",       "active-low",  "on_black",    1, "黑色/無物=HIGH，白色=LOW"),
    ("sensor/digital/photointerrupter", "photointerrupter.py", "Photointerrupter",
     "光折斷",     "active-high", "is_blocked",  1, "遮擋=HIGH，未遮擋=LOW"),
    ("sensor/digital/tilt",         "tilt.py",         "TiltSensor",
     "傾斜",       "active-low",  "is_tilted",   0, "傾斜=LOW，直立=HIGH"),
    ("sensor/digital/collision",     "collision.py",    "CollisionSensor",
     "碰撞",       "active-low",  "is_hit",      0, "碰觸=LOW，未碰=HIGH"),
    ("sensor/digital/hall",          "hall.py",         "HallSensor",
     "霍爾",       "active-low",  "is_magnet",   0, "偵測到磁場=LOW（A3144）"),
    ("sensor/digital/reed-switch",   "reed_switch.py",  "ReedSwitch",
     "乾簧管",     "active-low",  "is_closed",   0, "有磁場=LOW，無磁場=HIGH"),
    ("sensor/digital/pir",           "pir.py",          "PIRSensor",
     "PIR 人體紅外", "active-high", "is_detected", 1, "偵測到人=HIGH，無人=LOW"),
]

GPIO_DRV_TMPL = '''\
from machine import Pin
import time

class {cls}:
    def __init__(self, pin, pull=Pin.PULL_UP):
        self._pin = Pin(pin, Pin.IN, pull)
        self._last_irq_ms = 0

    def {method}(self):
        return self._pin.value() == {active}

    def on_{method}(self, callback, debounce_ms=50):
        trigger = Pin.IRQ_FALLING if {active} == 0 else Pin.IRQ_RISING
        def _cb(p):
            now = time.ticks_ms()
            if time.ticks_diff(now, self._last_irq_ms) >= debounce_ms:
                self._last_irq_ms = now
                callback(p)
        self._pin.irq(trigger=trigger, handler=_cb)

    def irq_disable(self):
        self._pin.irq(handler=None)
'''

GPIO_EXAMPLE_TMPL = '''\
from {mod} import {cls}
import time

sensor = {cls}(14)   # 信號端 S 接 GPIO14

print("開始偵測 {name_zh}，Ctrl+C 停止...")
while True:
    if sensor.{method}():
        print("{method}: True")
    time.sleep_ms(100)
'''

# Special: line-following has is_black() / is_white()
LINE_FOLLOWING_DRV = '''\
from machine import Pin
import time

class LineSensor:
    """巡線感應器：黑色/無物=HIGH，白色=LOW（LM393 比較器）"""
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.IN)
        self._last_irq_ms = 0

    def is_black(self):
        return self._pin.value() == 1

    def is_white(self):
        return self._pin.value() == 0

    def on_line_change(self, callback, debounce_ms=20):
        def _cb(p):
            now = time.ticks_ms()
            if time.ticks_diff(now, self._last_irq_ms) >= debounce_ms:
                self._last_irq_ms = now
                callback(p)
        self._pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=_cb)
'''

LINE_FOLLOWING_EXAMPLE = '''\
from line_following import LineSensor
import time

sensor = LineSensor(14)   # 信號端 S 接 GPIO14

print("開始巡線偵測，Ctrl+C 停止...")
while True:
    if sensor.is_black():
        print("偵測到黑線")
    elif sensor.is_white():
        print("偵測到白色")
    time.sleep_ms(50)
'''

for (rel, fname, cls, name_zh, logic, method, active, desc) in GPIO_SENSORS:
    mod = fname.replace(".py", "")
    if rel == "sensor/digital/line-following":
        drv_content = LINE_FOLLOWING_DRV
        ex_content = LINE_FOLLOWING_EXAMPLE
    else:
        pull = "Pin.PULL_UP" if active == 0 else "Pin.PULL_DOWN"
        drv_content = GPIO_DRV_TMPL.format(cls=cls, method=method, active=active, pull=pull)
        ex_content = GPIO_EXAMPLE_TMPL.format(mod=mod, cls=cls, method=method, name_zh=name_zh)
    write(drv_path(rel, fname), drv_content)
    write(drv_path(rel, "example.py"), ex_content)

print("Group 1 (GPIO digital) done")

# ─────────────────────────────────────────────
# Group 2: Simple ADC analog sensors
# ─────────────────────────────────────────────

ANALOG_SENSORS = [
    ("sensor/analog/potentiometer", "potentiometer.py", "Potentiometer", "旋轉電位器",
     "讀取值越大代表旋轉角度越大"),
    ("sensor/analog/water-steam",   "water_steam.py",   "WaterSensor",  "水滴/水蒸氣感應器",
     "讀取值越大代表水量越多或濕度越高"),
    ("sensor/analog/sound",         "sound.py",         "SoundSensor",  "聲音感應器",
     "讀取值越大代表聲音越響"),
    ("sensor/analog/photoresistor", "photoresistor.py", "PhotoresistorSensor", "光敏電阻感應器",
     "讀取值越大代表光線越強"),
    ("sensor/analog/pressure-film", "pressure_film.py", "PressureSensor", "薄膜壓力感應器",
     "讀取值越小代表壓力越大"),
    ("sensor/analog/uv",            "uv.py",            "UVSensor",     "紫外線感應器",
     "讀取值越大代表紫外線越強"),
]

ANALOG_DRV_TMPL = '''\
from machine import ADC, Pin

class {cls}:
    _VREF = 3.3

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def read_raw(self):
        return self._adc.read_u16()

    def read_voltage(self):
        return self.read_raw() / 65535 * self._VREF

    def read_percent(self):
        return self.read_raw() / 65535 * 100
'''

ANALOG_EXAMPLE_TMPL = '''\
from {mod} import {cls}
import time

sensor = {cls}(26)   # 信號端 S 接 ADC GPIO26

print("開始讀取 {name_zh}，Ctrl+C 停止...")
print("提示：{hint}")
while True:
    raw = sensor.read_raw()
    voltage = sensor.read_voltage()
    percent = sensor.read_percent()
    print(f"raw={{raw:5d}}  voltage={{voltage:.3f}}V  {{percent:.1f}}%")
    time.sleep_ms(200)
'''

for (rel, fname, cls, name_zh, hint) in ANALOG_SENSORS:
    mod = fname.replace(".py", "")
    write(drv_path(rel, fname), ANALOG_DRV_TMPL.format(cls=cls))
    write(drv_path(rel, "example.py"),
          ANALOG_EXAMPLE_TMPL.format(mod=mod, cls=cls, name_zh=name_zh, hint=hint))

print("Group 2 (ADC analog) done")

# ─────────────────────────────────────────────
# Group 3: NTC temperature (Steinhart-Hart)
# ─────────────────────────────────────────────

NTC_DRV = '''\
from machine import ADC, Pin
import math

class NTCTemperature:
    # NTC-MF52AT: 10kΩ @ 25°C, B=3950, 串聯 10kΩ 上拉電阻
    _B = 3950
    _R0 = 10000
    _T0 = 298.15   # 25°C in Kelvin
    _R_SERIES = 10000
    _VREF = 3.3

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def _read_r_ntc(self):
        raw = self._adc.read_u16()
        if raw == 0:
            return float("inf")
        # 分壓：Vout = VCC * R_NTC / (R_NTC + R_series) → R_NTC = R_series * raw / (65535 - raw)
        return self._R_SERIES * raw / (65535 - raw)

    def read_celsius(self):
        r = self._read_r_ntc()
        if r == float("inf") or r <= 0:
            return None
        t_k = 1 / (1 / self._T0 + math.log(r / self._R0) / self._B)
        return t_k - 273.15

    def read_fahrenheit(self):
        c = self.read_celsius()
        return None if c is None else c * 9 / 5 + 32
'''

NTC_EXAMPLE = '''\
from ntc_temperature import NTCTemperature
import time

sensor = NTCTemperature(26)   # 信號端 S 接 ADC GPIO26

print("開始讀取 NTC 類比溫度，Ctrl+C 停止...")
while True:
    c = sensor.read_celsius()
    f = sensor.read_fahrenheit()
    if c is not None:
        print(f"溫度：{c:.2f}°C  /  {f:.2f}°F")
    else:
        print("讀取失敗")
    time.sleep(1)
'''

write(drv_path("sensor/analog/ntc-temperature", "ntc_temperature.py"), NTC_DRV)
write(drv_path("sensor/analog/ntc-temperature", "example.py"), NTC_EXAMPLE)
print("Group 3 (NTC temperature) done")

# ─────────────────────────────────────────────
# Group 4: Dual ADC + GPIO sensors
# ─────────────────────────────────────────────

DUAL_SENSORS = [
    ("sensor/dual/flame",      "flame.py",      "FlameSensor",  "火焰感應器",
     "is_flame_detected", "A0 類比值越小表示火焰越強（IR 越強）"),
    ("sensor/dual/mq2-smoke",  "mq2_smoke.py",  "MQ2Smoke",     "MQ-2 煙霧感應器",
     "is_alarm",          "A0 類比值越大表示煙霧濃度越高"),
    ("sensor/dual/mq3-alcohol","mq3_alcohol.py","MQ3Alcohol",   "MQ-3 酒精感應器",
     "is_alarm",          "A0 類比值越大表示酒精濃度越高"),
]

DUAL_DRV_TMPL = '''\
from machine import ADC, Pin

class {cls}:
    _VREF = 3.3

    def __init__(self, a0_pin, d0_pin):
        self._adc = ADC(Pin(a0_pin))
        self._d0  = Pin(d0_pin, Pin.IN)

    def read_analog(self):
        return self._adc.read_u16()

    def read_voltage(self):
        return self.read_analog() / 65535 * self._VREF

    def {method}(self):
        return self._d0.value() == 0   # active-low
'''

DUAL_EXAMPLE_TMPL = '''\
from {mod} import {cls}
import time

sensor = {cls}(a0_pin=26, d0_pin=14)   # A0 接 GPIO26（ADC），D0 接 GPIO14

print("開始讀取 {name_zh}，Ctrl+C 停止...")
print("提示：{hint}")
while True:
    raw = sensor.read_analog()
    voltage = sensor.read_voltage()
    alarm = sensor.{method}()
    print(f"raw={{raw:5d}}  {{voltage:.3f}}V  alarm={{alarm}}")
    time.sleep_ms(200)
'''

for (rel, fname, cls, name_zh, method, hint) in DUAL_SENSORS:
    mod = fname.replace(".py", "")
    write(drv_path(rel, fname), DUAL_DRV_TMPL.format(cls=cls, method=method))
    write(drv_path(rel, "example.py"),
          DUAL_EXAMPLE_TMPL.format(mod=mod, cls=cls, name_zh=name_zh,
                                   method=method, hint=hint))

print("Group 4 (dual ADC+GPIO) done")

# ─────────────────────────────────────────────
# Group 5: Protocol sensors
# ─────────────────────────────────────────────

DS18B20_DRV = '''\
import onewire, ds18x20
from machine import Pin
import time

class DS18B20:
    def __init__(self, pin):
        ow = onewire.OneWire(Pin(pin))
        self._ds = ds18x20.DS18X20(ow)
        self._roms = self._ds.scan()
        if not self._roms:
            raise RuntimeError("找不到 DS18B20，請確認接線和上拉電阻")

    def read_celsius(self, index=0):
        self._ds.convert_temp()
        time.sleep_ms(750)
        return self._ds.read_temp(self._roms[index])

    def read_fahrenheit(self, index=0):
        return self.read_celsius(index) * 9 / 5 + 32

    @property
    def device_count(self):
        return len(self._roms)
'''

DS18B20_EXAMPLE = '''\
from ds18b20 import DS18B20
import time

# DQ 接 GPIO14，DQ 和 VCC 之間接 4.7K 上拉電阻
sensor = DS18B20(14)
print(f"發現 {sensor.device_count} 個 DS18B20")

while True:
    c = sensor.read_celsius()
    f = sensor.read_fahrenheit()
    print(f"溫度：{c:.2f}°C  /  {f:.2f}°F")
    time.sleep(1)
'''

XHT11_DRV = '''\
import dht
from machine import Pin

class XHT11:
    """XHT11 溫濕度感應器（DHT11 相容）"""
    def __init__(self, pin):
        self._dht = dht.DHT11(Pin(pin))

    def read(self):
        """回傳 (temperature_celsius, humidity_percent)"""
        self._dht.measure()
        return self._dht.temperature(), self._dht.humidity()

    def read_temperature(self):
        self._dht.measure()
        return self._dht.temperature()

    def read_humidity(self):
        self._dht.measure()
        return self._dht.humidity()
'''

XHT11_EXAMPLE = '''\
from xht11 import XHT11
import time

sensor = XHT11(14)   # 信號端 S 接 GPIO14

print("開始讀取 XHT11 溫濕度，Ctrl+C 停止...")
while True:
    temp, humi = sensor.read()
    print(f"溫度：{temp}°C  濕度：{humi}%RH")
    time.sleep(2)
'''

HCSR04_DRV = '''\
from machine import Pin, time_pulse_us
import time

class HCSR04:
    """HC-SR04 超聲波測距，量程 2-400cm"""
    _TIMEOUT_US = 30000   # 500ms 超時 → 無回波

    def __init__(self, trig_pin, echo_pin):
        self._trig = Pin(trig_pin, Pin.OUT)
        self._echo = Pin(echo_pin, Pin.IN)
        self._trig.low()

    def distance_cm(self):
        self._trig.low()
        time.sleep_us(2)
        self._trig.high()
        time.sleep_us(10)
        self._trig.low()
        duration = time_pulse_us(self._echo, 1, self._TIMEOUT_US)
        if duration < 0:
            return None   # 超時或無回波
        return duration / 58.0

    def distance_mm(self):
        d = self.distance_cm()
        return None if d is None else d * 10
'''

HCSR04_EXAMPLE = '''\
from hc_sr04 import HCSR04
import time

# TRIG 接 GPIO14，ECHO 接 GPIO15
# 注意：HC-SR04 使用 5V 供電，ECHO 輸出為 5V，需分壓後接 Pico GPIO
sensor = HCSR04(trig_pin=14, echo_pin=15)

print("開始超聲波測距，Ctrl+C 停止...")
while True:
    d = sensor.distance_cm()
    if d is not None:
        print(f"距離：{d:.1f} cm")
    else:
        print("超出測距範圍（>400cm）或無回波")
    time.sleep_ms(200)
'''

ROTARY_DRV = '''\
from machine import Pin
import time

class RotaryEncoder:
    """增量式旋轉編碼器，20 脈衝/轉"""
    def __init__(self, clk_pin, dt_pin, sw_pin=None):
        self._clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self._dt  = Pin(dt_pin,  Pin.IN, Pin.PULL_UP)
        self._sw  = Pin(sw_pin,  Pin.IN, Pin.PULL_UP) if sw_pin is not None else None
        self._count = 0
        self._last_irq_ms = 0
        self._clk.irq(trigger=Pin.IRQ_FALLING, handler=self._on_clk)

    def _on_clk(self, pin):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_irq_ms) < 5:
            return
        self._last_irq_ms = now
        if self._dt.value() == 1:
            self._count += 1    # CLK↓ 時 DT=HIGH → 順時針
        else:
            self._count -= 1    # CLK↓ 時 DT=LOW  → 逆時針

    @property
    def value(self):
        return self._count

    @value.setter
    def value(self, v):
        self._count = v

    def reset(self):
        self._count = 0

    def is_pressed(self):
        return self._sw.value() == 0 if self._sw else False
'''

ROTARY_EXAMPLE = '''\
from rotary_encoder import RotaryEncoder
import time

# CLK 接 GPIO14，DT 接 GPIO15，SW 接 GPIO16（可選）
enc = RotaryEncoder(clk_pin=14, dt_pin=15, sw_pin=16)

print("旋轉編碼器測試，Ctrl+C 停止...")
last = None
while True:
    val = enc.value
    if val != last:
        print(f"計數：{val}")
        last = val
    if enc.is_pressed():
        enc.reset()
        print("按下按鈕，計數重置為 0")
        time.sleep_ms(300)
    time.sleep_ms(10)
'''

IR_DRV = '''\
from machine import Pin, time_pulse_us
import time

class IRReceiver:
    """NEC 協議 IR 接收，38kHz 載波"""
    _LEADER_LOW  = 4500   # Leader code low: 4.5ms
    _LEADER_HIGH = 9000   # Leader code high: 9ms
    _ONE_PULSE   = 1125   # bit "1": 562.5μs high + 562.5μs low = 1125μs total high-low
    _TOLERANCE   = 300

    def __init__(self, pin):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def receive(self, timeout_ms=100):
        """等待並解碼一個 NEC 32-bit 碼，返回 int 或 None（超時）"""
        # 等待 leader: 9ms HIGH，確認為 NEC
        duration = time_pulse_us(self._pin, 0, timeout_ms * 1000)
        if duration < self._LEADER_HIGH - self._TOLERANCE:
            return None
        # 等 4.5ms LOW space
        time_pulse_us(self._pin, 1, 5000)
        # 讀 32 bits
        bits = 0
        for i in range(32):
            # 每個 bit 從 LOW→HIGH 開始
            w = time_pulse_us(self._pin, 1, 2000)
            if w < 0:
                return None
            bits |= (1 if w > self._ONE_PULSE else 0) << i
        return bits
'''

IR_EXAMPLE = '''\
from ir_receiver import IRReceiver
import time

# 信號端 S 接 GPIO14，S 端已有 4.7K 上拉電阻
ir = IRReceiver(14)

print("等待 IR 遙控器信號，Ctrl+C 停止...")
while True:
    code = ir.receive(timeout_ms=100)
    if code is not None:
        print(f"收到：0x{code:08X}")
    time.sleep_ms(10)
'''

write(drv_path("sensor/1wire/ds18b20",    "ds18b20.py"),      DS18B20_DRV)
write(drv_path("sensor/1wire/ds18b20",    "example.py"),      DS18B20_EXAMPLE)
write(drv_path("sensor/humidity/xht11",   "xht11.py"),        XHT11_DRV)
write(drv_path("sensor/humidity/xht11",   "example.py"),      XHT11_EXAMPLE)
write(drv_path("sensor/ultrasonic/hc-sr04", "hc_sr04.py"),   HCSR04_DRV)
write(drv_path("sensor/ultrasonic/hc-sr04", "example.py"),   HCSR04_EXAMPLE)
write(drv_path("input/rotary-encoder",    "rotary_encoder.py"), ROTARY_DRV)
write(drv_path("input/rotary-encoder",    "example.py"),      ROTARY_EXAMPLE)
write(drv_path("input/ir-receiver",       "ir_receiver.py"),  IR_DRV)
write(drv_path("input/ir-receiver",       "example.py"),      IR_EXAMPLE)
print("Group 5 (protocol sensors) done")

# ─────────────────────────────────────────────
# Group 6: Actuators
# ─────────────────────────────────────────────

BUZZER_DRV = '''\
from machine import Pin
import time

class ActiveBuzzer:
    """有源蜂鳴器，S=HIGH 蜂鳴（active-high）"""
    def __init__(self, pin):
        self._pin = Pin(pin, Pin.OUT)
        self._pin.low()

    def on(self):
        self._pin.high()

    def off(self):
        self._pin.low()

    def beep(self, duration_ms=100):
        self.on()
        time.sleep_ms(duration_ms)
        self.off()

    def beep_n(self, n, on_ms=100, off_ms=100):
        for _ in range(n):
            self.beep(on_ms)
            time.sleep_ms(off_ms)
'''

BUZZER_EXAMPLE = '''\
from buzzer_active import ActiveBuzzer
import time

buzzer = ActiveBuzzer(14)   # 信號端 S 接 GPIO14

print("蜂鳴器測試...")
buzzer.beep(200)
time.sleep(1)
buzzer.beep_n(3, on_ms=100, off_ms=100)
print("完成")
'''

SPEAKER_DRV = '''\
from machine import Pin, PWM
import time

class Speaker8002B:
    """8002B 功放喇叭，PWM 輸出音調，放大倍數約 8.5 倍"""
    def __init__(self, pin):
        self._pwm = PWM(Pin(pin))
        self._pwm.duty_u16(0)

    def tone(self, freq_hz, duration_ms=500):
        self._pwm.freq(freq_hz)
        self._pwm.duty_u16(32768)   # 50% duty
        time.sleep_ms(duration_ms)
        self.stop()

    def play_melody(self, notes):
        """notes: [(freq_hz, duration_ms), ...]，freq=0 代表休止符"""
        for freq, duration in notes:
            if freq == 0:
                self.stop()
                time.sleep_ms(duration)
            else:
                self.tone(freq, duration)
            time.sleep_ms(20)

    def stop(self):
        self._pwm.duty_u16(0)

    def deinit(self):
        self._pwm.deinit()
'''

SPEAKER_EXAMPLE = '''\
from speaker_8002b import Speaker8002B
import time

speaker = Speaker8002B(14)   # IN 接 GPIO14

# 簡單旋律：Do Re Mi
MELODY = [
    (262, 300), (294, 300), (330, 300), (349, 300),
    (392, 300), (440, 300), (494, 300), (523, 500),
    (0,   200),
]

print("播放旋律...")
speaker.play_melody(MELODY)
print("完成")
speaker.deinit()
'''

MOTOR_DRV = '''\
from machine import Pin

class Motor130:
    """130 DC 馬達 + HR1124S H 橋驅動"""
    def __init__(self, in_plus_pin, in_minus_pin):
        self._in_p = Pin(in_plus_pin,  Pin.OUT)
        self._in_m = Pin(in_minus_pin, Pin.OUT)
        self.stop()

    def forward(self):
        self._in_p.high()
        self._in_m.low()

    def reverse(self):
        self._in_p.low()
        self._in_m.high()

    def stop(self):
        self._in_p.low()
        self._in_m.low()

    def brake(self):
        self._in_p.high()
        self._in_m.high()
'''

MOTOR_EXAMPLE = '''\
from motor_130 import Motor130
import time

# IN+ 接 GPIO14，IN- 接 GPIO15
motor = Motor130(in_plus_pin=14, in_minus_pin=15)

print("馬達正轉 2 秒...")
motor.forward()
time.sleep(2)

print("停止 1 秒...")
motor.stop()
time.sleep(1)

print("馬達反轉 2 秒...")
motor.reverse()
time.sleep(2)

motor.stop()
print("完成")
'''

SERVO_DRV = '''\
from machine import Pin, PWM

class Servo:
    """伺服舵機薄包裝，PWM 50Hz，脈寬 0.5ms-2.5ms 對應 0°-180°"""
    _FREQ = 50
    _MIN_US = 500
    _MAX_US = 2500

    def __init__(self, pin):
        self._pwm = PWM(Pin(pin), freq=self._FREQ)
        self.angle(90)

    def _us_to_duty(self, us):
        period_us = 1_000_000 // self._FREQ
        return int(us / period_us * 65535)

    def angle(self, deg):
        deg = max(0, min(180, deg))
        us = self._MIN_US + (self._MAX_US - self._MIN_US) * deg / 180
        self._pwm.duty_u16(self._us_to_duty(int(us)))

    def min(self):
        self.angle(0)

    def max(self):
        self.angle(180)

    def center(self):
        self.angle(90)

    def deinit(self):
        self._pwm.deinit()
'''

SERVO_EXAMPLE = '''\
from servo import Servo
import time

servo = Servo(14)   # PWM 信號端接 GPIO14

print("舵機測試：0° → 90° → 180° → 90°")
servo.min()
time.sleep(1)
servo.center()
time.sleep(1)
servo.max()
time.sleep(1)
servo.center()
time.sleep(1)

print("掃描 0°-180°...")
for deg in range(0, 181, 10):
    servo.angle(deg)
    time.sleep_ms(100)
for deg in range(180, -1, -10):
    servo.angle(deg)
    time.sleep_ms(100)

servo.deinit()
print("完成")
'''

write(drv_path("actuator/buzzer-active",  "buzzer_active.py"), BUZZER_DRV)
write(drv_path("actuator/buzzer-active",  "example.py"),       BUZZER_EXAMPLE)
write(drv_path("actuator/speaker-8002b",  "speaker_8002b.py"), SPEAKER_DRV)
write(drv_path("actuator/speaker-8002b",  "example.py"),       SPEAKER_EXAMPLE)
write(drv_path("actuator/motor-130",      "motor_130.py"),     MOTOR_DRV)
write(drv_path("actuator/motor-130",      "example.py"),       MOTOR_EXAMPLE)
write(drv_path("actuator/servo",          "servo.py"),         SERVO_DRV)
write(drv_path("actuator/servo",          "example.py"),       SERVO_EXAMPLE)
print("Group 6 (actuators) done")

# ─────────────────────────────────────────────
# Group 7: Displays & Input
# ─────────────────────────────────────────────

ADC5WAY_DRV = '''\
from machine import ADC, Pin

class ADCButton5Way:
    """五路 AD 按鍵，電阻分壓，16-bit ADC 區分各鍵（3.3V 系統）"""
    _RANGES = [
        (60000, 65535, 1),
        (45000, 59999, 2),
        (32000, 44999, 3),
        (19000, 31999, 4),
        (6000,  18999, 5),
    ]

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def read(self):
        """回傳按下的鍵號 1-5，無按鍵回傳 None"""
        val = self._adc.read_u16()
        for lo, hi, key in self._ranges:
            if lo <= val <= hi:
                return key
        return None

    @property
    def _ranges(self):
        return self._RANGES

    def read_raw(self):
        return self._adc.read_u16()
'''

ADC5WAY_EXAMPLE = '''\
from adc_button_5way import ADCButton5Way
import time

btn = ADCButton5Way(26)   # 信號端 S 接 ADC GPIO26

print("五路按鍵測試，Ctrl+C 停止...")
last = None
while True:
    key = btn.read()
    if key != last:
        if key:
            print(f"按下 SW{key}  (raw={btn.read_raw()})")
        else:
            print("無按鍵")
        last = key
    time.sleep_ms(50)
'''

JOYSTICK_DRV = '''\
from machine import ADC, Pin

class Joystick:
    """搖桿模組，X/Y 類比，Z（按鈕）active-high（按下=HIGH）"""
    def __init__(self, x_pin, y_pin, btn_pin=None):
        self._x = ADC(Pin(x_pin))
        self._y = ADC(Pin(y_pin))
        self._btn = Pin(btn_pin, Pin.IN, Pin.PULL_DOWN) if btn_pin is not None else None

    def read_x(self):
        return self._x.read_u16()

    def read_y(self):
        return self._y.read_u16()

    def read_xy(self):
        return self._x.read_u16(), self._y.read_u16()

    def is_pressed(self):
        return self._btn.value() == 1 if self._btn else False
'''

JOYSTICK_EXAMPLE = '''\
from joystick import Joystick
import time

# X 接 GPIO26，Y 接 GPIO27，B（Z軸按鈕）接 GPIO14
js = Joystick(x_pin=26, y_pin=27, btn_pin=14)

print("搖桿測試，Ctrl+C 停止...")
while True:
    x, y = js.read_xy()
    pressed = js.is_pressed()
    print(f"X={x:5d}  Y={y:5d}  按鈕={'按下' if pressed else '未按'}")
    time.sleep_ms(100)
'''

RGB3_DRV = '''\
from machine import Pin

class RGB3LED:
    """三色 LED 模組（紅/黃/綠），各腳高電平亮起（active-high）"""
    def __init__(self, r_pin, y_pin, g_pin):
        self._r = Pin(r_pin, Pin.OUT)
        self._y = Pin(y_pin, Pin.OUT)
        self._g = Pin(g_pin, Pin.OUT)
        self.off()

    def red(self):
        self.set(1, 0, 0)

    def yellow(self):
        self.set(0, 1, 0)

    def green(self):
        self.set(0, 0, 1)

    def off(self):
        self.set(0, 0, 0)

    def set(self, r, y, g):
        self._r.value(r)
        self._y.value(y)
        self._g.value(g)
'''

RGB3_EXAMPLE = '''\
from rgb_3color import RGB3LED
import time

# R 接 GPIO12，Y 接 GPIO13，G 接 GPIO14
led = RGB3LED(r_pin=12, y_pin=13, g_pin=14)

print("三色 LED 測試...")
for color, fn in [("紅", led.red), ("黃", led.yellow), ("綠", led.green)]:
    print(f"  {color}色")
    fn()
    time.sleep(1)

led.off()
print("完成")
'''

RGBPLUGIN_DRV = '''\
from machine import Pin

class PluginRGB:
    """直插式 RGB LED（共陰），高電平亮起"""
    def __init__(self, r_pin, g_pin, b_pin):
        self._r = Pin(r_pin, Pin.OUT)
        self._g = Pin(g_pin, Pin.OUT)
        self._b = Pin(b_pin, Pin.OUT)
        self.off()

    def set_color(self, r, g, b):
        self._r.value(1 if r else 0)
        self._g.value(1 if g else 0)
        self._b.value(1 if b else 0)

    def off(self):
        self.set_color(0, 0, 0)
'''

RGBPLUGIN_EXAMPLE = '''\
from rgb_plugin import PluginRGB
import time

# R 接 GPIO12，G 接 GPIO13，B 接 GPIO14
led = PluginRGB(r_pin=12, g_pin=13, b_pin=14)

colors = [
    ("紅", 1, 0, 0),
    ("綠", 0, 1, 0),
    ("藍", 0, 0, 1),
    ("白", 1, 1, 1),
    ("關", 0, 0, 0),
]
for name, r, g, b in colors:
    print(f"  {name}")
    led.set_color(r, g, b)
    time.sleep(1)
'''

SK6812_DRV = '''\
import array, time
from machine import Pin
import rp2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def _sk6812_pio():
    # SK6812：0碼 300ns HIGH + 900ns LOW；1碼 600ns HIGH + 600ns LOW（@125MHz）
    T1 = 3   # 300ns
    T2 = 3   # 300ns
    T3 = 9   # 900ns
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)   [T3-1]
    jmp(not_x, "do_zero")   .side(1)   [T1-1]
    jmp("bitloop")           .side(1)   [T2-1]
    label("do_zero")
    nop()                    .side(0)   [T2-1]
    wrap()

class SK6812:
    def __init__(self, pin, n):
        self._n = n
        self._buf = array.array("I", [0] * n)
        self._sm = rp2.StateMachine(0, _sk6812_pio, freq=8_000_000, sideset_base=Pin(pin))
        self._sm.active(1)

    def set_pixel(self, index, r, g, b):
        self._buf[index] = (g << 16) | (r << 8) | b   # GRB order

    def fill(self, r, g, b):
        for i in range(self._n):
            self.set_pixel(i, r, g, b)

    def show(self):
        for val in self._buf:
            self._sm.put(val, 8)
        time.sleep_us(100)   # reset pulse

    def brightness(self, level):
        """level: 0.0-1.0，縮放所有像素亮度"""
        self._buf = array.array("I", [
            (int(((v >> 16) & 0xFF) * level) << 16) |
            (int(((v >>  8) & 0xFF) * level) <<  8) |
            (int( (v        & 0xFF) * level))
            for v in self._buf
        ])
'''

SK6812_EXAMPLE = '''\
from sk6812 import SK6812
import time

# DIN 接 GPIO14，共 4 顆 SK6812
leds = SK6812(pin=14, n=4)

print("SK6812 測試...")
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,0,0)]
for r, g, b in colors:
    leds.fill(r, g, b)
    leds.show()
    time.sleep_ms(500)

print("彩虹跑馬燈...")
rainbow = [(255,0,0),(255,128,0),(255,255,0),(0,255,0),(0,0,255),(128,0,255)]
for i in range(24):
    for j in range(4):
        r, g, b = rainbow[(i + j) % len(rainbow)]
        leds.set_pixel(j, r, g, b)
    leds.show()
    time.sleep_ms(100)

leds.fill(0,0,0)
leds.show()
print("完成")
'''

TM1650_DRV = '''\
from machine import I2C, Pin
import time

class TM1650:
    """TM1650 四位七段數碼管，I2C-like 協議"""
    _CTRL_BASE = 0x24   # 控制地址：0x24-0x27（4位）
    _DATA_BASE = 0x34   # 顯示地址：0x34-0x37（4位）
    _DIGITS = {
        "0":0x3F,"1":0x06,"2":0x5B,"3":0x4F,"4":0x66,
        "5":0x6D,"6":0x7D,"7":0x07,"8":0x7F,"9":0x6F,
        "-":0x40," ":0x00,"A":0x77,"b":0x7C,"C":0x39,
        "d":0x5E,"E":0x79,"F":0x71,"H":0x76,"L":0x38,
        "P":0x73,"r":0x50,"U":0x3E,
    }

    def __init__(self, sda=4, scl=5, brightness=2):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=100_000)
        self._brightness = brightness
        self._setup()

    def _setup(self):
        for i in range(4):
            self._i2c.writeto(self._CTRL_BASE + i, bytes([0x01 | (self._brightness << 4)]))

    def clear(self):
        for i in range(4):
            self._i2c.writeto(self._DATA_BASE + i, bytes([0x00]))

    def show_raw(self, segments):
        """segments: list of 4 segment bytes"""
        for i, seg in enumerate(segments[:4]):
            self._i2c.writeto(self._DATA_BASE + i, bytes([seg]))

    def show(self, text):
        """text: 最多 4 個字元的字串"""
        text = str(text).ljust(4)[:4]
        segs = [self._DIGITS.get(c, 0x00) for c in text]
        self.show_raw(segs)

    def show_number(self, n):
        self.show(f"{n:4d}")

    def brightness(self, level):
        """level: 0-7"""
        self._brightness = max(0, min(7, level))
        self._setup()
'''

TM1650_EXAMPLE = '''\
from tm1650 import TM1650
import time

# SDA 接 GPIO4，SCL 接 GPIO5
display = TM1650(sda=4, scl=5)

print("TM1650 四位數碼管測試...")
for i in range(100):
    display.show_number(i)
    time.sleep_ms(100)

display.show("HELLO"[:4])
time.sleep(2)
display.clear()
print("完成")
'''

HT16K33_DRV = '''\
from machine import I2C, Pin
import time

class HT16K33Matrix:
    """HT16K33 8×8 LED 點陣，I2C 地址 0x70"""
    _ADDR = 0x70

    def __init__(self, sda=4, scl=5, addr=0x70):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=400_000)
        self._addr = addr
        self._buf = bytearray(16)   # 8 rows × 2 bytes (16-bit row data)
        self._init()

    def _write_cmd(self, cmd):
        self._i2c.writeto(self._addr, bytes([cmd]))

    def _init(self):
        self._write_cmd(0x21)    # oscillator on
        self._write_cmd(0x81)    # display on, no blink
        self.brightness(8)
        self.clear()

    def brightness(self, level):
        """level: 0-15"""
        self._write_cmd(0xE0 | (level & 0x0F))

    def set_pixel(self, x, y, val):
        """x: 0-7（列），y: 0-7（行）"""
        if val:
            self._buf[y * 2] |= (1 << x)
        else:
            self._buf[y * 2] &= ~(1 << x)

    def fill(self, val):
        b = 0xFF if val else 0x00
        for i in range(0, 16, 2):
            self._buf[i] = b
            self._buf[i+1] = 0

    def clear(self):
        self.fill(0)
        self.show()

    def show(self):
        data = bytearray([0x00]) + self._buf
        self._i2c.writeto(self._addr, data)
'''

HT16K33_EXAMPLE = '''\
from ht16k33_8x8 import HT16K33Matrix
import time

# SDA 接 GPIO4，SCL 接 GPIO5，I2C 地址 0x70
matrix = HT16K33Matrix(sda=4, scl=5)

print("HT16K33 8×8 點陣測試...")
# 顯示笑臉
SMILEY = [
    0b00111100,
    0b01000010,
    0b10100101,
    0b10000001,
    0b10100101,
    0b10011001,
    0b01000010,
    0b00111100,
]
for y, row in enumerate(SMILEY):
    for x in range(8):
        matrix.set_pixel(x, y, (row >> (7-x)) & 1)
matrix.show()
time.sleep(3)
matrix.clear()
print("完成")
'''

LCD_DRV = '''\
from machine import SPI, Pin
import time

class LCD128x32:
    """ST7567A 128×32 像素 LCD，SPI 介面，頁式定址"""
    WIDTH  = 128
    HEIGHT = 32
    PAGES  = HEIGHT // 8   # 4 pages

    def __init__(self, sck=2, sda=3, rs=4, rst=5, cs=6):
        self._spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(sda), miso=None)
        self._rs  = Pin(rs,  Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._cs  = Pin(cs,  Pin.OUT)
        self._buf = bytearray(self.WIDTH * self.PAGES)
        self._init()

    def _cmd(self, b):
        self._rs.low()
        self._cs.low()
        self._spi.write(bytes([b]))
        self._cs.high()

    def _data(self, buf):
        self._rs.high()
        self._cs.low()
        self._spi.write(buf)
        self._cs.high()

    def _init(self):
        self._rst.low()
        time.sleep_ms(10)
        self._rst.high()
        time.sleep_ms(10)
        for cmd in [0xE2, 0xA3, 0xA0, 0xC8, 0x44, 0xAB, 0xF8, 0x00,
                    0x27, 0x81, 0x18, 0xAC, 0x00, 0xAF]:
            self._cmd(cmd)

    def clear(self):
        for i in range(len(self._buf)):
            self._buf[i] = 0

    def pixel(self, x, y, val):
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            page = y // 8
            bit  = y % 8
            idx  = page * self.WIDTH + x
            if val:
                self._buf[idx] |= (1 << bit)
            else:
                self._buf[idx] &= ~(1 << bit)

    def show(self):
        for page in range(self.PAGES):
            self._cmd(0xB0 | page)
            self._cmd(0x10)
            self._cmd(0x00)
            self._data(self._buf[page*self.WIDTH:(page+1)*self.WIDTH])
'''

LCD_EXAMPLE = '''\
from lcd_128x32_st7567a import LCD128x32
import time

# SCK=GPIO2, SDA=GPIO3, RS=GPIO4, RST=GPIO5, CS=GPIO6
lcd = LCD128x32(sck=2, sda=3, rs=4, rst=5, cs=6)

print("LCD 128×32 測試...")
# 畫邊框
for x in range(128):
    lcd.pixel(x, 0, 1)
    lcd.pixel(x, 31, 1)
for y in range(32):
    lcd.pixel(0, y, 1)
    lcd.pixel(127, y, 1)
lcd.show()
time.sleep(3)
lcd.clear()
lcd.show()
print("完成")
'''

write(drv_path("input/adc-button-5way", "adc_button_5way.py"), ADC5WAY_DRV)
write(drv_path("input/adc-button-5way", "example.py"),         ADC5WAY_EXAMPLE)
write(drv_path("input/joystick",        "joystick.py"),         JOYSTICK_DRV)
write(drv_path("input/joystick",        "example.py"),          JOYSTICK_EXAMPLE)
write(drv_path("display/led/rgb-3color", "rgb_3color.py"),      RGB3_DRV)
write(drv_path("display/led/rgb-3color", "example.py"),         RGB3_EXAMPLE)
write(drv_path("display/led/rgb-plugin", "rgb_plugin.py"),      RGBPLUGIN_DRV)
write(drv_path("display/led/rgb-plugin", "example.py"),         RGBPLUGIN_EXAMPLE)
write(drv_path("display/led/sk6812",     "sk6812.py"),           SK6812_DRV)
write(drv_path("display/led/sk6812",     "example.py"),          SK6812_EXAMPLE)
write(drv_path("display/7seg/tm1650",    "tm1650.py"),           TM1650_DRV)
write(drv_path("display/7seg/tm1650",    "example.py"),          TM1650_EXAMPLE)
write(drv_path("display/matrix/ht16k33-8x8", "ht16k33_8x8.py"), HT16K33_DRV)
write(drv_path("display/matrix/ht16k33-8x8", "example.py"),     HT16K33_EXAMPLE)
write(drv_path("display/lcd/lcd-128x32-st7567a", "lcd_128x32_st7567a.py"), LCD_DRV)
write(drv_path("display/lcd/lcd-128x32-st7567a", "example.py"),             LCD_EXAMPLE)
print("Group 7 (displays & input) done")

# ─────────────────────────────────────────────
# Group 8: I2C/SPI modules
# ─────────────────────────────────────────────

DS1307_DRV = '''\
from machine import I2C, Pin
import time

class DS1307:
    """DS1307 I2C 實時時鐘，地址 0x68，BCD 格式"""
    _ADDR = 0x68

    def __init__(self, sda=4, scl=5):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=100_000)

    @staticmethod
    def _bcd2dec(b): return (b >> 4) * 10 + (b & 0x0F)
    @staticmethod
    def _dec2bcd(d): return ((d // 10) << 4) | (d % 10)

    def is_running(self):
        return not bool(self._i2c.readfrom_mem(self._ADDR, 0x00, 1)[0] & 0x80)

    def get_datetime(self):
        d = self._i2c.readfrom_mem(self._ADDR, 0x00, 7)
        return {
            "second": self._bcd2dec(d[0] & 0x7F),
            "minute": self._bcd2dec(d[1]),
            "hour":   self._bcd2dec(d[2] & 0x3F),
            "day":    self._bcd2dec(d[3]),
            "date":   self._bcd2dec(d[4]),
            "month":  self._bcd2dec(d[5]),
            "year":   self._bcd2dec(d[6]) + 2000,
        }

    def set_datetime(self, year, month, date, hour, minute, second, day=1):
        self._i2c.writeto_mem(self._ADDR, 0x00, bytes([
            self._dec2bcd(second),
            self._dec2bcd(minute),
            self._dec2bcd(hour),
            self._dec2bcd(day),
            self._dec2bcd(date),
            self._dec2bcd(month),
            self._dec2bcd(year - 2000),
        ]))
'''

DS1307_EXAMPLE = '''\
from ds1307 import DS1307
import time

# SDA 接 GPIO4，SCL 接 GPIO5
rtc = DS1307(sda=4, scl=5)

# 首次使用請先設定時間（之後可以注解掉）
# rtc.set_datetime(year=2026, month=5, date=14, hour=12, minute=0, second=0)

print(f"時鐘運行中：{rtc.is_running()}")
while True:
    dt = rtc.get_datetime()
    print(f"{dt['year']}-{dt['month']:02d}-{dt['date']:02d} "
          f"{dt['hour']:02d}:{dt['minute']:02d}:{dt['second']:02d}")
    time.sleep(1)
'''

ADXL345_DRV = '''\
from machine import I2C, Pin
import struct

class ADXL345:
    """ADXL345 三軸加速度計，I2C 模式"""
    _ADDR        = 0x53   # SDO=GND；SDO=VCC 時為 0x1D
    _POWER_CTL   = 0x2D
    _DATA_FORMAT = 0x31
    _DATAX0      = 0x32

    def __init__(self, sda=4, scl=5, addr=0x53):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=400_000)
        self._addr = addr
        # Measurement mode, ±2g, full resolution
        self._i2c.writeto_mem(self._addr, self._DATA_FORMAT, bytes([0x08]))
        self._i2c.writeto_mem(self._addr, self._POWER_CTL,   bytes([0x08]))

    def read_xyz_raw(self):
        data = self._i2c.readfrom_mem(self._addr, self._DATAX0, 6)
        x, y, z = struct.unpack("<hhh", data)
        return x, y, z

    def read_xyz(self):
        """回傳 (x, y, z) in g，full-resolution: 3.9mg/LSB"""
        x, y, z = self.read_xyz_raw()
        scale = 0.0039
        return x * scale, y * scale, z * scale
'''

ADXL345_EXAMPLE = '''\
from adxl345 import ADXL345
import time

# SDA 接 GPIO4，SCL 接 GPIO5，SDO 接 GND（地址 0x53）
acc = ADXL345(sda=4, scl=5)

print("ADXL345 加速度計測試，Ctrl+C 停止...")
while True:
    x, y, z = acc.read_xyz()
    print(f"X={x:+.3f}g  Y={y:+.3f}g  Z={z:+.3f}g")
    time.sleep_ms(200)
'''

MFRC522_DRV = '''\
from machine import SPI, Pin
import time

class MFRC522:
    """MFRC522 RFID 讀卡器，SPI 介面"""
    # 主要暫存器
    _CommandReg     = 0x01
    _ComIEnReg      = 0x02
    _ComIrqReg      = 0x04
    _ErrorReg       = 0x06
    _FIFODataReg    = 0x09
    _FIFOLevelReg   = 0x0A
    _ControlReg     = 0x0C
    _BitFramingReg  = 0x0D
    _ModeReg        = 0x11
    _TxControlReg   = 0x14
    _TxASKReg       = 0x15
    _CRCResultRegH  = 0x21
    _CRCResultRegL  = 0x22
    _TModeReg       = 0x2A
    _TPrescalerReg  = 0x2B
    _TReloadRegH    = 0x2C
    _TReloadRegL    = 0x2D

    OK   = 0
    ERR  = 1
    NOTAGERR = 2

    REQIDL  = 0x26
    REQALL  = 0x52
    ANTICOLL = 0x93

    def __init__(self, sck=2, mosi=3, miso=4, cs=5, rst=6):
        self._spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self._cs  = Pin(cs,  Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._cs.high()
        self._rst.high()
        self._init()

    def _reg_write(self, reg, val):
        self._cs.low()
        self._spi.write(bytes([(reg << 1) & 0x7E, val]))
        self._cs.high()

    def _reg_read(self, reg):
        self._cs.low()
        self._spi.write(bytes([((reg << 1) & 0x7E) | 0x80]))
        result = self._spi.read(1)
        self._cs.high()
        return result[0]

    def _set_bit(self, reg, mask):
        self._reg_write(reg, self._reg_read(reg) | mask)

    def _clear_bit(self, reg, mask):
        self._reg_write(reg, self._reg_read(reg) & (~mask))

    def _init(self):
        self._rst.low()
        time.sleep_ms(10)
        self._rst.high()
        self._reg_write(self._TModeReg,     0x8D)
        self._reg_write(self._TPrescalerReg,0x3E)
        self._reg_write(self._TReloadRegH,  0x00)
        self._reg_write(self._TReloadRegL,  0x1E)
        self._reg_write(self._TxASKReg,     0x40)
        self._reg_write(self._ModeReg,      0x3D)
        self._set_bit(self._TxControlReg,   0x03)

    def request(self, mode):
        self._reg_write(self._BitFramingReg, 0x07)
        tag_type = [mode]
        status, back_data, back_bits = self._to_card(0x0C, tag_type)
        if status != self.OK or back_bits != 0x10:
            status = self.ERR
        return status, back_data

    def anticoll(self):
        self._reg_write(self._BitFramingReg, 0x00)
        ser_chk = 0
        ser_num = [self.ANTICOLL, 0x20]
        status, back_data, back_bits = self._to_card(0x0C, ser_num)
        if status == self.OK:
            if len(back_data) == 5:
                for i in range(4):
                    ser_chk ^= back_data[i]
                if ser_chk != back_data[4]:
                    status = self.ERR
        return status, back_data

    def _to_card(self, command, send_data):
        back_data, back_len, status = [], 0, self.ERR
        irq_en, wait_irq = (0x77, 0x30) if command == 0x0C else (0x12, 0x10)
        self._reg_write(self._ComIEnReg, irq_en | 0x80)
        self._clear_bit(self._ComIrqReg, 0x80)
        self._set_bit(self._FIFOLevelReg, 0x80)
        self._reg_write(self._CommandReg, 0x00)
        for b in send_data:
            self._reg_write(self._FIFODataReg, b)
        self._reg_write(self._CommandReg, command)
        if command == 0x0C:
            self._set_bit(self._BitFramingReg, 0x80)
        i = 2000
        while True:
            n = self._reg_read(self._ComIrqReg)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break
        self._clear_bit(self._BitFramingReg, 0x80)
        if i != 0:
            if not (self._reg_read(self._ErrorReg) & 0x1B):
                status = self.OK
                n = self._reg_read(self._FIFOLevelReg)
                last_bits = self._reg_read(self._ControlReg) & 0x07
                back_len  = (n - 1) * 8 + last_bits if last_bits else n * 8
                n = min(n, 16)
                back_data = [self._reg_read(self._FIFODataReg) for _ in range(n)]
        return status, back_data, back_len
'''

MFRC522_EXAMPLE = '''\
from mfrc522 import MFRC522
import time

# SCK=GPIO2, MOSI=GPIO3, MISO=GPIO4, CS=GPIO5, RST=GPIO6
rfid = MFRC522(sck=2, mosi=3, miso=4, cs=5, rst=6)

print("RFID 讀卡器就緒，請刷卡...")
while True:
    status, tag_type = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        status, uid = rfid.anticoll()
        if status == rfid.OK:
            uid_str = ":".join(f"{b:02X}" for b in uid[:4])
            print(f"UID: {uid_str}")
            time.sleep_ms(500)
    time.sleep_ms(50)
'''

write(drv_path("module/rtc/ds1307",   "ds1307.py"),  DS1307_DRV)
write(drv_path("module/rtc/ds1307",   "example.py"), DS1307_EXAMPLE)
write(drv_path("sensor/imu/adxl345",  "adxl345.py"), ADXL345_DRV)
write(drv_path("sensor/imu/adxl345",  "example.py"), ADXL345_EXAMPLE)
write(drv_path("module/rfid/mfrc522", "mfrc522.py"), MFRC522_DRV)
write(drv_path("module/rfid/mfrc522", "example.py"), MFRC522_EXAMPLE)
print("Group 8 (I2C/SPI modules) done")

print("\n全部 40 個元件 driver 寫入完成")
