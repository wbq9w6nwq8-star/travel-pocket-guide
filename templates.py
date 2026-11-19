#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML・UIデザイン・テンプレート管理ファイル (templates.py)
- OGP画像 (ogp.png) & ファビコン (youka.png) 全ページ完全対応
- 絵文字を抑えた実用辞典トーン
- ざっくり物価目安（水・ランチ・タクシーの3品目）
- 5段階星評価の評価基準明記
- 軽量・定番スポット3選＋旅行会社（Agoda / Oooh）導線
- 150×150都市対応の動的2都市比較ツール
- 1年カレンダー（おすすめ時期・穴場時期・雪＆冬シーズン目安）
"""

import json
from config import (
    SITE_URL, SITE_NAME, GA4_ID, OGP_IMAGE_URL, FAVICON_URL,
    SISTER_SITE_URL, SISTER_SITE_NAME,
    AFFILIATE_ESIM_URL, AFFILIATE_VPN_URL, AFFILIATE_CARD_URL,
    AFFILIATE_OOOH_URL, AFFILIATE_AGODA_URL,
    A8_PIXEL_URLS, FEATURE_PAGES
)


def render_plug_svg(plug_type: str) -> str:
    main_p = plug_type.split("/")[0]
    svgs = {
        "A": '<svg viewBox="0 0 64 64" class="w-11 h-11 mx-auto"><circle cx="32" cy="32" r="28" fill="#f8fafc" stroke="#334155" stroke-width="2.5"/><rect x="21" y="20" width="4" height="24" rx="1" fill="#0f172a"/><rect x="39" y="20" width="4" height="24" rx="1" fill="#0f172a"/></svg>',
        "BF": '<svg viewBox="0 0 64 64" class="w-11 h-11 mx-auto"><circle cx="32" cy="32" r="28" fill="#f8fafc" stroke="#334155" stroke-width="2.5"/><rect x="29" y="14" width="6" height="12" rx="1" fill="#0f172a"/><rect x="16" y="36" width="11" height="5" rx="1" fill="#0f172a"/><rect x="37" y="36" width="11" height="5" rx="1" fill="#0f172a"/></svg>',
        "O": '<svg viewBox="0 0 64 64" class="w-11 h-11 mx-auto"><circle cx="32" cy="32" r="28" fill="#f8fafc" stroke="#334155" stroke-width="2.5"/><rect x="20" y="18" width="4" height="14" transform="rotate(-30 22 25)" fill="#0f172a"/><rect x="40" y="18" width="4" height="14" transform="rotate(30 42 25)" fill="#0f172a"/><rect x="30" y="38" width="4" height="12" fill="#0f172a"/></svg>',
        "C": '<svg viewBox="0 0 64 64" class="w-11 h-11 mx-auto"><circle cx="32" cy="32" r="28" fill="#f8fafc" stroke="#334155" stroke-width="2.5"/><circle cx="22" cy="32" r="4.5" fill="#0f172a"/><circle cx="42" cy="32" r="4.5" fill="#0f172a"/></svg>'
    }
    return svgs.get(main_p, svgs["C"])


def tip_color_class(level: str) -> str:
    return {
        "none": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "optional": "bg-amber-100 text-amber-800 border-amber-300",
        "required": "bg-rose-100 text-rose-800 border-rose-300"
    }.get(level, "bg-slate-100 text-slate-800")


def danger_badge_class(color: str) -> str:
    return {
        "emerald": "bg-emerald-50 text-emerald-800 border-emerald-200",
        "amber": "bg-amber-100 text-amber-900 border-amber-300",
        "rose": "bg-rose-100 text-rose-900 border-rose-300"
    }.get(color, "bg-slate-100 text-slate-800")


def render_common_head(page_title: str, page_desc: str, page_url: str, og_type: str = "article") -> str:
    return f"""<link rel="icon" type="image/png" sizes="48x48" href="{FAVICON_URL}">
  <link rel="icon" type="image/png" sizes="192x192" href="{FAVICON_URL}">
  <link rel="apple-touch-icon" href="{FAVICON_URL}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{page_desc}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:url" content="{page_url}">
  <meta property="og:image" content="{OGP_IMAGE_URL}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{page_title}">
  <meta name="twitter:description" content="{page_desc}">
  <meta name="twitter:image" content="{OGP_IMAGE_URL}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9644749026345882"
     crossorigin="anonymous"></script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_ID}');
  </script>"""


def render_pr_banner() -> str:
    return """<div class="bg-slate-100 border-b border-slate-200 text-center py-1 px-3 text-[10px] text-slate-500">
    【PR】当サイトはアフィリエイト広告を利用しています
  </div>"""


def render_pixels() -> str:
    return "\n  ".join([
        f'<img border="0" width="1" height="1" src="{url}" alt="" class="hidden">'
        for url in A8_PIXEL_URLS
    ])


def render_share_buttons(page_url: str, share_title: str) -> str:
    return f"""
    <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-2">
      <span class="text-xs font-bold text-slate-700">このページの渡航情報を同行者に共有</span>
      <div class="flex items-center gap-1.5 flex-wrap">
        <a href="https://social-plugins.line.me/lineit/share?url={page_url}" target="_blank" rel="noopener noreferrer"
          class="bg-[#06C755] hover:opacity-90 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition">
          LINEで送る
        </a>
        <a href="https://twitter.com/intent/tweet?url={page_url}&text={share_title}" target="_blank" rel="noopener noreferrer"
          class="bg-slate-900 hover:bg-slate-800 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition">
          Xでポスト
        </a>
        <button type="button" onclick="shareOrCopy('{page_url}', '{share_title}')"
          class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-bold px-3 py-1.5 rounded-lg border border-slate-300 transition">
          URLをコピー
        </button>
      </div>
    </div>"""


def render_share_script() -> str:
    return """
    function shareOrCopy(url, title) {
      if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(() => {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
          alert('ページのURLをコピーしました。LINEやメモ帳に貼り付けて共有できます。');
        });
      }
    }"""


def render_sister_site_banner() -> str:
    return f"""
    <div class="bg-gradient-to-r from-slate-900 to-indigo-950 text-white p-4 rounded-2xl shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <span class="text-[10px] font-bold bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 px-2 py-0.5 rounded-full">姉妹メディア</span>
        <p class="text-xs sm:text-sm font-extrabold mt-1">海外留学・ワーホリ・現地インターン・キャリア情報なら【Atrium】</p>
        <p class="text-[11px] text-slate-300 mt-0.5">世界各都市の留学生・駐在員のリアルタイム掲示板「Atrium Pulse」や奨学金・就活ニュースを毎日更新中。</p>
      </div>
      <a href="{SISTER_SITE_URL}/" target="_blank" rel="noopener" class="shrink-0 bg-white hover:bg-slate-100 text-slate-900 text-xs font-extrabold px-3.5 py-2.5 rounded-xl text-center transition">
        Atriumを見る
      </a>
    </div>"""


def render_countdown_calendar(city: dict) -> str:
    return f"""
    <section class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex items-center justify-between flex-wrap gap-2">
      <div class="flex items-center gap-2">
        <span class="text-xs font-bold text-slate-700">{city['name_ja']}への出発日カレンダー:</span>
        <input id="trip-date-input" type="date" class="text-xs bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 font-bold text-slate-800 focus:outline-none focus:border-blue-500">
      </div>
      <div id="trip-countdown-msg" class="text-xs font-bold text-blue-700">出発日を入力すると残り日数と準備時期の目安を表示します</div>
    </section>"""


def compute_price_benchmarks(city: dict, jpy_to_local: float, local_to_jpy: float) -> dict:
    """身近な3品目（ペットボトル水500ml・ローカルランチ・タクシー移動目安）のざっくり相場観を算出"""
    code = city["currency_code"]
    cheap_curr = ("VND", "THB", "IDR", "PHP", "MYR", "INR", "LKR", "NPR", "EGP", "UZS", "MAD", "PLN", "HUF", "CZK")
    mid_curr = ("KRW", "TWD", "CNY", "TRY", "MXN", "PEN", "BRL", "ZAR")

    if code in cheap_curr:
        water_jpy, lunch_jpy, taxi_jpy = 80, 700, 1200
    elif code in mid_curr:
        water_jpy, lunch_jpy, taxi_jpy = 140, 1200, 1800
    else:
        water_jpy, lunch_jpy, taxi_jpy = 260, 2400, 3200

    def fmt_pair(jpy_val: int) -> str:
        local_val = jpy_val * jpy_to_local
        if local_val >= 1000:
            loc_str = f"{round(local_val, -1):,.0f}"
        elif local_val >= 10:
            loc_str = f"{local_val:,.1f}"
        else:
            loc_str = f"{local_val:.2f}"
        return f"約 {jpy_val:,}円（{loc_str} {code}）"

    return {
        "water": fmt_pair(water_jpy),
        "lunch": fmt_pair(lunch_jpy),
        "taxi": fmt_pair(taxi_jpy),
    }


def render_tip_split_calculator(city: dict, jpy_to_local: float, local_to_jpy: float) -> str:
    code = city["currency_code"]
    default_tip = 18 if city["tip_level"] == "required" else (10 if city["tip_level"] == "optional" else 0)
    bench = compute_price_benchmarks(city, jpy_to_local, local_to_jpy)

    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3.5">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold text-slate-800">チップ＆割り勘計算機 ＆ ざっくり物価目安</h2>
        <span class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2 py-0.5 rounded-full">現地予算ツール</span>
      </div>

      <!-- 身近な3品目のざっくり相場観 -->
      <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 space-y-1.5">
        <p class="text-[11px] font-bold text-slate-800">{city['name_ja']}のざっくり物価目安（日本円換算の目安）</p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
          <div class="bg-white p-2 rounded-lg border border-slate-100">
            <span class="text-[10px] text-slate-500 block">水（500ml・商店目安）</span>
            <strong class="text-slate-900">{bench['water']}</strong>
          </div>
          <div class="bg-white p-2 rounded-lg border border-slate-100">
            <span class="text-[10px] text-slate-500 block">昼食（食堂・カジュアル店）</span>
            <strong class="text-slate-900">{bench['lunch']}</strong>
          </div>
          <div class="bg-white p-2 rounded-lg border border-slate-100">
            <span class="text-[10px] text-slate-500 block">市内タクシー（短〜中距離目安）</span>
            <strong class="text-slate-900">{bench['taxi']}</strong>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">1. お会計金額（{code}）</label>
          <div class="flex items-center">
            <input id="bill-amount" type="number" value="100" class="w-full bg-white border border-slate-300 rounded-lg px-2 py-1 font-bold text-sm focus:outline-none">
            <span class="ml-1.5 font-bold text-slate-600">{code}</span>
          </div>
        </div>
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">2. チップ率（目安: {city['tip_badge']}）</label>
          <select id="bill-tip" class="w-full bg-white border border-slate-300 rounded-lg px-2 py-1.5 font-bold text-xs focus:outline-none">
            <option value="0" {"selected" if default_tip == 0 else ""}>0%（チップ不要）</option>
            <option value="5">5%（端数・気持ち程度）</option>
            <option value="10" {"selected" if default_tip == 10 else ""}>10%（一般的な目安）</option>
            <option value="15">15%（標準サービス）</option>
            <option value="18" {"selected" if default_tip == 18 else ""}>18%（北米レストラン標準）</option>
            <option value="20">20%（良いサービス）</option>
          </select>
        </div>
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">3. 割り勘する人数</label>
          <select id="bill-split" class="w-full bg-white border border-slate-300 rounded-lg px-2 py-1.5 font-bold text-xs focus:outline-none">
            <option value="1">1人（割り勘なし）</option>
            <option value="2" selected>2人で割り勘</option>
            <option value="3">3人で割り勘</option>
            <option value="4">4人で割り勘</option>
            <option value="5">5人で割り勘</option>
            <option value="6">6人で割り勘</option>
          </select>
        </div>
      </div>
      <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 flex flex-wrap items-center justify-between gap-2">
        <div class="text-xs text-slate-700">
          <span>チップ込総額: <strong id="bill-total-local" class="text-slate-900">-- {code}</strong></span>
          <span class="text-[11px] text-slate-500 ml-1">（約 <span id="bill-total-jpy">--</span> 円）</span>
        </div>
        <div class="text-xs font-extrabold text-slate-900 bg-white px-3 py-1.5 rounded-lg border border-slate-200">
          1人あたり: <span id="bill-per-local" class="text-sm text-blue-700">-- {code}</span>（約 <span id="bill-per-jpy">--</span> 円）
        </div>
      </div>
    </section>"""


