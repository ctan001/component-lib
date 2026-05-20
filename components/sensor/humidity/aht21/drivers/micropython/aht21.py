"""
aht21.py — AHT21 Temperature & Humidity Sensor Driver for MicroPython
I2C address: 0x38 (fixed)

Wiring (Pico):
  VDD → 3.3V
  GND → GND
  SCL → e.g. GP5
  SDA → e.g. GP4

Usage:
  from machine import Pin, SoftI2C
  from aht21 import AHT21
  i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
  sensor = AHT21(i2c)
  temp, rh = sensor.read()
"""

import time

_ADDR       = 0x38
_CMD_STATUS  = bytes([0x71])
_CMD_MEASURE = bytes([0xAC, 0x33, 0x00])


class AHT21:
    """AHT21 I2C driver. Pass a SoftI2C (or I2C) instance."""

    def __init__(self, i2c, addr=_ADDR):
        self._i2c = i2c
        self._addr = addr
        self._init()

    def _init(self):
        time.sleep_ms(100)              # datasheet: ≥100ms after power-on
        self._i2c.writeto(self._addr, _CMD_STATUS)
        status = self._i2c.readfrom(self._addr, 1)[0]
        if (status & 0x18) != 0x18:    # calibration bit not set
            self._calibrate()

    def _calibrate(self):
        for reg in (0x1B, 0x1C, 0x1E):
            self._i2c.writeto(self._addr, bytes([reg, 0x00, 0x00]))
            time.sleep_ms(10)

    def read(self):
        """Trigger measurement. Returns (temperature_C, humidity_pct)."""
        self._i2c.writeto(self._addr, _CMD_MEASURE)
        time.sleep_ms(80)               # datasheet: wait ≥80ms

        for _ in range(10):             # poll until not busy
            data = self._i2c.readfrom(self._addr, 7)
            if not (data[0] & 0x80):
                break
            time.sleep_ms(10)

        # humidity: bits [39:20] of data bytes 1-3
        s_rh = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        rh   = (s_rh / (1 << 20)) * 100.0

        # temperature: bits [19:0] of data bytes 3-5
        s_t  = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        temp = (s_t / (1 << 20)) * 200.0 - 50.0

        return temp, rh
