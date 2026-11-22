#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_climate_normals.py ― 概算の気候データを、実測（再解析）の月別平年値に置き換えるスクリプト

【何をするか】
  Open-Meteo の過去気象API（https://open-meteo.com/en/docs/historical-weather-api）から、
  各都市の日別データ（最高気温・最低気温・降水量・日照時間）を取得し、月別に集計して
  climate_data_measured.py を書き出します。

  - 書き出された都市は、climate_calendar.py が自動的に優先して使い、
    画面の出典表記も「WMO平年値…をもとに算出」側に切り替わります。
  - 湿度とUV指数は取得しません。既存（概算）の値をそのまま引き継ぎます。
  - 降水日数は「1mm以上の日」を数えます。再解析データは弱い雨の日を多めに数える傾向があるため、
    --wet-threshold で調整できます（既定 1.0）。

【使い方】（インターネット接続が必要）
  python3 fetch_climate_normals.py --all-estimates          # 概算データの全都市
  python3 fetch_climate_normals.py --slugs guam,barcelona   # 指定した都市だけ
  python3 fetch_climate_normals.py --years 2001-2020        # 集計期間（既定 2001-2020）
  python3 fetch_climate_normals.py --sleep 5                # リクエスト間隔(秒)

  取得結果は climate_cache/<slug>.json にキャッシュされるので、途中で止まっても再実行で続きから進みます。
  無料枠の上限に当たった場合は、時間をおいて再実行してください。

【注意】
  - このスクリプトは作成時点でネットワークのない環境で書かれており、集計部分だけをテストしています。
    初回は --slugs で1〜2都市だけ試し、出力が既存の概算値と大きくずれていないか確認してください。
  - 出力後は `python3 setup_and_build.py` を実行し、QAの警告と出力ページを必ず確認してください。