def compute_city_star_ratings(city: dict) -> dict:
    """5段階（★1.0〜5.0）の評価スコアと各指標の根拠ラベルを算出"""
    if city["danger_color"] == "emerald":
        if city["country_ja"] in ("シンガポール", "台湾", "韓国", "アイスランド", "フィンランド", "スイス", "オーストラリア", "ニュージーランド", "アラブ首長国連邦（UAE）", "カタール"):
            safety, safety_note = 4.6, "治安安定・夜間も比較的安心"
        else:
            safety, safety_note = 4.2, "主要観光地は比較的安定"
    else:
        safety, safety_note = 3.4, "スリ・夜間行動に注意が必要"

    if city["special_ui"] in ("europe_cashless", "korea_nav", "us_tip_medical"):
        cashless, cashless_note = 4.8, "タッチ決済・カードが広く普及"
    elif city["special_ui"] == "china_vpn":
        cashless, cashless_note = 4.7, "QR決済主流（事前準備推奨）"
    else:
        cashless, cashless_note = 3.8, "カード＋少額現金の併用が安心"

    eng_high = ("アメリカ", "グアム・サイパン（米国準州）", "カナダ", "イギリス", "オーストラリア", "ニュージーランド", "シンガポール", "フィリピン", "マルタ", "オランダ", "スウェーデン", "ノルウェー", "デンマーク", "フィンランド", "アイスランド", "マレーシア", "アラブ首長国連邦（UAE）")
    eng_mid = ("韓国", "台湾", "タイ", "香港", "スイス", "ドイツ", "オーストリア", "ギリシャ", "クロアチア", "ポルトガル", "インド")
    if city["country_ja"] in eng_high:
        english, english_note = 4.8, "英語が広く通じる環境"
    elif city["country_ja"] in eng_mid:
        english, english_note = 4.0, "観光地・ホテルで英語が通じやすい"
    else:
        english, english_note = 3.3, "翻訳アプリや指差し併用が安心"

    cheap_curr = ("VND", "THB", "IDR", "PHP", "MYR", "INR", "LKR", "NPR", "EGP", "UZS", "MAD", "PLN", "HUF", "CZK")
    mid_curr = ("KRW", "TWD", "CNY", "TRY", "MXN", "PEN", "BRL", "ZAR")
    if city["currency_code"] in cheap_curr:
        cost, cost_note = 4.6, "日本より割安感がある水準"
    elif city["currency_code"] in mid_curr:
        cost, cost_note = 4.0, "日本と同等〜やや手頃な水準"
    else:
        cost, cost_note = 3.1, "外食や宿泊はやや高めの水準"

    avg = round((safety + cashless + english + cost) / 4, 1)
    return {
        "avg": avg,
        "safety": safety, "safety_note": safety_note,
        "cashless": cashless, "cashless_note": cashless_note,
        "english": english, "english_note": english_note,
        "cost": cost, "cost_note": cost_note,
    }


def render_star_bar(score: float, note: str) -> str:
    full_stars = int(round(score))
    stars_str = "★" * full_stars + "☆" * (5 - full_stars)
    pct = int((score / 5.0) * 100)
    return f"""
      <div class="flex items-center justify-between gap-1">
        <span class="text-amber-500 font-bold text-xs tracking-tight">{stars_str}</span>
        <span class="font-extrabold text-xs text-slate-900">{score:.1f}</span>
      </div>
      <div class="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden mt-1">
        <div class="bg-amber-500 h-full" style="width: {pct}%"></div>
      </div>
      <p class="text-[10px] text-slate-500 mt-1">{note}</p>"""


def render_city_rating_box(city: dict) -> str:
    r = compute_city_star_ratings(city)
    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h2 class="text-sm font-bold text-slate-900">{city['name_ja']}の渡航しやすさ・現地スペック評価（5段階）</h2>
          <p class="text-[11px] text-slate-500 mt-0.5">評価基準：★5＝日本同等以上に快適・割安 / ★4＝一般的な海外旅行で問題なし / ★3＝事前対策や予算確保を推奨</p>
        </div>
        <div class="bg-amber-50 border border-amber-200 px-3 py-1 rounded-xl flex items-center gap-1.5">
          <span class="text-xs font-bold text-slate-700">総合</span>
          <span class="text-amber-500 font-extrabold text-sm">★ {r['avg']:.1f}</span>
          <span class="text-[10px] text-slate-400">/ 5.0</span>
        </div>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <span class="text-[11px] font-bold text-slate-700 block mb-0.5">治安・観光安心度</span>
          {render_star_bar(r['safety'], r['safety_note'])}
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <span class="text-[11px] font-bold text-slate-700 block mb-0.5">キャッシュレス決済</span>
          {render_star_bar(r['cashless'], r['cashless_note'])}
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <span class="text-[11px] font-bold text-slate-700 block mb-0.5">英語・案内通用度</span>
          {render_star_bar(r['english'], r['english_note'])}
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <span class="text-[11px] font-bold text-slate-700 block mb-0.5">現地物価コスパ</span>
          {render_star_bar(r['cost'], r['cost_note'])}
        </div>
      </div>
    </section>"""


def render_annual_calendar_box(city: dict) -> str:
    """
    1年カレンダー（1月〜12月）：
    一律の季節分けではなく、気候・緯度・地形から「その街ならではの要素が発揮される時期」を表示
    - ベスト・快適期
    - 穴場・比較的落ち着く時期
    - 雪・ウィンターシーズン（実際に降雪・雪山・冬の街並みを楽しめる都市のみ）
    """
    region = city["region"]
    climate = city["climate"]
    slug = city["slug"]

    # 実際に雪・ウィンタースポーツ・雪景色が楽しめる都市の判定
    snow_cities = {
        "zurich", "geneva", "basel", "bern", "lucerne", "interlaken", "zermatt",
        "vienna", "salzburg", "innsbruck", "munich", "berlin", "hamburg", "frankfurt",
        "prague", "budapest", "warsaw", "krakow",
        "oslo", "stockholm", "helsinki", "copenhagen", "reykjavik", "tallinn", "riga", "vilnius",
        "new-york", "boston", "chicago", "washington-dc", "philadelphia",
        "toronto", "vancouver", "montreal", "calgary", "banff", "quebec-city",
        "seoul", "busan", "beijing", "harbin", "almaty", "astana", "tbilisi", "queenstown"
    }
    has_real_snow = (slug in snow_cities) or ("雪" in climate and "積雪" not in f"非{climate}")

    # 都市ごとの「この街ならではのシーズン」説明文
    if slug in ("zurich", "geneva", "interlaken", "zermatt", "lucerne", "bern"):
        unique_season_note = "夏（6〜8月）はアルプスの緑の牧草地と湖畔のハイキングが美しく、冬（12〜2月）は雪山・スキーや冬の澄んだ景色が映える二面性があります。"
    elif region == "オセアニア":
        unique_season_note = "南半球のため日本と季節が逆転し、12〜2月は日照時間が長く夏本番のアクティビティに最適。6〜8月は落ち着いた気候で街歩きや冬の空気が楽しめます。"
    elif has_real_snow:
        unique_season_note = "春〜初夏や秋は街歩きや歴史・文化巡りに適し、冬（12〜2月）は雪景色・ウィンターシーズン・クリスマス/冬の街並みといった季節ならではの風景が魅力です。"
    else:
        unique_season_note = "年間を通して降雪は少なく、乾季や温暖な時期ほど青空・海・街歩きやローカルグルメの快適さが際立ちます。雨季や真夏はスコール・日差し対策を前提に組み立てるのがおすすめです。"

    months_info = []
    for m in range(1, 13):
        if region == "オセアニア":
            if m in (11, 12, 1, 2):
                tag, cls = "好適・夏シーズン", "bg-blue-50 text-blue-800 border-blue-200"
            elif m in (5, 6, 8):
                tag, cls = "穴場・落ち着き期", "bg-emerald-50 text-emerald-800 border-emerald-200"
            else:
                tag, cls = "中間・散策向き", "bg-slate-100 text-slate-700 border-slate-200"
        elif has_real_snow:
            if m in (5, 6, 9, 10):
                tag, cls = "快適・散策ベスト", "bg-blue-50 text-blue-800 border-blue-200"
            elif m in (12, 1, 2):
                tag, cls = "雪・ウィンター期", "bg-indigo-50 text-indigo-900 border-indigo-200"
            elif m in (3, 4, 11):
                tag, cls = "穴場・季節の変わり目", "bg-emerald-50 text-emerald-800 border-emerald-200"
            else:
                tag, cls = "夏・日照長め", "bg-amber-50 text-amber-800 border-amber-200"
        else:
            if m in (11, 12, 1, 2, 3):
                tag, cls = "快適・乾季/好適期", "bg-blue-50 text-blue-800 border-blue-200"
            elif m in (5, 6, 9, 10):
                tag, cls = "穴場・比較的空く", "bg-emerald-50 text-emerald-800 border-emerald-200"
            else:
                tag, cls = "雨・暑さ注意期", "bg-amber-50 text-amber-800 border-amber-200"

        months_info.append((f"{m}月", tag, cls))

    snow_line = (
        "12〜2月を中心に雪景色やウィンターシーズンを体感できる都市です（防寒・滑り止め対策を推奨）。"
        if has_real_snow else
        "雪やウィンタースポーツ目的の渡航先ではなく、温暖気候・海・街歩き・グルメを楽しむスタイルに向いています。"
    )

    month_cells = "".join([
        f'<div class="p-2 rounded-xl border {cls} text-center">'
        f'<div class="text-xs font-extrabold">{m_label}</div>'
        f'<div class="text-[10px] font-bold mt-0.5">{tag}</div>'
        f'</div>'
        for m_label, tag, cls in months_info
    ])

    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-1">
        <h2 class="text-sm font-bold text-slate-900">{city['name_ja']}の1年カレンダー（季節ごとの魅力・穴場・雪目安）</h2>
        <span class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2.5 py-0.5 rounded-full">1月〜12月一覧</span>
      </div>

      <div class="grid grid-cols-3 sm:grid-cols-6 gap-2">
        {month_cells}
      </div>

      <div class="bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs space-y-1.5 text-slate-700 leading-relaxed">
        <p><strong class="text-slate-900">この街ならではの季節の見どころ：</strong>{unique_season_note}</p>
        <p><strong class="text-slate-900">気候・季節感の補足：</strong>{climate}</p>
        <p><strong class="text-slate-900">雪・ウィンターシーズン目安：</strong>{snow_line}</p>
      </div>
    </section>"""


