"""
_test_oled.py — SH1106 OLED 硬體驗證測試 — 無感應器，純顯示測試。

作者：Jerry（Claude Code 協助撰寫）
建立日期：2026-07-18
最後修改：2026-07-18
相依檔案：oled_sh1106.py

測試涵蓋兩個 SH1106 特有風險點：
1. 全部8個page都要正常顯示（比照oled-128x64-ssd1309的冷開機驗證方式）
2. 132欄GDDRAM的2欄offset在邊界處(欄0與欄127)是否正確，
   若offset算錯，欄127的字會被截斷或整排偏移到看不見

用法：mpremote連線後執行，每個測試頁面顯示3秒，肉眼比對輸出結果跟預期敘述是否一致；
整組循環跑4次方便反覆確認。
"""
from oled_sh1106 import OLED
import time

CYCLES = 4                 # 整組測試循環次數
PAGE_DISPLAY_SECONDS = 3   # 每個測試頁面停留秒數

oled = OLED(sda=4, scl=5)


def test1_all_pages():
    # 測試1：8個page全部顯示
    oled.fill(0)
    oled.text("Page0: HELLO", 0, 0)
    oled.text("Page1: WORLD", 0, 8)
    oled.text("Page2: 12345", 0, 16)
    oled.text("Page3: ABCDE", 0, 24)
    oled.text("Page4: FGHIJ", 0, 32)
    oled.text("Page5: KLMNO", 0, 40)
    oled.text("Page6: PQRST", 0, 48)
    oled.text("Page7: UVWXY", 0, 56)
    oled.show()
    print("測試1：8個page文字已送出，請確認全部8行都正常顯示（無跑版/偏移）。")


def test2_column_offset():
    # 測試2：欄位邊界（欄0與欄127），驗證132欄offset處理正確
    oled.fill(0)
    oled.pixel(0, 30, 1)                 # 最左欄(欄0)點一個像素
    oled.pixel(127, 30, 1)               # 最右欄(欄127)點一個像素
    oled.text("L", 0, 0)                 # 左上角文字，緊貼欄0
    oled.text("R", 120, 0)               # 右上角文字，緊貼欄127
    oled.hline(0, 63, 128, 1)            # 貫穿整排的橫線，確認128欄都能點亮
    oled.show()
    print("測試2：請確認畫面最左邊、最右邊都有點亮，橫線貫穿整個寬度沒有斷開或跑到面板外。")


for cycle in range(CYCLES):
    print(f"--- 第 {cycle + 1}/{CYCLES} 輪 ---")
    test1_all_pages()
    time.sleep(PAGE_DISPLAY_SECONDS)
    test2_column_offset()
    time.sleep(PAGE_DISPLAY_SECONDS)
