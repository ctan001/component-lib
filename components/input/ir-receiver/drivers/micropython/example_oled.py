"""
example_oled.py — IR 遙控接收 + SSD1309 OLED 顯示

接線：
  IR Receiver: S=GP15, V=3.3V, G=GND
  OLED:        SDA=GP4, SCL=GP5, VDD=3.3V

遙控器：HX1838 17鍵，NEC 協議，Address=0xFF
"""

from ir_receiver import IRReceiver
from oled_ssd1309 import OLED

ir   = IRReceiver(15)
oled = OLED(sda=4, scl=5)

# 實測按鍵碼（address=0x00，17鍵遙控器）
KEY_MAP = {
    0x16: "1",
    0x19: "2",
    0x0D: "3",
    0x0C: "4",
    0x18: "5",
    0x5E: "6",
    0x08: "7",
    0x1C: "8",
    0x5A: "9",
    0x52: "0",
    0x42: "*",
    0x4A: "#",
    0x46: "UP",
    0x15: "DOWN",
    0x44: "LEFT",
    0x43: "RIGHT",
    0x40: "OK",
}


def draw(raw, cmd, name):
    oled.fill(0)
    oled.text("IR Receiver", 16, 0)
    oled.hline(0, 10, 128, 1)
    oled.text("Raw:", 0, 18)
    oled.text(f"0x{raw:08X}", 36, 18)
    oled.text("CMD:", 0, 32)
    oled.text(f"0x{cmd:02X}", 36, 32)
    oled.text("Key:", 0, 46)
    oled.text(name[:10], 36, 46)
    oled.hline(0, 57, 128, 1)
    oled.text("GP15 NEC", 24, 57)
    oled.show()


oled.fill(0)
oled.text("IR Receiver", 16, 0)
oled.hline(0, 10, 128, 1)
oled.text("Waiting...", 20, 28)
oled.show()
print("等待 IR 遙控器信號，Ctrl+C 停止...")

while True:
    code = ir.receive(timeout_ms=100)
    if code is None:
        continue

    cmd     = (code >> 16) & 0xFF
    inv_cmd = (code >> 24) & 0xFF

    if (cmd ^ inv_cmd) != 0xFF:
        # 奇偶校驗失敗 → 長按重複碼或雜訊
        name = "HOLD"
        cmd  = 0xFF
    else:
        name = KEY_MAP.get(cmd, "?")

    draw(code, cmd, name)
    print(f"0x{code:08X}  CMD=0x{cmd:02X}  {name}")
