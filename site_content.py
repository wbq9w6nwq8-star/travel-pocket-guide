# -*- coding: utf-8 -*-
"""
site_content.py ― トップページ・ガイドページ用の編集データ

- POPULAR     : トップページで最初に見せる人気都市（この順で先頭に並びます）
- THEMES      : テーマ別の都市分類（トップの「テーマで探す」に使用）
- GUIDE_PAGES : ガイド（早見表・チェックリスト）の一覧
スラッグが存在しない場合は無視されます（ビルド時に警告を表示）。
"""

POPULAR = [
    "seoul", "taipei", "bangkok", "honolulu", "singapore", "bali", "hong-kong", "busan",
    "phuket", "ho-chi-minh", "da-nang", "guam", "london", "paris", "rome", "barcelona",
    "new-york", "los-angeles", "sydney", "vancouver", "dubai", "istanbul", "kuala-lumpur", "cebu",
]

THEMES = {
    "beach": ("ビーチ・リゾート", [
        "bali", "phuket", "krabi", "koh-samui", "cebu", "boracay", "palawan", "phu-quoc", "nha-trang", "da-nang",
        "langkawi", "kota-kinabalu", "lombok", "honolulu", "kona", "maui", "guam", "saipan", "cancun", "rio-de-janeiro",
        "gold-coast", "cairns", "nadi", "noumea", "tahiti", "male", "santorini", "mykonos", "malaga", "nice", "split",
        "dubrovnik", "busan", "jeju", "penang", "miami", "san-diego", "barcelona", "sydney", "hualien", "san-sebastian",
        "valencia", "pattaya", "antalya",
    ]),
    "food": ("グルメ・食べ歩き", [
        "seoul", "busan", "taipei", "tainan", "kaohsiung", "bangkok", "chiang-mai", "hanoi", "ho-chi-minh", "penang",
        "malacca", "hong-kong", "macau", "singapore", "kuala-lumpur", "shanghai", "chengdu", "xian", "guangzhou", "mumbai",
        "istanbul", "rome", "bologna", "naples", "florence", "barcelona", "san-sebastian", "madrid", "seville", "lisbon",
        "porto", "paris", "lyon", "bordeaux", "brussels", "melbourne", "new-york", "los-angeles", "mexico-city", "lima",
        "marrakech", "osaka", "palermo", "bruges",
    ]),
    "history": ("歴史・街歩き", [
        "xian", "beijing", "hanoi", "hue", "siem-reap", "delhi", "jaipur", "kathmandu", "istanbul", "cappadocia", "athens",
        "rome", "florence", "venice", "naples", "paris", "london", "edinburgh", "oxford", "cambridge", "bath", "prague",
        "vienna", "salzburg", "budapest", "krakow", "warsaw", "berlin", "granada", "seville", "madrid", "lisbon", "porto",
        "cairo", "luxor", "marrakech", "fes", "cusco", "quebec-city", "boston", "washington-dc", "malacca", "ayutthaya",
        "gyeongju", "tainan", "valletta", "dubrovnik", "bruges", "strasbourg", "mont-saint-michel", "zagreb", "bologna",
    ]),
    "nature": ("自然・絶景", [
        "banff", "queenstown", "reykjavik", "rovaniemi", "interlaken", "zermatt", "lucerne", "innsbruck", "cusco", "uyuni",
        "hobart", "uluru", "vancouver", "victoria", "hualien", "bergen", "cape-town", "tahiti", "kona", "maui", "krabi",
        "palawan", "cairns", "christchurch", "geneva", "salzburg", "kathmandu", "mont-saint-michel", "santorini", "jiufen",
    ]),
    "city": ("買い物・都会", [
        "new-york", "los-angeles", "san-francisco", "las-vegas", "chicago", "seattle", "hong-kong", "macau", "shanghai",
        "shenzhen", "beijing", "seoul", "taipei", "singapore", "kuala-lumpur", "dubai", "abu-dhabi", "doha", "milan", "paris",
        "london", "frankfurt", "munich", "berlin", "sydney", "melbourne", "toronto", "bangkok", "manila", "jakarta", "mumbai",
        "mexico-city", "sao-paulo", "buenos-aires", "amsterdam", "copenhagen", "stockholm", "hamburg",
    ]),
    "first": ("初めてでも安心", [
        "taipei", "seoul", "singapore", "honolulu", "guam", "sydney", "melbourne", "auckland", "vancouver", "zurich", "vienna",
        "helsinki", "hong-kong", "busan", "jeju", "kaohsiung", "taichung", "macau", "saipan", "kuala-lumpur", "toronto",
        "london", "paris", "rome", "barcelona", "new-york", "los-angeles", "bali", "phuket", "da-nang", "bangkok",
    ]),
}

GUIDE_PAGES = [
    ("packing-checklist", "海外旅行の持ち物チェックリスト", "出発前の確認を、チェックしながら進められるリスト。保存・印刷にも対応。", "list-checks"),
    ("time-difference", "世界の時差早見表（冬時間・夏時間）", "日本との時差を都市別に一覧。夏時間の切り替えと、日本時間→現地時間の換算ツール付き。", "clock"),
    ("plug-types", "世界のコンセント・電圧早見表", "プラグ形状別の対応都市と、変換プラグ・変圧器の考え方をまとめました。", "plug"),
    ("tipping", "世界のチップ早見表", "国・都市別のチップ相場と渡し方。必要・任意・不要で分類し、簡易計算つき。", "coins"),
]
