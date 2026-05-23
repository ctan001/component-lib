"""
ens160.py — ENS160 Digital Air Quality Sensor Driver for MicroPython
I2C address: 0x52 (ADDR=GND) or 0x53 (ADDR=VDD, ENS160+AHT21 combo board)

Wiring (Pico):
  VIN → 5V (module has onboard regulator)
  GND → GND
  SCL → e.g. GP5
  SDA → e.g. GP4

Usage:
  from machine import Pin, SoftI2C
  from ens160 import ENS160
  i2c = SoftI2C(sda=Pin(4), scl=Pin(5))
  ens = ENS160(i2c)                    # 0x53 for combo board
  ens.set_compensation(25.0, 50.0)     # feed T/RH before reading
  result = ens.read()
  if result:
      aqi, tvoc, eco2, validity = result  # None if no new data yet
"""

import time
import struct

_ADDR = 0x53  # ENS160+AHT21 combo board; change to 0x52 for standalone

# Registers
_REG_PART_ID       = 0x00
_REG_OPMODE        = 0x10
_REG_TEMP_IN       = 0x13  # 2 bytes LE: (T_celsius + 273.15) * 64
_REG_RH_IN         = 0x15  # 2 bytes LE: RH_percent * 512
_REG_DEVICE_STATUS = 0x20
_REG_DATA_AQI      = 0x21
_REG_DATA_TVOC     = 0x22  # 2 bytes LE, ppb
_REG_DATA_ECO2     = 0x24  # 2 bytes LE, ppm

# OPMODE values (DataSheet Table 18, p.26)
_OPMODE_SLEEP    = 0x00
_OPMODE_IDLE     = 0x01
_OPMODE_STANDARD = 0x02
_OPMODE_RESET    = 0xF0  # Full hardware reset — reloads NVM baseline

# DEVICE_STATUS masks
_STATUS_NEWDAT    = 0x02        # bit 1: new measurement data ready
_STATUS_VALIDITY  = 0x0C        # bits[3:2]: validity flag mask
_STATUS_VALIDITY_SHIFT = 2

AQI_LABELS = ("", "Excellent", "Good", "Moderate", "Poor", "Unhealthy")


class ENS160:
    """ENS160 I2C driver. Pass a SoftI2C (or I2C) instance."""

    def __init__(self, i2c, addr=_ADDR):
        self._i2c = i2c
        self._addr = addr
        self._init()

    def _write_reg(self, reg, data):
        if isinstance(data, int):
            data = bytes([data])
        self._i2c.writeto_mem(self._addr, reg, data)

    def _read_reg(self, reg, n):
        return self._i2c.readfrom_mem(self._addr, reg, n)

    def _init(self):
        # NOTE: Do NOT use OPMODE_RESET (0xF0) here.
        # RESET clears NVM-commit progress; until the sensor has run continuously
        # for 24h (NVM saved), each RESET restarts Initial Start-Up from scratch.
        # After 24h NVM is committed, RESET may be used to reload a known-good baseline.
        self._write_reg(_REG_OPMODE, _OPMODE_IDLE)
        time.sleep_ms(20)
        self._write_reg(_REG_OPMODE, _OPMODE_STANDARD)
        time.sleep_ms(50)

    def set_compensation(self, temp_c, rh_percent):
        """Feed AHT21 readings to ENS160 for better accuracy. Call before read()."""
        temp_in = int((temp_c + 273.15) * 64)
        rh_in   = int(rh_percent * 512)
        self._write_reg(_REG_TEMP_IN, struct.pack('<H', temp_in))
        self._write_reg(_REG_RH_IN,   struct.pack('<H', rh_in))

    def read(self):
        """Returns (aqi 1-5, tvoc_ppb, eco2_ppm, validity), or None if no new data.
        Call set_compensation() first.

        NEWDAT (bit 1 of DEVICE_STATUS) must be 1 before reading DATA_x registers.
        It is cleared automatically by the hardware on first DATA_x read.
        Returns None when NEWDAT=0 — caller should skip this cycle and retry.

        validity:
          0 = Normal (data valid)
          1 = Warm-Up (~3 min after power-on, data approximate)
          2 = Initial Start-Up (up to 1h+ on first use, data unreliable)
          3 = Invalid output
        """
        raw_status = self._read_reg(_REG_DEVICE_STATUS, 1)[0]
        new_data   = raw_status & _STATUS_NEWDAT          # bit 1
        validity   = (raw_status & _STATUS_VALIDITY) >> _STATUS_VALIDITY_SHIFT  # bits[3:2]

        if not new_data:
            return None  # No new measurement ready — skip this cycle

        aqi  = self._read_reg(_REG_DATA_AQI,  1)[0]
        tvoc = struct.unpack('<H', self._read_reg(_REG_DATA_TVOC, 2))[0]
        eco2 = struct.unpack('<H', self._read_reg(_REG_DATA_ECO2, 2))[0]
        return aqi, tvoc, eco2, validity

    def aqi_label(self):
        """Return human-readable AQI string."""
        aqi = self._read_reg(_REG_DATA_AQI, 1)[0]
        return AQI_LABELS[aqi] if 1 <= aqi <= 5 else "?"

    def status(self):
        """Raw DEVICE_STATUS byte.
        bits[3:2] = VALIDITY_FLAG: 0=Normal, 1=WarmUp, 2=InitStartUp, 3=Invalid
        bit[1]    = NEWDAT: 1=new data available
        """
        return self._read_reg(_REG_DEVICE_STATUS, 1)[0]

    def validity(self):
        """Return validity flag only: 0=Normal, 1=WarmUp, 2=InitStartUp, 3=Invalid."""
        raw = self._read_reg(_REG_DEVICE_STATUS, 1)[0]
        return (raw >> 2) & 0x03