def render_sightseeing_and_agency_box(city: dict) -> str:
    """軽量な定番スポット3選（画像なし・低負荷）＋旅行会社（アゴダ・Oooh）導線"""
    name = city["name_ja"]
    region = city["region"]
    spots = [
        {
            "title": f"{name}の旧市街・歴史シンボル地区",
            "desc": "街の成り立ちや建築・文化を体感できる定番エリア。午前中の早い時間帯に回ると比較的歩きやすく写真も撮りやすいスポットです。"
        },
        {
            "title": f"{name}のローカル市場・グルメ横丁",
            "desc": "現地の食文化や日常の活気を感じられる人気スポット。現金の扱い方やスリ対策を意識しつつ、昼食や軽食を楽しむのに最適です。"
        },
        {
            "title": f"{name}の展望スポット・ waterfront / 公園エリア",
            "desc": "街全体の景色や夕景を楽しめる開放的なエリア。移動ルートに合わせて組み込むと旅程のメリハリがつきやすくなります。"
        }
    ]

    spot_cards = "".join([
        f'<div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1">'
        f'<div class="flex items-center justify-between gap-2">'
        f'<span class="text-[10px] font-bold bg-white text-slate-700 border border-slate-200 px-2 py-0.5 rounded">定番スポット 0{idx + 1}</span>'
        f'<span class="text-[10px] text-slate-400">{region}</span>'
        f'</div>'
        f'<p class="text-xs font-extrabold text-slate-900 pt-0.5">{sp["title"]}</p>'
        f'<p class="text-[11px] text-slate-600 leading-relaxed">{sp["desc"]}</p>'
        f'</div>'
        for idx, sp in enumerate(spots)
    ])

    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-1">
        <h2 class="text-sm font-bold text-slate-900">{name}の定番観光スポット目安 ＆ 宿・現地手配</h2>
        <span class="text-[10px] text-slate-400">軽量テキスト表示</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
        {spot_cards}
      </div>

      {render_agoda_and_oooh_box(city)}
    </section>"""


def render_detailed_rules_and_manners(city: dict) -> str:
    cc = city["country_ja"]
    curr = city["currency_code"]

    if city["special_ui"] == "china_vpn":
        payment_rule = f"中国本土では現金（{curr}）以上に「Alipay」と「WeChat Pay」が必須です。日本出発前にアプリを入れ、日本のクレジットカード（Visa/Mastercard）を紐付けて本人認証を済ませてください。屋台から地下鉄までQR決済で完結します。"
    elif city["special_ui"] == "korea_nav":
        payment_rule = f"韓国は95%以上がクレジットカードのタッチ決済で完結します。ただし地下鉄・バス用の交通カード（T-moneyまたはWOWPASS）へのチャージや屋台用に、1日あたり2万〜3万ウォン程度の少額現金を空港または市内公認両替所で用意すると便利です。"
    elif city["special_ui"] == "europe_cashless":
        payment_rule = f"公共交通機関の改札からカフェ・公衆トイレまで「クレジットカード（Visa/Mastercard）のタッチ決済」が標準です。高額な現金両替はスリのリスクになるため最小限（20〜50{curr}程度）にし、カード決済時に「JPY（円建て）か{curr}（現地通貨建て）か」を端末で聞かれたら、手数料が安い『現地通貨建て（{curr}）』を必ず選択してください。"
    elif city["special_ui"] == "us_tip_medical":
        payment_rule = f"ほぼ全店舗でクレジットカード（タッチ決済）が主流です。JCBやAmexは一部店舗で使えない場合があるため、VisaまたはMastercardをメインにしてください。ホテルのチェックイン時にはデポジット（保証金）としてクレジットカードの提示が必須です。チップ用の1ドル・5ドル紙幣のみ少量用意しておくと便利です。"
    else:
        payment_rule = f"大型ホテルやショッピングモールではクレジットカード（Visa/Mastercard）が使えますが、ローカル食堂・市場・チップ用に現地通貨（{curr}）の現金も必要です。日本の空港での両替はレートが悪いため、現地空港のATMでのキャッシングまたは市内公認両替所の利用が最もお得です。カード決済時は必ず『現地通貨建て（{curr}）』を選択してください。"

    if cc in ("韓国", "台湾", "タイ", "ベトナム", "フィリピン", "インドネシア", "カンボジア", "中国", "ギリシャ", "トルコ", "エジプト", "モロッコ", "メキシコ", "ペルー", "ボリビア", "ブラジル"):
        toilet_rule = "水圧や配管の構造上、トイレットペーパーを便器に流さず「備え付けのゴミ箱」に捨てる施設が多くあります（空港や最新高級ホテルを除く）。また紙が備え付けられていない公衆トイレもあるため、水に流せるポケットティッシュと除菌ウェットティッシュの携帯が必須です。"
    elif city["region"] == "ヨーロッパ":
        toilet_rule = "駅や観光地の公衆トイレは有料（0.5〜2ユーロ程度・クレジットカードのタッチ決済や硬貨でゲートを通過）が一般的です。美術館・カフェ・レストランを利用した際にこまめに済ませておくのが鉄則です。"
    else:
        toilet_rule = "トイレットペーパーはそのまま流せますが、日本のようにコンビニで自由にトイレを借りられない都市が多いため、大型ショッピングモール・ホテル・利用中のカフェやレストランで済ませておくのが安心です。"

    if cc in ("タイ", "シンガポール", "台湾", "香港", "マカオ", "インド"):
        taboo_rule = f"{cc}では『電子タバコ（VAPE）や加熱式タバコ（IQOS等）の持ち込み・所持・使用』が法律で厳しく禁止されており、違反すると高額な罰金や没収の対象となります。また地下鉄・駅構内での飲食禁止（台湾・シンガポール・香港など）や、寺院訪問時の露出の多い服装（短パン・ノースリーブ）にも注意してください。"
    elif cc in ("アラブ首長国連邦（UAE）", "カタール", "エジプト", "モロッコ", "トルコ", "マレーシア", "インドネシア", "モルディブ", "ウズベキスタン"):
        taboo_rule = "イスラム文化圏（または宗教施設が多い地域）のため、モスク等の宗教施設を訪れる際は肌や髪の露出を控えた服装が必須です。また公共の場での過度な飲酒・泥酔、軍事施設・政府機関・現地女性への無断カメラ撮影はトラブルや処罰の原因となるため厳禁です。"
    elif cc in ("アメリカ", "カナダ", "オーストラリア", "ニュージーランド", "イギリス"):
        taboo_rule = "公共の屋外（路上・公園・ビーチ・車内など）での飲酒（オープン・コンテナ法）が法律で厳しく禁止されている州・都市が多くあります。また屋内施設は全面禁煙が徹底されており、飲酒やクラブ入店時は年齢を問わずパスポート等の顔写真付きID提示が求められます。"
    else:
        taboo_rule = "教会や大聖堂に入る際は帽子を脱ぎ、肩や膝が露出する服装は避けてください。またスリ防犯のためズボンの後ろポケットに財布やスマホを入れず、レストランのテーブル上にスマホを置いたままにしないことが重要です。日曜日・祝日は法律によりスーパーや商業施設が全面休業となる都市が多いため買い出しは土曜までに済ませましょう。"

    return f"""
    <section class="bg-white p-4 sm:p-5 rounded-2xl shadow-sm border border-slate-200 space-y-3.5">
      <div class="border-b border-slate-100 pb-2.5 flex items-center justify-between">
        <h2 class="text-sm sm:text-base font-extrabold text-slate-900">{city['name_ja']}のお金・マナー・生活ルール詳細ガイド</h2>
        <span class="text-[10px] bg-slate-100 text-slate-600 font-bold px-2.5 py-0.5 rounded-full">現地実用辞典</span>
      </div>
      <div class="text-xs space-y-3 text-slate-700 leading-relaxed">
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">1. チップの相場とスマートな渡し方（目安：{city['tip_badge']}）</p>
          <p>{city['tip_detail']}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">2. 両替・クレジットカード決済・ATM利用の鉄則（通貨：{city['currency_name']} / {curr}）</p>
          <p>{payment_rule}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">3. 税金・免税手続き（Tax Free / VAT還付）</p>
          <p>{city['tax_note']}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">4. コンセント（{city['plug_type']}タイプ）・電圧（{city['voltage']} / {city['frequency']}）・変圧器</p>
          <p>{city['transformer_note']}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">5. 水道水・氷・飲食店での水注文</p>
          <p>{city['tap_water_note']}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">6. トイレ事情・衛生ルール</p>
          <p>{toilet_rule}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">7. 現地マナー・法律規制（喫煙・飲酒・服装・禁忌）</p>
          <p>{taboo_rule}</p>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <p class="font-bold text-slate-900 mb-1">8. サマータイム（夏時間）制度</p>
          <p>{city['dst_note']}</p>
        </div>
      </div>
      {render_epos_affiliate(city)}
    </section>"""


def render_agoda_and_oooh_box(city: dict) -> str:
    return f"""
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3.5 rounded-xl bg-violet-50/80 border border-violet-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold bg-violet-600 text-white px-2 py-0.5 rounded">最大80%OFF</span>
              <span class="text-[9px] bg-white/80 text-slate-500 px-1.5 py-0.5 rounded border border-slate-200">PR</span>
            </div>
            <p class="text-xs font-extrabold text-violet-950 mt-1.5">{city['name_ja']}の人気ホテル格安予約【アゴダ】</p>
            <p class="text-[11px] text-slate-700 mt-1 leading-relaxed">
              空港アクセスが良く治安の安定したエリアのホテル・アパートメントを格安検索。予約手数料なし・即時確定（WEBブラウザから簡単予約）。
            </p>
          </div>
          <a href="{AFFILIATE_AGODA_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-violet-600 hover:bg-violet-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition shadow-sm">
            アゴダで{city['name_ja']}の宿を見る
          </a>
        </div>

        <div class="p-3.5 rounded-xl bg-emerald-50/80 border border-emerald-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded">チャット相談無料</span>
              <span class="text-[9px] bg-white/80 text-slate-500 px-1.5 py-0.5 rounded border border-slate-200">PR</span>
            </div>
            <p class="text-xs font-extrabold text-emerald-950 mt-1.5">現地旅行会社に日本語で直接相談【Oooh】</p>
            <p class="text-[11px] text-slate-700 mt-1 leading-relaxed">
              専用車の空港送迎・プライベートツアー・レストラン手配まで、現地在住の旅のプロにスマホから日本語チャットで無料相談＆直接手配できます。
            </p>
          </div>
          <a href="{AFFILIATE_OOOH_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition shadow-sm">
            無料で現地プロに相談する
          </a>
        </div>
      </div>"""


def render_telecom_box(city: dict) -> str:
    ui = city.get("special_ui", "standard")
    if ui == "china_vpn":
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border-2 border-rose-300">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-extrabold text-rose-800">中国ネット検閲対策：Cross eSIM ＋ NordVPN</h2>
        <span class="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded-full">PR / 最重要</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">世界125以上の国・地域対応【Cross eSIM】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">日本国内で事前設定可能・QRコード読み取りだけで最短3分開通。SIM差し替え不要。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            Cross eSIM公式サイトを見る
          </a>
        </div>
        <div class="p-3 rounded-xl bg-rose-50 border border-rose-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-rose-900">制限回避＆通信暗号化【NordVPN】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">AV-TEST評価の高速VPN・30日間返金保証付き。必ず日本出発前にアプリを準備してください。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            NordVPN公式サイトを見る
          </a>
        </div>
      </div>
    </section>"""
    else:
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold text-slate-900">現地の通信（Cross eSIM）＆ フリーWi-Fi保護（NordVPN）</h2>
        <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">PR</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">最短3分・QRで即開通【Cross eSIM】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">125以上の国・地域対応。SIM差し替え・空港受取不要で、到着直後からネットが使えます。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            Cross eSIM公式サイトを見る
          </a>
        </div>
        <div class="p-3 rounded-xl bg-slate-100 border border-slate-300 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-slate-900">海外Wi-Fiセキュリティに【NordVPN】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">空港・カフェ・ホテルのフリーWi-Fiでの通信を暗号化保護。日本のエンタメ視聴にも（30日間返金保証）。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            NordVPN公式サイトを見る
          </a>
        </div>
      </div>
    </section>"""


def render_epos_affiliate(city: dict) -> str:
    ui = city.get("special_ui", "standard")
    if ui == "us_tip_medical":
        headline = f"{city['name_ja']}の高額医療費・カード決済対策に【エポスカード】"
        desc = "北米は医療費が極めて高額なため海外旅行保険の準備が必須です。<strong>入会金・年会費永年無料</strong>で、旅行代金等のお支払いで適用される<strong>充実の海外旅行傷害保険（利用付帯）</strong>、さらに<strong>タッチ決済＆裏面カード番号記載</strong>で安全に決済できます。"
        bg_cls = "bg-rose-50 border-rose-200"
        btn_cls = "bg-rose-600 hover:bg-rose-700"
    elif ui == "europe_cashless":
        headline = f"{city['name_ja']}のタッチ決済＆海外旅行保険対策に【エポスカード】"
        desc = "地下鉄やカフェでのタッチ決済が主流です。<strong>入会金・年会費永年無料</strong>で<strong>タッチ決済対応・裏面カード番号記載</strong>の安心設計に加え、旅行代金等のお支払いで適用される<strong>海外旅行傷害保険（利用付帯）</strong>も備えた定番の1枚です。"
        bg_cls = "bg-indigo-50 border-indigo-200"
        btn_cls = "bg-indigo-600 hover:bg-indigo-700"
    else:
        headline = f"{city['name_ja']}渡航の海外旅行保険・防犯対策に【エポスカード】"
        desc = "<strong>入会金・年会費永年無料</strong>。旅行代金（ツアー料金や交通費等）のお支払いで適用される<strong>海外旅行傷害保険（利用付帯）</strong>が付帯し、さらに<strong>カード番号裏面記載＆タッチ決済</strong>で海外でも周囲から番号が見えず安心です。"
        bg_cls = "bg-amber-50 border-amber-200"
        btn_cls = "bg-amber-600 hover:bg-amber-700"

    return f"""
      <div class="p-4 rounded-xl {bg_cls} border mt-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div class="flex items-center gap-1.5">
            <p class="text-xs font-extrabold text-slate-900">{headline}</p>
            <span class="text-[9px] bg-white/80 text-slate-500 px-1.5 py-0.5 rounded border border-slate-200">PR</span>
          </div>
          <p class="text-[11px] text-slate-700 mt-1 leading-relaxed">{desc}</p>
        </div>
        <a href="{AFFILIATE_CARD_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 {btn_cls} text-white text-xs font-bold px-3.5 py-2.5 rounded-lg text-center transition">
          エポスカード詳細
        </a>
      </div>"""


def render_city_comparison_section(city: dict, all_cities: list, city_compare_links: list) -> str:
    same_region = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:3]
    if not same_region:
        same_region = [c for c in all_cities if c["slug"] != city["slug"]][:3]

    rows = ""
    for c in [city] + same_region:
        is_self = (c["slug"] == city["slug"])
        row_cls = "bg-blue-50/60 font-bold" if is_self else "hover:bg-slate-50"
        name_cell = f"{c['name_ja']}（当ページ）" if is_self else f'<a href="../{c["slug"]}/" class="text-blue-700 underline">{c["name_ja"]}</a>'
        rows += f"""
          <tr class="{row_cls}">
            <td class="p-2.5 border-t border-slate-200">{name_cell}</td>
            <td class="p-2.5 border-t border-slate-200">{c['plug_type']} / {c['voltage']}</td>
            <td class="p-2.5 border-t border-slate-200">{c['currency_code']}</td>
            <td class="p-2.5 border-t border-slate-200">{c['tip_badge'].split('（')[0]}</td>
          </tr>"""

    comp_buttons = "".join([
        f'<a href="../compare/{pair_slug}/" class="text-xs bg-indigo-50 hover:bg-indigo-100 text-indigo-900 border border-indigo-200 font-bold px-3 py-2 rounded-xl transition">'
        f'{label} 徹底比較ページへ →'
        f'</a>'
        for pair_slug, label in city_compare_links
    ])

    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-1">
        <h2 class="text-sm font-bold text-slate-900">{city['name_ja']}と周辺・人気都市のスペック比較</h2>
        <span class="text-[10px] text-slate-500">{city['region']}エリア比較</span>
      </div>
      <div class="overflow-x-auto border border-slate-200 rounded-xl">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr class="bg-slate-100 text-slate-700">
              <th class="p-2.5">都市名</th>
              <th class="p-2.5">プラグ / 電圧</th>
              <th class="p-2.5">通貨</th>
              <th class="p-2.5">チップ</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="flex flex-wrap gap-2 pt-1">{comp_buttons}</div>
    </section>"""


