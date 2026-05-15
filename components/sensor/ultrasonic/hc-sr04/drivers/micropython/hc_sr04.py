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
