"""
main.py — CC1101 OOK 遙控器捕捉 + 重播

狀態機：
  IDLE       → 等待信號（OLED 顯示 "LISTENING..."）
  CAPTURING  → 偵測到信號，IRQ 計時中
  DECODED    → 解碼完成，OLED 顯示結果
  READY_TX   → 按下按鍵，準備發射
  TX         → 發射中，OLED 顯示 "TRANSMITTING..."

接線：
  CC1101  Pin2 VCC  → 3.3V    CC1101 Pin5 SCK  → GP2
  CC1101  Pin4 CSN  → GP5     CC1101 Pin6 MOSI → GP3
  CC1101  Pin3 GDO0 → GP6     CC1101 Pin7 MISO → GP4
  CC1101  Pin8 GDO2 → GP7 (選用)
  OLED    SDA       → GP10    OLED    SCL       → GP11
  Button            → GP15 / GND
"""

from cc1101    import CC1101
from ook_capture import OOKCapture
from oled_ssd1309 import OLED
from machine import Pin
import time

# ── 硬體初始化 ─────────────────────────────────────────────
print("Init CC1101...")
radio = CC1101(spi_id=0, sck=2, mosi=3, miso=4, cs=5)
print(f"CC1101 version: 0x{radio.version:02X}")   # 期望 0x14

print("Init OLED...")
oled = OLED(sda=10, scl=11)

btn = Pin(15, Pin.IN, Pin.PULL_UP)
cap = OOKCapture(gdo0_pin=6)

# ── OLED helper ────────────────────────────────────────────
def oled_show(lines: list):
    """顯示最多 7 行文字（每行最多 16 字元）"""
    oled.fill(0)
    for i, ln in enumerate(lines[:7]):
        oled.text(str(ln)[:16], 0, i * 9)
    oled.show()

# ── 主狀態機 ───────────────────────────────────────────────
STATE   = 'IDLE'
result  = None     # 最後一次解碼結果

oled_show(["== CC1101 OOK ==", "LISTENING...", "", "Press remote to", "capture signal"])

print("Ready. Press the fan remote...")

while True:

    # ════════════════ IDLE ════════════════════════════════
    if STATE == 'IDLE':
        radio.configure_ook()
        radio.rx()
        STATE = 'CAPTURING'
        oled_show(["== CC1101 OOK ==", "LISTENING...", "", "Press remote to", "capture signal"])
        print("\n[IDLE] Listening...")

    # ════════════════ CAPTURING ═══════════════════════════
    elif STATE == 'CAPTURING':
        # ── RSSI gate: wait for real signal (not background noise) ──
        RSSI_THRESHOLD = -85   # dBm; noise floor ~-97, real signal >-85
        t_gate = time.ticks_add(time.ticks_ms(), 30_000)
        got_signal = False
        while time.ticks_diff(t_gate, time.ticks_ms()) > 0:
            if radio.rssi_dbm() > RSSI_THRESHOLD:
                got_signal = True
                break
            time.sleep_ms(10)

        if not got_signal:
            STATE = 'IDLE'
            continue

        # ── Timed capture: grab one burst (~400ms covers 3-4 repeats) ──
        cap.start_rx()
        time.sleep_ms(400)
        cap.stop()

        pulses = list(cap._buf[:cap._idx])

        if len(pulses) < 10:
            STATE = 'IDLE'
            continue

        print(f"[CAP] {len(pulses)} pulses captured")
        rssi = radio.rssi_dbm()
        radio.idle()

        result = cap.decode(pulses)
        result['rssi'] = rssi
        STATE = 'DECODED'

    # ════════════════ DECODED ═════════════════════════════
    elif STATE == 'DECODED':
        r = result
        hex_str  = r['hex']      or '???'
        proto    = r['protocol'] or '???'
        bits     = r['bit_count']
        T        = r['T_us']
        reps     = r['repeats']
        rssi_val = r.get('rssi', 0)

        print(f"[DEC] Protocol : {proto}")
        print(f"      Code     : {hex_str}  ({bits} bits)")
        print(f"      T        : {T} us")
        print(f"      Repeats  : {reps}")
        print(f"      RSSI     : {rssi_val} dBm")
        print("      [BTN] Press button to retransmit")

        oled_show([
            proto[:16],
            hex_str[:16],
            f"{bits}b T={T}us",
            f"RSSI:{rssi_val}dBm x{reps}",
            "",
            "BTN=TX  Wait=RX",
        ])

        # 等待按鍵 5 秒，否則回去 IDLE 繼續捕捉
        t_end = time.ticks_add(time.ticks_ms(), 10_000)
        while time.ticks_diff(t_end, time.ticks_ms()) > 0:
            if not btn.value():       # 按鍵按下（低電平）
                time.sleep_ms(30)     # debounce
                STATE = 'TX'
                break
            time.sleep_ms(50)
        else:
            STATE = 'IDLE'            # 超時 → 繼續監聽

    # ════════════════ TX ══════════════════════════════════
    elif STATE == 'TX':
        print("[TX] Transmitting...")
        oled_show([
            "TRANSMITTING...",
            result['protocol'][:16],
            result['hex'][:16],
            f"x{result['repeats']} repeats",
        ])

        radio.configure_ook()
        radio.tx()
        time.sleep_ms(5)   # 等 TX PLL 鎖定

        OOKCapture.transmit(
            gdo0_pin = 6,
            pulses   = result['raw'],
            repeats  = max(result['repeats'], 3),
        )

        radio.idle()
        print("[TX] Done")

        oled_show([
            "TX DONE!",
            result['protocol'][:16],
            result['hex'][:16],
            "",
            "BTN=TX again",
            "Wait=listen",
        ])

        # 按鈕繼續發射 / 放開後 3 秒回到 IDLE
        time.sleep_ms(500)
        t_end = time.ticks_add(time.ticks_ms(), 3_000)
        while time.ticks_diff(t_end, time.ticks_ms()) > 0:
            if not btn.value():
                STATE = 'TX'          # 再發一次
                time.sleep_ms(300)
                break
            time.sleep_ms(50)
        else:
            STATE = 'IDLE'
