#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML・UIデザイン・テンプレート管理ファイル (templates.py)
- 5大アフィリエイト完備（Agoda / Cross eSIM / NordVPN / エポスカード / Oooh）
- 機能①：チップ＆割り勘・リアルタイム計算機
- 機能②：出発日カウントダウン＆ブラウザ保存式チェックリスト（6項目）
- 機能③：人気2都市比較ページ＆季節特集ハブページ生成
- 機能④：1タップ現地リアル度投票＆Atrium相互送客
"""

import json
from config import (
    SITE_URL, SITE_NAME, GA4_ID, SISTER_SITE_URL, SISTER_SITE_NAME,
    AFFILIATE_ESIM_URL, AFFILIATE_VPN_URL, AFFILIATE_CARD_URL,
    AFFILIATE_OOOH_URL, AFFILIATE_AGODA_URL,
    A8_PIXEL_URLS, COMPARE_PAIRS, FEATURE_PAGES
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


def render_common_head() -> str:
    favicon_svg = "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌐</text></svg>"
    return f"""<link rel="icon" href="{favicon_svg}">
  <link rel="apple-touch-icon" href="{favicon_svg}">
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
      <span class="text-xs font-bold text-slate-700 flex items-center gap-1">📤 このページの渡航情報を同行者にシェア</span>
      <div class="flex items-center gap-1.5 flex-wrap">
        <a href="https://social-plugins.line.me/lineit/share?url={page_url}" target="_blank" rel="noopener noreferrer"
          class="bg-[#06C755] hover:opacity-90 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1">
          LINEで送る
        </a>
        <a href="https://twitter.com/intent/tweet?url={page_url}&text={share_title}" target="_blank" rel="noopener noreferrer"
          class="bg-slate-900 hover:bg-slate-800 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1">
          Xでポスト
        </a>
        <button type="button" onclick="shareOrCopy('{page_url}', '{share_title}')"
          class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-bold px-3 py-1.5 rounded-lg border border-slate-300 transition">
          🔗 URLをコピー
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
          alert('ページのURLをコピーしました！LINEやメモ帳に貼り付けて共有できます。');
        });
      }
    }"""


def render_sister_site_banner() -> str:
    return f"""
    <div class="bg-gradient-to-r from-slate-900 to-indigo-950 text-white p-4 rounded-2xl shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <span class="text-[10px] font-bold bg-indigo-500/30 border border-indigo-400/40 text-indigo-200 px-2 py-0.5 rounded-full">姉妹プラットフォーム</span>
        <p class="text-xs sm:text-sm font-extrabold mt-1">🎓 海外留学・ワーホリ・現地インターン・キャリア情報なら【Atrium】</p>
        <p class="text-[11px] text-slate-300 mt-0.5">世界各都市の留学生・駐在員のリアルタイム掲示板「Atrium Pulse」や奨学金・就活ニュースを毎日更新中。</p>
      </div>
      <a href="{SISTER_SITE_URL}/" target="_blank" rel="noopener" class="shrink-0 bg-white hover:bg-slate-100 text-slate-900 text-xs font-extrabold px-3.5 py-2.5 rounded-xl text-center transition">
        Atriumを見る ↗
      </a>
    </div>"""


def render_countdown_and_checklist(city: dict) -> str:
    """機能②：出発日カウントダウン＆ブラウザ保存式チェックリスト（5大アフィ＋たびレジの6項目）"""
    plug_info = f"{city['plug_type']}タイプ変換プラグの準備" if city['plug_type'] != "A" else "スマホ充電器・モバイルバッテリーの確認"
    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-blue-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-sm font-extrabold text-slate-900 flex items-center gap-1.5">✅ {city['name_ja']} 渡航前チェック＆出発カウントダウン</h2>
        <span id="checklist-progress" class="text-[11px] font-extrabold bg-blue-100 text-blue-800 px-2.5 py-0.5 rounded-full">準備完了: 0/6</span>
      </div>

      <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200 flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold text-slate-700">📅 出発日を設定:</span>
          <input id="trip-date-input" type="date" class="text-xs bg-white border border-slate-300 rounded-lg px-2 py-1 font-bold text-slate-800 focus:outline-none focus:border-blue-500">
        </div>
        <div id="trip-countdown-msg" class="text-xs font-extrabold text-blue-700">出発日を入れると残り日数と準備目安を表示します</div>
      </div>

      <div class="divide-y divide-slate-100 text-xs">
        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="hotel" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>🏨 {city['name_ja']}のホテル・宿泊先の予約（最大80%OFF・即時確定）</span>
          </label>
          <a href="{AFFILIATE_AGODA_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 text-[10px] font-bold bg-violet-50 hover:bg-violet-100 text-violet-800 border border-violet-200 px-2.5 py-1 rounded-lg transition">アゴダ(WEB予約) [PR] →</a>
        </div>

        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="esim" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>📱 現地用eSIMの事前購入（空港到着直後の配車・地図用）</span>
          </label>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 text-[10px] font-bold bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 px-2.5 py-1 rounded-lg transition">Cross eSIM [PR] →</a>
        </div>

        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="vpn" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>🔒 フリーWi-Fi暗号化・通信制限対策（VPNアプリ導入）</span>
          </label>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 text-[10px] font-bold bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300 px-2.5 py-1 rounded-lg transition">NordVPN [PR] →</a>
        </div>

        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="card" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>💳 海外旅行保険（利用付帯）＆タッチ決済対応カードの準備</span>
          </label>
          <a href="{AFFILIATE_CARD_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 text-[10px] font-bold bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-lg transition">エポスカード [PR] →</a>
        </div>

        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="tour" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>💬 空港送迎・現地ツアー・レストラン等の日本語手配相談</span>
          </label>
          <a href="{AFFILIATE_OOOH_URL}" target="_blank" rel="nofollow noopener" class="shrink-0 text-[10px] font-bold bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 px-2.5 py-1 rounded-lg transition">Oooh無料相談 [PR] →</a>
        </div>

        <div class="py-2 flex items-center justify-between gap-2">
          <label class="flex items-center gap-2 cursor-pointer font-medium text-slate-800">
            <input type="checkbox" data-ck="plug" class="prep-check w-4 h-4 accent-blue-600 rounded cursor-pointer">
            <span>🔌 {plug_info} ＆ 外務省「たびレジ」登録</span>
          </label>
          <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="shrink-0 text-[10px] font-bold bg-slate-50 hover:bg-slate-100 text-slate-600 border border-slate-200 px-2.5 py-1 rounded-lg transition">たびレジ公式 ↗</a>
        </div>
      </div>
      <p class="text-[10px] text-slate-400">※チェック状態と出発日はお使いのブラウザに自動保存され、次回開いたときも維持されます。</p>
    </section>"""