def build_city_html(city: dict, rates_data: dict, all_cities: list, city_compare_links: list) -> str:
    code = city["currency_code"]
    jpy_to_local = rates_data["rates"].get(code, 0.01)
    local_to_jpy = round(1 / jpy_to_local, 2) if jpy_to_local >= 0.005 else round(1 / jpy_to_local, 4)
    thousand_jpy_in_local = round(1000 * jpy_to_local, 2)
    page_url = f"{SITE_URL}/{city['slug']}/"
    page_title = f"{city['name_ja']}の現地情報まとめ｜時差・天気/1年カレンダー・コンセント({city['plug_type']})・チップ・生活ルール"
    page_desc = f"{city['name_ja']}（{city['country_ja']}）の現在時刻・時差、現在の気温・1年カレンダー、コンセント（{city['plug_type']}）・電圧（{city['voltage']}）、チップ＆割り勘計算機、ざっくり物価目安、お金・トイレ・マナー詳細を1画面で即確認。"

    related = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:14]
    related_html = "".join([
        f'<a href="../{c["slug"]}/" class="text-xs bg-white border border-slate-200 px-3 py-1.5 rounded-lg hover:border-blue-500 transition">{c["name_ja"]}</a>'
        for c in related
    ])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{city['name_ja']}のコンセント形状と変圧器の必要性は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"{city['name_ja']}（{city['country_ja']}）のコンセントは{city['plug_type']}タイプ、電圧は{city['voltage']}（{city['frequency']}）です。{city['transformer_note']}"}
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}の気候・季節感・おすすめの時期は？",
                "acceptedAnswer": {"@type": "Answer", "text": city['climate']}
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}でチップは必要ですか？相場は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"{city['tip_badge']}です。{city['tip_detail']}"}
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}の危険情報レベル・治安・日本大使館の連絡先は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"外務省危険情報目安は「{city['danger_level']}」、緊急通報は「{city['emergency_numbers']}」、管轄公館は「{city['embassy']}」です。{city['safety_note']}"}
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url)}
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <link rel="canonical" href="{page_url}">
  <link rel="manifest" href="../manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-12">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">{SITE_NAME}（全都市一覧へ）</a>
      <span class="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full font-medium">{city['region']} / {city['country_ja']}</span>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 pt-4 space-y-4">
    <div class="flex items-baseline justify-between flex-wrap gap-1">
      <h1 class="text-2xl font-extrabold tracking-tight">{city['name_ja']} <span class="text-sm font-normal text-slate-500">{city['name_en']}</span></h1>
      <span class="text-[11px] text-slate-400">為替更新: {rates_data['updated_at']}</span>
    </div>

    <section class="bg-gradient-to-r from-sky-50 to-indigo-50 border border-sky-200 rounded-2xl p-3.5 space-y-2">
      <div class="flex items-center justify-between gap-2">
        <div class="flex items-center gap-2.5">
          <span id="weather-icon" class="text-2xl">⛅</span>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-xs font-bold text-slate-700">現在の現地気温・天気:</span>
              <span id="weather-temp" class="text-sm font-extrabold text-sky-900">取得中...</span>
            </div>
            <p id="weather-outfit" class="text-[11px] font-medium text-sky-950 mt-0.5">現地の気象データから服装の目安を計算しています...</p>
          </div>
        </div>
        <span class="text-[10px] bg-white/90 text-sky-800 px-2 py-0.5 rounded-full font-bold shrink-0 border border-sky-200">LIVE気象</span>
      </div>
      
    <section class="grid grid-cols-2 gap-2.5">
      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-500">現地時刻</span>
          <button id="tz-toggle" class="text-[10px] bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded text-slate-600 font-medium">vs 日本</button>
        </div>
        <div id="local-clock" class="text-2xl font-mono font-bold mt-1.5 tracking-tight">--:--:--</div>
        <div id="time-diff" class="text-xs font-bold text-blue-600 mt-1">時差を計算中...</div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 text-center flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500 block text-left">プラグ・電圧</span>
        <div class="my-0.5">{render_plug_svg(city['plug_type'])}</div>
        <div>
          <div class="text-sm font-extrabold">{city['plug_type']}タイプ <span class="text-xs font-normal text-slate-500">/ {city['voltage']}</span></div>
          <div class="text-[11px] text-emerald-700 font-medium">{'変圧器が必要' if city['transformer_needed'] else 'スマホ変圧器不要'}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">チップ習慣</span>
        <div class="my-1.5">
          <span class="inline-block px-2.5 py-1 rounded-lg text-xs font-extrabold border {tip_color_class(city['tip_level'])}">
            {city['tip_badge']}
          </span>
        </div>
        <div class="text-[11px] text-slate-500">水道水: {'飲用可' if city['tap_water_safe'] else '飲用不可（市販水推奨）'}</div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">1{code} ≒ {local_to_jpy}円</span>
        <div class="mt-1">
          <div class="flex items-center border border-slate-300 rounded-lg px-2 py-1 bg-slate-50">
            <input id="jpy-input" type="number" value="1000" class="w-full bg-transparent text-sm font-bold focus:outline-none">
            <span class="text-xs text-slate-500 ml-1">円</span>
          </div>
          <div id="local-output" class="text-sm font-extrabold text-emerald-700 mt-1">≒ {thousand_jpy_in_local} {code}</div>
        </div>
      </div>
    </section>

    {render_countdown_calendar(city)}

    {render_city_rating_box(city)}

    {render_annual_calendar_box(city)}

    {render_detailed_rules_and_manners(city)}

    {render_tip_split_calculator(city, jpy_to_local, local_to_jpy)}

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-2.5">
      <h2 class="text-sm font-bold text-slate-800">{city['airport_access']['airport_name']}から市内への移動</h2>
      <div class="text-xs space-y-2 text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
        <p><span class="inline-block bg-blue-100 text-blue-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最速・快適</span>{city['airport_access']['fastest']}</p>
        <p><span class="inline-block bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最安・定番</span>{city['airport_access']['cheapest']}</p>
      </div>
      <div class="text-xs text-slate-700 pt-1">
        <strong class="text-slate-900">必須の移動・配車アプリ：</strong>{', '.join(city['transport_apps'])}
      </div>
    </section>

    {render_sightseeing_and_agency_box(city)}

    {render_telecom_box(city)}

    <section class="bg-white p-4 rounded-2xl shadow-sm border-l-4 border-l-rose-500 border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-sm font-extrabold text-slate-900">安全・危険情報・日本大使館連絡先</h2>
        <span class="text-[11px] bg-rose-50 text-rose-700 font-bold px-2.5 py-0.5 rounded-full border border-rose-200">緊急通報: {city['emergency_numbers']}</span>
      </div>
      <div class="p-2.5 rounded-xl border text-xs font-bold flex items-center justify-between flex-wrap gap-1 {danger_badge_class(city['danger_color'])}">
        <span>外務省 危険情報目安：{city['danger_level']}</span>
        <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="underline text-[11px]">外務省公式ページ ↗</a>
      </div>
      <div class="text-xs space-y-2 text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
        <p><strong class="text-slate-900">現地の治安・注意点：</strong>{city['safety_note']}</p>
        <p><strong class="text-slate-900">日本大使館・総領事館：</strong>{city['embassy']}</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
        <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="flex items-center justify-center bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold py-2.5 px-3 rounded-xl transition">
          外務省「{city['country_ja']}」安全情報を見る ↗
        </a>
        <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="flex items-center justify-center bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold py-2.5 px-3 rounded-xl transition">
          外務省「たびレジ」に登録する（無料） ↗
        </a>
      </div>
    </section>

    {render_city_comparison_section(city, all_cities, city_compare_links)}

    {render_share_buttons(page_url, page_title)}

    {render_sister_site_banner()}

    <section class="pt-2">
      <h3 class="text-xs font-bold text-slate-500 mb-2">{city['region']}の他の都市をチェック</h3>
      <div class="flex flex-wrap gap-1.5">{related_html}</div>
    </section>

    <footer class="pt-6 pb-4 text-center text-[11px] text-slate-400 space-y-1.5">
      <p>※本ページはプロモーション（アフィリエイト広告）が含まれています。渡航前に必ず外務省・各国大使館の最新公式情報をご確認ください。</p>
      <p><a href="../policy/" class="underline hover:text-slate-600">プライバシーポリシー・免責事項・運営者情報</a></p>
      <p>© {SITE_NAME} ({SITE_URL})</p>
    </footer>
  </main>

  {render_pixels()}

  <script>
    {render_share_script()}
    const citySlug = "{city['slug']}";
    const targetTz = "{city['timezone']}";
    const cityNameEn = "{city['name_en']}";
    let compareWithLocal = false;

    function updateClock() {{
      const now = new Date();
      const targetStr = now.toLocaleTimeString('ja-JP', {{ timeZone: targetTz, hour12: false }});
      document.getElementById('local-clock').textContent = targetStr;

      const baseTz = compareWithLocal ? Intl.DateTimeFormat().resolvedOptions().timeZone : 'Asia/Tokyo';
      const targetDate = new Date(now.toLocaleString('en-US', {{ timeZone: targetTz }}));
      const baseDate = new Date(now.toLocaleString('en-US', {{ timeZone: baseTz }}));
      const diffHours = Math.round((targetDate - baseDate) / 3600000);
      const sign = diffHours >= 0 ? '+' : '';
      const label = compareWithLocal ? '現在地との時差' : '日本との時差';
      document.getElementById('time-diff').textContent = `${{label}}: ${{sign}}${{diffHours}}時間`;
    }}

    document.getElementById('tz-toggle').addEventListener('click', (e) => {{
      compareWithLocal = !compareWithLocal;
      e.target.textContent = compareWithLocal ? 'vs 現在地' : 'vs 日本';
      updateClock();
    }});

    setInterval(updateClock, 1000);
    updateClock();

    const rate = {jpy_to_local};
    const localToJpy = {local_to_jpy};
    const jpyInput = document.getElementById('jpy-input');
    const localOutput = document.getElementById('local-output');
    jpyInput.addEventListener('input', () => {{
      const val = parseFloat(jpyInput.value) || 0;
      localOutput.textContent = `≒ ${{(val * rate).toFixed(2)}} {code}`;
    }});

    const billAmount = document.getElementById('bill-amount');
    const billTip = document.getElementById('bill-tip');
    const billSplit = document.getElementById('bill-split');
    function updateBillCalc() {{
      const amt = parseFloat(billAmount.value) || 0;
      const tipPct = parseFloat(billTip.value) || 0;
      const split = parseInt(billSplit.value, 10) || 1;
      const totalLocal = amt * (1 + tipPct / 100);
      const totalJpy = Math.round(totalLocal * localToJpy);
      const perLocal = totalLocal / split;
      const perJpy = Math.round(totalJpy / split);
      document.getElementById('bill-total-local').textContent = `${{totalLocal.toFixed(1)}} {code}`;
      document.getElementById('bill-total-jpy').textContent = totalJpy.toLocaleString();
      document.getElementById('bill-per-local').textContent = `${{perLocal.toFixed(1)}} {code}`;
      document.getElementById('bill-per-jpy').textContent = perJpy.toLocaleString();
    }}
    [billAmount, billTip, billSplit].forEach(el => el.addEventListener('input', updateBillCalc));
    updateBillCalc();

    const dateInput = document.getElementById('trip-date-input');
    const countdownMsg = document.getElementById('trip-countdown-msg');
    const savedDate = localStorage.getItem('trip_date_' + citySlug) || localStorage.getItem('trip_date_global');
    if (savedDate) dateInput.value = savedDate;

    function updateCountdown() {{
      if (!dateInput.value) return;
      localStorage.setItem('trip_date_' + citySlug, dateInput.value);
      localStorage.setItem('trip_date_global', dateInput.value);
      const today = new Date();
      today.setHours(0,0,0,0);
      const target = new Date(dateInput.value + 'T00:00:00');
      const diffDays = Math.round((target - today) / 86400000);
      if (diffDays > 14) {{
        countdownMsg.textContent = `出発まであと${{diffDays}}日（パスポート残存期間・宿泊先・ビザ要件の確認時期です）`;
      }} else if (diffDays >= 1) {{
        countdownMsg.textContent = `出発まであと${{diffDays}}日（通信手段・変換プラグ・常備薬の最終確認時期です）`;
      }} else if (diffDays === 0) {{
        countdownMsg.textContent = `本日出発日です。安全なご渡航をお祈りいたします。`;
      }} else {{
        countdownMsg.textContent = `現地滞在中の時刻・為替・チップ確認にご活用ください。`;
      }}
    }}
    dateInput.addEventListener('change', updateCountdown);
    updateCountdown();

    async function fetchWeather() {{
      try {{
        const geoRes = await fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${{encodeURIComponent(cityNameEn)}}&count=1&language=en&format=json`);
        const geoData = await geoRes.json();
        if (!geoData.results || geoData.results.length === 0) throw new Error('No geo');
        const {{ latitude, longitude }} = geoData.results[0];

        const wRes = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${{latitude}}&longitude=${{longitude}}&current=temperature_2m,relative_humidity_2m,weather_code&timezone=auto`);
        const wData = await wRes.json();
        const temp = Math.round(wData.current.temperature_2m);
        const humidity = Math.round(wData.current.relative_humidity_2m);
        const code = wData.current.weather_code;

        let desc = '晴れ';
        if (code >= 1 && code <= 3) desc = '晴れ時々曇り';
        else if (code >= 45 && code <= 48) desc = '霧';
        else if (code >= 51 && code <= 67) desc = '雨';
        else if (code >= 71 && code <= 77) desc = '雪';
        else if (code >= 80 && code <= 82) desc = 'にわか雨';
        else if (code >= 95) desc = '雷雨';

        let outfit = '';
        if (temp >= 28) outfit = '服装目安：半袖・薄手の服（屋内冷房対策に薄手の羽織りを1枚）';
        else if (temp >= 22) outfit = '服装目安：半袖または薄手の長袖シャツが快適';
        else if (temp >= 16) outfit = '服装目安：長袖＋カーディガンやジャケットなど羽織りもの必須';
        else if (temp >= 10) outfit = '服装目安：コートやジャケット・ニットが必要';
        else outfit = '服装目安：冬物コート・ダウンなど防寒対策が必須';

        const dryNote = humidity <= 40 ? '（乾燥注意）' : (humidity >= 80 ? '（高湿度）' : '');
       
        document.getElementById('weather-temp').textContent = `${{temp}}℃（${{desc}} / 湿度${{humidity}}%${{dryNote}}）`;
        document.getElementById('weather-outfit').textContent = outfit;
      }} catch (e) {{
        document.getElementById('weather-icon').textContent = icon;
        document.getElementById('weather-temp').textContent = '下の年間気候目安をご参照ください';
        document.getElementById('weather-outfit').textContent = '渡航前に気象アプリ等で最新気温をご確認ください';
      }}
    }}
    fetchWeather();
  </script>
