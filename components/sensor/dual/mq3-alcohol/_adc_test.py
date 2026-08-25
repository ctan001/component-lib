from machine import ADC, Pin
import time
adc26 = ADC(26)
adc27 = ADC(27)
adc28 = ADC(28)
adc_temp = ADC(4)
for i in range(3):
    print(f'ADC26={adc26.read_u16()}  ADC27={adc27.read_u16()}  ADC28={adc28.read_u16()}  Temp={adc_temp.read_u16()}')
    time.sleep_ms(300)