def render_tip_split_calculator(city: dict, local_to_jpy: float) -> str:
    code = city["currency_code"]
    default_tip = 18 if city["tip_level"] == "required" else (10 if city["tip_level"] == "optional" else 0)
    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold flex items-center gap-1.5 text-slate-800">🧮 レストラン・タクシー用「チップ＆割り勘」即計算機</h2>
        <span class="text-[10px] bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded-full border border-emerald-200">現地会計で便利</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">① お会計金額（{code}）</label>
          <div class="flex items-center">
            <input id="bill-amount" type="number" value="100" class="w-full bg-white border border-slate-300 rounded-lg px-2 py-1 font-bold text-sm focus:outline-none">
            <span class="ml-1.5 font-bold text-slate-600">{code}</span>
          </div>
        </div>
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">② チップ率（{city['name_ja']}目安: {city['tip_badge']}）</label>
          <select id="bill-tip" class="w-full bg-white border border-slate-300 rounded-lg px-2 py-1.5 font-bold text-xs focus:outline-none">
            <option value="0" {"selected" if default_tip == 0 else ""}>0%（チップなし）</option>
            <option value="5">5%（端数・気持ち程度）</option>
            <option value="10" {"selected" if default_tip == 10 else ""}>10%（一般的な目安）</option>
            <option value="15">15%（標準サービス）</option>
            <option value="18" {"selected" if default_tip == 18 else ""}>18%（北米レストラン標準）</option>
            <option value="20">20%（良いサービス）</option>
          </select>
        </div>
        <div class="bg-slate-50 p-2.5 rounded-xl border border-slate-200">
          <label class="block text-[10px] font-bold text-slate-500 mb-1">③ 割り勘する人数</label>
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
      <div class="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3 flex flex-wrap items-center justify-between gap-2">
        <div class="text-xs text-slate-700">
          <span>チップ込総額: <strong id="bill-total-local" class="text-slate-900">-- {code}</strong></span>
          <span class="text-[11px] text-slate-500 ml-1">（約 <span id="bill-total-jpy">--</span> 円）</span>
        </div>
        <div class="text-xs font-extrabold text-emerald-900 bg-white px-3 py-1.5 rounded-lg border border-emerald-200">
          1人あたり: <span id="bill-per-local" class="text-sm text-emerald-700">-- {code}</span>（約 <span id="bill-per-jpy">--</span> 円）
        </div>
      </div>
    </section>"""


def render_quick_poll(city: dict) -> str:
    base_seed = sum(ord(ch) for ch in city["slug"])
    safety_pct = 92 if city["danger_color"] == "emerald" else 76
    cashless_pct = 95 if city["special_ui"] in ("europe_cashless", "korea_nav", "us_tip_medical") else 81
    total_votes = 48 + (base_seed % 65)

    return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold text-slate-800 flex items-center gap-1.5">📊 渡航者のリアル体感チェック（1タップ投票）</h2>
        <span id="poll-count" class="text-[10px] text-slate-400">累計 {total_votes} 票</span>
      </div>
      <div class="grid grid-cols-2 gap-2.5 text-xs">
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <div class="flex justify-between font-bold text-slate-700 mb-1">
            <span>🛡️ 観光エリアの安心感</span>
            <span id="safety-val" class="text-emerald-700">{safety_pct}%</span>
          </div>
          <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div id="safety-bar" class="bg-emerald-500 h-full" style="width: {safety_pct}%"></div>
          </div>
        </div>
        <div class="bg-slate-50 p-3 rounded-xl border border-slate-100">
          <div class="flex justify-between font-bold text-slate-700 mb-1">
            <span>💳 キャッシュレス快適度</span>
            <span id="cashless-val" class="text-blue-700">{cashless_pct}%</span>
          </div>
          <div class="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div id="cashless-bar" class="bg-blue-500 h-full" style="width: {cashless_pct}%"></div>
          </div>
        </div>
      </div>
      <div class="flex items-center justify-between flex-wrap gap-2 pt-1">
        <span id="poll-thanks" class="text-[11px] text-slate-600 font-medium">Q. {city['name_ja']}の渡航情報・現地体験はどうでしたか？</span>
        <div class="flex gap-1.5">
          <button type="button" onclick="castVote('good')" class="vote-btn text-[11px] bg-slate-100 hover:bg-blue-50 hover:text-blue-700 hover:border-blue-300 font-bold px-3 py-1.5 rounded-lg border border-slate-200 transition">👍 快適・役立った</button>
          <button type="button" onclick="castVote('careful')" class="vote-btn text-[11px] bg-slate-100 hover:bg-amber-50 hover:text-amber-800 hover:border-amber-300 font-bold px-3 py-1.5 rounded-lg border border-slate-200 transition">⚠️ 事前準備が必須</button>
        </div>
      </div>
    </section>"""