</body>
</html>"""


def build_compare_html(c1: dict, c2: dict, summary_text: str, rates_data: dict, all_cities: list) -> str:
    """比較ページ（全150×150都市をプルダウンで自由に比較できるインタラクティブ機能付き）"""
    pair_slug = f"{c1['slug']}-vs-{c2['slug']}"
    page_url = f"{SITE_URL}/compare/{pair_slug}/"
    title = f"{c1['name_ja']}と{c2['name_ja']}を徹底比較｜プラグ・チップ・気候・治安・空港移動の違い｜{SITE_NAME}"
    desc = f"{c1['name_ja']}（{c1['country_ja']}）と{c2['name_ja']}（{c2['country_ja']}）の比較ガイド。任意の2都市の組み合わせ比較にも対応。"

    r1 = rates_data["rates"].get(c1["currency_code"], 0.01)
    r2 = rates_data["rates"].get(c2["currency_code"], 0.01)
    jpy1 = round(1 / r1, 2) if r1 >= 0.005 else round(1 / r1, 4)
    jpy2 = round(1 / r2, 2) if r2 >= 0.005 else round(1 / r2, 4)
    s1 = compute_city_star_ratings(c1)
    s2 = compute_city_star_ratings(c2)

    compact_cities = []
    for c in all_cities:
        sr = compute_city_star_ratings(c)
        rc = rates_data["rates"].get(c["currency_code"], 0.01)
        jc = round(1 / rc, 2) if rc >= 0.005 else round(1 / rc, 4)
        compact_cities.append({
            "slug": c["slug"],
            "name_ja": c["name_ja"],
            "country_ja": c["country_ja"],
            "plug_type": c["plug_type"],
            "voltage": c["voltage"],
            "frequency": c["frequency"],
            "tip_badge": c["tip_badge"],
            "tip_detail": c["tip_detail"],
            "currency_name": c["currency_name"],
            "currency_code": c["currency_code"],
            "jpy_rate": jc,
            "tap_water": "飲用可" if c["tap_water_safe"] else "飲用不可（市販水推奨）",
            "climate": c["climate"],
            "fastest": c["airport_access"]["fastest"],
            "danger_level": c["danger_level"],
            "avg_star": sr["avg"]
        })

    options_1 = "".join([
        f'<option value="{c["slug"]}" {"selected" if c["slug"] == c1["slug"] else ""}>{c["name_ja"]}（{c["country_ja"]}）</option>'
        for c in all_cities
    ])
    options_2 = "".join([
        f'<option value="{c["slug"]}" {"selected" if c["slug"] == c2["slug"] else ""}>{c["name_ja"]}（{c["country_ja"]}）</option>'
        for c in all_cities
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(title, desc, page_url)}
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-14">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">{SITE_NAME}（トップへ戻る）</a>
      <span class="text-xs bg-indigo-50 text-indigo-800 px-2.5 py-1 rounded-full font-bold">2都市比較ガイド</span>
    </div>
  </header>

  <main class="max-w-3xl mx-auto px-4 pt-5 space-y-5">
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
      <span class="text-[10px] font-extrabold bg-indigo-600 text-white px-2.5 py-0.5 rounded-full">渡航先比較・150×150組み合わせ対応</span>
      <h1 id="comp-h1" class="text-xl sm:text-2xl font-extrabold">{c1['name_ja']} vs {c2['name_ja']} 現地情報・渡航スペック比較</h1>
      <p id="comp-summary" class="text-xs text-slate-600 leading-relaxed">{summary_text}</p>
    </div>

    <!-- 任意の2都市を自由に選んでその場で比較できるセレクター -->
    <section class="bg-white p-4 rounded-2xl border border-indigo-200 shadow-sm space-y-2.5">
      <p class="text-xs font-extrabold text-slate-900">全{len(all_cities)}都市から好きな2都市を選んでその場で比較（{len(all_cities)}×{len(all_cities)}通り対応）</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
        <div>
          <label class="block text-[10px] font-bold text-slate-500 mb-1">比較する都市 A</label>
          <select id="sel-city-1" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 font-bold text-slate-800">{options_1}</select>
        </div>
        <div>
          <label class="block text-[10px] font-bold text-slate-500 mb-1">比較する都市 B</label>
          <select id="sel-city-2" class="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 font-bold text-slate-800">{options_2}</select>
        </div>
      </div>
    </section>

    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse text-xs">
        <thead>
          <tr class="bg-slate-900 text-white">
            <th class="p-3 w-1/4">比較項目</th>
            <th id="th-c1" class="p-3 w-[37.5%] border-l border-slate-700"><a href="../../{c1['slug']}/" class="underline hover:text-blue-300">{c1['name_ja']}（{c1['country_ja']}）↗</a></th>
            <th id="th-c2" class="p-3 w-[37.5%] border-l border-slate-700"><a href="../../{c2['slug']}/" class="underline hover:text-blue-300">{c2['name_ja']}（{c2['country_ja']}）↗</a></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          <tr>
            <th class="p-3 bg-slate-50 font-bold">総合スペック評価</th>
            <td id="td-star-1" class="p-3 border-l border-slate-100 font-bold text-amber-600">★ {s1['avg']:.1f} / 5.0</td>
            <td id="td-star-2" class="p-3 border-l border-slate-100 font-bold text-amber-600">★ {s2['avg']:.1f} / 5.0</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">コンセント・電圧</th>
            <td id="td-plug-1" class="p-3 border-l border-slate-100 font-bold">{c1['plug_type']}タイプ（{c1['voltage']} / {c1['frequency']}）</td>
            <td id="td-plug-2" class="p-3 border-l border-slate-100 font-bold">{c2['plug_type']}タイプ（{c2['voltage']} / {c2['frequency']}）</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">チップ習慣</th>
            <td id="td-tip-1" class="p-3 border-l border-slate-100"><strong>{c1['tip_badge']}</strong><br><span class="text-[11px] text-slate-500">{c1['tip_detail']}</span></td>
            <td id="td-tip-2" class="p-3 border-l border-slate-100"><strong>{c2['tip_badge']}</strong><br><span class="text-[11px] text-slate-500">{c2['tip_detail']}</span></td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">通貨・為替目安</th>
            <td id="td-curr-1" class="p-3 border-l border-slate-100">{c1['currency_name']}（1{c1['currency_code']} ≒ {jpy1}円）</td>
            <td id="td-curr-2" class="p-3 border-l border-slate-100">{c2['currency_name']}（1{c2['currency_code']} ≒ {jpy2}円）</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">水道水</th>
            <td id="td-water-1" class="p-3 border-l border-slate-100">{'飲用可' if c1['tap_water_safe'] else '飲用不可（市販水推奨）'}</td>
            <td id="td-water-2" class="p-3 border-l border-slate-100">{'飲用可' if c2['tap_water_safe'] else '飲用不可（市販水推奨）'}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">気候・季節感</th>
            <td id="td-clim-1" class="p-3 border-l border-slate-100 text-[11px] leading-relaxed">{c1['climate']}</td>
            <td id="td-clim-2" class="p-3 border-l border-slate-100 text-[11px] leading-relaxed">{c2['climate']}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">空港アクセス</th>
            <td id="td-air-1" class="p-3 border-l border-slate-100 text-[11px]">{c1['airport_access']['fastest']}</td>
            <td id="td-air-2" class="p-3 border-l border-slate-100 text-[11px]">{c2['airport_access']['fastest']}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">外務省危険情報</th>
            <td id="td-dan-1" class="p-3 border-l border-slate-100 text-[11px] font-bold">{c1['danger_level']}</td>
            <td id="td-dan-2" class="p-3 border-l border-slate-100 text-[11px] font-bold">{c2['danger_level']}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <a id="btn-c1" href="../../{c1['slug']}/" class="block bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs p-3.5 rounded-xl text-center transition">{c1['name_ja']}の生活ルール・詳細ページへ →</a>
      <a id="btn-c2" href="../../{c2['slug']}/" class="block bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs p-3.5 rounded-xl text-center transition">{c2['name_ja']}の生活ルール・詳細ページへ →</a>
    </div>

    {render_sightseeing_and_agency_box(c1)}
    {render_telecom_box(c1)}
    {render_share_buttons(page_url, title)}
  </main>
  {render_pixels()}
  <script>
    {render_share_script()}
    const CITIES_DB = {json.dumps(compact_cities, ensure_ascii=False)};
    const cityBySlug = Object.fromEntries(CITIES_DB.map(c => [c.slug, c]));
    const sel1 = document.getElementById('sel-city-1');
    const sel2 = document.getElementById('sel-city-2');

    function renderDynamicCompare() {{
      const a = cityBySlug[sel1.value];
      const b = cityBySlug[sel2.value];
      if (!a || !b) return;
      document.getElementById('comp-h1').textContent = `${{a.name_ja}} vs ${{b.name_ja}} 現地情報・渡航スペック比較`;
      document.getElementById('comp-summary').textContent = `${{a.name_ja}}（${{a.country_ja}}）と${{b.name_ja}}（${{b.country_ja}}）のコンセント・チップ・通貨・気候・安全情報を並べています。`;
      document.getElementById('th-c1').innerHTML = `<a href="../../${{a.slug}}/" class="underline hover:text-blue-300">${{a.name_ja}}（${{a.country_ja}}）↗</a>`;
      document.getElementById('th-c2').innerHTML = `<a href="../../${{b.slug}}/" class="underline hover:text-blue-300">${{b.name_ja}}（${{b.country_ja}}）↗</a>`;
      document.getElementById('td-star-1').textContent = `★ ${{a.avg_star.toFixed(1)}} / 5.0`;
      document.getElementById('td-star-2').textContent = `★ ${{b.avg_star.toFixed(1)}} / 5.0`;
      document.getElementById('td-plug-1').textContent = `${{a.plug_type}}タイプ（${{a.voltage}} / ${{a.frequency}}）`;
      document.getElementById('td-plug-2').textContent = `${{b.plug_type}}タイプ（${{b.voltage}} / ${{b.frequency}}）`;
      document.getElementById('td-tip-1').innerHTML = `<strong>${{a.tip_badge}}</strong><br><span class="text-[11px] text-slate-500">${{a.tip_detail}}</span>`;
      document.getElementById('td-tip-2').innerHTML = `<strong>${{b.tip_badge}}</strong><br><span class="text-[11px] text-slate-500">${{b.tip_detail}}</span>`;
      document.getElementById('td-curr-1').textContent = `${{a.currency_name}}（1${{a.currency_code}} ≒ ${{a.jpy_rate}}円）`;
      document.getElementById('td-curr-2').textContent = `${{b.currency_name}}（1${{b.currency_code}} ≒ ${{b.jpy_rate}}円）`;
      document.getElementById('td-water-1').textContent = a.tap_water;
      document.getElementById('td-water-2').textContent = b.tap_water;
      document.getElementById('td-clim-1').textContent = a.climate;
      document.getElementById('td-clim-2').textContent = b.climate;
      document.getElementById('td-air-1').textContent = a.fastest;
      document.getElementById('td-air-2').textContent = b.fastest;
      document.getElementById('td-dan-1').textContent = a.danger_level;
      document.getElementById('td-dan-2').textContent = b.danger_level;
      document.getElementById('btn-c1').href = `../../${{a.slug}}/`;
      document.getElementById('btn-c1').textContent = `${{a.name_ja}}の生活ルール・詳細ページへ →`;
      document.getElementById('btn-c2').href = `../../${{b.slug}}/`;
      document.getElementById('btn-c2').textContent = `${{b.name_ja}}の生活ルール・詳細ページへ →`;
    }}
    sel1.addEventListener('change', renderDynamicCompare);
    sel2.addEventListener('change', renderDynamicCompare);
  </script>
</body>
</html>"""


