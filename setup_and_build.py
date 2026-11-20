#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビルド実行エンジン (setup_and_build.py)
- OGPサムネイル画像 (ogp.png) とファビコン (youka.png) を dist/ に自動コピー
- 全都市が比較ページを持つように自動ペアリング生成
- レビュー指摘（リスボン・夏休み特集・比較ペア要約など）の補正を適用
"""

import json
import shutil
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

from config import SITE_URL, SITE_NAME, OGP_IMAGE_FILENAME, FAVICON_FILENAME, COMPARE_PAIRS, FEATURE_PAGES
from cities_data import generate_cities_data
from templates import (
    build_city_html, build_index_html, build_policy_html,
    build_compare_html, build_feature_html
)

LISBON_SPOTS = [
    {
        "name": "ジェロニモス修道院",
        "area": "ベレン地区",
        "desc": "マヌエル様式の壮麗な修道院と回廊。ベレンの塔やエッグタルトの老舗と合わせて回りやすい定番です。",
        "best_time": "開館直後の午前中",
        "caution": "人気のため行列ができやすく、時間帯別の事前予約や早めの到着が安心です。",
    },
    {
        "name": "サン・ジョルジェ城",
        "area": "アルファマ周辺（丘の上）",
        "desc": "リスボン旧市街とテージョ川を見渡せる歴史ある城跡。夕暮れ時の眺望も人気です。",
        "best_time": "午前〜夕方（日没前は混雑）",
        "caution": "坂道や石畳が多いため歩きやすい靴が必須。入場待ち時間に余裕を持ちましょう。",
    },
    {
        "name": "アルファマ地区＆トラム28番線",
        "area": "アルファマ地区",
        "desc": "迷路のような路地と坂道、ファドが響く旧市街エリア。レトロな路面電車は景色が魅力です。",
        "best_time": "午前中",
        "caution": "トラム28番線や坂道の混雑箇所はスリが多発しやすいため、バッグは前で持ちましょう。",
    },
]


def apply_review_fixes_to_cities(cities: list) -> list:
    """レビュー指摘に基づく都市データの補正"""
    for c in cities:
        slug = c.get("slug")
        if slug == "lisbon":
            c["climate"] = (
                "地中海性気候で、夏（6〜8月）は乾燥して晴れの日が多く日差しが強め、冬（11〜2月）は雨や曇りが増えやすい傾向です。"
                "朝晩や海風による体感温度差があるため羽織りものがあると安心です。"
            )
            c["airport_access"] = {
                "airport_name": "ウンベルト・デルガード空港（リスボン空港 / LIS）",
                "fastest": "空港からタクシー・配車アプリ（Uber / Bolt）で約15〜25分（市内中心部まで目安10〜20€前後・渋滞により変動）。",
                "cheapest": "地下鉄レッドライン（Aeroporto駅）で市内中心部へ約20〜30分（片道目安1.80€・IC/タッチ決済対応）。",
            }
            if not c.get("spots"):
                c["spots"] = LISBON_SPOTS
    return cities


def apply_review_fixes_to_features(features: list) -> list:
    """特集ページの説明文を時期・実態に合わせて調整"""
    adjusted = []
    for feat in features:
        item = dict(feat)
        if item.get("slug") == "summer-vacation":
            item["desc"] = (
                "7〜8月の夏休みシーズンに向けた12都市の気候・服装・電源・治安まとめ。"
                "夏の乾季リゾートや涼しい高地・北欧のほか、南半球の冬にあたるオセアニアの気温差も含めて確認できます。"
            )
        adjusted.append(item)
    return adjusted


def customize_compare_summary(c1: dict, c2: dict, default_desc: str) -> str:
    """比較ペアごとの違い・選び方が伝わる要約文"""
    pair = {c1.get("slug"), c2.get("slug")}
    if pair == {"sydney", "melbourne"}:
        return (
            "ハーバーとビーチ・開放感のシドニーと、路地裏のカフェ文化・アートとコンパクトな街歩きのメルボルン。"
            "同じオーストラリアでも街の個性や7〜8月の冬の体感、向いている旅のスタイルが異なります。"
        )
    if pair == {"los-angeles", "new-york"}:
        return (
            "車・配車移動と海・テーマパークの開放感があるロサンゼルスと、地下鉄・徒歩で美術館や舞台を巡るニューヨーク。"
            "3時間の時差や冬の寒さ、街の回り方が大きく異なります。"
        )
    return default_desc


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
                final_desc = customize_compare_summary(city_map[s1], city_map[s2], desc)
                all_pairs.append((s1, s2, final_desc))
                label = f"{city_map[s1]['name_ja']} vs {city_map[s2]['name_ja']}"
                city_to_links[s1].append((pair_slug, label))
                city_to_links[s2].append((pair_slug, label))

    by_region = {}
    for c in cities:
        by_region.setdefault(c["region"], []).append(c)

    for reg, reg_cities in by_region.items():
        for i, c in enumerate(reg_cities):
            if not city_to_links[c["slug"]]:
                partner = reg_cities[(i + 1) % len(reg_cities)]
                if partner["slug"] == c["slug"] and len(cities) > 1:
                    partner = cities[0]
                s1, s2 = c["slug"], partner["slug"]
                pair_slug = f"{s1}-vs-{s2}"
                rev_slug = f"{s2}-vs-{s1}"
                if pair_slug not in seen_slugs and rev_slug not in seen_slugs:
                    seen_slugs.add(pair_slug)
                    desc = f"{c['region']}の人気渡航先である{c['name_ja']}と{partner['name_ja']}のコンセント・チップ・物価・気候・治安の違いを1画面で比較。"
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

    raw_cities = generate_cities_data()
    cities = apply_review_fixes_to_cities(raw_cities)
    features = apply_review_fixes_to_features(FEATURE_PAGES)

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
