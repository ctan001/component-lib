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
