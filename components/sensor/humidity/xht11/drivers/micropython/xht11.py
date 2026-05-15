import dht
from machine import Pin

class XHT11:
    """XHT11 溫濕度感應器（DHT11 相容）"""
    def __init__(self, pin):
        self._dht = dht.DHT11(Pin(pin))

    def read(self):
        """回傳 (temperature_celsius, humidity_percent)"""
        self._dht.measure()
        return self._dht.temperature(), self._dht.humidity()

    def read_temperature(self):
        self._dht.measure()
        return self._dht.temperature()

    def read_humidity(self):
        self._dht.measure()
        return self._dht.humidity()
