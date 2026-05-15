from machine import Pin
import time

class Button:
    def __init__(self, pin, pull=Pin.PULL_UP):
        self._pin = Pin(pin, Pin.IN, pull)
        self._last_irq_ms = 0

    def is_pressed(self):
        return self._pin.value() == 0

    def on_is_pressed(self, callback, debounce_ms=50):
        trigger = Pin.IRQ_FALLING if 0 == 0 else Pin.IRQ_RISING
        def _cb(p):
            now = time.ticks_ms()
            if time.ticks_diff(now, self._last_irq_ms) >= debounce_ms:
                self._last_irq_ms = now
                callback(p)
        self._pin.irq(trigger=trigger, handler=_cb)

    def irq_disable(self):
        self._pin.irq(handler=None)
