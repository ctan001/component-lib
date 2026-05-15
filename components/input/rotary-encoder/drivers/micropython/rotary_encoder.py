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
