from machine import ADC, Pin, mem32
import time

ADC_BASE = 0x4004c000

# Clear ERR_STICKY (bit 10 = write 1 to clear)
mem32[ADC_BASE] = mem32[ADC_BASE] | (1 << 10)
time.sleep_ms(5)

cs = mem32[ADC_BASE]
print(f'CS after clear: {hex(cs)}, ERR={( cs>>9)&1}, ERR_STICKY={(cs>>10)&1}')

# Try ADC(0) - channel number style (user suggestion)
adc0 = ADC(0)        # ADC channel 0 = GPIO26
adc1 = ADC(1)        # ADC channel 1 = GPIO27
adc2 = ADC(2)        # ADC channel 2 = GPIO28
adc4 = ADC(4)        # internal temp sensor

time.sleep_ms(10)
print(f'ADC(0)={adc0.read_u16()}  ADC(1)={adc1.read_u16()}  ADC(2)={adc2.read_u16()}  ADC(4)={adc4.read_u16()}')

# Check ERR again
cs2 = mem32[ADC_BASE]
print(f'CS after read: {hex(cs2)}, ERR={(cs2>>9)&1}, ERR_STICKY={(cs2>>10)&1}')

# Also try VSYS (ADC3/GPIO29)
adc3 = ADC(3)
print(f'ADC(3) VSYS_raw={adc3.read_u16()}')
