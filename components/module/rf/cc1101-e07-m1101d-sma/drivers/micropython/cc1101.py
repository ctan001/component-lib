"""
cc1101.py — CC1101 433MHz RF transceiver driver (MicroPython / Pico)

Wiring (E07-M1101D-SMA):
  Pin 2  VCC  → 3.3V      ⚠️ MAX 3.6V
  Pin 1  GND  → GND
  Pin 5  SCK  → GP2  (SPI0)
  Pin 6  MOSI → GP3  (SPI0)
  Pin 7  MISO → GP4  (SPI0)
  Pin 4  CSN  → GP5
  Pin 3  GDO0 → GP6  (OOK data in/out, IRQ)
  Pin 8  GDO2 → GP7  (optional status)
"""

from machine import SPI, Pin
import time

# ── Strobe commands ──────────────────────────────────────
SRES  = 0x30   # Software reset
SCAL  = 0x33   # Calibrate frequency synthesizer
SRX   = 0x34   # Enable RX
STX   = 0x35   # Enable TX
SIDLE = 0x36   # Exit RX/TX, freq synth off
SFRX  = 0x3A   # Flush RX FIFO
SFTX  = 0x3B   # Flush TX FIFO

# ── Register addresses ───────────────────────────────────
IOCFG2   = 0x00
IOCFG1   = 0x01
IOCFG0   = 0x02
FIFOTHR  = 0x03
PKTLEN   = 0x06
PKTCTRL1 = 0x07
PKTCTRL0 = 0x08
CHANNR   = 0x0A
FSCTRL1  = 0x0B
FSCTRL0  = 0x0C
FREQ2    = 0x0D
FREQ1    = 0x0E
FREQ0    = 0x0F
MDMCFG4  = 0x10
MDMCFG3  = 0x11
MDMCFG2  = 0x12
MDMCFG1  = 0x13
MDMCFG0  = 0x14
DEVIATN  = 0x15
MCSM2    = 0x16
MCSM1    = 0x17
MCSM0    = 0x18
FOCCFG   = 0x19
BSCFG    = 0x1A
AGCCTRL2 = 0x1B
AGCCTRL1 = 0x1C
AGCCTRL0 = 0x1D
WOREVT1  = 0x1E
WOREVT0  = 0x1F
WORCTRL  = 0x20
FREND1   = 0x21
FREND0   = 0x22
FSCAL3   = 0x23
FSCAL2   = 0x24
FSCAL1   = 0x25
FSCAL0   = 0x26
TEST2    = 0x2C
TEST1    = 0x2D
TEST0    = 0x2E
PATABLE  = 0x3E   # PA power table (burst write)

# Status registers (read with burst bit 0xC0|addr)
REG_RSSI    = 0x34
REG_MARCST  = 0x35
REG_PARTNUM = 0x30
REG_VERSION = 0x31

# ── OOK Async config for 433.92 MHz ─────────────────────
# Frequency: 433.92 MHz
# Bandwidth: ~60 kHz  (narrow, good SNR for 433 MHz band)
# Modulation: OOK async (GDO0 = demodulated output in RX, data input in TX)
# Note: Flipper Zero shows f=303.87 MHz for nearby CAME devices (garage doors
#       etc.) — not this fan remote. Fan remote confirmed at 433.92 MHz by
#       clean 32-bit captures at RSSI -79 dBm.
OOK_CONFIG = [
    (IOCFG2,   0x0B),  # GDO2: RSSI_VALID
    (IOCFG0,   0x0D),  # GDO0: async serial data (RX out / TX in)
    (FIFOTHR,  0x47),
    (PKTLEN,   0xFF),
    (PKTCTRL1, 0x04),  # no append status
    (PKTCTRL0, 0x32),  # PKT_FORMAT=11(async), CRC off, infinite length
    (CHANNR,   0x00),
    (FSCTRL1,  0x06),  # IF = 152 kHz
    (FSCTRL0,  0x00),
    (FREQ2,    0x0B),  # 303.875 MHz  (Flipper: f=303.87 MHz, CAME protocol)
    (FREQ1,    0xB0),
    (FREQ0,    0x00),
    (MDMCFG4,  0x65),  # BW = 271 kHz, DRATE_E = 5  (AM270 preset, same as Flipper Zero)
    (MDMCFG3,  0x83),  # DRATE_M = 131 → ~3.79 kbps
    (MDMCFG2,  0x34),  # MOD=OOK, no sync word (carrier-sense only)
    (MDMCFG1,  0x22),
    (MDMCFG0,  0xF8),
    (DEVIATN,  0x00),
    (MCSM2,    0x07),
    (MCSM1,    0x20),
    (MCSM0,    0x18),  # auto-cal on IDLE→RX
    (FOCCFG,   0x16),
    (BSCFG,    0x6C),
    (AGCCTRL2, 0x43),  # OOK optimal: MAGN_TARGET=33dB
    (AGCCTRL1, 0x40),
    (AGCCTRL0, 0x91),
    (WOREVT1,  0x87),
    (WOREVT0,  0x6B),
    (WORCTRL,  0xFB),
    (FREND1,   0x56),
    (FREND0,   0x11),
    (FSCAL3,   0xE9),
    (FSCAL2,   0x2A),
    (FSCAL1,   0x00),
    (FSCAL0,   0x1F),
    (TEST2,    0x81),
    (TEST1,    0x35),
    (TEST0,    0x09),
]