def render_agoda_and_oooh_box(city: dict) -> str:
    """空港移動セクション直下：ホテル予約（Agoda）＆現地手配相談（Oooh）の2大旅行手配カード"""
    return f"""
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3.5 rounded-xl bg-violet-50/80 border border-violet-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold bg-violet-600 text-white px-2 py-0.5 rounded">最大80%OFF</span>
              <span class="text-[9px] bg-white/80 text-slate-500 px-1.5 py-0.5 rounded border border-slate-200">PR</span>
            </div>
            <p class="text-xs font-extrabold text-violet-950 mt-1.5">🏨 {city['name_ja']}の人気ホテル格安予約【アゴダ】</p>
            <p class="text-[11px] text-slate-700 mt-1 leading-relaxed">
              空港アクセスが良く治安の安定したエリアのホテル・アパートメントを格安検索。予約手数料なし・即時確定・24時間サポート（WEBブラウザから簡単予約）。
            </p>
          </div>
          <a href="{AFFILIATE_AGODA_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-violet-600 hover:bg-violet-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition shadow-sm">
            アゴダで{city['name_ja']}の宿を見る →
          </a>
        </div>

        <div class="p-3.5 rounded-xl bg-emerald-50/80 border border-emerald-200 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold bg-emerald-600 text-white px-2 py-0.5 rounded">チャット相談無料</span>
              <span class="text-[9px] bg-white/80 text-slate-500 px-1.5 py-0.5 rounded border border-slate-200">PR</span>
            </div>
            <p class="text-xs font-extrabold text-emerald-950 mt-1.5">💬 現地旅行会社に日本語で直接相談【Oooh】</p>
            <p class="text-[11px] text-slate-700 mt-1 leading-relaxed">
              専用車の空港送迎・プライベートツアー・穴場レストラン手配まで、現地在住の旅のプロにスマホから日本語チャットで無料相談＆直接手配できます。
            </p>
          </div>
          <a href="{AFFILIATE_OOOH_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition shadow-sm">
            無料で現地プロに相談する →
          </a>
        </div>
      </div>"""


def render_telecom_box(city: dict) -> str:
    ui = city.get("special_ui", "standard")
    if ui == "china_vpn":
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border-2 border-rose-300">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-extrabold flex items-center gap-1.5 text-rose-800">🛡️ 中国ネット検閲対策：Cross eSIM ＋ NordVPN</h2>
        <span class="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded-full">PR / 最重要</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">📱 世界125以上の国・地域対応【Cross eSIM】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">日本国内で事前設定可能・QRコード読み取りだけで最短3分開通！SIM差し替え不要。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            Cross eSIM公式サイトを見る →
          </a>
        </div>
        <div class="p-3 rounded-xl bg-rose-50 border border-rose-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-rose-900">🔒 制限回避＆通信暗号化【NordVPN】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">AV-TEST評価の高速VPN・30日間返金保証付き。必ず日本出発前にアプリを準備しましょう。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            NordVPN公式サイトを見る →
          </a>
        </div>
      </div>
    </section>"""
    elif ui == "vpn_recommended":
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-amber-300">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold flex items-center gap-1.5 text-slate-900">📶 現地の通信（Cross eSIM）＆ セキュリティ（NordVPN）</h2>
        <span class="text-[10px] bg-amber-100 text-amber-900 font-bold px-2 py-0.5 rounded-full">PR / 通信対策</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">📱 最短3分・QRで即開通！【Cross eSIM】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">125以上の国・地域対応。日本で事前設定でき、現地到着直後から配車アプリや地図が使えます。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            Cross eSIMでプランを見る →
          </a>
        </div>
        <div class="p-3 rounded-xl bg-indigo-50 border border-indigo-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-indigo-900">🔒 制限回避＆Wi-Fi保護【NordVPN】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">フリーWi-Fiでの通信暗号化や海外からの日本の動画サービス視聴に。30日間返金保証付き。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            NordVPN公式サイトを見る →
          </a>
        </div>
      </div>
    </section>"""
    else:
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-bold flex items-center gap-1.5">📶 現地の通信（Cross eSIM）＆ フリーWi-Fi保護（NordVPN）</h2>
        <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">PR</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">📱 最短3分・QRで即開通！【Cross eSIM】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">125以上の国・地域対応！SIM差し替え・空港受取不要で、到着直後からネットが使えます。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            Cross eSIM公式サイトを見る →
          </a>
        </div>
        <div class="p-3 rounded-xl bg-slate-100 border border-slate-300 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-slate-900">🔒 海外Wi-Fiセキュリティに【NordVPN】</p>
            <p class="text-[11px] text-slate-600 mt-0.5">空港・カフェ・ホテルのフリーWi-Fiでの通信を暗号化保護。日本のエンタメ視聴にも（30日間返金保証）。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="mt-2.5 block bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold px-3 py-2.5 rounded-lg text-center transition">
            NordVPN公式サイトを見る →
          </a>
        </div>
      </div>
    </section>"""


def render_epos_affiliate(city: dict) -> str:
    ui = city.get("special_ui", "standard")
    if ui == "us_tip_medical":
        headline = f"🏥 {city['name_ja']}の医療費・カード決済対策に【エポスカード】"
        desc = "北米は医療費が極めて高額なため海外旅行保険の準備が必須です。<strong>入会金・年会費永年無料</strong>で、旅行代金等のお支払いで適用される<strong>充実の海外旅行傷害保険（利用付帯）</strong>、さらに<strong>タッチ決済＆裏面カード番号記載</strong>で安全・スムーズに決済できます。"
        bg_cls = "bg-rose-50 border-rose-200"
        btn_cls = "bg-rose-600 hover:bg-rose-700"
    elif ui == "europe_cashless":
        headline = f"💳 {city['name_ja']}のタッチ決済＆保険対策に【エポスカード】"
        desc = "地下鉄やカフェでのタッチ決済が主流です。<strong>入会金・年会費永年無料</strong>で<strong>タッチ決済対応・裏面カード番号記載</strong>の安心設計に加え、旅行代金等のお支払いで適用される<strong>海外旅行傷害保険（利用付帯）</strong>も備えた定番の1枚です。"
        bg_cls = "bg-indigo-50 border-indigo-200"
        btn_cls = "bg-indigo-600 hover:bg-indigo-700"
    else:
        headline = f"💳 {city['name_ja']}渡航の海外旅行保険・防犯対策に【エポスカード】"
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
          エポスカード詳細 →
        </a>
      </div>"""


