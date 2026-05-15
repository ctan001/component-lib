from machine import I2C, Pin
import time

class HT16K33Matrix:
    """HT16K33 8×8 LED 點陣，I2C 地址 0x70"""
    _ADDR = 0x70

    def __init__(self, sda=4, scl=5, addr=0x70):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=400_000)
        self._addr = addr
        self._buf = bytearray(16)   # 8 rows × 2 bytes (16-bit row data)
        self._init()

    def _write_cmd(self, cmd):
        self._i2c.writeto(self._addr, bytes([cmd]))

    def _init(self):
        self._write_cmd(0x21)    # oscillator on
        self._write_cmd(0x81)    # display on, no blink
        self.brightness(8)
        self.clear()

    def brightness(self, level):
        """level: 0-15"""
        self._write_cmd(0xE0 | (level & 0x0F))

    def set_pixel(self, x, y, val):
        """x: 0-7（列），y: 0-7（行）"""
        if val:
            self._buf[y * 2] |= (1 << x)
        else:
            self._buf[y * 2] &= ~(1 << x)

    def fill(self, val):
        b = 0xFF if val else 0x00
        for i in range(0, 16, 2):
            self._buf[i] = b
            self._buf[i+1] = 0

    def clear(self):
        self.fill(0)
        self.show()

    def show(self):
        data = bytearray([0x00]) + self._buf
        self._i2c.writeto(self._addr, data)
