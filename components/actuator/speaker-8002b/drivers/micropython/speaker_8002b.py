from machine import Pin, PWM
import time

class Speaker8002B:
    """8002B 功放喇叭，PWM 輸出音調，放大倍數約 8.5 倍"""
    def __init__(self, pin):
        self._pwm = PWM(Pin(pin))
        self._pwm.duty_u16(0)

    def tone(self, freq_hz, duration_ms=500):
        self._pwm.freq(freq_hz)
        self._pwm.duty_u16(32768)   # 50% duty
        time.sleep_ms(duration_ms)
        self.stop()

    def play_melody(self, notes):
        """notes: [(freq_hz, duration_ms), ...]，freq=0 代表休止符"""
        for freq, duration in notes:
            if freq == 0:
                self.stop()
                time.sleep_ms(duration)
            else:
                self.tone(freq, duration)
            time.sleep_ms(20)

    def stop(self):
        self._pwm.duty_u16(0)

    def deinit(self):
        self._pwm.deinit()
