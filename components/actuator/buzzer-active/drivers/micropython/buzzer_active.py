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