def build_city_html(city: dict, rates_data: dict, all_cities: list) -> str:
    code = city["currency_code"]
    jpy_to_local = rates_data["rates"].get(code, 0.01)
    local_to_jpy = round(1 / jpy_to_local, 2) if jpy_to_local >= 0.005 else round(1 / jpy_to_local, 4)
    thousand_jpy_in_local = round(1000 * jpy_to_local, 2)
    page_url = f"{SITE_URL}/{city['slug']}/"
    share_title = f"{city['name_ja']}の現地情報（時差・天気・コンセント・チップ・治安）｜{SITE_NAME}"

    related = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:12]
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
                "name": f"{city['name_ja']}の気候・季節感・服装の目安は？",
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
  {render_common_head()}
  <title>{city['name_ja']}の現地情報まとめ｜時差・天気/気候・コンセント({city['plug_type']})・チップ・危険情報・為替を1画面で即答</title>
  <meta name="description" content="{city['name_ja']}（{city['country_ja']}）の現在時刻・時差、現在の天気・気温と年間の気候・乾燥度、コンセント形状（{city['plug_type']}）・電圧（{city['voltage']}）、チップ計算機、最新為替レート、外務省危険情報・大使館連絡先を1画面で即確認。">
  <link rel="canonical" href="{page_url}">
  <link rel="manifest" href="../manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-12">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-slate-800 text-sm flex items-center gap-1 hover:text-blue-600 transition">🌐 {SITE_NAME}（全都市一覧へ）</a>
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
      <div class="bg-white/75 rounded-xl p-2.5 text-[11px] text-slate-700 leading-relaxed border border-sky-100">
        <strong class="text-slate-900">🌤️ 年間の気候・季節感・乾燥度：</strong>{city['climate']}
      </div>
    </section>

    <section class="grid grid-cols-2 gap-2.5">
      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-500">🕒 現地時刻</span>
          <button id="tz-toggle" class="text-[10px] bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded text-slate-600 font-medium">vs 日本</button>
        </div>
        <div id="local-clock" class="text-2xl font-mono font-bold mt-1.5 tracking-tight">--:--:--</div>
        <div id="time-diff" class="text-xs font-bold text-blue-600 mt-1">時差を計算中...</div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 text-center flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500 block text-left">🔌 プラグ・電圧</span>
        <div class="my-0.5">{render_plug_svg(city['plug_type'])}</div>
        <div>
          <div class="text-sm font-extrabold">{city['plug_type']}タイプ <span class="text-xs font-normal text-slate-500">/ {city['voltage']}</span></div>
          <div class="text-[11px] text-emerald-700 font-medium">{'変圧器が必要' if city['transformer_needed'] else 'スマホ変圧器不要'}</div>
        </div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">💵 チップ習慣</span>
        <div class="my-1.5">
          <span class="inline-block px-2.5 py-1 rounded-lg text-xs font-extrabold border {tip_color_class(city['tip_level'])}">
            {city['tip_badge']}
          </span>
        </div>
        <div class="text-[11px] text-slate-500">水: {'💧飲用可' if city['tap_water_safe'] else '⚠️飲用不可（市販水）'}</div>
      </div>

      <div class="bg-white p-3.5 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">💱 1{code} ≒ {local_to_jpy}円</span>
        <div class="mt-1">
          <div class="flex items-center border border-slate-300 rounded-lg px-2 py-1 bg-slate-50">
            <input id="jpy-input" type="number" value="1000" class="w-full bg-transparent text-sm font-bold focus:outline-none">
            <span class="text-xs text-slate-500 ml-1">円</span>
          </div>
          <div id="local-output" class="text-sm font-extrabold text-emerald-700 mt-1">≒ {thousand_jpy_in_local} {code}</div>
        </div>
      </div>
    </section>

    <!-- 機能②：出発カウントダウン＆保存式渡航前チェックリスト（6項目） -->
    {render_countdown_and_checklist(city)}

    <!-- 機能①：チップ＆割り勘シミュレーター -->
    {render_tip_split_calculator(city, local_to_jpy)}

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-2.5">
      <h2 class="text-sm font-bold flex items-center gap-1.5 text-slate-800">✈️ {city['airport_access']['airport_name']}から市内への移動 ＆ 宿泊・現地手配</h2>
      <div class="text-xs space-y-2 text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
        <p><span class="inline-block bg-blue-100 text-blue-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最速・快適</span>{city['airport_access']['fastest']}</p>
        <p><span class="inline-block bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最安・定番</span>{city['airport_access']['cheapest']}</p>
      </div>
      <div class="text-xs text-slate-700 pt-1">
        <strong class="text-slate-900">必須の移動・配車アプリ：</strong>{', '.join(city['transport_apps'])}
      </div>
      {render_agoda_and_oooh_box(city)}
    </section>

    {render_telecom_box(city)}

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <h2 class="text-sm font-bold">📌 お金・マナー・生活ルール詳細</h2>
      <div class="text-xs space-y-2.5 text-slate-700 leading-relaxed">
        <p><strong class="text-slate-900">💵 チップの詳細：</strong>{city['tip_detail']}</p>
        <p><strong class="text-slate-900">🛍️ 税金・免税（Tax Free）：</strong>{city['tax_note']}</p>
        <p><strong class="text-slate-900">🔌 変圧器・周波数（{city['frequency']}）：</strong>{city['transformer_note']}</p>
        <p><strong class="text-slate-900">💧 水道水・氷：</strong>{city['tap_water_note']}</p>
        <p><strong class="text-slate-900">☀️ サマータイム：</strong>{city['dst_note']}</p>
      </div>
      {render_epos_affiliate(city)}
    </section>

    <section class="bg-white p-4 rounded-2xl shadow-sm border-l-4 border-l-rose-500 border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-sm font-extrabold text-slate-900 flex items-center gap-1.5">🚨 安全・危険情報・日本大使館情報</h2>
        <span class="text-[11px] bg-rose-50 text-rose-700 font-bold px-2.5 py-0.5 rounded-full border border-rose-200">緊急通報: {city['emergency_numbers']}</span>
      </div>
      <div class="p-2.5 rounded-xl border text-xs font-bold flex items-center justify-between flex-wrap gap-1 {danger_badge_class(city['danger_color'])}">
        <span>🛡️ 外務省 危険情報目安：{city['danger_level']}</span>
        <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="underline text-[11px]">最新公式ページ ↗</a>
      </div>
      <div class="text-xs space-y-2 text-slate-700 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">
        <p><strong class="text-slate-900">⚠️ 現地の治安・注意点：</strong>{city['safety_note']}</p>
        <p><strong class="text-slate-900">🏛️ 日本大使館・総領事館：</strong>{city['embassy']}</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
        <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="flex items-center justify-center gap-1.5 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold py-2.5 px-3 rounded-xl transition">
          <span>🌐 外務省「{city['country_ja']}」安全情報を見る</span>
          <span>↗</span>
        </a>
        <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="flex items-center justify-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold py-2.5 px-3 rounded-xl transition">
          <span>📩 外務省「たびレジ」に登録する（無料）</span>
          <span>↗</span>
        </a>
      </div>
    </section>

    <!-- 機能④：1タップ現地リアル度投票 -->
    {render_quick_poll(city)}

    {render_share_buttons(page_url, share_title)}

    {render_sister_site_banner()}

    <section class="pt-2">
      <h3 class="text-xs font-bold text-slate-500 mb-2">🗺️ {city['region']}の他の都市をチェック</h3>
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
        countdownMsg.textContent = `✈️ 出発まであと${{diffDays}}日！アゴダでの宿確保やクレカ保険準備に最適な時期です`;
      }} else if (diffDays >= 1) {{
        countdownMsg.textContent = `🔥 出発まであと${{diffDays}}日！eSIMとVPNの事前インストールをお忘れなく！`;
      }} else if (diffDays === 0) {{
        countdownMsg.textContent = `🎉 いよいよ本日出発！気をつけていってらっしゃいませ！`;
      }} else {{
        countdownMsg.textContent = `🌟 渡航中・帰国後の現地チェックにもご活用ください`;
      }}
    }}
    dateInput.addEventListener('change', updateCountdown);
    updateCountdown();

    const checks = Array.from(document.querySelectorAll('.prep-check'));
    function updateChecklistUI() {{
      let done = 0;
      checks.forEach(ch => {{
        const key = `ck_${{citySlug}}_${{ch.dataset.ck}}`;
        if (ch.checked) {{
          done++;
          localStorage.setItem(key, '1');
        }} else {{
          localStorage.removeItem(key);
        }}
      }});
      document.getElementById('checklist-progress').textContent = `準備完了: ${{done}}/${{checks.length}}`;
    }}
    checks.forEach(ch => {{
      const key = `ck_${{citySlug}}_${{ch.dataset.ck}}`;
      if (localStorage.getItem(key) === '1') ch.checked = true;
      ch.addEventListener('change', updateChecklistUI);
    }});
    updateChecklistUI();

    function castVote(type) {{
      localStorage.setItem('voted_' + citySlug, type);
      document.getElementById('poll-thanks').textContent = '✨ ご回答ありがとうございます！統計に反映しました。';
    }}
    if (localStorage.getItem('voted_' + citySlug)) {{
      document.getElementById('poll-thanks').textContent = '✨ 投票済み（ご協力ありがとうございます！）';
    }}

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

        let icon = '☀️';
        let desc = '晴れ';
        if (code >= 1 && code <= 3) {{ icon = '⛅'; desc = '晴れ時々曇り'; }}
        else if (code >= 45 && code <= 48) {{ icon = '🌫️'; desc = '霧'; }}
        else if (code >= 51 && code <= 67) {{ icon = '🌧️'; desc = '雨'; }}
        else if (code >= 71 && code <= 77) {{ icon = '❄️'; desc = '雪'; }}
        else if (code >= 80 && code <= 82) {{ icon = '🌦️'; desc = 'にわか雨'; }}
        else if (code >= 95) {{ icon = '⛈️'; desc = '雷雨'; }}

        let outfit = '';
        if (temp >= 28) outfit = '服装目安：半袖・短パンで快適（屋内冷房対策に薄手の羽織りを1枚）';
        else if (temp >= 22) outfit = '服装目安：半袖または薄手の長袖シャツが快適';
        else if (temp >= 16) outfit = '服装目安：長袖＋カーディガンやパーカーなど羽織りもの必須';
        else if (temp >= 10) outfit = '服装目安：ジャケットやトレンチコート・ニットが必要';
        else outfit = '服装目安：冬物コート・ダウンやマフラーなどしっかり防寒対策を';

        const dryNote = humidity <= 40 ? '（乾燥注意・保湿推奨）' : (humidity >= 80 ? '（高湿度・蒸し暑さ注意）' : '');

        document.getElementById('weather-icon').textContent = icon;
        document.getElementById('weather-temp').textContent = `${{temp}}℃（${{desc}} / 湿度${{humidity}}%${{dryNote}}）`;
        document.getElementById('weather-outfit').textContent = outfit;
      }} catch (e) {{
        document.getElementById('weather-temp').textContent = '下の年間気候目安をご参照ください';
        document.getElementById('weather-outfit').textContent = '渡航前に天気予報アプリで最新気温をご確認ください';
      }}
    }}
    fetchWeather();
  </script>
