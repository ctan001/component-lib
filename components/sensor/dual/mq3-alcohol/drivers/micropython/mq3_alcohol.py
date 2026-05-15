from machine import ADC, Pin

class MQ3Alcohol:
    _VREF = 3.3

    def __init__(self, a0_pin, d0_pin):
        self._adc = ADC(Pin(a0_pin))
        self._d0  = Pin(d0_pin, Pin.IN)

    def read_analog(self):
        return self._adc.read_u16()

    def read_voltage(self):
        return self.read_analog() / 65535 * self._VREF

    def is_alarm(self):
        return self._d0.value() == 0   # active-low
