# -*- coding: utf-8 -*-
"""
templates_pages.py ― トップページとガイドページ（早見表・チェックリスト）

- build_index_html    : 離脱を減らすための新トップページ
                        （検索＋人気都市、今が行き時の都市、テーマ/予算の絞り込み、人気順の段階表示）
- build_guides_hub_html / build_plug_guide_html / build_time_guide_html /
  build_tipping_guide_html / build_packing_html : データから自動生成するオリジナルのガイド
"""
import html as _html
import json
from datetime import datetime, timezone

from config import SITE_URL, SITE_NAME, FAVICON_URL, FEATURE_PAGES
from templates import (
    render_common_head, render_editorial_styles, render_pr_banner, render_pixels,
    render_share_buttons, render_share_script, render_theme_and_toast_script,
    render_sister_site_banner, render_agoda_and_oooh_box, render_telecom_box,
    compute_city_star_ratings, compute_price_benchmarks, render_plug_svg,
)
from site_content import POPULAR, THEMES, GUIDE_PAGES

_esc = _html.escape


# ---------------------------------------------------------------------------
# 共通：ガイドページの外枠
# ---------------------------------------------------------------------------
def _guide_shell(title: str, desc: str, url: str, body: str, script: str = "", head_extra: str = "",
                 crumb: str = "") -> str:
    crumb_html = f'<nav class="text-[11px]" style="color: var(--text-muted);"><a href="../../" class="underline">トップ</a> › <a href="../" class="underline">ガイド・早見表</a>{crumb}</nav>'
    return f"""<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(title, desc, url)}
  {render_editorial_styles()}
  <title>{_esc(title)}</title>
  <meta name="description" content="{_esc(desc)}">
  <link rel="canonical" href="{url}">
  <script src="https://cdn.tailwindcss.com"></script>
  {head_extra}
</head>
<body class="pb-14">
  {render_pr_banner()}
  <header class="ed-header">
    <div class="max-w-[780px] mx-auto px-4 py-2.5 flex items-center justify-between gap-2">
      <a href="../../" class="inline-flex items-center gap-2 py-1 pr-2 rounded-lg" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4" style="color: var(--accent-text);"></i>
        <span class="font-extrabold text-sm sm:text-base">{SITE_NAME}</span>
      </a>
      <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-6">
    {crumb_html}
    {body}
    {render_share_buttons(url, title)}
    {render_sister_site_banner()}
    <footer class="pt-6 pb-4 text-center text-[11px] space-y-1.5" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>※当ページはプロモーション（アフィリエイト広告）を含みます。制度・規則は変更されるため、渡航前に公式情報をご確認ください。</p>
      <p><a href="../" class="underline">ガイド・早見表一覧</a> · <a href="../../policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a></p>
      <p>© {SITE_NAME} ({SITE_URL})</p>
    </footer>
  </main>

  <div id="toast" class="toast-msg" role="status" aria-live="polite">
    <i data-lucide="check" class="w-3.5 h-3.5"></i>
    <span id="toast-text">コピーしました</span>
  </div>
  {render_pixels()}
  <script>
    lucide.createIcons();
    {render_theme_and_toast_script()}
    {render_share_script()}
  </script>
  {script}
</body>
</html>"""


def _page_header(kicker: str, h1: str, lead: str) -> str:
    return f"""
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-semibold uppercase tracking-wider" style="color: var(--accent-text);">{_esc(kicker)}</span>
      <h1 class="text-xl sm:text-2xl font-bold">{_esc(h1)}</h1>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">{lead}</p>
    </div>"""


def _city_links(cs: list, prefix: str = "../../") -> str:
    return " ".join(
        f'<a href="{prefix}{c["slug"]}/" class="inline-block text-[11px] px-2 py-0.5 rounded-full underline-offset-2 hover:underline" '
        f'style="background: var(--bg-tint); color: var(--accent-text);">{_esc(c["name_ja"].split("（")[0])}</a>'
        for c in cs
    )


# ---------------------------------------------------------------------------
# ガイド一覧
# ---------------------------------------------------------------------------
def build_guides_hub_html() -> str:
    url = f"{SITE_URL}/guides/"
    title = f"ガイド・早見表｜持ち物・時差・コンセント・チップ｜{SITE_NAME}"
    desc = "海外旅行の準備に役立つ早見表とチェックリスト。持ち物チェックリスト、世界の時差早見表、コンセント・電圧、チップ相場を、都市データから自動でまとめています。"
    cards = "".join(
        f'<a href="./{slug}/" class="ed-surface block p-4 space-y-1.5">'
        f'<div class="flex items-center gap-2"><i data-lucide="{icon}" class="w-4 h-4" style="color: var(--accent-text);"></i>'
        f'<span class="font-bold text-sm" style="color: var(--text-primary);">{_esc(label)}</span></div>'
        f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{_esc(d)}</p></a>'
        for slug, label, d, icon in GUIDE_PAGES
    )
    feats = "".join(
        f'<a href="../features/{f["slug"]}/" class="ed-surface block p-3.5"><span class="text-[10px]" style="color: var(--text-muted);">{_esc(f["badge"])}</span>'
        f'<p class="text-xs font-semibold mt-1 leading-relaxed" style="color: var(--text-primary);">{_esc(f["title"])}</p></a>'
        for f in FEATURE_PAGES
    )
    body = f"""
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-semibold uppercase tracking-wider" style="color: var(--accent-text);">GUIDES</span>
      <h1 class="text-xl sm:text-2xl font-bold">ガイド・早見表</h1>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">渡航の準備に役立つ早見表とチェックリストです。都市ごとの詳しい情報は、各都市ページでご確認ください。</p>
    </div>
    <section class="grid grid-cols-1 sm:grid-cols-2 gap-3">{cards}</section>
    <section class="space-y-2.5">
      <h2 class="text-sm font-bold pb-1.5" style="color: var(--text-primary); border-bottom: 1px solid var(--divider);">季節・テーマ別の特集</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">{feats}</div>
    </section>"""
    out = _guide_shell(title, desc, url, body)
    # 一覧ページは1階層浅いので、相対リンクを調整する
    out = out.replace('<a href="../../" class="underline">トップ</a> › <a href="../" class="underline">ガイド・早見表</a>', '<a href="../" class="underline">トップ</a>')
    out = out.replace('href="../../', 'href="../').replace('<a href="../" class="underline">ガイド・早見表一覧</a>', '<a href="./" class="underline">ガイド・早見表一覧</a>')
    return out


# ---------------------------------------------------------------------------
# コンセント・電圧
# ---------------------------------------------------------------------------
_PLUG_NOTES = {
    "A": "平行な2本ピン。日本のプラグがそのまま差せる地域が多い形状です。電圧は日本より高い国もあるため、機器の対応電圧を確認してください。",
    "C": "丸い2本ピン。ヨーロッパを中心に広く使われます。電圧は220〜240Vが中心です。",
    "BF": "3本の角ピン。イギリスやシンガポール、マレーシアなどで使われる形状です（電圧は230V前後）。",
    "O": "斜めに開いた2本ピンと中央の1本。オーストラリア・ニュージーランド系の形状です（電圧は230〜240V）。",
}


