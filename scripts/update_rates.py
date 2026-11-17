import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API_URL = "https://open.er-api.com/v6/latest/JPY"
OUTPUT_PATH = Path("data/rates.json")

def main():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as res:
        data = json.loads(res.read().decode("utf-8"))

    if data.get("result") != "success":
        raise RuntimeError("為替APIの取得に失敗しました")

    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst).strftime("%Y-%m-%d %H:%M JST")

    output = {
        "updated_at": now_jst,
        "base": "JPY",
        "rates": data["rates"]  # 例: {"USD": 0.0065, "GBP": 0.0051, ...}
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated rates at {now_jst}")

if __name__ == "__main__":
    main()