from mfrc522 import MFRC522
import time

# SCK=GPIO2, MOSI=GPIO3, MISO=GPIO4, CS=GPIO5, RST=GPIO6
rfid = MFRC522(sck=2, mosi=3, miso=4, cs=5, rst=6)

print("RFID 讀卡器就緒，請刷卡...")
while True:
    status, tag_type = rfid.request(rfid.REQIDL)
    if status == rfid.OK:
        status, uid = rfid.anticoll()
        if status == rfid.OK:
            uid_str = ":".join(f"{b:02X}" for b in uid[:4])
            print(f"UID: {uid_str}")
            time.sleep_ms(500)
    time.sleep_ms(50)
