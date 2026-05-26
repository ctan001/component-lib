"""
test_cc1101.py — 驗證 CC1101 SPI 通訊

接線：
  CC1101 Pin5  SCK   → Pico GP2
  CC1101 Pin6  MOSI  → Pico GP3
  CC1101 Pin7  MISO  → Pico GP4
  CC1101 Pin4  CSN   → Pico GP5
  CC1101 Pin2  VCC   → 3.3V
  CC1101 Pin1  GND   → GND

預期結果：
  PARTNUM = 0x00
  VERSION = 0x14
"""
from machine import SPI, Pin
import time

# ── SPI 初始化 ──────────────────────────────────────────
spi = SPI(0, baudrate=4_000_000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT, value=1)

# ── 低階 SPI 操作 ────────────────────────────────────────
def _strobe(cmd):
    """送出 strobe 命令（單位元組），回傳狀態位元組"""
    cs(0); time.sleep_us(2)
    buf = bytearray(1)
    spi.write_readinto(bytes([cmd]), buf)
    cs(1)
    return buf[0]

def _read_status_reg(addr):
    """讀取 Status Register（0x30-0x3D），需加 burst bit"""
    cs(0); time.sleep_us(2)
    spi.write(bytes([addr | 0xC0]))   # Read=1, Burst=1
    result = bytearray(1)
    spi.readinto(result)
    cs(1)
    return result[0]

# ── CC1101 硬體重置程序（依 datasheet §10.1）────────────
def cc1101_reset():
    cs(1); time.sleep_us(5)
    cs(0); time.sleep_us(10)
    cs(1); time.sleep_us(41)   # 等 MISO 穩定
    cs(0); time.sleep_us(10)
    cs(1); time.sleep_us(200)
    _strobe(0x30)               # SRES
    time.sleep_ms(10)

# ── 主測試 ───────────────────────────────────────────────
print("=" * 30)
print("CC1101 SPI 連通測試")
print("=" * 30)

cc1101_reset()
print("SRES 完成")

partnum = _read_status_reg(0x30)   # PARTNUM
version = _read_status_reg(0x31)   # VERSION

print(f"PARTNUM : 0x{partnum:02X}  (期望 0x00)")
print(f"VERSION : 0x{version:02X}  (期望 0x14)")

if version == 0x14 and partnum == 0x00:
    print()
    print("✅  CC1101 SPI 正常！")
elif version == 0xFF:
    print()
    print("❌  全部讀到 0xFF → MISO 懸空或 CS 沒拉低")
    print("   檢查：GP4(MISO)、GP5(CSN) 接線")
elif version == 0x00:
    print()
    print("❌  全部讀到 0x00 → MOSI/SCK 可能接反或 VCC 未供電")
    print("   檢查：GP2(SCK)、GP3(MOSI) 接線，確認 3.3V")
else:
    print()
    print(f"⚠️  讀到非預期值 (0x{version:02X}) → 可能是 SPI mode 或速率問題")
