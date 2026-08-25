from machine import mem32, ADC
import time

ADC_BASE = 0x4004c000
cs = mem32[ADC_BASE]
print(f'ADC CS register = {hex(cs)}')
print(f'  EN={cs&1}  TS_EN={(cs>>1)&1}  READY={(cs>>8)&1}  ERR={(cs>>9)&1}  ERR_STICKY={(cs>>10)&1}')
print(f'  AINSEL={(cs>>12)&7}')

# Enable ADC, enable temp sensor
mem32[ADC_BASE] = (1<<1) | (1<<0)  # EN=1, TS_EN=1
time.sleep_ms(10)
cs2 = mem32[ADC_BASE]
print(f'After EN: READY={(cs2>>8)&1}')

adc4 = ADC(4)
print(f'ADC(4) temp = {adc4.read_u16()}')

adc26 = ADC(26)
print(f'ADC(26) = {adc26.read_u16()}')

# Try read_uv if available
try:
    print(f'ADC(4) uv = {adc4.read_uv()}')
    print(f'ADC(26) uv = {adc26.read_uv()}')
except AttributeError:
    print('read_uv not available')
