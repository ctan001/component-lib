# 檔名: max31855_test_v1.py
# 作者: Claude (312-heat-module 專案)
# 建立日期: 2026-08-13
# 最後修改日期: 2026-08-13
# 用途: 確認 Pico 能透過 SPI0 讀到 MAX31855 decoder 的溫度資料（概念驗證階段的硬體 bring-up 測試腳本，
#       尚未抽象為 component-lib driver）
# 相依檔案: 無外部模組，僅用 MicroPython 內建 machine/time
#
# 接線（見 100_Projects/active/Microcontroller/312-heat-module/project.md）：
#   MAX31855 Vin -> Pico 3V3(OUT) pin36
#   MAX31855 GND -> Pico GND
#   MAX31855 CLK -> Pico GP2 (SPI0 SCK)
#   MAX31855 DO  -> Pico GP0 (SPI0 RX/MISO)
#   MAX31855 CS  -> Pico GP1 (軟體控制 GPIO)
#
# 協定依據：MAX31855 datasheet (analog.com, component-lib 存檔) p.5 Serial-Interface Timing,
#           p.9-10 Serial Interface / Table 2 Memory Map, Table 4/5 溫度對照表
#   - 32-bit frame, MSB(D31) first, SPI mode 0 (CPOL=0, CPHA=0)
#   - D[31:18] = 14-bit thermocouple溫度 (sign+13bit, 0.25°C/LSB)
#   - D17 = reserved(0), D16 = fault flag (SCV/SCG/OC 任一為1時為1)
#   - D[15:4] = 12-bit cold-junction(internal)溫度 (sign+11bit, 0.0625°C/LSB)
#   - D3 = reserved(0), D2 = SCV(短路到VCC), D1 = SCG(短路到GND), D0 = OC(斷路)

from machine import Pin, SPI
import time

# --- 接線腳位 ---
SCK_PIN = 2
MOSI_PIN = 3  # 未實接（MAX31855為唯讀裝置），僅滿足 machine.SPI 建構子需求
MISO_PIN = 0
CS_PIN = 1

# --- SPI 參數（datasheet: fSCL 最大 5MHz，這裡取保守值） ---
SPI_BAUDRATE = 1_000_000

# --- 32-bit frame 的 bit 欄位定義（datasheet Table 2, p.10） ---
TC_SHIFT = 18        # D[31:18] 起始位元
TC_MASK = 0x3FFF      # 14-bit
TC_SIGN_BIT = 0x2000
TC_SIGN_EXTEND = 0x4000
TC_LSB_C = 0.25

FAULT_BIT = 1 << 16

CJ_SHIFT = 4          # D[15:4] 起始位元
CJ_MASK = 0x0FFF       # 12-bit
CJ_SIGN_BIT = 0x0800
CJ_SIGN_EXTEND = 0x1000
CJ_LSB_C = 0.0625

SCV_BIT = 1 << 2  # 短路到VCC
SCG_BIT = 1 << 1  # 短路到GND
OC_BIT = 1 << 0   # 熱電偶斷路

# 上電後首次轉換需要的等待時間（datasheet Note 6, tCONV_PU 典型200ms）
POWER_UP_WAIT_MS = 250
READ_INTERVAL_MS = 200
READ_COUNT = 10


def decode(value32):
    """把 MAX31855 讀回的 32-bit frame 解成 (熱電偶溫度, 冷端溫度, fault, SCV, SCG, OC)。純函式，不碰硬體。"""
    tc_raw = (value32 >> TC_SHIFT) & TC_MASK
    if tc_raw & TC_SIGN_BIT:
        tc_raw -= TC_SIGN_EXTEND
    tc_temp_c = tc_raw * TC_LSB_C

    fault = bool(value32 & FAULT_BIT)

    cj_raw = (value32 >> CJ_SHIFT) & CJ_MASK
    if cj_raw & CJ_SIGN_BIT:
        cj_raw -= CJ_SIGN_EXTEND
    cj_temp_c = cj_raw * CJ_LSB_C

    scv = bool(value32 & SCV_BIT)
    scg = bool(value32 & SCG_BIT)
    oc = bool(value32 & OC_BIT)

    return tc_temp_c, cj_temp_c, fault, scv, scg, oc


def self_test():
    """用 datasheet Table 4/5 的已知數值反推組出 32-bit frame，驗證 decode() 邏輯正確。
    涵蓋：正溫度、負溫度（sign-extension）兩種邊界情況。"""
    # Table 4: TC +100.75C = 0000 0110 0100 11 ; Table 5: CJ +100.5625C = 0110 0100 1001
    frame_pos = (0b00000110010011 << TC_SHIFT) | (0b011001001001 << CJ_SHIFT)
    tc, cj, fault, scv, scg, oc = decode(frame_pos)
    assert tc == 100.75, "TC正值解碼錯誤: %r" % tc
    assert cj == 100.5625, "CJ正值解碼錯誤: %r" % cj
    assert not (fault or scv or scg or oc), "正值測試不應有fault"

    # Table 4: TC -1.00C = 1111 1111 1111 00 ; Table 5: CJ -1.0000C = 1111 1111 0000
    frame_neg = (0b11111111111100 << TC_SHIFT) | (0b111111110000 << CJ_SHIFT)
    tc, cj, fault, scv, scg, oc = decode(frame_neg)
    assert tc == -1.00, "TC負值(sign-extend)解碼錯誤: %r" % tc
    assert cj == -1.00, "CJ負值(sign-extend)解碼錯誤: %r" % cj

    print("self_test passed")


def read_raw(spi, cs):
    cs.value(0)
    raw = spi.read(4)
    cs.value(1)
    return int.from_bytes(raw, 'big')


def main():
    self_test()

    spi = SPI(0, baudrate=SPI_BAUDRATE, polarity=0, phase=0,
              sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
    cs = Pin(CS_PIN, Pin.OUT, value=1)

    time.sleep_ms(POWER_UP_WAIT_MS)

    print("=== MAX31855 讀取測試 (v1) ===")
    for _ in range(READ_COUNT):
        raw = read_raw(spi, cs)
        tc, cj, fault, scv, scg, oc = decode(raw)
        print("raw=0x%08X  case(TC)=%.2fC  internal(CJ)=%.2fC  fault=%s (SCV=%s SCG=%s OC=%s)" %
              (raw, tc, cj, fault, scv, scg, oc))
        time.sleep_ms(READ_INTERVAL_MS)


if __name__ == '__main__':
    main()