def build_plug_guide_html(cities: list) -> str:
    url = f"{SITE_URL}/guides/plug-types/"
    title = f"【世界のコンセント・電圧 早見表】プラグ形状別の対応都市一覧｜{SITE_NAME}"
    desc = "世界の主要都市のコンセント形状（A・C・BFなど）と電圧を、プラグ形状別にまとめた早見表。変換プラグと変圧器が必要かどうかの考え方も解説します。"

    groups = {}
    for c in cities:
        groups.setdefault(c["plug_type"], []).append(c)
    ordered = sorted(groups.items(), key=lambda kv: -len(kv[1]))

    sections = []
    for ptype, cs in ordered:
        volts = sorted({c["voltage"] for c in cs})
        countries = {}
        for c in cs:
            countries.setdefault(c["country_ja"], []).append(c)
        main = ptype.split("/")[0]
        svg = f'<span style="color: var(--text-primary);">{render_plug_svg(ptype)}</span>' if ptype in _PLUG_NOTES else ""
        note = _PLUG_NOTES.get(ptype, "複数の形状が混在する地域です。最も多く使われる形状に合わせた変換プラグ、または複数形状に対応した万能タイプが便利です。")
        rows = "".join(
            f'<div class="py-1.5" style="border-top: 1px solid var(--divider);"><span class="text-[11px] font-bold" style="color: var(--text-primary);">{_esc(country)}</span> '
            f'{_city_links(cl)}</div>'
            for country, cl in sorted(countries.items(), key=lambda kv: kv[0])
        )
        sections.append(f"""
    <section class="ed-surface p-4 space-y-2 reveal-section">
      <div class="flex items-center gap-3">
        {svg}
        <div>
          <h2 class="text-sm font-bold" style="color: var(--text-primary);">{_esc(ptype)}タイプ <span class="text-[11px] font-normal" style="color: var(--text-muted);">（{len(cs)}都市・電圧 {' / '.join(_esc(v) for v in volts)}）</span></h2>
          <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{note}</p>
        </div>
      </div>
      <div class="text-xs">{rows}</div>
    </section>""")

    faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "海外で日本の電化製品を使うのに変圧器は必要ですか？",
             "acceptedAnswer": {"@type": "Answer", "text": "日本の電圧は100Vですが、海外は220〜240Vの国が多くあります。スマートフォンやパソコンの充電器は100〜240V対応のものが多く、その場合は変換プラグだけで使えます。ヘアドライヤーなど対応電圧が100V専用の機器は、変圧器が必要になるか、海外対応品への買い替えが安全です。機器本体や充電器の「INPUT」表記を必ず確認してください。"}},
            {"@type": "Question", "name": "変換プラグと変圧器の違いは何ですか？",
             "acceptedAnswer": {"@type": "Answer", "text": "変換プラグは差込口の形状を合わせるもので、電圧は変えません。変圧器は電圧を変えるものです。電圧が合わない機器を、変換プラグだけで使うと故障や発火の原因になります。"}},
        ],
    }
    body = _page_header("PLUG & VOLTAGE GUIDE", "世界のコンセント・電圧 早見表",
        f"掲載{len(cities)}都市のコンセント形状と電圧を、プラグ形状別にまとめました。都市名をタップすると、その都市の詳細ページへ移動できます。") + f"""
    <section class="ed-tint p-4 text-xs leading-relaxed space-y-2" style="color: var(--text-secondary);">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">変換プラグと変圧器、どちらが必要？</h2>
      <p><strong style="color: var(--text-primary);">1. まず機器の「INPUT」表記を確認：</strong>スマホ・パソコンの充電器の多くは「100-240V」に対応しています。この場合は、渡航先の形状に合う<strong>変換プラグだけ</strong>で使えます。</p>
      <p><strong style="color: var(--text-primary);">2. 「100V」専用の機器は要注意：</strong>ヘアドライヤーやヘアアイロンなどは、そのまま220〜240Vの地域で使うと故障の原因になります。海外対応の機器を選ぶのが安全です。</p>
      <p><strong style="color: var(--text-primary);">3. 形状の確認：</strong>下の一覧で渡航先の形状を確認し、複数国を回る場合は万能タイプの変換プラグが便利です。</p>
      <p class="text-[11px]" style="color: var(--text-muted);">※形状の表記は当サイト基準の簡易分類です。ホテルや建物によって異なる場合があります。</p>
    </section>
    {''.join(sections)}
    {render_telecom_box(custom_note="コンセントの準備とあわせて、現地での地図・配車アプリ用の通信手段も出発前に確認しておくと安心です。")}"""
    head_extra = f'<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>'
    return _guide_shell(title, desc, url, body, head_extra=head_extra, crumb=" › コンセント・電圧")


# ---------------------------------------------------------------------------
# 時差
# ---------------------------------------------------------------------------
def _offsets_for(tz_name: str, year: int):
    from zoneinfo import ZoneInfo
    jst, local = ZoneInfo("Asia/Tokyo"), ZoneInfo(tz_name)
    vals = {}
    for key, m in (("jan", 1), ("jul", 7)):
        dt = datetime(year, m, 15, 12, tzinfo=timezone.utc)
        vals[key] = (dt.astimezone(local).utcoffset() - dt.astimezone(jst).utcoffset()).total_seconds() / 3600.0
    return vals["jan"], vals["jul"]


def _hours_label(h: float) -> str:
    if h == 0:
        return "同じ"
    sign = "+" if h > 0 else "−"
    n = abs(h)
    return f"{sign}{int(n)}時間" if float(n).is_integer() else f"{sign}{n:.1f}時間"


