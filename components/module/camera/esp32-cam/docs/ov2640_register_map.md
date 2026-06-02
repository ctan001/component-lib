# OV2640 Register Map

**Source**: [espressif/esp32-camera ov2640_regs.h](https://github.com/espressif/esp32-camera/blob/master/sensors/private_include/ov2640_regs.h)  
**SCCB Address**: 0x30 (write=0x60, read=0x61)  
**Bank Select**: Register 0xFF (0x00=DSP bank, 0x01=Sensor bank)

---

## DSP Register Bank (0xFF = 0x00)

| Addr | Name | Description |
|:-----|:-----|:------------|
| 0x05 | R_BYPASS | Bypass DSP (bit0: 0=DSP on, 1=bypass) |
| 0x44 | QS | JPEG quantization scale (quality) |
| 0x50 | CTRLI | Horizontal/vertical divider control |
| 0x51 | HSIZE | Horizontal size (low 8 bits) |
| 0x52 | VSIZE | Vertical size (low 8 bits) |
| 0x53 | XOFFL | X offset (low 8 bits) |
| 0x54 | YOFFL | Y offset (low 8 bits) |
| 0x55 | VHYX | High bits for HSIZE/VSIZE/XOFF/YOFF |
| 0x56 | DPRP | Reserved |
| 0x57 | TEST | Test pattern (bit7: color bar) |
| 0x5A | ZMOW | Zoom output width (low 8 bits) |
| 0x5B | ZMOH | Zoom output height (low 8 bits) |
| 0x5C | ZMHH | High bits for ZMOW/ZMOH |
| 0x7C | BPADDR | SDE indirect register address |
| 0x7D | BPDATA | SDE indirect register data |
| 0x86 | CTRL2 | DCW enable, SDE enable, UV average, CMX enable |
| 0x87 | CTRL3 | BPC, WPC, interpolation control |
| 0x8C | SIZEL | Low bits for HSIZE8/VSIZE8 |
| 0xC0 | HSIZE8 | Image output horizontal size / 8 |
| 0xC1 | VSIZE8 | Image output vertical size / 8 |
| 0xC2 | CTRL0 | AEC enable, YUV422, YUV, RGB, RAW sel |
| 0xDA | IMAGE_MODE | Image output format control |
| 0xD7 | R_DVP_SP | DVP speed and auto mode |
| 0xE0 | RESET | Module reset control |

### CTRL0 (0xC2) Bit Definitions

| Bit | Mask | Name | Description |
|:----|:-----|:-----|:------------|
| 7 | 0x80 | AEC_EN | Auto exposure enable |
| 6 | 0x40 | AEC_SEL | AEC method select |
| 5 | 0x20 | STAT_SEL | Statistics select |
| 4 | 0x10 | VFIRST | YUV byte order |
| 3 | 0x08 | YUV422 | YUV422 output enable |
| 2 | 0x04 | YUV_EN | YUV output enable |
| 1 | 0x02 | RGB_EN | RGB output enable |
| 0 | 0x01 | RAW_EN | RAW output enable |

### IMAGE_MODE (0xDA) Bit Definitions

| Bit | Mask | Name | Description |
|:----|:-----|:-----|:------------|
| 4 | 0x10 | JPEG_EN | JPEG output enable |
| 3 | 0x08 | DVP_OUT_FMT_MSB | Output format bit 1 |
| 2 | 0x04 | DVP_OUT_FMT_LSB | Output format bit 0 |
| 1 | 0x02 | HREF_TIMING | HREF timing select |
| 0 | 0x01 | BYTE_SWAP | Byte swap (big/little endian) |

Output Format (bits [3:2]):
- 00 = YUV422
- 01 = RAW10 (DVP)
- 10 = RGB565
- 11 = Reserved

### RESET (0xE0) Bit Definitions

| Bit | Mask | Name | Description |
|:----|:-----|:-----|:------------|
| 6 | 0x40 | MICROC | Microcontroller reset |
| 5 | 0x20 | SCCB | SCCB reset |
| 4 | 0x10 | JPEG | JPEG module reset |
| 2 | 0x04 | DVP | DVP interface reset |
| 1 | 0x02 | IPU | Image processing reset |
| 0 | 0x01 | CIF | CIF module reset |

### CTRL2 (0x86) Bit Definitions

| Bit | Mask | Description |
|:----|:-----|:------------|
| 5 | 0x20 | DCW enable (downsize/crop/window) |
| 4 | 0x10 | SDE enable (special digital effects) |
| 3 | 0x08 | UV average enable |
| 2 | 0x04 | UV adjust enable |
| 1 | 0x02 | CMX enable (color matrix) |

### CTRL3 (0x87) Bit Definitions

| Bit | Mask | Description |
|:----|:-----|:------------|
| 7 | 0x80 | BPC enable (black pixel correction) |
| 6 | 0x40 | WPC enable (white pixel correction) |

---

## Sensor Register Bank (0xFF = 0x01)

| Addr | Name | Description |
|:-----|:-----|:------------|
| 0x00 | GAIN | AGC gain (low 8 bits) |
| 0x03 | COM1 | Common control 1 (dummy frame, VWIN low bits) |
| 0x04 | REG04 | Mirror, flip, AEC high bits |
| 0x08 | REG08 | Frame exposure one-pin control |
| 0x09 | COM2 | Common control 2 (soft standby, drive strength) |
| 0x0A | REG_PID | Product ID high byte (should be 0x26) |
| 0x0B | REG_VER | Product ID low byte (should be 0x42) |
| 0x0C | COM3 | Common control 3 (swap, mirror, band filter) |
| 0x0D | COM4 | Common control 4 (clock output) |
| 0x10 | AEC | Exposure value (mid 8 bits) |
| 0x11 | CLKRC | Clock rate control |
| 0x12 | COM7 | Common control 7 (reset, resolution, zoom) |
| 0x13 | COM8 | Common control 8 (banding, AGC, AEC enable) |
| 0x14 | COM9 | Common control 9 (AGC gain ceiling) |
| 0x15 | COM10 | Common control 10 (PCLK, HREF, VSYNC) |
| 0x17 | HSTART | Horizontal window start |
| 0x18 | HSTOP | Horizontal window stop |
| 0x19 | VSTART | Vertical window start |
| 0x1A | VSTOP | Vertical window stop |
| 0x1C | MIDH | Manufacturer ID high byte (0x7F = OmniVision) |
| 0x1D | MIDL | Manufacturer ID low byte (0xA2) |
| 0x24 | AEW | Luminance signal high range (AEC upper limit) |
| 0x25 | AEB | Luminance signal low range (AEC lower limit) |
| 0x26 | VV | Fast AEC/Slow AEC step thresholds |
| 0x2A | REG2A | Line interval adjust (high bits) |
| 0x2B | FRARL | Frame rate adjust (low bits) |
| 0x2D | ADDVSL | Dummy line low 8 bits |
| 0x2E | ADDVSH | Dummy line high 8 bits |
| 0x32 | YAVG | Y average control |
| 0x46 | FLL | Frame length low byte |
| 0x47 | FLH | Frame length high byte |
| 0x48 | COM19 | Zoom mode vertical window start |
| 0x4B | COM22 | Flash light control |
| 0x4E | COM25 | Exposure control for 50Hz |
| 0x4F | BD50 | 50Hz banding AEC 8-bit |
| 0x50 | BD60 | 60Hz banding AEC 8-bit |
| 0x5D | BD50MAX | 50Hz banding max step |
| 0x5E | BD60MAX | 60Hz banding max step |

### REG04 (0x04) Bit Definitions

| Bit | Mask | Name | Description |
|:----|:-----|:-----|:------------|
| 7 | 0x80 | HFLIP_IMG | Horizontal mirror |
| 6 | 0x40 | VFLIP_IMG | Vertical flip |
| 5 | 0x20 | VREF_EN | VREF enable |

### COM7 (0x12) Resolution Modes

| Bits [6:4] | Mode |
|:------------|:-----|
| 0x00 | UXGA (1600x1200) |
| 0x40 | SVGA (800x600) |
| 0x20 | CIF (352x288) |
| 0x10 | (reserved) |

### COM8 (0x13) Control

| Bit | Mask | Description |
|:----|:-----|:------------|
| 5 | 0x20 | Banding filter enable |
| 2 | 0x04 | AGC auto enable |
| 0 | 0x01 | AEC auto enable |

### COM9 (0x14) AGC Gain Ceiling

| Bits [7:5] | Gain |
|:------------|:-----|
| 000 | 2x |
| 001 | 4x |
| 010 | 8x |
| 011 | 16x |
| 100 | 32x |
| 101 | 64x |
| 110 | 128x |

### CLKRC (0x11) Clock

| Bit | Description |
|:----|:------------|
| 7 | 0 = use XCLK, 1 = use 2x XCLK |
| [5:0] | Clock divider (0 = no divide, 1 = /2, N = /(N+1)) |

---

## OV2640 Key Specifications

| Item | Value |
|:-----|:------|
| Product ID (PID) | 0x26 (reg 0x0A) |
| Version (VER) | 0x42 (reg 0x0B) |
| Manufacturer ID | 0x7FA2 (regs 0x1C, 0x1D) |
| Max Resolution | UXGA 1600x1200 |
| Pixel Size | 2.2um x 2.2um |
| Output Formats | JPEG, YUV422/420, RGB565/555, RAW8/10 |
| SCCB Address | 0x30 (7-bit) |
| Max Frame Rate | UXGA 15fps, SVGA 30fps, CIF 60fps |
| Power (UXGA YUV) | 125 mW |
| Power (UXGA JPEG) | 140 mW |

---

## Driver Function Summary (from ov2640.c)

| Function | Range | Notes |
|:---------|:------|:------|
| set_pixformat | RGB565/888, YUV422, GRAY, JPEG | |
| set_framesize | 96x96 to UXGA | Auto PLL/window config |
| set_quality | 0-63 | via QS register |
| set_brightness | -2 to +2 | 7 preset levels |
| set_contrast | -2 to +2 | 7 preset levels |
| set_saturation | -2 to +2 | 7 preset levels |
| set_sharpness | N/A | Unsupported on OV2640 |
| set_agc_gain | 0-30 | Lookup table |
| set_aec_value | 0-1200 | 3-register spread |
| set_ae_level | -2 to +2 | 7 levels |
| set_wb_mode | 0-4 | Auto/Sunny/Cloudy/Office/Home |
| set_special_effect | 0-6 | None/Neg/Gray/R/G/B/Sepia |
| set_hmirror | 0/1 | REG04 bit 7 |
| set_vflip | 0/1 | REG04 bit 6 |
| set_colorbar | 0/1 | Test pattern |
