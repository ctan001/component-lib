from machine import ADC, mem32
import time

# Datasheet 4.9 NOTE: IE must be low, OD must be high for ADC pins
# PADS_BANK0_BASE = 0x4001c000
# Pad register: 0x4001c004 + gpio*4
for gpio in [26, 27, 28]:
    pad_addr = 0x4001c000 + 0x04 + gpio * 0x04
    # OD=1 (bit7), IE=0 (bit6), no pull-up/down (bit3/2=0)
    mem32[pad_addr] = 0x80
    print(f'GPIO{gpio} pad reg = {hex(mem32[pad_addr])}')

time.sleep_ms(10)

adc26 = ADC(26)
adc27 = ADC(27)
adc28 = ADC(28)
adc_temp = ADC(4)

for i in range(5):
    print(f'ADC26={adc26.read_u16()}  ADC27={adc27.read_u16()}  ADC28={adc28.read_u16()}  Temp={adc_temp.read_u16()}')
    time.sleep_ms(200)
