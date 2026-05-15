from motor_130 import Motor130
import time

# IN+ 接 GPIO14，IN- 接 GPIO15
motor = Motor130(in_plus_pin=14, in_minus_pin=15)

print("馬達正轉 2 秒...")
motor.forward()
time.sleep(2)

print("停止 1 秒...")
motor.stop()
time.sleep(1)

print("馬達反轉 2 秒...")
motor.reverse()
time.sleep(2)

motor.stop()
print("完成")
