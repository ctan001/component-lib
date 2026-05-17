"""
I2C 2004 LCD driver for MicroPython (HD44780 + PCF8574A backpack)

PCF8574A bit mapping:
  bit 0 (0x01) = RS
  bit 1 (0x02) = RW  (always 0 = write)
  bit 2 (0x04) = EN
  bit 3 (0x08) = BL  (backlight)
  bit 4 (0x10) = D4
  bit 5 (0x20) = D5
  bit 6 (0x40) = D6
  bit 7 (0x80) = D7

Default I2C address:
  PCF8574AT (A0-A2 open) → 0x3F
  PCF8574T  (A0-A2 open) → 0x27
"""

import time

_RS = 0x01
_EN = 0x04
_BL = 0x08

# HD44780 command codes
_CLEAR   = 0x01
_HOME    = 0x02
_ENTRY   = 0x04
_DISPLAY = 0x08
_FUNC    = 0x20

# Flags
_ENTRY_INC  = 0x02
_DISP_ON    = 0x04
_CURSOR_ON  = 0x02
_BLINK_ON   = 0x01
_FUNC_4BIT  = 0x00
_FUNC_2LINE = 0x08

# DDRAM row start addresses for 20×4
_ROW_OFFSETS = (0x00, 0x40, 0x14, 0x54)


class LCD2004I2C:
    def __init__(self, i2c, addr=0x3F):
        self._i2c = i2c
        self._addr = addr
        self._bl = _BL
        self._ctrl = _DISP_ON
        self._init()

    # ── low-level PCF8574 helpers ──────────────────────────────────────────

    def _write_pcf(self, val):
        self._i2c.writeto(self._addr, bytes([val]))

    def _pulse(self, val):
        self._write_pcf(val | _EN)
        time.sleep_us(1)
        self._write_pcf(val & ~_EN)
        time.sleep_us(50)

    def _send_nibble(self, nibble, mode):
        # nibble must already be in bits 7-4 of the byte
        self._pulse(nibble | mode | self._bl)

    def _send(self, byte, mode):
        self._send_nibble(byte & 0xF0, mode)
        self._send_nibble((byte & 0x0F) << 4, mode)

    # ── init ──────────────────────────────────────────────────────────────

    def _init(self):
        time.sleep_ms(50)
        self._write_pcf(self._bl)
        time.sleep_ms(50)
        # 3× send function-set in 8-bit mode to ensure known state
        for delay in (5, 1, 1):
            self._send_nibble(0x30, 0)
            time.sleep_ms(delay)
        # Switch to 4-bit mode
        self._send_nibble(0x20, 0)
        time.sleep_ms(1)
        # Function set: 4-bit, 2-line, 5×8
        self._cmd(_FUNC | _FUNC_4BIT | _FUNC_2LINE)
        # Display on, cursor/blink off
        self._cmd(_DISPLAY | self._ctrl)
        self.clear()
        # Entry mode: cursor moves right, no display shift
        self._cmd(_ENTRY | _ENTRY_INC)

    # ── public commands ───────────────────────────────────────────────────

    def _cmd(self, val):
        self._send(val, 0)

    def clear(self):
        self._cmd(_CLEAR)
        time.sleep_ms(2)

    def home(self):
        self._cmd(_HOME)
        time.sleep_ms(2)

    def set_cursor(self, col, row):
        row = min(row, 3)
        self._cmd(0x80 | (col + _ROW_OFFSETS[row]))

    def write(self, text):
        for ch in text:
            self._send(ord(ch), _RS)

    # alias
    print = write

    def backlight(self, on=True):
        self._bl = _BL if on else 0
        self._write_pcf(self._bl)

    def display(self, on=True):
        if on:
            self._ctrl |= _DISP_ON
        else:
            self._ctrl &= ~_DISP_ON
        self._cmd(_DISPLAY | self._ctrl)

    def cursor(self, on=True):
        if on:
            self._ctrl |= _CURSOR_ON
        else:
            self._ctrl &= ~_CURSOR_ON
        self._cmd(_DISPLAY | self._ctrl)

    def blink(self, on=True):
        if on:
            self._ctrl |= _BLINK_ON
        else:
            self._ctrl &= ~_BLINK_ON
        self._cmd(_DISPLAY | self._ctrl)

    def create_char(self, slot, rows):
        """Define custom character (slot 0-7, rows = list of 8 bytes)."""
        self._cmd(0x40 | ((slot & 0x07) << 3))
        for row in rows:
            self._send(row, _RS)
