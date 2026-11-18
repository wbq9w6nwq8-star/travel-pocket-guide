#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビルド実行エンジン (setup_and_build.py)
- 全150都市ページ ＋ 2都市比較10ページ ＋ 季節特集2ページ ＋ ポリシーページを一括生成
"""

import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

from config import SITE_URL, SITE_NAME, COMPARE_PAIRS, FEATURE_PAGES
from cities_data import generate_cities_data
from templates import (
    build_city_html, build_index_html, build_policy_html,
    build_compare_html, build_feature_html
)


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


def write_auxiliary_files(dist_dir: Path):
    (dist_dir / "CNAME").write_text("tokou-pocket.com\n", encoding="utf-8")

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

    cities = generate_cities_data()
    city_map = {c["slug"]: c for c in cities}
    (data_dir / "cities.json").write_text(json.dumps(cities, ensure_ascii=False, indent=2), encoding="utf-8")

    rates_data = fetch_exchange_rates()
    (data_dir / "rates.json").write_text(json.dumps(rates_data, ensure_ascii=False, indent=2), encoding="utf-8")

    urls = [f"{SITE_URL}/"]

    # 1. 各都市ページ生成
    for city in cities:
        city_dir = dist_dir / city["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        html = build_city_html(city, rates_data, cities)
        (city_dir / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"{SITE_URL}/{city['slug']}/")

    # 2. 人気2都市比較ページ生成 (/compare/slug1-vs-slug2/)
    for s1, s2, summary_text in COMPARE_PAIRS:
        if s1 in city_map and s2 in city_map:
            pair_slug = f"{s1}-vs-{s2}"
            comp_dir = dist_dir / "compare" / pair_slug
            comp_dir.mkdir(parents=True, exist_ok=True)
            comp_html = build_compare_html(city_map[s1], city_map[s2], summary_text, rates_data)
            (comp_dir / "index.html").write_text(comp_html, encoding="utf-8")
            urls.append(f"{SITE_URL}/compare/{pair_slug}/")

    # 3. 季節特集ハブページ生成 (/features/slug/)
    for feat in FEATURE_PAGES:
        feat_dir = dist_dir / "features" / feat["slug"]
        feat_dir.mkdir(parents=True, exist_ok=True)
        feat_html = build_feature_html(feat, cities)
        (feat_dir / "index.html").write_text(feat_html, encoding="utf-8")
        urls.append(f"{SITE_URL}/features/{feat['slug']}/")

    # 4. トップページ＆ポリシーページ生成
    index_html = build_index_html(cities, rates_data)
    (dist_dir / "index.html").write_text(index_html, encoding="utf-8")

    policy_dir = dist_dir / "policy"
    policy_dir.mkdir(parents=True, exist_ok=True)
    (policy_dir / "index.html").write_text(build_policy_html(), encoding="utf-8")

    # 5. サイトマップ＆robots.txt更新
    sitemap_items = "\n".join([f"  <url><loc>{u}</loc></url>" for u in urls])
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>'
    (dist_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    (dist_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    write_auxiliary_files(dist_dir)
    print(f"✅ フル機能ビルド完了！ 全 {len(urls)} ページ（150都市＋比較10＋特集2＋トップ）を生成しました。")


if __name__ == "__main__":
    main()
