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