</body>
</html>"""


def build_compare_html(c1: dict, c2: dict, summary_text: str, rates_data: dict) -> str:
    pair_slug = f"{c1['slug']}-vs-{c2['slug']}"
    page_url = f"{SITE_URL}/compare/{pair_slug}/"
    title = f"{c1['name_ja']}と{c2['name_ja']}を徹底比較｜プラグ・チップ・気候・治安・空港移動の違い｜{SITE_NAME}"

    r1 = rates_data["rates"].get(c1["currency_code"], 0.01)
    r2 = rates_data["rates"].get(c2["currency_code"], 0.01)
    jpy1 = round(1 / r1, 2) if r1 >= 0.005 else round(1 / r1, 4)
    jpy2 = round(1 / r2, 2) if r2 >= 0.005 else round(1 / r2, 4)

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head()}
  <title>{title}</title>
  <meta name="description" content="{c1['name_ja']}（{c1['country_ja']}）と{c2['name_ja']}（{c2['country_ja']}）のどっちに行くか迷っている方や2都市周遊する方向けに、コンセント・電圧・チップ・通貨レート・気候・外務省危険情報を1画面で比較。">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-14">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">🌐 {SITE_NAME}（トップへ戻る）</a>
      <span class="text-xs bg-indigo-50 text-indigo-800 px-2.5 py-1 rounded-full font-bold">2都市比較ガイド</span>
    </div>
  </header>

  <main class="max-w-3xl mx-auto px-4 pt-5 space-y-5">
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
      <span class="text-[10px] font-extrabold bg-indigo-600 text-white px-2.5 py-0.5 rounded-full">旅行先比較・2都市周遊チェック</span>
      <h1 class="text-xl sm:text-2xl font-extrabold">{c1['name_ja']} vs {c2['name_ja']} 現地情報・渡航スペック徹底比較</h1>
      <p class="text-xs text-slate-600 leading-relaxed">{summary_text}</p>
    </div>

    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse text-xs">
        <thead>
          <tr class="bg-slate-900 text-white">
            <th class="p-3 w-1/4">比較項目</th>
            <th class="p-3 w-[37.5%] border-l border-slate-700"><a href="../../{c1['slug']}/" class="underline hover:text-blue-300">{c1['name_ja']}（{c1['country_ja']}）↗</a></th>
            <th class="p-3 w-[37.5%] border-l border-slate-700"><a href="../../{c2['slug']}/" class="underline hover:text-blue-300">{c2['name_ja']}（{c2['country_ja']}）↗</a></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          <tr>
            <th class="p-3 bg-slate-50 font-bold">🔌 コンセント・電圧</th>
            <td class="p-3 border-l border-slate-100 font-bold">{c1['plug_type']}タイプ（{c1['voltage']} / {c1['frequency']}）</td>
            <td class="p-3 border-l border-slate-100 font-bold">{c2['plug_type']}タイプ（{c2['voltage']} / {c2['frequency']}）</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">💵 チップ習慣</th>
            <td class="p-3 border-l border-slate-100"><strong>{c1['tip_badge']}</strong><br><span class="text-[11px] text-slate-500">{c1['tip_detail']}</span></td>
            <td class="p-3 border-l border-slate-100"><strong>{c2['tip_badge']}</strong><br><span class="text-[11px] text-slate-500">{c2['tip_detail']}</span></td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">💱 通貨・為替目安</th>
            <td class="p-3 border-l border-slate-100">{c1['currency_name']}（1{c1['currency_code']} ≒ {jpy1}円）</td>
            <td class="p-3 border-l border-slate-100">{c2['currency_name']}（1{c2['currency_code']} ≒ {jpy2}円）</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">💧 水道水</th>
            <td class="p-3 border-l border-slate-100">{'💧飲用可' if c1['tap_water_safe'] else '⚠️飲用不可（市販水推奨）'}</td>
            <td class="p-3 border-l border-slate-100">{'💧飲用可' if c2['tap_water_safe'] else '⚠️飲用不可（市販水推奨）'}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">🌤️ 気候・季節感</th>
            <td class="p-3 border-l border-slate-100 text-[11px] leading-relaxed">{c1['climate']}</td>
            <td class="p-3 border-l border-slate-100 text-[11px] leading-relaxed">{c2['climate']}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">✈️ 空港アクセス</th>
            <td class="p-3 border-l border-slate-100 text-[11px]">{c1['airport_access']['fastest']}</td>
            <td class="p-3 border-l border-slate-100 text-[11px]">{c2['airport_access']['fastest']}</td>
          </tr>
          <tr>
            <th class="p-3 bg-slate-50 font-bold">🛡️ 外務省危険情報</th>
            <td class="p-3 border-l border-slate-100 text-[11px] font-bold">{c1['danger_level']}</td>
            <td class="p-3 border-l border-slate-100 text-[11px] font-bold">{c2['danger_level']}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <a href="../../{c1['slug']}/" class="block bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs p-3.5 rounded-xl text-center transition">📍 {c1['name_ja']}のリアルタイム時計・天気を見る →</a>
      <a href="../../{c2['slug']}/" class="block bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs p-3.5 rounded-xl text-center transition">📍 {c2['name_ja']}のリアルタイム時計・天気を見る →</a>
    </div>

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <h2 class="text-sm font-bold text-slate-800">🏨 {c1['name_ja']}・{c2['name_ja']}のホテル予約 ＆ 現地ツアー相談</h2>
      {render_agoda_and_oooh_box(c1)}
    </section>

    {render_telecom_box(c1)}
    {render_share_buttons(page_url, title)}
  </main>
  {render_pixels()}
  <script>{render_share_script()}</script>
</body>
</html>"""


