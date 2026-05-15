from machine import ADC, Pin
import math

class NTCTemperature:
    # NTC-MF52AT: 10kΩ @ 25°C, B=3950, 串聯 10kΩ 上拉電阻
    _B = 3950
    _R0 = 10000
    _T0 = 298.15   # 25°C in Kelvin
    _R_SERIES = 10000
    _VREF = 3.3

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def _read_r_ntc(self):
        raw = self._adc.read_u16()
        if raw == 0:
            return float("inf")
        # 分壓：Vout = VCC * R_NTC / (R_NTC + R_series) → R_NTC = R_series * raw / (65535 - raw)
        return self._R_SERIES * raw / (65535 - raw)

    def read_celsius(self):
        r = self._read_r_ntc()
        if r == float("inf") or r <= 0:
            return None
        t_k = 1 / (1 / self._T0 + math.log(r / self._R0) / self._B)
        return t_k - 273.15

    def read_fahrenheit(self):
        c = self.read_celsius()
        return None if c is None else c * 9 / 5 + 32
