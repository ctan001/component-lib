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
