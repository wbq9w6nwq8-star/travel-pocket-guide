#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenStreetMap (Overpass API) を使って観光スポット候補を取得し、
渡航ポケット辞典用の下書き JSON (spots_draft.json) を生成するスクリプト。
"""

import json
import time
import urllib.parse
import urllib.request

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# まずは主要都市からスタート（必要に応じて都市を追加）
TARGET_CITIES = {
    "lisbon": {"name_ja": "リスボン", "lat": 38.7223, "lon": -9.1393, "radius": 4500},
    "seoul": {"name_ja": "ソウル", "lat": 37.5665, "lon": 126.9780, "radius": 6000},
    "sydney": {"name_ja": "シドニー", "lat": -33.8688, "lon": 151.2093, "radius": 5000},
    "melbourne": {"name_ja": "メルボルン", "lat": -37.8136, "lon": 144.9631, "radius": 5000},
    "los-angeles": {"name_ja": "ロサンゼルス", "lat": 34.0522, "lon": -118.2437, "radius": 7000},
    "new-york": {"name_ja": "ニューヨーク", "lat": 40.7128, "lon": -74.0060, "radius": 6000},
}


def query_overpass_spots(lat: float, lon: float, radius: int, limit: int = 8) -> list[dict]:
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"~"attraction|museum|viewpoint"](around:{radius},{lat},{lon});
      way["tourism"~"attraction|museum|viewpoint"](around:{radius},{lat},{lon});
    );
    out center 60;
    """
    data = urllib.parse.urlencode({"data": query}).encode("utf-8")
    req = urllib.request.Request(
        OVERPASS_URL,
        data=data,
        headers={"User-Agent": "TokouPocketSpotDraft/1.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as res:
        payload = json.loads(res.read().decode("utf-8"))

    seen = set()
    candidates = []

    for el in payload.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name:ja") or tags.get("name") or tags.get("name:en")
        if not name or name in seen:
            continue
        seen.add(name)

        tourism_type = tags.get("tourism", "attraction")
        area = (
            tags.get("addr:suburb")
            or tags.get("addr:district")
            or tags.get("addr:city")
            or "市内中心部"
        )

        candidates.append({
            "name": name,
            "area": area,
            "category": tourism_type,
            "desc": "【要編集】現地の特徴や回り方のポイントを追記してください。",
            "best_time": "【要編集】午前／夕方など",
            "caution": "【要編集】混雑・スリ・営業時間などの注意点",
            "source": "OpenStreetMap (Overpass API)"
        })

        if len(candidates) >= limit:
            break

    return candidates


def main() -> None:
    result = {}
    for slug, info in TARGET_CITIES.items():
        print(f"取得中: {info['name_ja']} ({slug}) ...")
        try:
            spots = query_overpass_spots(info["lat"], info["lon"], info["radius"], limit=8)
            result[slug] = {
                "city_name_ja": info["name_ja"],
                "spots": spots
            }
            print(f"  -> {len(spots)}件の候補を取得")
        except Exception as exc:
            print(f"  -> 取得エラー: {exc}")
            result[slug] = {
                "city_name_ja": info["name_ja"],
                "spots": []
            }
        # サーバー負荷軽減のため少し待機
        time.sleep(2)

    with open("spots_draft.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n完了: spots_draft.json に下書きを保存しました。")


if __name__ == "__main__":
    main()
