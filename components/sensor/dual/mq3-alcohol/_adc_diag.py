from machine import ADC, Pin
import time
adc = ADC(26)
samples = []
for i in range(20):
    v = adc.read_u16()
    samples.append(v)
    time.sleep_ms(50)
mn = min(samples)
mx = max(samples)
avg = sum(samples)//len(samples)
print(f'min={mn}  max={mx}  avg={avg}')
print(f'samples={samples}')
