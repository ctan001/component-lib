from machine import SPI, Pin
import time

class MFRC522:
    """MFRC522 RFID 讀卡器，SPI 介面"""
    # 主要暫存器
    _CommandReg     = 0x01
    _ComIEnReg      = 0x02
    _ComIrqReg      = 0x04
    _ErrorReg       = 0x06
    _FIFODataReg    = 0x09
    _FIFOLevelReg   = 0x0A
    _ControlReg     = 0x0C
    _BitFramingReg  = 0x0D
    _ModeReg        = 0x11
    _TxControlReg   = 0x14
    _TxASKReg       = 0x15
    _CRCResultRegH  = 0x21
    _CRCResultRegL  = 0x22
    _TModeReg       = 0x2A
    _TPrescalerReg  = 0x2B
    _TReloadRegH    = 0x2C
    _TReloadRegL    = 0x2D

    OK   = 0
    ERR  = 1
    NOTAGERR = 2

    REQIDL  = 0x26
    REQALL  = 0x52
    ANTICOLL = 0x93

    def __init__(self, sck=2, mosi=3, miso=4, cs=5, rst=6):
        self._spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self._cs  = Pin(cs,  Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._cs.high()
        self._rst.high()
        self._init()

    def _reg_write(self, reg, val):
        self._cs.low()
        self._spi.write(bytes([(reg << 1) & 0x7E, val]))
        self._cs.high()

    def _reg_read(self, reg):
        self._cs.low()
        self._spi.write(bytes([((reg << 1) & 0x7E) | 0x80]))
        result = self._spi.read(1)
        self._cs.high()
        return result[0]

    def _set_bit(self, reg, mask):
        self._reg_write(reg, self._reg_read(reg) | mask)

    def _clear_bit(self, reg, mask):
        self._reg_write(reg, self._reg_read(reg) & (~mask))

    def _init(self):
        self._rst.low()
        time.sleep_ms(10)
        self._rst.high()
        self._reg_write(self._TModeReg,     0x8D)
        self._reg_write(self._TPrescalerReg,0x3E)
        self._reg_write(self._TReloadRegH,  0x00)
        self._reg_write(self._TReloadRegL,  0x1E)
        self._reg_write(self._TxASKReg,     0x40)
        self._reg_write(self._ModeReg,      0x3D)
        self._set_bit(self._TxControlReg,   0x03)

    def request(self, mode):
        self._reg_write(self._BitFramingReg, 0x07)
        tag_type = [mode]
        status, back_data, back_bits = self._to_card(0x0C, tag_type)
        if status != self.OK or back_bits != 0x10:
            status = self.ERR
        return status, back_data

    def anticoll(self):
        self._reg_write(self._BitFramingReg, 0x00)
        ser_chk = 0
        ser_num = [self.ANTICOLL, 0x20]
        status, back_data, back_bits = self._to_card(0x0C, ser_num)
        if status == self.OK:
            if len(back_data) == 5:
                for i in range(4):
                    ser_chk ^= back_data[i]
                if ser_chk != back_data[4]:
                    status = self.ERR
        return status, back_data

    def _to_card(self, command, send_data):
        back_data, back_len, status = [], 0, self.ERR
        irq_en, wait_irq = (0x77, 0x30) if command == 0x0C else (0x12, 0x10)
        self._reg_write(self._ComIEnReg, irq_en | 0x80)
        self._clear_bit(self._ComIrqReg, 0x80)
        self._set_bit(self._FIFOLevelReg, 0x80)
        self._reg_write(self._CommandReg, 0x00)
        for b in send_data:
            self._reg_write(self._FIFODataReg, b)
        self._reg_write(self._CommandReg, command)
        if command == 0x0C:
            self._set_bit(self._BitFramingReg, 0x80)
        i = 2000
        while True:
            n = self._reg_read(self._ComIrqReg)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break
        self._clear_bit(self._BitFramingReg, 0x80)
        if i != 0:
            if not (self._reg_read(self._ErrorReg) & 0x1B):
                status = self.OK
                n = self._reg_read(self._FIFOLevelReg)
                last_bits = self._reg_read(self._ControlReg) & 0x07
                back_len  = (n - 1) * 8 + last_bits if last_bits else n * 8
                n = min(n, 16)
                back_data = [self._reg_read(self._FIFODataReg) for _ in range(n)]
        return status, back_data, back_len