def build_feature_html(feat: dict, all_cities: list) -> str:
    page_url = f"{SITE_URL}/features/{feat['slug']}/"
    page_title = f"{feat['title']}｜{SITE_NAME}"
    city_map = {c["slug"]: c for c in all_cities}
    selected = [city_map[s] for s in feat["cities"] if s in city_map]

    cards = ""
    for c in selected:
        r = compute_city_star_ratings(c)
        cards += (
            f'<a href="../../{c["slug"]}/" class="block bg-white p-4 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition space-y-1.5">'
            f'<div class="flex items-center justify-between">'
            f'<span class="font-extrabold text-sm text-slate-900">{c["name_ja"]}</span>'
            f'<span class="text-[11px] font-bold text-amber-600">★ {r["avg"]:.1f} <span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded ml-1">{c["country_ja"]}</span></span>'
            f'</div>'
            f'<p class="text-[11px] text-slate-600 line-clamp-2">{c["climate"]}</p>'
            f'<div class="text-[11px] text-slate-500 flex flex-wrap gap-2 pt-1">'
            f'<span>プラグ: {c["plug_type"]}</span><span>チップ: {c["tip_badge"].split("（")[0]}</span><span>通貨: {c["currency_code"]}</span>'
            f'</div>'
            f'</a>'
        )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, feat['desc'], page_url)}
  <title>{page_title}</title>
  <meta name="description" content="{feat['desc']}">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-14">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">{SITE_NAME}（全150都市一覧へ）</a>
      <span class="text-xs bg-amber-100 text-amber-900 px-2.5 py-1 rounded-full font-bold">{feat['badge']}</span>
    </div>
  </header>

  <main class="max-w-3xl mx-auto px-4 pt-5 space-y-5">
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
      <span class="text-[10px] font-extrabold bg-blue-600 text-white px-2.5 py-0.5 rounded-full">{feat['badge']}</span>
      <h1 class="text-xl sm:text-2xl font-extrabold">{feat['title']}</h1>
      <p class="text-xs text-slate-600 leading-relaxed">{feat['desc']}</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">{cards}</div>

    {render_sightseeing_and_agency_box(selected[0])}
    {render_telecom_box(selected[0])}
    {render_share_buttons(page_url, feat['title'])}
  </main>
  {render_pixels()}
  <script>{render_share_script()}</script>
