from speaker_8002b import Speaker8002B
import time

speaker = Speaker8002B(14)   # IN 接 GPIO14

# 簡單旋律：Do Re Mi
MELODY = [
    (262, 300), (294, 300), (330, 300), (349, 300),
    (392, 300), (440, 300), (494, 300), (523, 500),
    (0,   200),
]

print("播放旋律...")
speaker.play_melody(MELODY)
print("完成")
speaker.deinit()
