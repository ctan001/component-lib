"""從所有 component.json 自動生成 index.md

Usage:
  python sync_index.py          # 生成 index.md
  python sync_index.py --check  # 只檢查差異，不寫入

每次驗證元件後、或收工前執行一次，確保 index.md 與 component.json 同步。
"""

import json, os, sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).parent
COMPONENTS_DIR = BASE / "components"
INDEX_PATH = BASE / "index.md"

IFACE_ORDER = ["GPIO", "ADC", "PWM", "I2C", "SPI", "UART", "1-Wire", "DHT", "PIO"]

CATEGORY_ORDER = [
    "board/mcu",
    "actuator",
    "display/7seg",
    "display/lcd",
    "display/led",
    "display/matrix",
    "display/oled",
    "input",
    "module/rfid",
    "module/rtc",
    "sensor/1wire",
    "sensor/analog",
    "sensor/digital",
    "sensor/dual",
    "sensor/gas",
    "sensor/humidity",
    "sensor/imu",
    "sensor/ultrasonic",
]


def load_components():
    entries = []
    for path in sorted(COMPONENTS_DIR.rglob("component.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        # relative link path (forward slashes for markdown)
        rel = path.parent.relative_to(BASE).as_posix()

        driver_ok = "✅" if data.get("drivers", {}).get("micropython") else "❌"

        v = data.get("verification", {})
        status = v.get("status", "pending")
        verified_ok = "✅" if status == "verified" else ("❌" if status == "failed" else "⏳")

        iface_list = data.get("interface", [])
        iface_str = ", ".join(iface_list)

        entries.append({
            "name": data["name"],
            "name_zh": data.get("name_zh", ""),
            "category": data.get("category", ""),
            "interface": iface_str,
            "driver": driver_ok,
            "verified": verified_ok,
            "rel": rel,
        })
    return entries


def sort_key(e):
    cat = e["category"]
    try:
        ci = CATEGORY_ORDER.index(cat)
    except ValueError:
        ci = 999
    return (ci, e["name"])


def build_table(entries):
    rows = []
    for e in sorted(entries, key=sort_key):
        link = f"[{e['name']}]({e['rel']}/)"
        rows.append(
            f"| {link} | {e['name_zh']} | {e['category']} | {e['interface']} "
            f"| {e['driver']} | {e['verified']} |"
        )
    return rows


def build_index(entries):
    today = date.today().isoformat()
    count = len(entries)
    header = f"""# component-lib 元件索引

> 更新時間：{today}
> 元件總數：{count}

| 元件 | 中文名 | 類別 | 介面 | MicroPython Driver | 驗證狀態 |
|:--|:--|:--|:--|:--|:--|
"""
    rows = build_table(entries)
    footer = """
---

驗證狀態：⏳ pending | ✅ verified | ❌ failed
"""
    return header + "\n".join(rows) + "\n" + footer


def check_diff(current_text, new_text):
    if current_text.strip() == new_text.strip():
        return False, []
    current_lines = set(current_text.splitlines())
    new_lines = set(new_text.splitlines())
    added = sorted(new_lines - current_lines)
    removed = sorted(current_lines - new_lines)
    return True, (added, removed)


def main():
    check_only = "--check" in sys.argv

    entries = load_components()
    new_text = build_index(entries)

    if INDEX_PATH.exists():
        current_text = INDEX_PATH.read_text(encoding="utf-8")
        has_diff, diff = check_diff(current_text, new_text)
        if not has_diff:
            print("✅ index.md 已是最新，無需更新。")
            return
        if check_only:
            added, removed = diff
            print(f"⚠️  index.md 與 component.json 有差異：")
            for line in removed:
                if line.startswith("|") and "元件" not in line and "---" not in line:
                    print(f"  - {line.strip()}")
            for line in added:
                if line.startswith("|") and "元件" not in line and "---" not in line:
                    print(f"  + {line.strip()}")
            return
    else:
        if check_only:
            print("⚠️  index.md 不存在，需要生成。")
            return

    INDEX_PATH.write_text(new_text, encoding="utf-8")
    print(f"✅ index.md 已更新，共 {len(entries)} 個元件。")


if __name__ == "__main__":
    main()
