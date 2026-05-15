from machine import I2C, Pin
import time

class TM1650:
    """TM1650 四位七段數碼管，I2C-like 協議"""
    _CTRL_BASE = 0x24   # 控制地址：0x24-0x27（4位）
    _DATA_BASE = 0x34   # 顯示地址：0x34-0x37（4位）
    _DIGITS = {
        "0":0x3F,"1":0x06,"2":0x5B,"3":0x4F,"4":0x66,
        "5":0x6D,"6":0x7D,"7":0x07,"8":0x7F,"9":0x6F,
        "-":0x40," ":0x00,"A":0x77,"b":0x7C,"C":0x39,
        "d":0x5E,"E":0x79,"F":0x71,"H":0x76,"L":0x38,
        "P":0x73,"r":0x50,"U":0x3E,
    }

    def __init__(self, sda=4, scl=5, brightness=2):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=100_000)
        self._brightness = brightness
        self._setup()

    def _setup(self):
        for i in range(4):
            self._i2c.writeto(self._CTRL_BASE + i, bytes([0x01 | (self._brightness << 4)]))

    def clear(self):
        for i in range(4):
            self._i2c.writeto(self._DATA_BASE + i, bytes([0x00]))

    def show_raw(self, segments):
        """segments: list of 4 segment bytes"""
        for i, seg in enumerate(segments[:4]):
            self._i2c.writeto(self._DATA_BASE + i, bytes([seg]))

    def show(self, text):
        """text: 最多 4 個字元的字串"""
        text = str(text).ljust(4)[:4]
        segs = [self._DIGITS.get(c, 0x00) for c in text]
        self.show_raw(segs)

    def show_number(self, n):
        self.show(f"{n:4d}")

    def brightness(self, level):
        """level: 0-7"""
        self._brightness = max(0, min(7, level))
        self._setup()
