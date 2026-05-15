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