def build_time_guide_html(cities: list) -> str:
    url = f"{SITE_URL}/guides/time-difference/"
    title = f"【世界の時差早見表】日本との時差・サマータイム（冬時間/夏時間）｜{SITE_NAME}"
    desc = "日本との時差を都市別にまとめた早見表。冬時間・夏時間それぞれの時差と、日本時間から現地時間への換算ツール付き。"
    year = datetime.now(timezone.utc).year + (0 if datetime.now(timezone.utc).month < 11 else 1)

    rows = []
    for c in cities:
        try:
            jan, jul = _offsets_for(c["timezone"], year)
        except Exception:
            continue
        rows.append((c, jan, jul))
    # 1月基準（北半球の冬時間）の時差で分類
    buckets = {}
    for c, jan, jul in rows:
        buckets.setdefault(jan, []).append((c, jan, jul))

    sections = []
    for off in sorted(buckets.keys(), reverse=True):
        items = buckets[off]
        label = "日本と同じ時刻" if off == 0 else f"日本より{abs(int(off)) if float(off).is_integer() else abs(off)}時間{'進んでいる' if off > 0 else '遅れている'}"
        chips = []
        for c, jan, jul in sorted(items, key=lambda t: t[0]["name_ja"]):
            dst = f' <span class="text-[10px]" style="color: var(--amber-text);">（夏は{_hours_label(jul)}）</span>' if jan != jul else ""
            chips.append(f'<span class="inline-block mr-1 mb-1">{_city_links([c])}{dst}</span>')
        sections.append(f"""
    <section class="ed-surface p-4 space-y-1.5 reveal-section">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">{label}<span class="text-[11px] font-normal ml-1" style="color: var(--text-muted);">（{_hours_label(off)}・{len(items)}都市）</span></h2>
      <div class="text-xs">{''.join(chips)}</div>
    </section>""")

    options = "".join(
        f'<option value="{_esc(c["timezone"])}">{_esc(c["name_ja"])}（{_esc(c["country_ja"])}）</option>'
        for c in sorted(cities, key=lambda c: c["name_ja"])
    )
    body = _page_header("TIME DIFFERENCE GUIDE", "世界の時差早見表", f"日本時間を基準にした時差を都市別にまとめました。冬時間（1月）を基準に分類し、夏時間（サマータイム）で変わる都市は括弧で表示しています（{year}年のルールで計算）。") + f"""
    <section class="pr-card pr-card--accent space-y-2.5">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">日本時間 → 現地時間 換算ツール</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">日本の日時</label>
          <input id="tz-datetime" type="datetime-local" class="w-full rounded-lg px-2.5 py-2 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></div>
        <div class="sm:col-span-2"><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">都市</label>
          <select id="tz-city" class="w-full rounded-lg px-2.5 py-2 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{options}</select></div>
      </div>
      <p id="tz-result" class="text-sm font-bold tabular-nums" style="color: var(--accent-text);">都市を選んでください</p>
      <p class="text-[11px]" style="color: var(--text-muted);">ブラウザのタイムゾーン情報で計算します。端末が古い場合、最近の制度変更が反映されないことがあります。</p>
    </section>
    <section class="ed-tint p-4 text-xs leading-relaxed space-y-1.5" style="color: var(--text-secondary);">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">夏時間（サマータイム）の目安</h2>
      <p>・<strong>欧州</strong>：3月最終日曜〜10月最終日曜　・<strong>米国・カナダ（多くの地域）</strong>：3月第2日曜〜11月第1日曜</p>
      <p>・<strong>オーストラリア（南東部）</strong>：10月第1日曜〜4月第1日曜　・<strong>ニュージーランド</strong>：9月最終日曜〜4月第1日曜</p>
      <p>・近年、制度を変更した地域があります（例：モロッコは2026年9月から時刻を固定、カナダのブリティッシュ・コロンビア州とアルバータ州は2026年11月から夏時間を廃止）。渡航前に必ず公式情報を確認してください。</p>
    </section>
    {''.join(sections)}"""
    script = """<script>
    (function () {
      var dt = document.getElementById('tz-datetime');
      var sel = document.getElementById('tz-city');
      var out = document.getElementById('tz-result');
      function pad(n) { return String(n).padStart(2, '0'); }
      var now = new Date();
      var jstNow = new Date(now.getTime() + (now.getTimezoneOffset() + 540) * 60000);
      dt.value = jstNow.getFullYear() + '-' + pad(jstNow.getMonth() + 1) + '-' + pad(jstNow.getDate()) + 'T' + pad(jstNow.getHours()) + ':' + pad(jstNow.getMinutes());
      function update() {
        if (!dt.value) return;
        var d = new Date(dt.value + ':00+09:00');
        if (isNaN(d.getTime())) return;
        var fmt = new Intl.DateTimeFormat('ja-JP', { timeZone: sel.value, year: 'numeric', month: 'numeric', day: 'numeric', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false });
        var name = sel.options[sel.selectedIndex].text.split('（')[0];
        out.textContent = name + ' は ' + fmt.format(d);
      }
      dt.addEventListener('input', update); sel.addEventListener('change', update); update();
    })();
  </script>"""
    return _guide_shell(title, desc, url, body, script=script, crumb=" › 時差")


# ---------------------------------------------------------------------------
# チップ
# ---------------------------------------------------------------------------
def build_tipping_guide_html(cities: list) -> str:
    url = f"{SITE_URL}/guides/tipping/"
    title = f"【世界のチップ早見表】国・都市別のチップ相場と渡し方｜{SITE_NAME}"
    desc = "世界の主要都市のチップ相場を「必要・任意・不要」で分類。レストラン・タクシー・ホテルでの渡し方と、サービス料込みの見分け方もまとめました。"

    levels = [("required", "チップが必要（慣習として期待される）", "status-inline--danger"),
              ("optional", "チップは任意（気持ち・割合は目安）", "status-inline--warn"),
              ("none", "チップは基本不要", "status-inline--ok")]
    sections = []
    for key, label, cls in levels:
        by_country = {}
        for c in cities:
            if c["tip_level"] == key:
                by_country.setdefault(c["country_ja"], []).append(c)
        if not by_country:
            continue
        rows = []
        for country, cl in sorted(by_country.items(), key=lambda kv: kv[0]):
            c0 = cl[0]
            badge = _esc(c0["tip_badge"])
            rows.append(
                f'<div class="py-2" style="border-top: 1px solid var(--divider);">'
                f'<div class="flex items-baseline justify-between gap-2 flex-wrap"><span class="text-[12px] font-bold" style="color: var(--text-primary);">{_esc(country)}</span>'
                f'<span class="text-[11px] font-semibold" style="color: var(--accent-text);">{badge}</span></div>'
                f'<p class="text-[11px] leading-relaxed mt-0.5" style="color: var(--text-secondary);">{_esc(c0["tip_detail"])}</p>'
                f'<div class="mt-1">{_city_links(cl)}</div></div>')
        sections.append(f"""
    <section class="ed-surface p-4 space-y-1 reveal-section">
      <h2 class="text-sm font-bold flex items-center gap-2" style="color: var(--text-primary);"><span class="status-inline {cls}"><span class="status-dot"></span></span>{label}<span class="text-[11px] font-normal" style="color: var(--text-muted);">（{len(by_country)}か国・地域）</span></h2>
      <div>{''.join(rows)}</div>
    </section>""")

    body = _page_header("TIPPING GUIDE", "世界のチップ早見表", "チップの習慣は国や店によって大きく異なります。国・地域ごとの相場の目安を、必要・任意・不要で分類しました。表の割合は目安で、実際は店の案内を優先してください。") + """
    <section class="pr-card pr-card--accent space-y-2.5">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">チップ簡易計算</h2>
      <div class="grid grid-cols-3 gap-2 text-xs">
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">会計額</label><input id="tp-amount" type="number" value="100" class="w-full rounded-lg px-2.5 py-2 font-bold tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></div>
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">チップ率(%)</label><input id="tp-rate" type="number" value="15" class="w-full rounded-lg px-2.5 py-2 font-bold tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></div>
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">人数</label><input id="tp-people" type="number" value="2" min="1" class="w-full rounded-lg px-2.5 py-2 font-bold tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></div>
      </div>
      <p id="tp-result" class="text-sm font-bold tabular-nums" style="color: var(--accent-text);">--</p>
    </section>
    <section class="ed-tint p-4 text-xs leading-relaxed space-y-1.5" style="color: var(--text-secondary);">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">払う前に確認したい3つのポイント</h2>
      <p>・<strong>サービス料が含まれていないか：</strong>伝票に「Service Charge」「Gratuity」などの表記があれば、追加のチップは不要なことが多くあります。</p>
      <p>・<strong>カード払いの入力欄：</strong>端末でチップ額を選ぶ場合は、サービス料込みの金額に二重にならないよう確認してください。</p>
      <p>・<strong>少額の現金：</strong>ホテルのポーターや清掃などへは、少額の現金があると渡しやすくなります。</p>
    </section>""" + "".join(sections)
    script = """<script>
    (function () {
      var a = document.getElementById('tp-amount'), r = document.getElementById('tp-rate'), p = document.getElementById('tp-people'), o = document.getElementById('tp-result');
      function up() {
        var amt = parseFloat(a.value) || 0, rate = parseFloat(r.value) || 0, n = Math.max(1, parseInt(p.value, 10) || 1);
        var tip = amt * rate / 100, total = amt + tip;
        o.textContent = 'チップ ' + tip.toFixed(2) + ' ／ 合計 ' + total.toFixed(2) + ' ／ 1人あたり ' + (total / n).toFixed(2);
      }
      [a, r, p].forEach(function (el) { el.addEventListener('input', up); }); up();
    })();
  </script>"""
    return _guide_shell(title, desc, url, body, script=script, crumb=" › チップ")