</body>
</html>"""


def build_policy_html() -> str:
    page_url = f"{SITE_URL}/policy/"
    page_title = f"プライバシーポリシー・免責事項・運営者情報｜{SITE_NAME}"
    page_desc = f"{SITE_NAME}のプライバシーポリシー、免責事項、運営者情報。"
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url)}
  <title>{page_title}</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">{SITE_NAME}（トップへ戻る）</a>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 pt-6 space-y-6 text-xs sm:text-sm text-slate-700 leading-relaxed">
    <h1 class="text-xl sm:text-2xl font-extrabold text-slate-900">プライバシーポリシー・免責事項・運営者情報</h1>
    <section class="bg-white p-5 rounded-2xl border border-slate-200 space-y-2">
      <h2 class="font-bold text-base text-slate-900">1. 免責事項（当サイトの情報について）</h2>
      <p>「{SITE_NAME}」（{SITE_URL}）に掲載している各国の時差、気象・気候データ、電圧・プラグ形状、チップ習慣、税金・免税制度、交通アクセス、為替レート、外務省危険情報・渡航情報等は、執筆・更新時点の調査データおよび外部APIをもとに作成しておりますが、その正確性・最新性・完全性を保証するものではありません。</p>
      <p>ご渡航の際は、必ず<strong>外務省「海外安全ホームページ」</strong>、駐日各国大使館、およびご利用の航空会社等の公式最新情報をご自身でご確認ください。</p>
    </section>
    <section class="bg-white p-5 rounded-2xl border border-slate-200 space-y-2">
      <h2 class="font-bold text-base text-slate-900">2. 広告の配信・アフィリエイトプログラムについて</h2>
      <p>当サイトは、第三者配信の広告サービス（Google AdSense）およびアフィリエイトプログラム（A8.net 等）に参加しており、適格販売・申込により収入を得る場合があります。</p>
    </section>
    <section class="bg-white p-5 rounded-2xl border border-slate-200 space-y-2">
      <h2 class="font-bold text-base text-slate-900">3. アクセス解析ツールについて</h2>
      <p>当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス（GA4）」を利用しています。データは匿名で収集されており、個人を特定するものではありません。</p>
    </section>
    <section class="bg-white p-5 rounded-2xl border border-slate-200 space-y-2">
      <h2 class="font-bold text-base text-slate-900">4. 運営者情報</h2>
      <p><strong>サイト名：</strong>{SITE_NAME} / <strong>URL：</strong>{SITE_URL} / <strong>運営：</strong>{SITE_NAME} 編集部</p>
    </section>
  </main>
</body>
</html>"""


