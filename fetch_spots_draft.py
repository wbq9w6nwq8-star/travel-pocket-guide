#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本語Wikipedia API を使って全都市の観光スポット候補を自動取得し、
spots_draft.json に保存するスクリプト（全都市対応・差分更新）
"""

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from cities_data import generate_cities_data

WIKI_API = "https://ja.wikipedia.org/w/api.php"
OUTPUT_PATH = Path("spots_draft.json")


def wiki_request(params: dict) -> dict:
    params = {**params, "format": "json"}
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "TokouPocketBot/2.0 (https://tokou-pocket.com)"},
    )
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode("utf-8"))


def fetch_city_spots(city: dict, limit: int = 5) -> list[dict]:
    name_ja = city.get("name_ja", "")
    lat = city.get("lat")
    lon = city.get("lon")
    titles = []

    # 1. 緯度経度があれば周辺記事（geosearch）を優先取得
    if lat is not None and lon is not None:
        try:
            geo = wiki_request({
                "action": "query",
                "list": "geosearch",
                "gscoord": f"{lat}|{lon}",
                "gsradius": 8000,
                "gslimit": 15,
            })
            for item in geo.get("query", {}).get("geosearch", []):
                t = item.get("title", "")
                if t and t != name_ja and "駅" not in t and "空港" not in t:
                    titles.append(t)
        except Exception:
            pass

    # 2. 足りない場合は検索APIで補完
    if len(titles) < limit:
        try:
            sr = wiki_request({
                "action": "query",
                "list": "search",
                "srsearch": f"{name_ja} 観光 名所",
                "srlimit": 10,
            })
            for item in sr.get("query", {}).get("search", []):
                t = item.get("title", "")
                if t and t != name_ja and t not in titles and "の一覧" not in t:
                    titles.append(t)
        except Exception:
            pass

    titles = titles[:limit]
    if not titles:
        return []

    # 3. 概要文（extract）を一括取得
    spots = []
    try:
        ext = wiki_request({
            "action": "query",
            "prop": "extracts",
            "exintro": 1,
            "explaintext": 1,
            "exsentences": 2,
            "titles": "|".join(titles),
        })
        pages = ext.get("query", {}).get("pages", {})
        by_title = {p.get("title"): p.get("extract", "") for p in pages.values()}
        for t in titles:
            desc = (by_title.get(t) or "").replace("\n", " ").strip()
            if len(desc) > 110:
                desc = desc[:107].rstrip("、。") + "…"
            spots.append({
                "name": t,
                "area": f"{name_ja}エリア",
                "desc": desc or f"{name_ja}を代表する見どころのひとつです。",
                "best_time": "午前〜日中の明るい時間帯",
                "caution": "営業時間・休館日・混雑状況は訪問前に公式情報をご確認ください。",
                "source": "Wikipedia (ja)",
            })
    except Exception:
        pass

    return spots


def main() -> None:
    existing = {}
    if OUTPUT_PATH.exists():
        try:
            existing = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    cities = generate_cities_data()
    updated = 0

    for city in cities:
        slug = city["slug"]
        # すでにスポットが入っている都市はスキップ（差分更新）
        if existing.get(slug, {}).get("spots"):
            continue

        spots = fetch_city_spots(city, limit=5)
        existing[slug] = {
            "city_name_ja": city.get("name_ja", slug),
            "spots": spots,
        }
        updated += 1
        print(f"[{updated}] {city.get('name_ja', slug)} ({slug}): {len(spots)}件取得")
        time.sleep(0.2)

    OUTPUT_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完了: spots_draft.json を更新しました（新規取得 {updated} 都市 / 合計 {len(existing)} 都市）。")


if __name__ == "__main__":
    main()