# ---------------------------------------------------------------------------
# 持ち物チェックリスト
# ---------------------------------------------------------------------------
_PACKING = [
    ("書類・手続き", [
        ("passport", "パスポート（有効期限・残存期間・空白ページ。必要な残存期間は国ごとに異なるため確認）"),
        ("visa", "ビザ／電子渡航認証（要否は国・滞在日数・目的で異なります。公式で確認）"),
        ("tickets", "航空券・宿泊予約の控え（オフラインでも見られるよう保存）"),
        ("insurance", "海外旅行保険の加入証と緊急連絡先"),
        ("tabireg", "外務省「たびレジ」の登録"),
        ("copy", "パスポートの写し・予備の証明写真（紛失時の再発行に備える）"),
    ]),
    ("お金・カード", [
        ("cards", "クレジットカード（できれば複数枚・ブランド違い）"),
        ("cash", "少額の現金（現地通貨または米ドル等。チップや市場、交通用）"),
        ("pin", "カードの暗証番号・海外利用設定・利用限度額の確認"),
        ("split", "現金・カードを分けて持つ（盗難・紛失に備える）"),
    ]),
    ("通信・電子機器", [
        ("esim", "eSIM／ローミング／Wi-Fi の準備（端末の対応・設定を出発前に確認）"),
        ("plug", "変換プラグ（形状は「世界のコンセント・電圧早見表」で確認）"),
        ("battery", "モバイルバッテリー（機内持ち込み。預け入れ荷物には入れない）"),
        ("charger", "充電ケーブル・充電器（対応電圧の確認）"),
        ("offline", "地図・翻訳アプリのオフラインデータのダウンロード"),
    ]),
    ("衛生・薬", [
        ("meds", "常備薬（処方薬は、英文の薬剤情報や診断書が必要な場合があります）"),
        ("mask", "マスク・消毒液・ウェットティッシュ"),
        ("tissue", "ポケットティッシュ（トイレに紙がない場合に）"),
        ("sun", "日焼け止め・リップクリーム"),
    ]),
    ("衣類・靴", [
        ("clothes", "渡航先の気温に合わせた服（月別の気温は各都市ページで確認）"),
        ("layer", "重ね着しやすい羽織りもの（冷房や朝晩の冷え対策）"),
        ("shoes", "歩きやすい靴"),
        ("under", "下着・靴下・パジャマ"),
    ]),
    ("便利グッズ", [
        ("bag", "機内持ち込み用のバッグ（貴重品・薬・充電器はここに）"),
        ("liquid", "液体物は100ml以下の容器に分け、透明な袋にまとめる（国際線）"),
        ("lock", "スーツケースの鍵・ネームタグ"),
        ("pouch", "防犯用のポーチ・斜めがけバッグ"),
    ]),
]
_PACKING_EXTRA = {
    "rain": ("雨が多い時期・地域", [("umbrella", "折りたたみ傘・防水の上着"), ("dry", "濡れ物用の袋・速乾素材の服")]),
    "cold": ("寒い時期・地域", [("coat", "コート・手袋・マフラー・ニット帽"), ("heat", "カイロ・保湿クリーム")]),
    "long": ("1週間以上の長期", [("laundry", "洗濯用の洗剤・ハンガー・小型の洗濯袋"), ("sewing", "常備薬の予備・コンタクトの予備")]),
    "beach": ("ビーチ・リゾート", [("swim", "水着・ラッシュガード・サンダル"), ("marine", "マリンシューズ・防水ケース")]),
}


def build_packing_html() -> str:
    url = f"{SITE_URL}/guides/packing-checklist/"
    title = f"【海外旅行の持ち物チェックリスト】出発前の確認リスト（保存・印刷OK）｜{SITE_NAME}"
    desc = "海外旅行の持ち物を、書類・お金・通信・衛生・衣類・便利グッズに分けたチェックリスト。雨・寒さ・長期・ビーチの条件で項目を追加でき、チェックはブラウザに保存されます。"

    def block(group_id, label, items):
        lis = "".join(
            f'<li><label class="flex items-start gap-2 py-1.5 cursor-pointer"><input type="checkbox" class="pk-item mt-0.5" data-key="{group_id}:{k}">'
            f'<span class="text-xs leading-relaxed" style="color: var(--text-secondary);">{_esc(t)}</span></label></li>'
            for k, t in items
        )
        return f'<section class="ed-surface p-4 reveal-section"><h2 class="text-sm font-bold mb-1" style="color: var(--text-primary);">{_esc(label)}</h2><ul>{lis}</ul></section>'

    main_blocks = "".join(block(f"g{i}", label, items) for i, (label, items) in enumerate(_PACKING))
    extra_blocks = "".join(
        f'<div id="extra-{k}" class="hidden">{block("x" + k, lab, items)}</div>' for k, (lab, items) in _PACKING_EXTRA.items()
    )
    toggles = "".join(
        f'<label class="inline-flex items-center gap-1.5 text-xs font-medium cursor-pointer px-3 py-1.5 rounded-full" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">'
        f'<input type="checkbox" class="pk-toggle" data-extra="{k}"><span>{_esc(lab)}</span></label>'
        for k, (lab, _) in _PACKING_EXTRA.items()
    )
    body = _page_header("PACKING CHECKLIST", "海外旅行の持ち物チェックリスト", "出発前の確認漏れを防ぐためのチェックリストです。チェックの状態はこの端末のブラウザに保存されます。条件に合わせて項目を追加できます。") + f"""
    <section class="pr-card pr-card--accent space-y-2.5">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">条件に合わせて項目を追加</h2>
        <span id="pk-progress" class="text-xs font-bold tabular-nums" style="color: var(--accent-text);">0 / 0 完了</span>
      </div>
      <div class="flex flex-wrap gap-1.5">{toggles}</div>
      <div class="w-full h-1.5 rounded-full overflow-hidden" style="background: var(--bg-tint);"><div id="pk-bar" class="h-full rounded-full" style="width: 0%; background: var(--sage-text); transition: width .3s;"></div></div>
      <div class="flex gap-2 text-xs">
        <button id="pk-print" type="button" class="pr-cta" style="background: var(--text-primary); color: var(--bg-canvas);">印刷する</button>
        <button id="pk-reset" type="button" class="pr-cta" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">チェックをリセット</button>
      </div>
    </section>
    {main_blocks}
    {extra_blocks}
    <section class="ed-tint p-4 text-xs leading-relaxed" style="color: var(--text-secondary);">
      <strong style="color: var(--text-primary);">あわせて確認：</strong>渡航先のコンセントは<a href="../plug-types/" class="underline" style="color: var(--accent-text);">コンセント・電圧早見表</a>、時差は<a href="../time-difference/" class="underline" style="color: var(--accent-text);">時差早見表</a>、チップは<a href="../tipping/" class="underline" style="color: var(--accent-text);">チップ早見表</a>で確認できます。持ち込み制限や入国条件は、渡航先と航空会社の公式情報が優先されます。
    </section>
    {render_agoda_and_oooh_box(context_label="渡航先")}
    {render_telecom_box()}"""
    script = """<script>
    (function () {
      var KEY = 'tokou_packing_v1';
      var state = {};
      try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { state = {}; }
      var items = Array.prototype.slice.call(document.querySelectorAll('.pk-item'));
      var toggles = Array.prototype.slice.call(document.querySelectorAll('.pk-toggle'));
      function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
      function progress() {
        var visible = items.filter(function (i) { return i.offsetParent !== null; });
        var done = visible.filter(function (i) { return i.checked; }).length;
        document.getElementById('pk-progress').textContent = done + ' / ' + visible.length + ' 完了';
        document.getElementById('pk-bar').style.width = (visible.length ? Math.round(done / visible.length * 100) : 0) + '%';
      }
      items.forEach(function (i) {
        i.checked = !!state[i.dataset.key];
        i.addEventListener('change', function () { state[i.dataset.key] = i.checked; save(); progress(); });
      });
      toggles.forEach(function (t) {
        var k = '_extra:' + t.dataset.extra;
        t.checked = !!state[k];
        function apply() { var el = document.getElementById('extra-' + t.dataset.extra); if (el) el.classList.toggle('hidden', !t.checked); }
        apply();
        t.addEventListener('change', function () { state[k] = t.checked; save(); apply(); progress(); });
      });
      document.getElementById('pk-reset').addEventListener('click', function () {
        if (!confirm('すべてのチェックをリセットしますか？')) return;
        state = {}; save(); items.forEach(function (i) { i.checked = false; }); toggles.forEach(function (t) { t.checked = false; var el = document.getElementById('extra-' + t.dataset.extra); if (el) el.classList.add('hidden'); }); progress();
      });
      document.getElementById('pk-print').addEventListener('click', function () { window.print(); });
      progress();
    })();
  </script>"""
    return _guide_shell(title, desc, url, body, script=script, crumb=" › 持ち物チェックリスト")