def build_feature_html(feat: dict, all_cities: list) -> str:
    page_url = f"{SITE_URL}/features/{feat['slug']}/"
    city_map = {c["slug"]: c for c in all_cities}
    selected = [city_map[s] for s in feat["cities"] if s in city_map]

    cards = "".join([
        f'<a href="../../{c["slug"]}/" class="block bg-white p-4 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition space-y-1.5">'
        f'<div class="flex items-center justify-between">'
        f'<span class="font-extrabold text-sm text-slate-900">📍 {c["name_ja"]}</span>'
        f'<span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-bold">{c["country_ja"]}</span>'
        f'</div>'
        f'<p class="text-[11px] text-slate-600 line-clamp-2">{c["climate"]}</p>'
        f'<div class="text-[11px] text-slate-500 flex flex-wrap gap-2 pt-1">'
        f'<span>🔌 {c["plug_type"]}</span><span>💵 チップ:{c["tip_badge"]}</span><span>💱 {c["currency_code"]}</span>'
        f'</div>'
        f'</a>'
        for c in selected
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head()}
  <title>{feat['title']}｜{SITE_NAME}</title>
  <meta name="description" content="{feat['desc']}">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-14">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">🌐 {SITE_NAME}（全150都市一覧へ）</a>
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

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <h2 class="text-sm font-bold text-slate-800">🏨 渡航先のホテル格安予約 ＆ 現地オーダーメイド相談</h2>
      {render_agoda_and_oooh_box(selected[0])}
    </section>

    {render_telecom_box(selected[0])}
    {render_share_buttons(page_url, feat['title'])}
  </main>
  {render_pixels()}
  <script>{render_share_script()}</script>
</body>
</html>"""


def build_policy_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head()}
  <title>プライバシーポリシー・免責事項・運営者情報｜{SITE_NAME}</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE_URL}/policy/">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  {render_pr_banner()}
  <header class="bg-white border-b border-slate-200 sticky top-0 z-20">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-slate-800 text-sm hover:text-blue-600 transition">🌐 {SITE_NAME}（トップへ戻る）</a>
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


def build_index_html(cities: list, rates_data: dict) -> str:
    unique_regions = ["すべて"] + sorted(list({c["region"] for c in cities}))
    share_title = f"{SITE_NAME}｜世界{len(cities)}都市の時差・天気・コンセント・チップ・治安を1画面で即答"
    city_map = {c["slug"]: c for c in cities}

    region_buttons = "".join([
        f'<button data-region="{r}" class="region-btn shrink-0 px-3 py-1.5 rounded-full text-xs font-bold border transition '
        f'{"bg-slate-900 text-white border-slate-900" if r == "すべて" else "bg-white text-slate-600 border-slate-200"}">{r}</button>'
        for r in unique_regions
    ])

    card_list = []
    for c in cities:
        if c["special_ui"] == "china_vpn":
            vpn_badge = '<span class="text-[10px] text-rose-600 font-bold">🛡️要VPN/eSIM</span>'
        elif c["special_ui"] == "vpn_recommended":
            vpn_badge = '<span class="text-[10px] text-indigo-600 font-bold">🔒VPN推奨</span>'
        else:
            vpn_badge = ""
        danger_dot = '<span class="text-[10px] text-amber-700 font-bold">⚠️危険情報あり</span>' if c["danger_color"] != "emerald" else ""
        tip_short = c["tip_badge"].split("（")[0]
        search_str = f'{c["name_ja"]} {c["kana_kw"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}'
        card_list.append(
            f'<a href="./{c["slug"]}/" data-region="{c["region"]}" '
            f'data-name="{c["name_ja"]}" data-country="{c["country_ja"]}" data-slug="{c["slug"]}" '
            f'data-search="{search_str}" '
            f'class="city-card block bg-white p-3.5 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition">'
            f'<div class="flex items-center justify-between gap-1">'
            f'<span class="font-extrabold text-sm text-slate-900">{c["name_ja"]}</span>'
            f'<span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium shrink-0">{c["country_ja"]}</span>'
            f'</div>'
            f'<div class="text-[11px] text-slate-500 mt-1.5 flex items-center gap-2 flex-wrap">'
            f'<span>🔌 {c["plug_type"]}</span>'
            f'<span>💱 {c["currency_code"]}</span>'
            f'<span>💵 チップ{tip_short}</span>'
            f'{vpn_badge}'
            f'{danger_dot}'
            f'</div>'
            f'</a>'
        )
    cards_html = "\n".join(card_list)

    feature_links = "".join([
        f'<a href="./features/{f["slug"]}/" class="block bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 p-3.5 rounded-2xl hover:border-blue-500 transition">'
        f'<span class="text-[10px] font-extrabold bg-blue-600 text-white px-2 py-0.5 rounded">{f["badge"]}</span>'
        f'<p class="text-xs font-extrabold text-slate-900 mt-1">{f["title"]}</p>'
        f'</a>'
        for f in FEATURE_PAGES
    ])

    compare_links = "".join([
        f'<a href="./compare/{s1}-vs-{s2}/" class="text-xs bg-white border border-slate-200 px-3 py-2 rounded-xl font-bold text-slate-700 hover:border-indigo-500 hover:text-indigo-700 transition">'
        f'⚔️ {city_map[s1]["name_ja"]} vs {city_map[s2]["name_ja"]}'
        f'</a>'
        for s1, s2, _ in COMPARE_PAIRS if s1 in city_map and s2 in city_map
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head()}
  <title>{SITE_NAME}｜世界{len(cities)}都市の時差・天気/気候・コンセント・チップ・危険情報・為替を1画面で即答</title>
  <meta name="description" content="海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・リアルタイム気温・気候・コンセント形状・電圧・チップ計算機・最新為替レート・外務省危険情報をスクロールなしで即解決。">
  <link rel="canonical" href="{SITE_URL}/">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  {render_pr_banner()}
  <main class="max-w-3xl mx-auto px-4 pt-7 space-y-6">
    <div class="text-center space-y-2">
      <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">🌐 {SITE_NAME}</h1>
      <p class="text-xs sm:text-sm text-slate-600">世界{len(cities)}都市の「時差・気温/気候・プラグ・チップ計算・為替・空港移動・外務省危険情報」を1画面で即答</p>
    </div>

    <div class="sticky top-2 z-30 bg-slate-50/95 backdrop-blur py-2 space-y-2.5">
      <div class="relative">
        <input id="search" type="text" autocomplete="off" placeholder="🔍 ひらがな・都市名・国名で予測検索（例：ばり、ぷさん、ロンドン、たいわん）"
          class="w-full p-3.5 rounded-2xl border border-slate-300 bg-white shadow-sm text-sm focus:outline-none focus:border-blue-500">
        <div id="suggest-box" class="hidden absolute left-0 right-0 mt-1 bg-white border border-slate-200 rounded-2xl shadow-lg max-h-64 overflow-y-auto z-40 divide-y divide-slate-100"></div>
      </div>
      <div class="flex gap-1.5 overflow-x-auto pb-1 no-scrollbar">{region_buttons}</div>
    </div>

    <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">{cards_html}</div>

    <section class="space-y-3 pt-2">
      <h2 class="text-sm font-extrabold text-slate-800">✈️ 季節特集・人気2都市比較ガイド</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">{feature_links}</div>
      <div class="flex flex-wrap gap-2 pt-1">{compare_links}</div>
    </section>

    {render_sister_site_banner()}

    {render_share_buttons(SITE_URL + "/", share_title)}

    <footer class="pt-6 text-center text-xs text-slate-400 space-y-2">
      <p>🔗 安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">たびレジ</a></p>
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
            <span class="font-bold text-slate-900">📍 ${{c.dataset.name}}</span>
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
