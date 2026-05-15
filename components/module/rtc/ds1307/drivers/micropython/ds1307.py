from machine import I2C, Pin
import time

class DS1307:
    """DS1307 I2C 實時時鐘，地址 0x68，BCD 格式"""
    _ADDR = 0x68

    def __init__(self, sda=4, scl=5):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=100_000)

    @staticmethod
    def _bcd2dec(b): return (b >> 4) * 10 + (b & 0x0F)
    @staticmethod
    def _dec2bcd(d): return ((d // 10) << 4) | (d % 10)

    def is_running(self):
        return not bool(self._i2c.readfrom_mem(self._ADDR, 0x00, 1)[0] & 0x80)

    def get_datetime(self):
        d = self._i2c.readfrom_mem(self._ADDR, 0x00, 7)
        return {
            "second": self._bcd2dec(d[0] & 0x7F),
            "minute": self._bcd2dec(d[1]),
            "hour":   self._bcd2dec(d[2] & 0x3F),
            "day":    self._bcd2dec(d[3]),
            "date":   self._bcd2dec(d[4]),
            "month":  self._bcd2dec(d[5]),
            "year":   self._bcd2dec(d[6]) + 2000,
        }

    def set_datetime(self, year, month, date, hour, minute, second, day=1):
        self._i2c.writeto_mem(self._ADDR, 0x00, bytes([
            self._dec2bcd(second),
            self._dec2bcd(minute),
            self._dec2bcd(hour),
            self._dec2bcd(day),
            self._dec2bcd(date),
            self._dec2bcd(month),
            self._dec2bcd(year - 2000),
        ]))
