import array, time
from machine import Pin
import rp2

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT,
             autopull=True, pull_thresh=24)
def _sk6812_pio():
    # SK6812：0碼 300ns HIGH + 900ns LOW；1碼 600ns HIGH + 600ns LOW（@125MHz）
    T1 = 3   # 300ns
    T2 = 3   # 300ns
    T3 = 9   # 900ns
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)   [T3-1]
    jmp(not_x, "do_zero")   .side(1)   [T1-1]
    jmp("bitloop")           .side(1)   [T2-1]
    label("do_zero")
    nop()                    .side(0)   [T2-1]
    wrap()

class SK6812:
    def __init__(self, pin, n):
        self._n = n
        self._buf = array.array("I", [0] * n)
        self._sm = rp2.StateMachine(0, _sk6812_pio, freq=8_000_000, sideset_base=Pin(pin))
        self._sm.active(1)

    def set_pixel(self, index, r, g, b):
        self._buf[index] = (g << 16) | (r << 8) | b   # GRB order

    def fill(self, r, g, b):
        for i in range(self._n):
            self.set_pixel(i, r, g, b)

    def show(self):
        for val in self._buf:
            self._sm.put(val, 8)
        time.sleep_us(100)   # reset pulse

    def brightness(self, level):
        """level: 0.0-1.0，縮放所有像素亮度"""
        self._buf = array.array("I", [
            (int(((v >> 16) & 0xFF) * level) << 16) |
            (int(((v >>  8) & 0xFF) * level) <<  8) |
            (int( (v        & 0xFF) * level))
            for v in self._buf
        ])
