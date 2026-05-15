from ds1307 import DS1307
import time

# SDA 接 GPIO4，SCL 接 GPIO5
rtc = DS1307(sda=4, scl=5)

# 首次使用請先設定時間（之後可以注解掉）
# rtc.set_datetime(year=2026, month=5, date=14, hour=12, minute=0, second=0)

print(f"時鐘運行中：{rtc.is_running()}")
while True:
    dt = rtc.get_datetime()
    print(f"{dt['year']}-{dt['month']:02d}-{dt['date']:02d} "
          f"{dt['hour']:02d}:{dt['minute']:02d}:{dt['second']:02d}")
    time.sleep(1)