# PA table: full power OOK (0xC0 = max, 0x00 = off)
PATABLE_OOK = bytes([0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])


class CC1101:
    def __init__(self, spi_id=0, sck=2, mosi=3, miso=4, cs=5):
        self._spi = SPI(spi_id, baudrate=4_000_000, polarity=0, phase=0,
                        sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
        self._cs = Pin(cs, Pin.OUT, value=1)
        self._reset()
        self.configure_ook()

    # ── Low-level SPI ────────────────────────────────────
    def _strobe(self, cmd):
        self._cs(0); time.sleep_us(2)
        buf = bytearray(1)
        self._spi.write_readinto(bytes([cmd]), buf)
        self._cs(1)
        return buf[0]

    def _write(self, addr, val):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr & 0x3F, val]))
        self._cs(1)

    def _write_burst(self, addr, data):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr | 0x40]) + bytes(data))
        self._cs(1)

    def _read(self, addr):
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr | 0x80]))
        r = bytearray(1)
        self._spi.readinto(r)
        self._cs(1)
        return r[0]

    def _read_status(self, addr):
        """Status registers need R=1 + burst bit = addr | 0xC0"""
        self._cs(0); time.sleep_us(2)
        self._spi.write(bytes([addr | 0xC0]))
        r = bytearray(1)
        self._spi.readinto(r)
        self._cs(1)
        return r[0]

    # ── Reset ─────────────────────────────────────────────
    def _reset(self):
        cs = self._cs
        cs(1); time.sleep_us(5)
        cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(41)
        cs(0); time.sleep_us(10)
        cs(1); time.sleep_us(200)
        self._strobe(SRES)
        time.sleep_ms(10)

    # ── OOK Configuration ─────────────────────────────────
    def configure_ook(self):
        """Load OOK async config + set PA table for OOK TX."""
        self._strobe(SIDLE)
        for addr, val in OOK_CONFIG:
            self._write(addr, val)
        # PA table: index 0 = power when OOK=1, index 1 = power when OOK=0
        self._write_burst(PATABLE, PATABLE_OOK)

    # ── Mode switching ────────────────────────────────────
    def rx(self):
        """Enter RX mode. GDO0 → async demodulated OOK output."""
        self._strobe(SIDLE)
        self._strobe(SFRX)
        self._strobe(SRX)

    def tx(self):
        """Enter TX mode. GDO0 ← async OOK data input from MCU."""
        self._strobe(SIDLE)
        self._strobe(SFTX)
        self._strobe(STX)

    def idle(self):
        self._strobe(SIDLE)

    # ── RSSI ─────────────────────────────────────────────
    def rssi_dbm(self):
        """Return RSSI in dBm."""
        raw = self._read_status(REG_RSSI)
        if raw >= 128:
            return (raw - 256) // 2 - 74
        else:
            return raw // 2 - 74

    # ── Info ──────────────────────────────────────────────
    @property
    def version(self):
        return self._read_status(REG_VERSION)

    @property
    def partnum(self):
        return self._read_status(REG_PARTNUM)