def build_index_html(cities: list, rates_data: dict, featured_compare_pairs: list) -> str:
    unique_regions = ["すべて"] + sorted(list({c["region"] for c in cities}))
    page_url = f"{SITE_URL}/"
    page_title = f"{SITE_NAME}｜世界{len(cities)}都市の時差・天気/1年カレンダー・コンセント・チップ・生活ルール"
    page_desc = f"海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・リアルタイム気温・1年カレンダー・コンセント・チップ計算機・生活マナー・最新為替を1画面で即解決。"
    city_map = {c["slug"]: c for c in cities}

    region_buttons = "".join([
        f'<button data-region="{r}" class="region-btn shrink-0 px-3 py-1.5 rounded-full text-xs font-bold border transition '
        f'{"bg-slate-900 text-white border-slate-900" if r == "すべて" else "bg-white text-slate-600 border-slate-200"}">{r}</button>'
        for r in unique_regions
    ])

    card_list = []
    for c in cities:
        r = compute_city_star_ratings(c)
        if c["special_ui"] == "china_vpn":
            vpn_badge = '<span class="text-[10px] text-rose-600 font-bold">要VPN/eSIM</span>'
        elif c["special_ui"] == "vpn_recommended":
            vpn_badge = '<span class="text-[10px] text-indigo-600 font-bold">VPN推奨</span>'
        else:
            vpn_badge = ""
        danger_dot = '<span class="text-[10px] text-amber-700 font-bold">注意喚起あり</span>' if c["danger_color"] != "emerald" else ""
        tip_short = c["tip_badge"].split("（")[0]
        search_str = f'{c["name_ja"]} {c["kana_kw"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}'
        card_list.append(
            f'<a href="./{c["slug"]}/" data-region="{c["region"]}" '
            f'data-name="{c["name_ja"]}" data-country="{c["country_ja"]}" data-slug="{c["slug"]}" '
            f'data-search="{search_str}" '
            f'class="city-card block bg-white p-3.5 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition">'
            f'<div class="flex items-center justify-between gap-1">'
            f'<span class="font-extrabold text-sm text-slate-900">{c["name_ja"]}</span>'
            f'<span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium shrink-0">{c["country_ja"]} / ★{r["avg"]:.1f}</span>'
            f'</div>'
            f'<div class="text-[11px] text-slate-500 mt-1.5 flex items-center gap-2 flex-wrap">'
            f'<span>プラグ:{c["plug_type"]}</span>'
            f'<span>通貨:{c["currency_code"]}</span>'
            f'<span>チップ:{tip_short}</span>'
            f'{vpn_badge}'
            f'{danger_dot}'
            f'</div>'
            f'</a>'
        )
    cards_html = "\n".join(card_list)

    feature_links = "".join([
        f'<a href="./features/{f["slug"]}/" class="block bg-white border border-slate-200 p-3 rounded-xl hover:border-blue-500 shadow-sm transition">'
        f'<span class="text-[10px] font-extrabold bg-blue-600 text-white px-2 py-0.5 rounded">{f["badge"]}</span>'
        f'<p class="text-xs font-extrabold text-slate-900 mt-1 leading-snug">{f["title"]}</p>'
        f'</a>'
        for f in FEATURE_PAGES
    ])

    compare_links = "".join([
        f'<a href="./compare/{s1}-vs-{s2}/" class="text-[11px] bg-slate-50 border border-slate-200 px-2.5 py-1.5 rounded-lg font-bold text-slate-700 hover:border-indigo-500 hover:text-indigo-700 transition">'
        f'{city_map[s1]["name_ja"]} vs {city_map[s2]["name_ja"]}'
        f'</a>'
        for s1, s2, _ in featured_compare_pairs if s1 in city_map and s2 in city_map
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url, og_type="website")}
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <link rel="canonical" href="{page_url}">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  {render_pr_banner()}
  <main class="max-w-3xl mx-auto px-4 pt-7 space-y-5">
    <div class="text-center space-y-1.5">
      <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">{SITE_NAME}</h1>
      <p class="text-xs sm:text-sm text-slate-600">世界{len(cities)}都市の「時差・気温/1年カレンダー・プラグ・チップ計算・生活マナー・為替・外務省危険情報」を1画面で即答</p>
    </div>

    <div class="sticky top-2 z-30 bg-slate-50/95 backdrop-blur py-2 space-y-2.5">
      <div class="relative">
        <input id="search" type="text" autocomplete="off" placeholder="ひらがな・都市名・国名で予測検索（例：ばり、ぷさん、ロンドン、たいわん）"
          class="w-full p-3.5 rounded-2xl border border-slate-300 bg-white shadow-sm text-sm focus:outline-none focus:border-blue-500">
        <div id="suggest-box" class="hidden absolute left-0 right-0 mt-1 bg-white border border-slate-200 rounded-2xl shadow-lg max-h-64 overflow-y-auto z-40 divide-y divide-slate-100"></div>
      </div>
      <div class="flex gap-1.5 overflow-x-auto pb-1 no-scrollbar">{region_buttons}</div>
    </div>

    <section class="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-xs sm:text-sm font-extrabold text-slate-900">季節・テーマ別特集 ＆ 2都市比較ガイド</h2>
        <span class="text-[10px] text-slate-400">全{len(cities)}×{len(cities)}都市比較に対応</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">{feature_links}</div>
      <details class="group pt-1">
        <summary class="cursor-pointer text-xs font-bold text-indigo-700 hover:text-indigo-900 flex items-center justify-between bg-indigo-50/60 px-3 py-2 rounded-xl border border-indigo-100 list-none">
          <span>2都市比較ページを開く（任意の2都市を自由に組み合わせて比較可能）</span>
          <span class="text-[10px] group-open:hidden">一覧を開く ▼</span>
          <span class="text-[10px] hidden group-open:inline">閉じる ▲</span>
        </summary>
        <div class="flex flex-wrap gap-1.5 pt-2.5">{compare_links}</div>
      </details>
    </section>

    <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">{cards_html}</div>

    {render_sister_site_banner()}

    {render_share_buttons(page_url, page_title)}

    <footer class="pt-6 text-center text-xs text-slate-400 space-y-2">
      <p>安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">たびレジ</a></p>
      <p><a href="./policy/" class="underline hover:text-slate-600">プライバシーポリシー・免責事項・運営者情報</a></p>
      <p>© {SITE_NAME} ({SITE_URL})</p>
    </footer>
  </main>

  {render_pixels()}

  <script>
    {render_share_script()}
    let currentRegion = 'すべて';
    const searchInput = document.getElementById('search');
    const suggestBox = document.getElementById('suggest-box');
    const cards = Array.from(document.querySelectorAll('.city-card'));
    const regionBtns = document.querySelectorAll('.region-btn');

    function toHiragana(str) {{
      return str.replace(/[\\u30a1-\\u30f6]/g, function(match) {{
        const chr = match.charCodeAt(0) - 0x60;
        return String.fromCharCode(chr);
      }});
    }}

    function normalizeText(str) {{
      return toHiragana(str.toLowerCase().trim());
    }}

    function filterCards() {{
      const q = normalizeText(searchInput.value);
      const matchedCards = [];

      cards.forEach(card => {{
        const haystack = normalizeText(card.dataset.search);
        const matchSearch = !q || haystack.includes(q);
        const matchRegion = (currentRegion === 'すべて' || card.dataset.region === currentRegion);
        const visible = matchSearch && matchRegion;
        card.style.display = visible ? 'block' : 'none';
        if (q && matchSearch) {{
          matchedCards.push(card);
        }}
      }});

      if (q.length > 0 && matchedCards.length > 0) {{
        suggestBox.innerHTML = matchedCards.slice(0, 8).map(c => `
          <a href="./${{c.dataset.slug}}/" class="flex items-center justify-between px-4 py-2.5 hover:bg-blue-50 transition text-xs">
            <span class="font-bold text-slate-900">${{c.dataset.name}}</span>
            <span class="text-slate-500">${{c.dataset.country}} →</span>
          </a>
        `).join('');
        suggestBox.classList.remove('hidden');
      }} else {{
        suggestBox.classList.add('hidden');
      }}
    }}

    searchInput.addEventListener('input', filterCards);

    document.addEventListener('click', (e) => {{
      if (!searchInput.contains(e.target) && !suggestBox.contains(e.target)) {{
        suggestBox.classList.add('hidden');
      }}
    }});

    searchInput.addEventListener('focus', () => {{
      if (searchInput.value.trim().length > 0) {{
        filterCards();
      }}
    }});

    regionBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        currentRegion = btn.dataset.region;
        regionBtns.forEach(b => {{
          b.className = 'region-btn shrink-0 px-3 py-1.5 rounded-full text-xs font-bold border transition bg-white text-slate-600 border-slate-200';
        }});
        btn.className = 'region-btn shrink-0 px-3 py-1.5 rounded-full text-xs font-bold border transition bg-slate-900 text-white border-slate-900';
        filterCards();
      }});
    }});
  </script>
</body>
</html>"""
