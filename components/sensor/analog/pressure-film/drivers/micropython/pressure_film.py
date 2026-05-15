from machine import ADC, Pin

class PressureSensor:
    _VREF = 3.3

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def read_raw(self):
        return self._adc.read_u16()

    def read_voltage(self):
        return self.read_raw() / 65535 * self._VREF

    def read_percent(self):
        return self.read_raw() / 65535 * 100
