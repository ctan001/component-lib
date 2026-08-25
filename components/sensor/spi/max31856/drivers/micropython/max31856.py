# 檔名: max31856.py
# 用途: MAX31856 K-type熱電偶轉換器 MicroPython driver（SPI），供312-heat-module專案PID控溫迴路讀取
#       case temperature（見component-lib的README.md與project memory project_312_heat_module）
# 相依檔案: 無(僅依賴MicroPython內建的machine/time模組)
# 參考接線(312-heat-module專案實際使用，見report/MAX31856_Wiring_Report_v1.docx，2026-08-24規劃)：
#   VIN->Pico 3V3(OUT) | GND->GND
#   SDO->GP0(SPI0 RX/MISO) | CS->GP1(SPI0 CSn) | SCK->GP2(SPI0 SCK) | SDI->GP3(SPI0 TX/MOSI)
#   DRDY/FLT：暫不接（本driver純SPI輪詢，不用硬體中斷/FAULT pin）
#   3Vo：不接（regulator輸出腳，不可接電源進去）
#   其他專案要重用時，接線依實際GPIO配置調整，上面是這顆晶片在本專案的參考範例，不是固定值。
# 建立日期: 2026-08-24
# 最後修改日期: 2026-08-24
import time
from machine import Pin, SPI

# Register addresses（datasheet Table 6, p.18）。讀=0x0X，寫=0x8X（address MSB=1 觸發寫入，p.15）。
_REG_CR0 = 0x00
_REG_CR1 = 0x01
_REG_CJTH = 0x0A  # 讀取起點：CJTH..SR 六個register位址連續(0Ah-0Fh)，可一次multibyte read讀完(p.15 multibyte transfer)
_WRITE_BIT = 0x80

# CR0 (00h) bit組合，拆兩階段(datasheet p.19明講：50/60Hz notch頻率只能在Normally Off模式下切換；
# Pico軟體reset不會讓MAX31856斷電——VIN接的是Pico自己3V3 regulator輸出，跟MCU core reset是獨立電源軌，
# 重開機當下晶片可能還卡在舊的continuous conversion狀態，所以初始化必須先強制回Normally Off再設定)：
#   Off階段：CMODE=0(Normally Off) | 1SHOT=0 | OCFAULT=01(開路偵測啟用,每16次轉換偵測一次,
#            RS<5kΩ典型13.3ms,Table4 p.14) | CJ=0(內建冷端感測啟用) | FAULT=0(comparator mode)
#            | FAULTCLR=0 | 50/60Hz(bit0，由建構子notch_50hz參數決定)
#   On階段：疊加CMODE=1(自動連續轉換,每100ms一次,p.19)
_CR0_OFF_BASE = 0b0001_0000
_CR0_CMODE_BIT = 1 << 7

# CR1 (01h) TC TYPE編碼（datasheet p.20）：K=0011（本專案K-type熱電偶，見312-heat-module專案筆記）
_TC_TYPE_K = 0b0011
_AVGSEL_1SAMPLE = 0b000  # 1 sample/無平均，維持跟MAX31855一樣的低延遲輪詢風格

# 19-bit linearized TC溫度暫存器(0Ch/0Dh/0Eh)：3 byte MSB-first，低5bit為未定義填充位(datasheet p.24-25)。
# LSB = 2^-7 = 0.0078125°C，公式對照datasheet Table 3(p.13)四筆範例驗證過(+25.00/-0.0625/+1600.00/-250.00°C皆算對)。
_TC_LSB_C = 0.0078125
_TC_SIGN_BIT = 1 << 18
_TC_SIGN_EXTEND = 1 << 19

# 14-bit CJ(冷端)溫度暫存器(0Ah/0Bh)：2 byte MSB-first，低2bit未定義填充位(datasheet p.24)。
# LSB = 2^-6 = 0.015625°C，公式對照datasheet Table 2(p.13)四筆範例驗證過(+0.015625/-0.5/+64/-55°C皆算對)。
_CJ_LSB_C = 0.015625
_CJ_SIGN_BIT = 1 << 13
_CJ_SIGN_EXTEND = 1 << 14

# Fault Status Register (0Fh) bit定義（datasheet p.25-26）
_SR_CJ_RANGE = 1 << 7
_SR_TC_RANGE = 1 << 6
_SR_OVUV = 1 << 1
_SR_OPEN = 1 << 0

# CMODE=1後到第一次conversion完成的等待時間：datasheet p.19「自動連續轉換每100ms(nominal)一次」，
# 加上開路偵測(OCFAULT=01)典型13.3ms/最大15ms(Table4 p.14)，抓250ms留足margin，避免建構子回傳後
# 第一次read()讀到reset殘值(reset後LTCB*/CJT*暫存器預設值皆為00h)。
_FIRST_CONVERSION_WAIT_MS = 250


