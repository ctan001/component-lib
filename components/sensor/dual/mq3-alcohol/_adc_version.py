import sys, os
print(sys.version)
print(sys.implementation)
from machine import ADC
adc_temp = ADC(4)
print(f'Temp ADC(4)={adc_temp.read_u16()}')
adc26 = ADC(26)
print(f'ADC26={adc26.read_u16()}')
