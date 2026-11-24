#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビルド実行エンジン (setup_and_build.py)
- 地域タブ重複解消・同音都市ピンイン併記・モロッコ時差補正・バリ島エリア/バス/危険情報補完
- 都市別1年カレンダー自動付与 ＆ 特集整合性チェック
- 同国優先＋地理距離ベースの比較ペア自動生成
"""

import json
import math
import re
import shutil
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

def _prefer_newer_tzdata():
    """OSのタイムゾーンDBが古いとき、pip の tzdata パッケージのほうが新しければそちらを使う。

    zoneinfo は既定で OS の DB を先に探し、pip の tzdata は「見つからないときの予備」にしか使わない。
    そのため CI（GitHub Actions 等）で `pip install -U tzdata` しただけでは、古い OS の DB が使われ続ける。
    """
    try:
        import zoneinfo
        import tzdata
        sys_ver = ""
        for base in zoneinfo.TZPATH:
            zi = Path(base) / "tzdata.zi"
            if zi.exists():
                first = zi.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
                sys_ver = first.replace("# version", "").strip()
                break
        if not sys_ver or str(tzdata.IANA_VERSION) > sys_ver:
            zoneinfo.reset_tzpath(to=[])
            print(f"[info] タイムゾーンDBは pip の tzdata {tzdata.IANA_VERSION} を使用します（OS: {sys_ver or '不明'}）")
    except Exception:
        pass


_prefer_newer_tzdata()

from config import SITE_URL, SITE_NAME, OGP_IMAGE_FILENAME, FAVICON_FILENAME, COMPARE_PAIRS, FEATURE_PAGES
try:
    from config import LEGACY_COMPARE_SLUGS
except ImportError:
    LEGACY_COMPARE_SLUGS = []
try:
    from config import INDEX_AUTO_COMPARE_PAGES
except ImportError:
    INDEX_AUTO_COMPARE_PAGES = False
from cities_data import generate_cities_data
from climate_calendar import evaluate_city_calendar, run_calendar_qa
from templates import (
    build_city_html, build_policy_html,
    build_compare_html, build_feature_html
)
from templates_pages import (
    build_index_html, build_guides_hub_html, build_plug_guide_html, build_time_guide_html,
    build_tipping_guide_html, build_packing_html,
)
from site_content import GUIDE_PAGES

REGION_NORMALIZE_MAP = {
    "アジア・中央アジア": "アジア",
    "中央アジア": "アジア",
    "北米・ハワイ": "北米",
    "ハワイ": "北米",
    "中東・ヨーロッパ": "中東・アフリカ",
    "中東": "中東・アフリカ",
    "アフリカ": "中東・アフリカ",
}

PINYIN_MAP = {
    "guangzhou": "Guangzhou",
    "hangzhou": "Hangzhou",
}

BALI_AREA_GUIDE = [
    {"name": "クタ・レギャン・スミニャック", "area": "空港から車で約15〜35分", "desc": "ビーチ沿いのサンセットやサーフィン、カフェ・雑貨巡りが楽しめる定番エリア。道路渋滞が起きやすいため移動時間に余裕を。", "best_time": "夕方〜サンセット", "caution": "夜間の繁華街やビーチ沿いではスリ・置き引きに注意。"},
    {"name": "ウブド", "area": "空港から車で約60〜90分（内陸・丘陵）", "desc": "ライステラスや寺院、スパ・ヨガ、アートギャラリーが集まる文化・自然エリア。朝晩は海辺よりやや涼しく感じることも。", "best_time": "午前〜午後早め", "caution": "街灯が少ない道もあるため、夜間の徒歩移動は控えめに。"},
    {"name": "ヌサドゥア・ジンバラン", "area": "空港から車で約20〜35分", "desc": "落ち着いたリゾートエリアやシーフードディナーが人気。比較的静かに滞在したい人に向いています。", "best_time": "日中〜ディナータイム", "caution": "敷地外へ出る際は配車アプリやホテル手配の車を利用すると安心。"},
]


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

    # 取得失敗時: 前回の正常値があればそれを使い、更新時刻に「前回値」と明記する
    try:
        prev = json.loads((Path("data") / "rates.json").read_text(encoding="utf-8"))
        if prev.get("rates") and not prev.get("is_fallback"):
            base_label = str(prev.get("updated_at", "不明")).replace("（取得失敗のため前回値）", "")
            prev["updated_at"] = f"{base_label}（取得失敗のため前回値）"
            prev["is_stale"] = True
            return prev
    except Exception:
        pass

    # 前回値もない場合の固定値。最新の更新時刻を名乗らず、参考値であることを明記する
    return {
        "updated_at": "取得失敗（参考値）",
        "is_fallback": True,
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


def _calc_japan_time_diff(city: dict) -> tuple[float | None, str]:
    tz_name = city.get("timezone", "")
    if not tz_name:
        return None, "現地時刻参照"
    try:
        now_utc = datetime.now(timezone.utc)
        jst_offset = now_utc.astimezone(ZoneInfo("Asia/Tokyo")).utcoffset()
        local_offset = now_utc.astimezone(ZoneInfo(tz_name)).utcoffset()
        if jst_offset is None or local_offset is None:
            return None, "現地時刻参照"
        diff_hours = (local_offset - jst_offset).total_seconds() / 3600.0
        # 注: モロッコは2026-09-20からUTC+0固定（-9時間）。tzdata 2026c以降が必要。個別補正は入れない
        if diff_hours == 0:
            return 0.0, "時差なし（日本と同じ）"
        sign = "+" if diff_hours > 0 else ""
        if diff_hours.is_integer():
            return diff_hours, f"{sign}{int(diff_hours)}時間"
        return diff_hours, f"{sign}{diff_hours:.1f}時間"
    except Exception:
        return None, "現地時刻参照"


def enhance_all_cities(cities: list) -> list:
    draft_path = Path("spots_draft.json")
    spots_map = {}
    if draft_path.exists():
        try:
            spots_map = json.loads(draft_path.read_text(encoding="utf-8"))
        except Exception:
            spots_map = {}

    # 編集済みのスポット（spots_curated.json）。spots_draft.json に同じ都市があればそちらを優先
    curated_path = Path("spots_curated.json")
    if curated_path.exists():
        try:
            for _slug, _v in json.loads(curated_path.read_text(encoding="utf-8")).items():
                spots_map.setdefault(_slug, _v)
        except Exception:
            pass

    primary_readings = []
    for c in cities:
        kw = (c.get("kana_kw") or "").strip().split()
        primary_readings.append(kw[0] if kw else "")
    reading_counts = Counter(r for r in primary_readings if r)

    for idx, c in enumerate(cities):
        slug = c.get("slug", "")

        # 1. 地域タブ重複を解消
        raw_region = c.get("region", "")
        if raw_region in REGION_NORMALIZE_MAP:
            c["region"] = REGION_NORMALIZE_MAP[raw_region]

        # 2. 広州・杭州や同音都市のピンイン／英語表記を一覧でも区別
        if slug in PINYIN_MAP and PINYIN_MAP[slug] not in c.get("name_ja", ""):
            c["name_ja"] = f"{c['name_ja']}（{PINYIN_MAP[slug]}）"
        else:
            first_reading = primary_readings[idx]
            if first_reading and reading_counts[first_reading] >= 2:
                name_en = c.get("name_en", "")
                if name_en and name_en not in c.get("name_ja", ""):
                    c["name_ja"] = f"{c['name_ja']}（{name_en}）"

        # 3. バリ島固有の整合性補正（危険情報・エリア案内・空港バス時間/料金）
        if slug == "bali":
            c["danger_level"] = "レベル1（十分注意）※一部地域は最新発出要確認"
            c["safety_note"] = (
                "インドネシアは地域ごとに外務省危険情報や治安状況が異なります。バリ島内でもクタ・レギャン等の繁華街でのスリや置き引き、バイク運転中のひったくりに注意し、最新情報は外務省公式ページで確認してください。"
            )
            c["spots"] = BALI_AREA_GUIDE
            c["airport_access"]["cheapest"] = "空港シャトルバス・路線バス（クタ/サヌール方面 約30〜60分 / 目安20,000〜50,000IDR・約180〜450円 ※路線・渋滞により変動）"

        # 4. スポット補完
        if not c.get("spots"):
            draft_spots = spots_map.get(slug, {}).get("spots", [])
            if draft_spots:
                c["spots"] = draft_spots

        # 5. 時差算出
        diff_val, diff_label = _calc_japan_time_diff(c)
        c["tz_diff_hours"] = diff_val
        c["tz_diff_label"] = diff_label

        # 6. 南半球注記
        lat = c.get("lat")
        if isinstance(lat, (int, float)) and lat < -10:
            climate = c.get("climate", "")
            if isinstance(climate, str) and "南半球" not in climate:
                c["climate"] = (
                    f"{climate}（南半球のため日本とは季節が逆になり、7〜8月は冬・12〜2月は夏にあたります）"
                    if climate else
                    "南半球に位置するため日本とは季節が逆になり、7〜8月は冬・12〜2月は夏にあたります。"
                )

        # 7. 文面整形
        for key in ("climate", "summary", "desc", "transport", "safety_note"):
            if key in c and isinstance(c[key], str):
                c[key] = _clean_text(c[key])

        # 8. 都市別1年カレンダー自動付与
        c["calendar"] = evaluate_city_calendar(c)

    # 9. 同国最優先＋地理的距離順の周辺都市
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
    default_months_by_slug = {
        "graduation-spring": [2, 3],
        "spring-break": [3],
        "golden-week": [4, 5],
        "summer-vacation": [7, 8],
        "autumn-silverweek": [9, 10, 11],
        "winter-newyear": [12, 1, 2],
        "first-time-safe": [4, 5, 9, 10],
    }
    result = []
    for feat in features:
        item = dict(feat)
        if not item.get("target_months") and item.get("slug") in default_months_by_slug:
            item["target_months"] = default_months_by_slug[item["slug"]]
        result.append(item)
    return result


def build_dynamic_compare_desc(c1: dict, c2: dict, fallback: str) -> str:
    diffs = []
    if c1.get("currency_code") != c2.get("currency_code"):
        diffs.append(f"通貨（{c1.get('currency_code')} vs {c2.get('currency_code')}）")
    if c1.get("plug_type") != c2.get("plug_type"):
        diffs.append("コンセント形状")
    if c1.get("tz_diff_hours") is not None and c2.get("tz_diff_hours") is not None and c1["tz_diff_hours"] != c2["tz_diff_hours"]:
        diffs.append(f"時差（{c1['tz_diff_label']} vs {c2['tz_diff_label']}）")
    if diffs:
        return f"{c1['name_ja']}と{c2['name_ja']}の比較。{'・'.join(diffs[:3])}や物価・気候・空港アクセスの違いを1画面で確認できます。"
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


def build_redirect_html(target_url: str) -> str:
    """旧URL用の移動案内ページ（GitHub Pages等、サーバー側301が使えない環境向け）"""
    return (
        '<!DOCTYPE html>\n<html lang="ja"><head><meta charset="UTF-8">'
        '<title>ページを移動しました</title><meta name="robots" content="noindex">'
        f'<link rel="canonical" href="{target_url}">'
        f'<meta http-equiv="refresh" content="0; url={target_url}"></head>'
        f'<body><p>ページを移動しました。<a href="{target_url}">こちら</a>をご覧ください。</p></body></html>'
    )


def write_legacy_compare_redirects(dist_dir: Path, existing_pair_slugs: set, city_map: dict) -> int:
    count = 0
    for legacy in LEGACY_COMPARE_SLUGS:
        if legacy in existing_pair_slugs or "-vs-" not in legacy:
            continue
        first = legacy.split("-vs-")[0]
        target = f"{SITE_URL}/{first}/" if first in city_map else f"{SITE_URL}/"
        out = dist_dir / "compare" / legacy
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_redirect_html(target), encoding="utf-8")
        count += 1
    return count


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

    qa_messages = run_calendar_qa(cities, features)
    if qa_messages:
        print("=== QA結果 ===")
        for w in qa_messages:
            print(" ", w)
    qa_errors = [w for w in qa_messages if w.startswith("[ERROR]")]
    if qa_errors:
        print(f"QAエラー {len(qa_errors)} 件のためビルドを中止します（data/ と dist/ は更新されません）。")
        sys.exit(1)

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

    curated_slugs = {f"{a}-vs-{b}" for a, b, _ in COMPARE_PAIRS}
    noindex_count = 0
    for s1, s2, summary_text in all_compare_pairs:
        pair_slug = f"{s1}-vs-{s2}"
        comp_dir = dist_dir / "compare" / pair_slug
        comp_dir.mkdir(parents=True, exist_ok=True)
        comp_html = build_compare_html(city_map[s1], city_map[s2], summary_text, rates_data, cities)
        # 自動生成ペアは、両都市に手書きの個性文がない限り noindex（薄いページの量産を避ける）
        has_content = bool(city_map[s1].get("best_for") and city_map[s2].get("best_for"))
        indexable = INDEX_AUTO_COMPARE_PAGES or pair_slug in curated_slugs or has_content
        if not indexable:
            comp_html = comp_html.replace("</head>", '  <meta name="robots" content="noindex,follow">\n</head>', 1)
            noindex_count += 1
        (comp_dir / "index.html").write_text(comp_html, encoding="utf-8")
        if indexable:
            urls.append(f"{SITE_URL}/compare/{pair_slug}/")

    redirected = write_legacy_compare_redirects(dist_dir, {f"{s1}-vs-{s2}" for s1, s2, _ in all_compare_pairs}, city_map)

    for feat in features:
        feat_dir = dist_dir / "features" / feat["slug"]
        feat_dir.mkdir(parents=True, exist_ok=True)
        feat_html = build_feature_html(feat, cities)
        (feat_dir / "index.html").write_text(feat_html, encoding="utf-8")
        urls.append(f"{SITE_URL}/features/{feat['slug']}/")

    # ガイド・早見表ページ（都市データから自動生成）
    guide_builders = {
        "": lambda: build_guides_hub_html(),
        "plug-types": lambda: build_plug_guide_html(cities),
        "time-difference": lambda: build_time_guide_html(cities),
        "tipping": lambda: build_tipping_guide_html(cities),
        "packing-checklist": lambda: build_packing_html(),
    }
    for gslug, fn in guide_builders.items():
        gdir = dist_dir / "guides" / gslug if gslug else dist_dir / "guides"
        gdir.mkdir(parents=True, exist_ok=True)
        (gdir / "index.html").write_text(fn(), encoding="utf-8")
        urls.append(f"{SITE_URL}/guides/{gslug + '/' if gslug else ''}")

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
    print(f"ビルド完了: 全 {len(urls)} ページ（{len(cities)}都市＋比較{len(all_compare_pairs)}ペア＋特集{len(features)}本）を生成しました。旧URLの移動案内 {redirected} 件、noindex の比較ページ {noindex_count} 件。")


if __name__ == "__main__":
    main()
