from machine import I2C, Pin
import struct

class ADXL345:
    """ADXL345 三軸加速度計，I2C 模式"""
    _ADDR        = 0x53   # SDO=GND；SDO=VCC 時為 0x1D
    _POWER_CTL   = 0x2D
    _DATA_FORMAT = 0x31
    _DATAX0      = 0x32

    def __init__(self, sda=4, scl=5, addr=0x53):
        self._i2c = I2C(0, sda=Pin(sda), scl=Pin(scl), freq=400_000)
        self._addr = addr
        # Measurement mode, ±2g, full resolution
        self._i2c.writeto_mem(self._addr, self._DATA_FORMAT, bytes([0x08]))
        self._i2c.writeto_mem(self._addr, self._POWER_CTL,   bytes([0x08]))

    def read_xyz_raw(self):
        data = self._i2c.readfrom_mem(self._addr, self._DATAX0, 6)
        x, y, z = struct.unpack("<hhh", data)
        return x, y, z

    def read_xyz(self):
        """回傳 (x, y, z) in g，full-resolution: 3.9mg/LSB"""
        x, y, z = self.read_xyz_raw()
        scale = 0.0039
        return x * scale, y * scale, z * scale
