from servo import Servo
import time

servo = Servo(14)   # PWM 信號端接 GPIO14

print("舵機測試：0° → 90° → 180° → 90°")
servo.min()
time.sleep(1)
servo.center()
time.sleep(1)
servo.max()
time.sleep(1)
servo.center()
time.sleep(1)

print("掃描 0°-180°...")
for deg in range(0, 181, 10):
    servo.angle(deg)
    time.sleep_ms(100)
for deg in range(180, -1, -10):
    servo.angle(deg)
    time.sleep_ms(100)

servo.deinit()
print("完成")
