from machine import mem32
import time

# Check clk_adc configuration
# CLOCKS_BASE = 0x40008000
# clk_adc_ctrl at offset 0x60, div at 0x64, selected at 0x68
CLK_BASE = 0x40008000
clk_adc_ctrl = mem32[CLK_BASE + 0x60]
clk_adc_div  = mem32[CLK_BASE + 0x64]
clk_adc_sel  = mem32[CLK_BASE + 0x68]

print(f'clk_adc_ctrl = {hex(clk_adc_ctrl)}')
print(f'  EN={(clk_adc_ctrl>>11)&1}  AUXSRC={(clk_adc_ctrl>>5)&0xF}')
print(f'clk_adc_div  = {hex(clk_adc_div)}')
print(f'clk_adc_sel  = {hex(clk_adc_sel)}')

# Check USB PLL status
# PLL_USB_BASE = 0x4002c000
PLL_USB = 0x4002c000
pll_cs  = mem32[PLL_USB]
pll_pwd = mem32[PLL_USB + 0x04]
print(f'PLL_USB CS = {hex(pll_cs)}, LOCK={(pll_cs>>31)&1}, BYPASS={(pll_cs>>8)&1}')

# Check if clk_adc EN bit is set, and AUXSRC=0 means USB PLL (48MHz)
# AUXSRC: 0=PLL_USB, 1=PLL_SYS, 2=ROSC, 3=XOSC
print(f'clk_adc enabled: {bool((clk_adc_ctrl>>11)&1)}')
print(f'clk_adc source: {(clk_adc_ctrl>>5)&0xF} (0=PLL_USB/48MHz)')