# ---------------------------------------------------------------------------
# トップページ
# ---------------------------------------------------------------------------
_LAB_CODE = {"ベスト": 0, "快適": 1, "標準": 2, "注意": 3}


def _budget_tier(lunch_jpy: int) -> int:
    if lunch_jpy <= 1000:
        return 1   # 安め
    if lunch_jpy <= 2200:
        return 2   # 普通
    return 3       # 高め


_INDEX_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  %%HEAD%%
  %%STYLES%%
  <style>
    .hero { background: radial-gradient(900px 300px at 0% -20%, var(--accent-soft), transparent 65%), var(--bg-surface); border: 1px solid var(--divider); border-radius: var(--radius-lg); padding: 18px 16px 16px; }
    .hero-search { width: 100%; padding: 14px 16px 14px 44px; border-radius: 14px; font-size: 15px; background: var(--bg-canvas); border: 1px solid var(--border-soft); color: var(--text-primary); }
    .hero-search:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
    .intent-tile { display: flex; align-items: center; gap: 10px; padding: 12px 12px; border-radius: var(--radius-md); background: var(--bg-surface); border: 1px solid var(--divider); text-align: left; transition: transform .2s var(--ease-spring), box-shadow .2s var(--ease-out-expo), border-color .2s; cursor: pointer; width: 100%; }
    .intent-tile:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); border-color: var(--accent); }
    .fchip { padding: 6px 12px; border-radius: 9999px; font-size: 12px; background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary); font-weight: 500; white-space: nowrap; flex-shrink: 0; transition: background .15s, color .15s; }
    .fchip:hover { background: var(--bg-tint); }
    .fchip.is-active { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 700; }
    .hscroll { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px; }
    .hscroll::-webkit-scrollbar { display: none; }
    .clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .lab-chip { display: inline-block; font-size: 10px; font-weight: 700; padding: 1px 7px; border-radius: 9999px; }
    .lab-0 { background: var(--sage-bg); color: var(--sage-text); }
    .lab-1 { background: var(--accent-soft); color: var(--accent-text); }
    .suggest-wrap { position: relative; }
    .suggest-wrap .search-ico { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); pointer-events: none; }
    .sub-text-link { display: inline-flex; align-items: center; gap: 4px; padding: 4px 2px; background: transparent; border: none; color: var(--text-muted); font-size: 11px; font-weight: 500; }
    .sub-text-link:hover { color: var(--text-primary); }
    .sub-text-link svg { transition: transform .3s var(--ease-out-expo); }
    .sub-text-link[aria-expanded="true"] svg { transform: rotate(180deg); }
  </style>
  <title>%%TITLE%%</title>
  <meta name="description" content="%%DESC%%">
  <link rel="canonical" href="%%URL%%">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="pb-16">
  %%PR_BANNER%%
  <header class="ed-header">
    <div id="scroll-progress" class="scroll-progress"></div>
    <div class="max-w-[780px] mx-auto px-4 py-2.5 flex items-center justify-between gap-2">
      <a href="./" class="font-extrabold text-sm flex items-center gap-2" style="color: var(--text-primary);">
        <img src="%%FAVICON%%" alt="" width="22" height="22" class="w-5 h-5 rounded-md object-cover shrink-0" onerror="this.style.display='none'">
        <span>%%SITE_NAME%%</span>
      </a>
      <div class="flex items-center gap-1.5">
        <a href="./guides/" class="hidden sm:inline-flex text-[11px] font-medium px-2.5 py-1 rounded-full" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">ガイド・早見表</a>
        <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
          <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
          <span id="theme-name">Light</span>
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-7">

    <section class="hero space-y-3 anim-enter">
      <div class="space-y-1">
        <p class="text-[11px] tracking-wider" style="color: var(--text-muted);">WORLD TRAVEL POCKET DICTIONARY · %%N_CITIES%% CITIES</p>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight leading-tight" style="color: var(--text-primary);">%%SITE_NAME%%</h1>
        <p class="text-sm sm:text-base font-bold leading-snug" style="color: var(--text-primary);">行き先を入れるだけ。時差・天気・プラグ・チップ・安全情報がひと目でわかる。</p>
        <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">世界%%N_CITIES%%都市の渡航前チェックを、出発前も現地でも、1画面で確認できます。</p>
      </div>

      <div class="suggest-wrap">
        <i data-lucide="search" class="search-ico w-4 h-4"></i>
        <input id="search" type="text" autocomplete="off" inputmode="search" class="hero-search" placeholder="行き先を入力（例：ばり、ソウル、ロンドン）">
        <div id="suggest-box" class="suggest-dropdown hidden"></div>
      </div>

      <div class="space-y-1.5">
        <p class="text-[11px] font-semibold" style="color: var(--text-muted);">人気の行き先</p>
        <div class="flex flex-wrap gap-1.5">%%POPULAR_CHIPS%%</div>
      </div>

      <div class="grid grid-cols-2 gap-2 pt-1">
        <a href="#sec-season" class="intent-tile">
          <i data-lucide="sun" class="w-5 h-5 shrink-0" style="color: var(--amber-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">いつ行く？</strong><span class="text-[11px]" style="color: var(--text-muted);">今月の行き時</span></span>
        </a>
        <a href="./features/first-time-safe/" class="intent-tile">
          <i data-lucide="shield-check" class="w-5 h-5 shrink-0" style="color: var(--sage-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">初めての海外</strong><span class="text-[11px]" style="color: var(--text-muted);">安心の12都市</span></span>
        </a>
        <a href="#sec-cities" class="intent-tile">
          <i data-lucide="compass" class="w-5 h-5 shrink-0" style="color: var(--accent-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">行き先を探す</strong><span class="text-[11px]" style="color: var(--text-muted);">テーマ・予算で絞り込み</span></span>
        </a>
        <a href="./guides/" class="intent-tile">
          <i data-lucide="list-checks" class="w-5 h-5 shrink-0" style="color: var(--brand-esim-btn);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">準備を進める</strong><span class="text-[11px]" style="color: var(--text-muted);">持ち物・時差・チップ</span></span>
        </a>
      </div>

      <p class="text-[10.5px] leading-relaxed" style="color: var(--text-muted);">外務省の海外安全情報へのリンク付き ・ 為替の更新: %%RATES_UPDATED%% ・ 月別の気候カレンダー: %%CAL_COUNT%%都市</p>
    </section>

    <section id="sec-season" class="space-y-2.5 hidden">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold flex items-center gap-1.5" style="color: var(--text-primary);"><i data-lucide="sun" class="w-4 h-4"></i><span>今が行き時の都市</span></h2>
        <span class="text-[11px]" style="color: var(--text-muted);">気温・雨量から自動で選定</span>
      </div>
      <div id="season-tabs" class="hscroll"></div>
      <div id="season-list" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5"></div>
      <p class="text-[10.5px] leading-relaxed" style="color: var(--text-muted);">月別の気温・降水量・湿度から算出した目安です（一部は編集部概算）。実際の天候は年によって異なります。各都市ページで1年のカレンダーを確認できます。</p>
    </section>

    <section id="sec-cities" class="space-y-3">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">条件から行き先を探す</h2>
        <span id="index-city-count" class="text-[11px] tabular-nums" style="color: var(--text-muted);">%%N_CITIES%%都市</span>
      </div>

      <div class="space-y-2">
        <div class="space-y-1"><p class="text-[11px] font-semibold" style="color: var(--text-muted);">テーマ</p><div class="hscroll" id="chips-theme">%%THEME_CHIPS%%</div></div>
        <div class="space-y-1"><p class="text-[11px] font-semibold" style="color: var(--text-muted);">地域</p><div class="hscroll" id="chips-region">%%REGION_CHIPS%%</div></div>
        <div class="space-y-1"><p class="text-[11px] font-semibold" style="color: var(--text-muted);">現地の物価（目安）</p>
          <div class="hscroll" id="chips-budget">
            <button type="button" class="fchip is-active" data-budget="all">すべて</button>
            <button type="button" class="fchip" data-budget="1">安め</button>
            <button type="button" class="fchip" data-budget="2">普通</button>
            <button type="button" class="fchip" data-budget="3">高め</button>
          </div>
        </div>
        <button id="filter-reset" type="button" class="sub-text-link hidden"><i data-lucide="rotate-ccw" class="w-3 h-3"></i><span>条件をリセット</span></button>
      </div>

      <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">%%CARDS%%</div>
      <div id="grid-empty" class="hidden ed-tint p-4 text-xs text-center" style="color: var(--text-secondary);">条件に合う都市が見つかりませんでした。条件を減らすか、リセットしてお試しください。</div>
      <div class="text-center"><button id="more-btn" type="button" class="pr-cta" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></button></div>
    </section>

    <section class="space-y-3">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">季節・テーマ別特集</h2>
        <span class="text-[11px]" style="color: var(--text-muted);">時期や目的から選ぶ</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">%%FEATURE_LINKS%%</div>
      <div class="pt-0.5">
        <button id="comp-toggle-btn" type="button" class="sub-text-link" aria-expanded="false"><span>2都市比較ページ一覧を開く</span><i data-lucide="chevron-down" class="w-3 h-3"></i></button>
        <div id="comp-toggle-panel" class="accordion-content"><div class="accordion-inner"><div class="flex flex-wrap gap-1.5 pt-2.5">%%COMPARE_LINKS%%</div></div></div>
      </div>
    </section>

    <section class="space-y-3">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">ガイド・早見表</h2>
        <a href="./guides/" class="text-[11px] underline" style="color: var(--accent-text);">一覧を見る</a>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">%%GUIDE_LINKS%%</div>
    </section>

    %%SISTER%%
    %%SHARE%%

    <footer class="pt-6 text-center text-xs space-y-2" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline">たびレジ</a></p>
      <p><a href="./guides/" class="underline">ガイド・早見表</a> · <a href="./policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a> · <a href="./policy/#contact" class="underline">お問い合わせ・情報修正依頼</a></p>
      <p>© %%SITE_NAME%% (%%SITE_URL%%)</p>
    </footer>
  </main>

  <div id="toast" class="toast-msg" role="status" aria-live="polite">
    <i data-lucide="check" class="w-3.5 h-3.5"></i>
    <span id="toast-text">コピーしました</span>
  </div>

  %%PIXELS%%

  <script>
    lucide.createIcons();
    %%THEME_TOAST_SCRIPT%%
    %%SHARE_SCRIPT%%

    const CITY_BRIEF = %%CITY_BRIEF%%;
    const MONTH_DATA = %%MONTH_DATA%%;
    const TOTAL_CITIES = %%N_CITIES%%;
    const LAB_NAME = ['ベスト', '快適', '標準', '注意'];

    // ---------- 比較ページ一覧の開閉 ----------
    const compBtn = document.getElementById('comp-toggle-btn');
    const compPanel = document.getElementById('comp-toggle-panel');
    if (compBtn && compPanel) {
      compBtn.addEventListener('click', () => {
        const expanded = compBtn.getAttribute('aria-expanded') === 'true';
        compBtn.setAttribute('aria-expanded', String(!expanded));
        compPanel.classList.toggle('is-open', !expanded);
      });
    }

    const progressBar = document.getElementById('scroll-progress');
    window.addEventListener('scroll', () => {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (progressBar && docHeight > 0) progressBar.style.width = `${Math.min((window.scrollY / docHeight) * 100, 100)}%`;
    }, { passive: true });

    // ---------- 今が行き時の都市 ----------
    const seasonSec = document.getElementById('sec-season');
    const seasonTabs = document.getElementById('season-tabs');
    const seasonList = document.getElementById('season-list');
    const baseMonth = new Date().getMonth();

    function recommendFor(mi) {
      const rows = [];
      Object.keys(MONTH_DATA).forEach((slug) => {
        const m = MONTH_DATA[slug][mi];
        if (!m || m[0] > 1 || !CITY_BRIEF[slug]) return;
        rows.push({ slug: slug, lab: m[0], tmin: m[1], tmax: m[2], score: m[3] });
      });
      rows.sort((a, b) => (b.score - a.score) || a.slug.localeCompare(b.slug));
      const out = [];
      const perRegion = {};
      for (const r of rows) {
        const reg = CITY_BRIEF[r.slug].r;
        if ((perRegion[reg] || 0) >= 2) continue;
        perRegion[reg] = (perRegion[reg] || 0) + 1;
        out.push(r);
        if (out.length >= 6) break;
      }
      return out;
    }

    function renderSeason(offset) {
      const mi = (baseMonth + offset) % 12;
      const rows = recommendFor(mi);
      seasonList.innerHTML = rows.map((r) => {
        const b = CITY_BRIEF[r.slug];
        return `<a href="./${r.slug}/" class="ed-surface block p-3 space-y-1">
          <div class="flex items-baseline justify-between gap-2"><span class="font-bold text-sm" style="color: var(--text-primary);">${b.n}</span><span class="lab-chip lab-${r.lab}">${LAB_NAME[r.lab]}</span></div>
          <p class="text-[11px] tabular-nums" style="color: var(--text-muted);">${b.c} ・ ${r.tmin}〜${r.tmax}℃</p>
          ${b.v ? `<p class="text-[11px] leading-relaxed clamp-2" style="color: var(--text-secondary);">${b.v}</p>` : ''}
        </a>`;
      }).join('');
      Array.from(seasonTabs.children).forEach((btn, i) => btn.classList.toggle('is-active', i === offset));
    }

    if (Object.keys(MONTH_DATA).length > 0) {
      for (let i = 0; i < 3; i++) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'fchip' + (i === 0 ? ' is-active' : '');
        btn.textContent = `${((baseMonth + i) % 12) + 1}月` + (i === 0 ? '（今月）' : (i === 1 ? '（来月）' : ''));
        btn.addEventListener('click', () => renderSeason(i));
        seasonTabs.appendChild(btn);
      }
      renderSeason(0);
      seasonSec.classList.remove('hidden');
    }

    // ---------- 検索・絞り込み ----------
    let currentRegion = 'すべて';
    let currentTheme = 'all';
    let currentBudget = 'all';
    let expanded = false;
    const searchInput = document.getElementById('search');
    const suggestBox = document.getElementById('suggest-box');
    const cards = Array.from(document.querySelectorAll('.city-card'));
    const countEl = document.getElementById('index-city-count');
    const moreBtn = document.getElementById('more-btn');
    const emptyEl = document.getElementById('grid-empty');
    const resetBtn = document.getElementById('filter-reset');

    function toHiragana(str) {
      return str.replace(/[\u30a1-\u30f6]/g, (m) => String.fromCharCode(m.charCodeAt(0) - 0x60));
    }
    function normalizeText(str) { return toHiragana(str.toLowerCase().trim()); }

    function applyFilters() {
      const q = normalizeText(searchInput.value);
      const filtering = !!q || currentRegion !== 'すべて' || currentTheme !== 'all' || currentBudget !== 'all';
      let visible = 0, hiddenByLimit = 0;
      const matched = [];

      cards.forEach((card) => {
        const okSearch = !q || normalizeText(card.dataset.search).includes(q);
        const okRegion = currentRegion === 'すべて' || card.dataset.region === currentRegion;
        const okTheme = currentTheme === 'all' || (' ' + card.dataset.themes + ' ').includes(' ' + currentTheme + ' ');
        const okBudget = currentBudget === 'all' || card.dataset.budget === currentBudget;
        const ok = okSearch && okRegion && okTheme && okBudget;
        let show = ok;
        if (ok && !filtering && !expanded && card.dataset.featured !== '1') { show = false; hiddenByLimit++; }
        card.style.display = show ? 'block' : 'none';
        if (show) visible++;
        if (q && okSearch) matched.push(card);
      });

      if (countEl) countEl.textContent = filtering ? `${visible}都市が該当` : (expanded ? `${TOTAL_CITIES}都市` : `人気 ${visible}都市 / 全${TOTAL_CITIES}都市`);
      emptyEl.classList.toggle('hidden', visible > 0);
      resetBtn.classList.toggle('hidden', !(currentRegion !== 'すべて' || currentTheme !== 'all' || currentBudget !== 'all'));
      if (!filtering && !expanded && hiddenByLimit > 0) {
        moreBtn.textContent = `すべての${TOTAL_CITIES}都市を表示（残り${hiddenByLimit}都市）`;
        moreBtn.classList.remove('hidden');
      } else {
        moreBtn.classList.add('hidden');
      }

      if (q.length > 0 && matched.length > 0) {
        suggestBox.innerHTML = matched.slice(0, 8).map((c) => `
          <button type="button" class="suggest-item" data-href="./${c.dataset.slug}/">
            <span class="font-bold">${c.dataset.name}</span>
            <span style="color: var(--text-muted);">${c.dataset.country} →</span>
          </button>`).join('');
        suggestBox.classList.remove('hidden');
      } else {
        suggestBox.classList.add('hidden');
      }
    }

    function setActive(container, matchFn) {
      Array.from(container.children).forEach((b) => b.classList.toggle('is-active', matchFn(b)));
    }
    document.getElementById('chips-theme').addEventListener('click', (e) => {
      const b = e.target.closest('[data-theme]'); if (!b) return;
      currentTheme = b.dataset.theme; setActive(e.currentTarget, (x) => x === b); applyFilters();
    });
    document.getElementById('chips-region').addEventListener('click', (e) => {
      const b = e.target.closest('[data-region]'); if (!b) return;
      currentRegion = b.dataset.region; setActive(e.currentTarget, (x) => x === b); applyFilters();
    });
    document.getElementById('chips-budget').addEventListener('click', (e) => {
      const b = e.target.closest('[data-budget]'); if (!b) return;
      currentBudget = b.dataset.budget; setActive(e.currentTarget, (x) => x === b); applyFilters();
    });
    resetBtn.addEventListener('click', () => {
      currentRegion = 'すべて'; currentTheme = 'all'; currentBudget = 'all';
      ['chips-theme', 'chips-region', 'chips-budget'].forEach((id) => {
        const c = document.getElementById(id);
        Array.from(c.children).forEach((b, i) => b.classList.toggle('is-active', i === 0));
      });
      applyFilters();
    });
    moreBtn.addEventListener('click', () => { expanded = true; applyFilters(); });

    suggestBox.addEventListener('pointerdown', (e) => {
      const item = e.target.closest('.suggest-item');
      if (item && item.dataset.href) { e.preventDefault(); window.location.href = item.dataset.href; }
    });
    searchInput.addEventListener('input', applyFilters);
    searchInput.addEventListener('focus', () => { if (searchInput.value.trim().length > 0) applyFilters(); });
    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !suggestBox.contains(e.target)) suggestBox.classList.add('hidden');
    });
    applyFilters();
  </script>
