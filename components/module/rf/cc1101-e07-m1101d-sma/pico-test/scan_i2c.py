"""
scan_i2c.py — 掃描 I2C1 (GP10/GP11) 上的裝置
"""
from machine import I2C, Pin

print("掃描 I2C1 (SDA=GP10, SCL=GP11)...")
i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=100_000)
devices = i2c.scan()

if devices:
    print(f"找到 {len(devices)} 個裝置：")
    for addr in devices:
        print(f"  0x{addr:02X}")
else:
    print("❌ 沒有找到任何裝置")
    print("   → 檢查 SDA/SCL 有沒有接反")
    print("   → 確認 VCC=3.3V, GND 有接")
    print("   → 確認 GP10=SDA, GP11=SCL")
