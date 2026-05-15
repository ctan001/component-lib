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