</body>
</html>"""


def build_index_html(cities: list, rates_data: dict, featured_compare_pairs: list) -> str:
    n = len(cities)
    page_url = f"{SITE_URL}/"
    page_title = f"{SITE_NAME}｜世界{n}都市の時差・天気・コンセント・チップ・安全情報をひと目で"
    page_desc = (f"行き先を入れるだけで、世界{n}都市の現在時刻・時差・気温・1年カレンダー・コンセント・チップ・為替・外務省危険情報が分かる渡航前チェックサイト。"
                 f"今月の行き時、テーマ別の探し方、持ち物チェックリストも。")
    city_map = {c["slug"]: c for c in cities}

    # --- 並び順: 人気 → その他（元の順） ---
    pop_rank = {s: i for i, s in enumerate(POPULAR)}
    ordered = sorted(cities, key=lambda c: (0, pop_rank[c["slug"]]) if c["slug"] in pop_rank else (1, 0))

    theme_of = {}
    for tkey, (_, slugs) in THEMES.items():
        for s in slugs:
            theme_of.setdefault(s, []).append(tkey)
    theme_counts = {tkey: sum(1 for c in cities if tkey in theme_of.get(c["slug"], [])) for tkey in THEMES}

    regions = ["すべて"] + sorted({c["region"] for c in cities})
    region_chips = "".join(
        f'<button type="button" class="fchip{" is-active" if r == "すべて" else ""}" data-region="{_esc(r)}">{_esc(r)}</button>' for r in regions
    )
    theme_chips = '<button type="button" class="fchip is-active" data-theme="all">すべて</button>' + "".join(
        f'<button type="button" class="fchip" data-theme="{k}">{_esc(lab)}（{theme_counts[k]}）</button>' for k, (lab, _) in THEMES.items() if theme_counts[k] > 0
    )
    popular_chips = "".join(
        f'<a href="./{s}/" class="text-xs font-semibold px-3 py-1.5 rounded-full transition" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{_esc(city_map[s]["name_ja"].split("（")[0])}</a>'
        for s in POPULAR[:10] if s in city_map
    )

    cards = []
    month_data, brief = {}, {}
    for c in ordered:
        r = compute_city_star_ratings(c)
        bench = compute_price_benchmarks(c, 0.01)
        tier = _budget_tier(bench["lunch_jpy"])
        cal = c.get("calendar")
        vibe = c.get("city_vibe") or ""
        themes = " ".join(theme_of.get(c["slug"], []))
        featured = "1" if c["slug"] in pop_rank else "0"
        tip_short = c["tip_badge"].split("（")[0]
        if c["special_ui"] == "china_vpn":
            extra = '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--rose-bg); color: var(--rose-text);">通信確認推奨</span>'
        elif c["special_ui"] == "vpn_recommended":
            extra = '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--accent-soft); color: var(--accent-text);">VPN活用可</span>'
        else:
            extra = ""
        danger = '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--amber-bg); color: var(--amber-text);">注意喚起</span>' if c["danger_color"] != "emerald" else ""
        best_chip = (f'<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--sage-bg); color: var(--sage-text);">ベスト {_esc(cal["best_months_str"])}</span>'
                     if cal and cal.get("best_months_str") and cal["best_months_str"] != "特になし" else "")
        tier_chip = f'<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--bg-tint); color: var(--text-secondary);">物価 {["", "安め", "普通", "高め"][tier]}</span>'
        line2 = (f'<p class="text-[11px] leading-relaxed mt-1 clamp-2" style="color: var(--text-secondary);">{_esc(vibe)}</p>' if vibe
                 else f'<p class="text-[11px] mt-1" style="color: var(--text-muted);">{_esc(c["region"])} ・ プラグ {_esc(c["plug_type"])} ・ {_esc(c["currency_code"])}</p>')
        search_str = f'{c["name_ja"]} {c["kana_kw"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}'
        cards.append(
            f'<a href="./{c["slug"]}/" data-region="{_esc(c["region"])}" data-name="{_esc(c["name_ja"])}" data-country="{_esc(c["country_ja"])}" '
            f'data-slug="{c["slug"]}" data-search="{_esc(search_str)}" data-themes="{themes}" data-budget="{tier}" data-featured="{featured}" '
            f'class="city-card ed-surface block px-3.5 py-3">'
            f'<div class="flex items-baseline justify-between gap-2"><span class="font-bold text-sm" style="color: var(--text-primary);">{_esc(c["name_ja"])}</span>'
            f'<span class="text-[11px] shrink-0" style="color: var(--text-muted);">{_esc(c["country_ja"])}</span></div>'
            f'{line2}'
            f'<div class="text-[10.5px] mt-1.5 flex items-center gap-1.5 flex-wrap">{best_chip}{tier_chip}<span class="tabular-nums" style="color: var(--text-muted);">チップ:{_esc(tip_short)}</span>{extra}{danger}</div>'
            f'</a>'
        )
        brief[c["slug"]] = {"n": c["name_ja"].split("（")[0], "c": c["country_ja"], "r": c["region"], "v": vibe}
        if cal:
            month_data[c["slug"]] = [[_LAB_CODE.get(m["label"], 2), m["tmin"], m["tmax"], m["score"]] for m in cal["months"]]

    feature_links = "".join(
        f'<a href="./features/{f["slug"]}/" class="ed-surface block p-3.5"><span class="text-[10px] font-medium tracking-wide block" style="color: var(--text-muted);">{_esc(f["badge"])}</span>'
        f'<p class="text-xs font-semibold mt-1 leading-relaxed" style="color: var(--text-primary);">{_esc(f["title"])}</p></a>'
        for f in FEATURE_PAGES
    )
    compare_links = "".join(
        f'<a href="./compare/{s1}-vs-{s2}/" class="text-[11px] px-2.5 py-1 rounded-full font-medium transition" style="background: var(--bg-tint); color: var(--text-secondary);">'
        f'{_esc(city_map[s1]["name_ja"].split("（")[0])} vs {_esc(city_map[s2]["name_ja"].split("（")[0])}</a>'
        for s1, s2, _ in featured_compare_pairs if s1 in city_map and s2 in city_map
    )
    guide_links = "".join(
        f'<a href="./guides/{slug}/" class="ed-surface block p-3.5 space-y-1"><div class="flex items-center gap-2"><i data-lucide="{icon}" class="w-4 h-4" style="color: var(--accent-text);"></i>'
        f'<span class="font-bold text-xs" style="color: var(--text-primary);">{_esc(label)}</span></div>'
        f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{_esc(d)}</p></a>'
        for slug, label, d, icon in GUIDE_PAGES
    )

    out = _INDEX_TEMPLATE
    repl = {
        "%%HEAD%%": render_common_head(page_title, page_desc, page_url, og_type="website"),
        "%%STYLES%%": render_editorial_styles(),
        "%%TITLE%%": _esc(page_title), "%%DESC%%": _esc(page_desc), "%%URL%%": page_url,
        "%%FAVICON%%": FAVICON_URL, "%%PR_BANNER%%": render_pr_banner(), "%%PIXELS%%": render_pixels(),
        "%%POPULAR_CHIPS%%": popular_chips, "%%THEME_CHIPS%%": theme_chips, "%%REGION_CHIPS%%": region_chips,
        "%%CARDS%%": "\n".join(cards), "%%FEATURE_LINKS%%": feature_links, "%%COMPARE_LINKS%%": compare_links,
        "%%GUIDE_LINKS%%": guide_links, "%%SISTER%%": render_sister_site_banner(), "%%SHARE%%": render_share_buttons(page_url, page_title),
        "%%THEME_TOAST_SCRIPT%%": render_theme_and_toast_script(), "%%SHARE_SCRIPT%%": render_share_script(),
        "%%CITY_BRIEF%%": json.dumps(brief, ensure_ascii=False), "%%MONTH_DATA%%": json.dumps(month_data, ensure_ascii=False),
        "%%RATES_UPDATED%%": _esc(str(rates_data.get("updated_at", ""))), "%%CAL_COUNT%%": str(len(month_data)),
        "%%SITE_NAME%%": SITE_NAME, "%%SITE_URL%%": SITE_URL, "%%N_CITIES%%": str(n),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    return out
