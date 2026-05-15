from machine import Pin, time_pulse_us
import time

class IRReceiver:
    """NEC 協議 IR 接收，38kHz 載波"""
    _LEADER_LOW  = 4500   # Leader code low: 4.5ms
    _LEADER_HIGH = 9000   # Leader code high: 9ms
    _ONE_PULSE   = 1125   # bit "1": 562.5μs high + 562.5μs low = 1125μs total high-low
    _TOLERANCE   = 300

    def __init__(self, pin):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def receive(self, timeout_ms=100):
        """等待並解碼一個 NEC 32-bit 碼，返回 int 或 None（超時）"""
        # 等待 leader: 9ms HIGH，確認為 NEC
        duration = time_pulse_us(self._pin, 0, timeout_ms * 1000)
        if duration < self._LEADER_HIGH - self._TOLERANCE:
            return None
        # 等 4.5ms LOW space
        time_pulse_us(self._pin, 1, 5000)
        # 讀 32 bits
        bits = 0
        for i in range(32):
            # 每個 bit 從 LOW→HIGH 開始
            w = time_pulse_us(self._pin, 1, 2000)
            if w < 0:
                return None
            bits |= (1 if w > self._ONE_PULSE else 0) << i
        return bits
