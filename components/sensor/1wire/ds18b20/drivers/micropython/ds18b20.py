import onewire, ds18x20
from machine import Pin
import time

class DS18B20:
    def __init__(self, pin):
        ow = onewire.OneWire(Pin(pin))
        self._ds = ds18x20.DS18X20(ow)
        self._roms = self._ds.scan()
        if not self._roms:
            raise RuntimeError("找不到 DS18B20，請確認接線和上拉電阻")

    def read_celsius(self, index=0):
        self._ds.convert_temp()
        time.sleep_ms(750)
        return self._ds.read_temp(self._roms[index])

    def read_fahrenheit(self, index=0):
        return self.read_celsius(index) * 9 / 5 + 32

    @property
    def device_count(self):
        return len(self._roms)
