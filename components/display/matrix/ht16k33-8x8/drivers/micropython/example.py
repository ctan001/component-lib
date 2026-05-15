from ht16k33_8x8 import HT16K33Matrix
import time

# SDA 接 GPIO4，SCL 接 GPIO5，I2C 地址 0x70
matrix = HT16K33Matrix(sda=4, scl=5)

print("HT16K33 8×8 點陣測試...")
# 顯示笑臉
SMILEY = [
    0b00111100,
    0b01000010,
    0b10100101,
    0b10000001,
    0b10100101,
    0b10011001,
    0b01000010,
    0b00111100,
]
for y, row in enumerate(SMILEY):
    for x in range(8):
        matrix.set_pixel(x, y, (row >> (7-x)) & 1)
matrix.show()
time.sleep(3)
matrix.clear()
print("完成")
