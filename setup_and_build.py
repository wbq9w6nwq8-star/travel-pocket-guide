#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビルド実行エンジン (setup_and_build.py)
- 全都市共通ルールによるデータ自動正規化（地域統一・同音都市区別・時差自動算出・距離ベース周辺都市）
- 都市別1年カレンダー自動評価 ＆ 公開前QAチェック（重複・矛盾検出）
- 同国優先＋地理的距離を考慮した自然な2都市比較ペアの自動生成
- OGPサムネイル画像 (ogp.png) とファビコン (youka.png) を dist/ に自動コピー
"""

import json
import math
import re
import shutil
import urllib.request
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from config import SITE_URL, SITE_NAME, OGP_IMAGE_FILENAME, FAVICON_FILENAME, COMPARE_PAIRS, FEATURE_PAGES
from cities_data import generate_cities_data
from climate_calendar import evaluate_city_calendar, run_calendar_qa
from templates import (
    build_city_html, build_index_html, build_policy_html,
    build_compare_html, build_feature_html
)

# 地域タブの重複を防ぐ正規化マップ（全都市共通）
REGION_NORMALIZE_MAP = {
    "アジア・中央アジア": "アジア",
    "中央アジア": "アジア",
    "北米・ハワイ": "北米",
    "ハワイ": "北米",
    "中東・ヨーロッパ": "中東・アフリカ",
    "中東": "中東・アフリカ",
    "アフリカ": "中東・アフリカ",
}


def fetch_exchange_rates() -> dict:
    api_url = "https://open.er-api.com/v6/latest/JPY"
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst).strftime("%Y-%m-%d %H:%M JST")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            if data.get("result") == "success":
                return {"updated_at": now_jst, "base": "JPY", "rates": data["rates"]}
    except Exception:
        pass

    return {
        "updated_at": now_jst,
        "base": "JPY",
        "rates": {
            "USD": 0.0065, "EUR": 0.0061, "GBP": 0.0051, "KRW": 9.1, "TWD": 0.21,
            "THB": 0.22, "SGD": 0.0087, "VND": 165.0, "PHP": 0.38, "MYR": 0.029,
            "IDR": 103.0, "HKD": 0.050, "MOP": 0.052, "CNY": 0.047, "INR": 0.55,
            "LKR": 1.9, "NPR": 0.88, "UZS": 83.0, "KZT": 3.2, "CAD": 0.0091,
            "MXN": 0.13, "PEN": 0.024, "BOB": 0.045, "CLP": 6.3, "BRL": 0.038,
            "ARS": 6.4, "CHF": 0.0057, "CZK": 0.15, "ISK": 0.90, "HUF": 2.45,
            "SEK": 0.070, "NOK": 0.072, "DKK": 0.045, "PLN": 0.026, "AUD": 0.010,
            "NZD": 0.011, "FJD": 0.015, "XPF": 0.73, "AED": 0.024, "TRY": 0.22,
            "QAR": 0.024, "EGP": 0.32, "MAD": 0.065, "ZAR": 0.12
        }
    }


def _clean_text(text: str) -> str:
    """括弧の入れ子や余分な空白を全都市共通で整形"""
    if not isinstance(text, str):
        return text
    text = re.sub(r"\(([^()]*)\(([^()]*)\)([^()]*)\)", r"（\1・\2\3）", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _haversine_km(c1: dict, c2: dict) -> float:
    lat1, lon1 = c1.get("lat"), c1.get("lon")
    lat2, lon2 = c2.get("lat"), c2.get("lon")
    if None in (lat1, lon1, lat2, lon2):
        return 99999.0
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _calc_japan_time_diff(tz_name: str) -> tuple[float | None, str]:
    """IANAタイムゾーンから日本(JST)との現在の時差と表示ラベルを自動算出"""
    if not tz_name:
        return None, "現地時刻参照"
    try:
        now_utc = datetime.now(timezone.utc)
        jst_offset = now_utc.astimezone(ZoneInfo("Asia/Tokyo")).utcoffset()
        local_offset = now_utc.astimezone(ZoneInfo(tz_name)).utcoffset()
        if jst_offset is None or local_offset is None:
            return None, "現地時刻参照"
        diff_hours = (local_offset - jst_offset).total_seconds() / 3600.0
        if diff_hours == 0:
            return 0.0, "時差なし（日本と同じ）"
        sign = "+" if diff_hours > 0 else ""
        if diff_hours.is_integer():
            return diff_hours, f"{sign}{int(diff_hours)}時間"
        return diff_hours, f"{sign}{diff_hours:.1f}時間"
    except Exception:
        return None, "現地時刻参照"


def enhance_all_cities(cities: list) -> list:
    """全都市に共通ルールで正規化・カレンダー・時差・周辺都市・スポット統合を適用"""
    draft_path = Path("spots_draft.json")
    spots_map = {}
    if draft_path.exists():
        try:
            spots_map = json.loads(draft_path.read_text(encoding="utf-8"))
        except Exception:
            spots_map = {}

    # 1. 同音異字（読みが重複する都市）を全都市から自動検出
    primary_readings = []
    for c in cities:
        kw = (c.get("kana_kw") or "").strip().split()
        primary_readings.append(kw[0] if kw else "")
    reading_counts = Counter(r for r in primary_readings if r)

    for idx, c in enumerate(cities):
        slug = c.get("slug")

        # 2. 地域タブの表記ゆれ・重複を全都市一括で正規化
        raw_region = c.get("region", "")
        if raw_region in REGION_NORMALIZE_MAP:
            c["region"] = REGION_NORMALIZE_MAP[raw_region]

        # 3. 読みが重複する都市（例：広州/杭州）は自動で英語名を併記
        first_reading = primary_readings[idx]
        if first_reading and reading_counts[first_reading] >= 2:
            name_en = c.get("name_en", "")
            if name_en and name_en not in c.get("name_ja", ""):
                c["name_ja"] = f"{c['name_ja']}（{name_en}）"

        # 4. spots_draft.json から実名スポットを自動統合
        if not c.get("spots"):
            draft_spots = spots_map.get(slug, {}).get("spots", [])
            if draft_spots:
                c["spots"] = draft_spots

        # 5. 日本との時差を timezone から全都市自動算出
        diff_val, diff_label = _calc_japan_time_diff(c.get("timezone", ""))
        c["tz_diff_hours"] = diff_val
        c["tz_diff_label"] = diff_label

        # 6. 南半球の季節注記を自動補完
        lat = c.get("lat")
        if isinstance(lat, (int, float)) and lat < -10:
            climate = c.get("climate", "")
            if isinstance(climate, str) and "南半球" not in climate:
                c["climate"] = (
                    f"{climate}（南半球のため日本とは季節が逆になり、7〜8月は冬・12〜2月は夏にあたります）"
                    if climate else
                    "南半球に位置するため日本とは季節が逆になり、7〜8月は冬・12〜2月は夏にあたります。"
                )

        # 7. 文字列フィールドの表記ゆれを一括クリーンアップ
        for key in ("climate", "summary", "desc", "transport", "safety_note"):
            if key in c and isinstance(c[key], str):
                c[key] = _clean_text(c[key])

        # 8. 都市別1年カレンダー（スコア・ラベル・理由タグ・服装）を全都市に自動付与
        c["calendar"] = evaluate_city_calendar(c)

    # 9. 全都市に対して「同国最優先＋地理的距離が近い順」で周辺都市リストを自動算出
    for c in cities:
        others = [x for x in cities if x["slug"] != c["slug"]]
        others.sort(key=lambda x: (
            0 if x.get("country_ja") == c.get("country_ja") else 1,
            0 if x.get("region") == c.get("region") else 1,
            _haversine_km(c, x),
        ))
        c["nearby_slugs"] = [x["slug"] for x in others[:6]]

    return cities


def enhance_features(features: list) -> list:
    """特集ページごとに対象月と説明文を統一ルールで補完"""
    default_months_by_slug = {
        "spring-break": [3],
        "golden-week": [4, 5],
        "summer-vacation": [7, 8],
        "autumn-break": [9, 10],
        "year-end": [12, 1],
    }
    result = []
    for feat in features:
        item = dict(feat)
        if not item.get("target_months") and item.get("slug") in default_months_by_slug:
            item["target_months"] = default_months_by_slug[item["slug"]]
        result.append(item)
    return result


def build_dynamic_compare_desc(c1: dict, c2: dict, fallback: str) -> str:
    """2都市の実際のデータ差から比較要約を自動生成"""
    diffs = []
    if c1.get("currency_code") != c2.get("currency_code"):
        diffs.append(f"通貨（{c1.get('currency_code')} vs {c2.get('currency_code')}）")
    if c1.get("plug_type") != c2.get("plug_type"):
        diffs.append("コンセント形状")
    if c1.get("tz_diff_hours") is not None and c2.get("tz_diff_hours") is not None and c1["tz_diff_hours"] != c2["tz_diff_hours"]:
        diffs.append(f"時差（{c1['tz_diff_label']} vs {c2['tz_diff_label']}）")
    lat1, lat2 = c1.get("lat"), c2.get("lat")
    if isinstance(lat1, (int, float)) and isinstance(lat2, (int, float)) and (lat1 * lat2 < 0):
        diffs.append("北半球と南半球の季節差")

    if diffs:
        diff_str = "・".join(diffs[:3])
        return f"{c1['name_ja']}と{c2['name_ja']}の比較。{diff_str}や物価・気候・空港アクセスの違いを1画面で確認できます。"
    return fallback


def build_all_comparison_pairs(cities: list) -> tuple[list, dict]:
    city_map = {c["slug"]: c for c in cities}
    all_pairs = []
    seen_slugs = set()
    city_to_links = {c["slug"]: [] for c in cities}

    for s1, s2, desc in COMPARE_PAIRS:
        if s1 in city_map and s2 in city_map:
            pair_slug = f"{s1}-vs-{s2}"
            if pair_slug not in seen_slugs:
                seen_slugs.add(pair_slug)
                all_pairs.append((s1, s2, desc))
                label = f"{city_map[s1]['name_ja']} vs {city_map[s2]['name_ja']}"
                city_to_links[s1].append((pair_slug, label))
                city_to_links[s2].append((pair_slug, label))

    # 未ペアの都市は「同国優先 → 同地域内の最近接都市」で自動ペアリング
    for c in cities:
        if not city_to_links[c["slug"]]:
            partner_slug = next((s for s in c.get("nearby_slugs", []) if s in city_map), None)
            if not partner_slug:
                continue
            partner = city_map[partner_slug]
            s1, s2 = c["slug"], partner["slug"]
            pair_slug = f"{s1}-vs-{s2}"
            rev_slug = f"{s2}-vs-{s1}"
            if pair_slug not in seen_slugs and rev_slug not in seen_slugs:
                seen_slugs.add(pair_slug)
                fallback = f"{c['name_ja']}と{partner['name_ja']}の物価・時差・気候・空港アクセス・治安の違いを1画面で比較。"
                desc = build_dynamic_compare_desc(c, partner, fallback)
                all_pairs.append((s1, s2, desc))
                label = f"{c['name_ja']} vs {partner['name_ja']}"
                city_to_links[s1].append((pair_slug, label))
                city_to_links[s2].append((pair_slug, label))

    return all_pairs, city_to_links


def write_auxiliary_files(dist_dir: Path):
    (dist_dir / "CNAME").write_text("tokou-pocket.com\n", encoding="utf-8")

    ogp_src = Path(OGP_IMAGE_FILENAME)
    if ogp_src.exists():
        shutil.copy2(ogp_src, dist_dir / OGP_IMAGE_FILENAME)

    favicon_src = Path(FAVICON_FILENAME)
    if favicon_src.exists():
        shutil.copy2(favicon_src, dist_dir / FAVICON_FILENAME)

    manifest = {
        "name": SITE_NAME,
        "short_name": SITE_NAME,
        "start_url": "./",
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#0f172a"
    }
    (dist_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    sw_js = """self.addEventListener('install', (e) => {
  self.skipWaiting();
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((names) => Promise.all(names.map((n) => caches.delete(n))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll())
      .then((clients) => clients.forEach((c) => c.navigate(c.url)))
  );
});
"""
    (dist_dir / "sw.js").write_text(sw_js, encoding="utf-8")


def main():
    data_dir = Path("data")
    dist_dir = Path("dist")
    data_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)

    cities = enhance_all_cities(generate_cities_data())
    features = enhance_features(FEATURE_PAGES)

    # 公開前QAチェック（カレンダー重複・特集との季節矛盾を全都市チェック）
    qa_warnings = run_calendar_qa(cities, features)
    if qa_warnings:
        print("=== QA警告（公開前チェック） ===")
        for w in qa_warnings:
            print(" ", w)

    city_map = {c["slug"]: c for c in cities}
    (data_dir / "cities.json").write_text(json.dumps(cities, ensure_ascii=False, indent=2), encoding="utf-8")

    rates_data = fetch_exchange_rates()
    (data_dir / "rates.json").write_text(json.dumps(rates_data, ensure_ascii=False, indent=2), encoding="utf-8")

    all_compare_pairs, city_to_links = build_all_comparison_pairs(cities)

    urls = [f"{SITE_URL}/"]

    for city in cities:
        city_dir = dist_dir / city["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        html = build_city_html(city, rates_data, cities, city_to_links.get(city["slug"], []))
        (city_dir / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"{SITE_URL}/{city['slug']}/")

    for s1, s2, summary_text in all_compare_pairs:
        pair_slug = f"{s1}-vs-{s2}"
        comp_dir = dist_dir / "compare" / pair_slug
        comp_dir.mkdir(parents=True, exist_ok=True)
        comp_html = build_compare_html(city_map[s1], city_map[s2], summary_text, rates_data, cities)
        (comp_dir / "index.html").write_text(comp_html, encoding="utf-8")
        urls.append(f"{SITE_URL}/compare/{pair_slug}/")

    for feat in features:
        feat_dir = dist_dir / "features" / feat["slug"]
        feat_dir.mkdir(parents=True, exist_ok=True)
        feat_html = build_feature_html(feat, cities)
        (feat_dir / "index.html").write_text(feat_html, encoding="utf-8")
        urls.append(f"{SITE_URL}/features/{feat['slug']}/")

    index_html = build_index_html(cities, rates_data, COMPARE_PAIRS)
    (dist_dir / "index.html").write_text(index_html, encoding="utf-8")

    policy_dir = dist_dir / "policy"
    policy_dir.mkdir(parents=True, exist_ok=True)
    (policy_dir / "index.html").write_text(build_policy_html(), encoding="utf-8")

    sitemap_items = "\n".join([f"  <url><loc>{u}</loc></url>" for u in urls])
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>'
    (dist_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    (dist_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    write_auxiliary_files(dist_dir)
    print(f"ビルド完了: 全 {len(urls)} ページ（{len(cities)}都市＋比較{len(all_compare_pairs)}ペア＋特集{len(features)}本）を生成しました。")


if __name__ == "__main__":
    main()