"""
import argparse
import json
import pprint
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

API = "https://archive-api.open-meteo.com/v1/archive"
CACHE_DIR = Path("climate_cache")
OUT_FILE = Path("climate_data_measured.py")


def fetch_daily(lat: float, lon: float, y0: int, y1: int, retries: int = 4) -> dict:
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": f"{y0}-01-01", "end_date": f"{y1}-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunshine_duration",
        "timezone": "auto",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    wait = 10
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # 429/5xx/一時的な通信エラー
            if attempt == retries:
                raise
            print(f"    再試行 {attempt}/{retries - 1}（{e}）… {wait}秒待ちます", file=sys.stderr)
            time.sleep(wait)
            wait *= 2


def aggregate(daily: dict, wet_threshold: float = 1.0):
    """日別データ → 月別 (tmax, tmin, rain_mm, rain_days, sun_h)。12要素のリストを返す。"""
    times = daily["time"]
    tmax_l, tmin_l = daily["temperature_2m_max"], daily["temperature_2m_min"]
    prec_l, sun_l = daily["precipitation_sum"], daily.get("sunshine_duration") or [None] * len(times)

    tmax_s, tmin_s, sun_s = defaultdict(list), defaultdict(list), defaultdict(list)
    rain_year_sum = defaultdict(float)   # (年, 月) -> 降水量合計
    wet_year_cnt = defaultdict(int)      # (年, 月) -> 1mm以上の日数
    years = set()
    for t, tx, tn, pr, su in zip(times, tmax_l, tmin_l, prec_l, sun_l):
        y, m = int(t[:4]), int(t[5:7])
        years.add(y)
        if tx is not None:
            tmax_s[m].append(tx)
        if tn is not None:
            tmin_s[m].append(tn)
        if su is not None:
            sun_s[m].append(su / 3600.0)
        if pr is not None:
            rain_year_sum[(y, m)] += pr
            if pr >= wet_threshold:
                wet_year_cnt[(y, m)] += 1
    ny = max(1, len(years))
    out = []
    for m in range(1, 13):
        mean = lambda xs: (sum(xs) / len(xs)) if xs else 0.0
        rain_mm = sum(v for (y, mm), v in rain_year_sum.items() if mm == m) / ny
        wet = sum(v for (y, mm), v in wet_year_cnt.items() if mm == m) / ny
        out.append((round(mean(tmax_s[m])), round(mean(tmin_s[m])), round(rain_mm), round(wet), round(mean(sun_s[m]), 1)))
    return out


def main():
    ap = argparse.ArgumentParser(description="月別気候データ（実測集計）を取得して climate_data_measured.py を作る")
    ap.add_argument("--slugs", default="", help="対象都市（カンマ区切り）")
    ap.add_argument("--all-estimates", action="store_true", help="概算データ(basis=estimate)の都市すべて")
    ap.add_argument("--years", default="2001-2020", help="集計期間 例: 2001-2020")
    ap.add_argument("--wet-threshold", type=float, default=1.0, help="降水日とみなす降水量(mm)")
    ap.add_argument("--sleep", type=float, default=3.0, help="都市ごとの待ち時間(秒)")
    args = ap.parse_args()

    sys.path.insert(0, ".")
    import climate_calendar as cc
    from cities_data import CITY_COORDS

    y0, y1 = [int(x) for x in args.years.split("-")]
    if args.all_estimates:
        slugs = [s for s, p in cc.CITY_MONTHLY_CLIMATE.items() if p.get("basis") == "estimate"]
    else:
        slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    if not slugs:
        ap.error("--slugs か --all-estimates を指定してください")

    CACHE_DIR.mkdir(exist_ok=True)
    measured = {}
    # 既に出力済みの measured を引き継ぐ
    if OUT_FILE.exists():
        ns = {}
        exec(OUT_FILE.read_text(encoding="utf-8"), ns)
        measured.update(ns.get("MEASURED_CITY_CLIMATE", {}))

    for slug in slugs:
        base = cc.CITY_MONTHLY_CLIMATE.get(slug)
        if base is None or slug not in CITY_COORDS:
            print(f"- {slug}: 既存データまたは座標がないためスキップ")
            continue
        cache = CACHE_DIR / f"{slug}_{y0}-{y1}.json"
        if cache.exists():
            daily = json.loads(cache.read_text(encoding="utf-8"))
            print(f"- {slug}: キャッシュを使用")
        else:
            lat, lon = CITY_COORDS[slug]
            print(f"- {slug}: 取得中（{y0}-{y1}）…")
            daily = fetch_daily(lat, lon, y0, y1)["daily"]
            cache.write_text(json.dumps(daily), encoding="utf-8")
            time.sleep(args.sleep)
        agg = aggregate(daily, args.wet_threshold)
        old = base["months"]
        months = [(a[0], a[1], a[2], a[3], old[i][4], a[4], old[i][6]) for i, a in enumerate(agg)]
        # 比較表示（概算との差）
        d_tmax = sum(abs(months[i][0] - old[i][0]) for i in range(12)) / 12
        d_rain = sum(abs(months[i][2] - old[i][2]) for i in range(12)) / 12
        print(f"    概算との平均差: 最高気温 {d_tmax:.1f}℃ / 月降水量 {d_rain:.0f}mm")
        entry = {k: v for k, v in base.items() if k not in ("months", "basis")}
        entry["months"] = months
        measured[slug] = entry

    header = '# -*- coding: utf-8 -*-\n"""fetch_climate_normals.py により自動生成。手で編集した場合は再実行で上書きされます。"""\n\n'
    # repr 形式で書き出す（int のキーやタプルを保つため json は使わない）
    OUT_FILE.write_text(header + "MEASURED_CITY_CLIMATE = " + pprint.pformat(measured, width=140, sort_dicts=False) + "\n", encoding="utf-8")
    print(f"\n{OUT_FILE} に {len(measured)} 都市を書き出しました。次に python3 setup_and_build.py を実行してください。")


if __name__ == "__main__":
    main()
