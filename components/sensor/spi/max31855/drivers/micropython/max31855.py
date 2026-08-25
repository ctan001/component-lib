# 檔名: max31855.py
# 用途: MAX31855 K-type熱電偶轉換器 MicroPython driver（SPI，唯讀）
# 相依檔案: 無(僅依賴MicroPython內建的machine模組)
# 參考接線(312-heat-module專案實際使用，2026-08-13實機驗證通過，見component-lib README.md)：
#   CLK->GP2(SPI0 SCK) | DO->GP0(SPI0 RX/MISO) | CS->GP1(SPI0 CSn，軟體GPIO)
#   Vin->Pico 3V3(OUT) | GND->GND
#   本晶片唯讀，沒有MOSI/SDI腳位，建構子的mosi參數只是滿足machine.SPI()的介面需求，實際不接線。
#   其他專案要重用時，接線依實際GPIO配置調整，上面是這顆晶片在本專案的參考範例，不是固定值。
# 建立日期: 2026-08-13
# 最後修改日期: 2026-08-24
from machine import Pin, SPI

# 32-bit frame 的 bit 欄位定義（datasheet Table 2, p.10；完整協定說明見 component-lib 知識分層原則，
# control mechanism 記在 Claude memory 的 312-heat-module 專案筆記，這裡只留最少量的欄位常數）
_TC_SHIFT, _TC_MASK, _TC_SIGN_BIT, _TC_SIGN_EXTEND, _TC_LSB_C = 18, 0x3FFF, 0x2000, 0x4000, 0.25
_CJ_SHIFT, _CJ_MASK, _CJ_SIGN_BIT, _CJ_SIGN_EXTEND, _CJ_LSB_C = 4, 0x0FFF, 0x0800, 0x1000, 0.0625
_FAULT_BIT, _SCV_BIT, _SCG_BIT, _OC_BIT = 1 << 16, 1 << 2, 1 << 1, 1 << 0


class MAX31855:
    def __init__(self, sck, mosi, miso, cs, spi_id=0, baudrate=1_000_000):
        self._spi = SPI(spi_id, baudrate=baudrate, polarity=0, phase=0,
                         sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self._cs = Pin(cs, Pin.OUT, value=1)

    def read(self):
        """回傳 (case溫度°C, 冷端溫度°C, fault, SCV短路VCC, SCG短路GND, OC斷路)"""
        self._cs.value(0)
        raw = self._spi.read(4)
        self._cs.value(1)
        value32 = int.from_bytes(raw, 'big')

        tc_raw = (value32 >> _TC_SHIFT) & _TC_MASK
        if tc_raw & _TC_SIGN_BIT:
            tc_raw -= _TC_SIGN_EXTEND
        tc_temp_c = tc_raw * _TC_LSB_C

        cj_raw = (value32 >> _CJ_SHIFT) & _CJ_MASK
        if cj_raw & _CJ_SIGN_BIT:
            cj_raw -= _CJ_SIGN_EXTEND
        cj_temp_c = cj_raw * _CJ_LSB_C

        fault = bool(value32 & _FAULT_BIT)
        scv = bool(value32 & _SCV_BIT)
        scg = bool(value32 & _SCG_BIT)
        oc = bool(value32 & _OC_BIT)
        return tc_temp_c, cj_temp_c, fault, scv, scg, oc
