from machine import ADC, Pin

class ADCButton5Way:
    """五路 AD 按鍵，電阻分壓，16-bit ADC 區分各鍵（3.3V 系統）"""
    _RANGES = [
        (60000, 65535, 1),
        (45000, 59999, 2),
        (32000, 44999, 3),
        (19000, 31999, 4),
        (6000,  18999, 5),
    ]

    def __init__(self, pin):
        self._adc = ADC(Pin(pin))

    def read(self):
        """回傳按下的鍵號 1-5，無按鍵回傳 None"""
        val = self._adc.read_u16()
        for lo, hi, key in self._ranges:
            if lo <= val <= hi:
                return key
        return None

    @property
    def _ranges(self):
        return self._RANGES

    def read_raw(self):
        return self._adc.read_u16()
