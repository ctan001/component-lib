from buzzer_active import ActiveBuzzer
import time

buzzer = ActiveBuzzer(14)   # 信號端 S 接 GPIO14

print("蜂鳴器測試...")
buzzer.beep(200)
time.sleep(1)
buzzer.beep_n(3, on_ms=100, off_ms=100)
print("完成")
