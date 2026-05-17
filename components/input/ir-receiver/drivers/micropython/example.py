from ir_receiver import IRReceiver
import time

# 信號端 S 接 GP15，S 端已有 4.7K 上拉電阻
ir = IRReceiver(15)

print("等待 IR 遙控器信號，Ctrl+C 停止...")
while True:
    code = ir.receive(timeout_ms=100)
    if code is not None:
        print(f"收到：0x{code:08X}")
    time.sleep_ms(10)
