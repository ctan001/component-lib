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
