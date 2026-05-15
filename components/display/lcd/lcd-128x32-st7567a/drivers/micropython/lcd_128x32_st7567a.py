from machine import SPI, Pin
import time

class LCD128x32:
    """ST7567A 128×32 像素 LCD，SPI 介面，頁式定址"""
    WIDTH  = 128
    HEIGHT = 32
    PAGES  = HEIGHT // 8   # 4 pages

    def __init__(self, sck=2, sda=3, rs=4, rst=5, cs=6):
        self._spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(sda), miso=None)
        self._rs  = Pin(rs,  Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._cs  = Pin(cs,  Pin.OUT)
        self._buf = bytearray(self.WIDTH * self.PAGES)
        self._init()

    def _cmd(self, b):
        self._rs.low()
        self._cs.low()
        self._spi.write(bytes([b]))
        self._cs.high()

    def _data(self, buf):
        self._rs.high()
        self._cs.low()
        self._spi.write(buf)
        self._cs.high()

    def _init(self):
        self._rst.low()
        time.sleep_ms(10)
        self._rst.high()
        time.sleep_ms(10)
        for cmd in [0xE2, 0xA3, 0xA0, 0xC8, 0x44, 0xAB, 0xF8, 0x00,
                    0x27, 0x81, 0x18, 0xAC, 0x00, 0xAF]:
            self._cmd(cmd)

    def clear(self):
        for i in range(len(self._buf)):
            self._buf[i] = 0

    def pixel(self, x, y, val):
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            page = y // 8
            bit  = y % 8
            idx  = page * self.WIDTH + x
            if val:
                self._buf[idx] |= (1 << bit)
            else:
                self._buf[idx] &= ~(1 << bit)

    def show(self):
        for page in range(self.PAGES):
            self._cmd(0xB0 | page)
            self._cmd(0x10)
            self._cmd(0x00)
            self._data(self._buf[page*self.WIDTH:(page+1)*self.WIDTH])