class MAX31856:
    """K-type熱電偶轉換器driver。跟MAX31855的差異：MAX31856只有OPEN(斷路)+OVUV(過/欠壓)兩種
    硬體故障位元，沒有MAX31855那種區分SHORT-GND/SHORT-VCC的機制——datasheet(p.14)裡OVUV是「輸入電壓
    為負或超過VDD」的單一狀態，不分是對地短路還是對電源短路。呼叫端(main.py的_tc_fault_label)需要
    重新設計，不能直接沿用MAX31855那三分類。另外datasheet(p.14)指出OVUV發生時conversion會被暫停，
    此時read()回傳的溫度值可能是舊值，呼叫端應優先檢查ovuv_fault再決定要不要採用溫度值。
    MASK register(02h)刻意不設定：本driver只走SPI輪詢，沒有接硬體FAULT pin，MASK只影響FAULT pin訊號。
    """

    def __init__(self, sck, mosi, miso, cs, spi_id=0, baudrate=1_000_000, notch_50hz=False):
        # SPI mode: CPHA必須=1(datasheet p.15明講)，CPOL可任一(datasheet:自動偵測)，這裡選CPOL=0 → mode 1
        self._spi = SPI(spi_id, baudrate=baudrate, polarity=0, phase=1,
                         sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self._cs = Pin(cs, Pin.OUT, value=1)
        self._init_registers(notch_50hz)

    def _write_reg(self, addr, data_bytes):
        payload = bytes([addr | _WRITE_BIT]) + bytes(data_bytes)  # CS拉低前先組好payload，非法輸入的例外不會讓bus卡在low
        self._cs.value(0)
        try:
            self._spi.write(payload)
        finally:
            self._cs.value(1)

    def _read_reg(self, addr, n):
        self._cs.value(0)
        try:
            self._spi.write(bytes([addr]))
            return self._spi.read(n)
        finally:
            self._cs.value(1)

    def _init_registers(self, notch_50hz):
        cr0_off = _CR0_OFF_BASE | (1 if notch_50hz else 0)
        cr1 = (_AVGSEL_1SAMPLE << 4) | _TC_TYPE_K

        self._write_reg(_REG_CR0, [cr0_off, cr1])  # multibyte write：CR0(00h)+CR1(01h)連續位址一次寫入，仍在Normally Off

        readback = self._read_reg(_REG_CR0, 2)
        if readback[0] != cr0_off or readback[1] != cr1:
            raise RuntimeError(
                "MAX31856 CR0/CR1 readback mismatch: wrote ({:#04x},{:#04x}), read back ({:#04x},{:#04x})"
                " -- 檢查SPI接線(SCK/SDI/SDO/CS)、CPHA=1設定、晶片是否有上電".format(
                    cr0_off, cr1, readback[0], readback[1]))

        self._write_reg(_REG_CR0, [cr0_off | _CR0_CMODE_BIT])  # 確認設定寫對後才切到自動連續轉換模式
        time.sleep_ms(_FIRST_CONVERSION_WAIT_MS)

    def read(self):
        """回傳 (TC溫度°C, CJ溫度°C, open_fault, ovuv_fault, cj_range_fault, tc_range_fault, fault_status_raw)。
        一次multibyte read讀CJTH..SR共6 byte(0Ah-0Fh)，確保數值來自同一輪轉換(datasheet p.12/p.24建議)。
        fault_status_raw是完整SR(0Fh)原始byte，CJHIGH/CJLOW/TCHIGH/TCLOW等threshold類fault位元
        （本driver未設定門檻暫存器，門檻式安全判斷交給main.py的軟體180°C cutoff處理）都保留在裡面，
        需要時呼叫端自己從raw byte解。"""
        self._cs.value(0)
        try:
            self._spi.write(bytes([_REG_CJTH]))
            raw = self._spi.read(6)
        finally:
            self._cs.value(1)

        cj_raw16 = (raw[0] << 8) | raw[1]
        cj_raw14 = cj_raw16 >> 2
        if cj_raw14 & _CJ_SIGN_BIT:
            cj_raw14 -= _CJ_SIGN_EXTEND
        cj_temp_c = cj_raw14 * _CJ_LSB_C

        tc_raw24 = (raw[2] << 16) | (raw[3] << 8) | raw[4]
        tc_raw19 = tc_raw24 >> 5
        if tc_raw19 & _TC_SIGN_BIT:
            tc_raw19 -= _TC_SIGN_EXTEND
        tc_temp_c = tc_raw19 * _TC_LSB_C

        sr = raw[5]
        open_fault = bool(sr & _SR_OPEN)
        ovuv_fault = bool(sr & _SR_OVUV)
        cj_range_fault = bool(sr & _SR_CJ_RANGE)
        tc_range_fault = bool(sr & _SR_TC_RANGE)
        return tc_temp_c, cj_temp_c, open_fault, ovuv_fault, cj_range_fault, tc_range_fault, sr
