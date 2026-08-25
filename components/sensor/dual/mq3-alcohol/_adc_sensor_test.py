from machine import ADC
import time

# Estimate VREF from internal temp sensor (V_temp ~= 0.706V at 27C)
adc_temp = ADC(4)
raw_temp = adc_temp.read_u16()
vref = 0.706 * 65535 / raw_temp if raw_temp > 0 else 3.3
print(f'ADC(4)={raw_temp}  estimated VREF={vref:.3f}V')

adc = ADC(0)   # ADC channel 0 = GPIO26
for i in range(10):
    raw = adc.read_u16()
    v = raw / 65535 * vref
    print(f'ADC0={raw:5d}  V={v:.4f}V')
    time.sleep_ms(300)
