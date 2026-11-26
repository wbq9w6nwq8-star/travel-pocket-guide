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
    render_site_nav, render_common_head, render_editorial_styles, render_pr_banner, render_pixels,
    render_share_buttons, render_share_script, render_theme_and_toast_script,
    render_sister_site_banner, render_agoda_and_oooh_box, render_telecom_box,
    compute_city_star_ratings, compute_price_benchmarks, render_plug_svg,
)
from site_content import POPULAR, THEMES, GUIDE_PAGES, CONTACT_FORM_ENDPOINT

_esc = _html.escape


# ---------------------------------------------------------------------------
# 共通：ガイドページの外枠
# ---------------------------------------------------------------------------
def _guide_shell(title: str, desc: str, url: str, body: str, script: str = "", head_extra: str = "",
                 crumb: str = "", depth: int = 2, active: str = "guides", crumb_html: str = "") -> str:
    up = "../" * depth
    guides_link = "../" if depth == 2 else "../guides/"
    if not crumb_html:
        crumb_html = f'<nav class="text-[11px]" style="color: var(--text-muted);"><a href="{up}" class="underline">トップ</a> › <a href="{guides_link}" class="underline">ガイド・早見表</a>{crumb}</nav>'
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
      <a href="{up}" class="inline-flex items-center gap-2 py-1 pr-2 rounded-lg" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4" style="color: var(--accent-text);"></i>
        <span class="font-extrabold text-sm sm:text-base">{SITE_NAME}</span>
      </a>
      <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>
  {render_site_nav(up, active)}

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-6">
    {crumb_html}
    {body}
    {render_share_buttons(url, title)}
    {render_sister_site_banner()}
    <footer class="pt-6 pb-4 text-center text-[11px] space-y-1.5" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>※当ページはプロモーション（アフィリエイト広告）を含みます。制度・規則は変更されるため、渡航前に公式情報をご確認ください。</p>
      <p><a href="{guides_link}" class="underline">ガイド・早見表一覧</a> · <a href="{up}policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a> · <a href="{up}contact/" class="underline">お問い合わせ</a></p>
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
    crumb = '<nav class="text-[11px]" style="color: var(--text-muted);"><a href="../" class="underline">トップ</a> › ガイド・早見表</nav>'
    out = _guide_shell(title, desc, url, body, depth=1, active="guides", crumb_html=crumb)
    return out.replace('<a href="../guides/" class="underline">ガイド・早見表一覧</a>', '<a href="./" class="underline">ガイド・早見表一覧</a>')


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
    .quick-nav { position: sticky; top: var(--hdr-h, 46px); z-index: 44; background: color-mix(in srgb, var(--bg-canvas) 94%, transparent); backdrop-filter: blur(12px); border-bottom: 1px solid var(--divider); }
    .hsnap { display: flex; gap: 10px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 6px; scrollbar-width: none; }
    .hsnap::-webkit-scrollbar { display: none; }
    .hsnap > a { flex: 0 0 76%; scroll-snap-align: start; }
    @media (min-width: 640px) { .hsnap { display: grid; grid-template-columns: repeat(3, 1fr); overflow: visible; } .hsnap > a { flex: none; } }
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

  <nav id="quick-nav" class="quick-nav" aria-label="ページ内ナビゲーション">
    <div class="max-w-[780px] mx-auto px-4"><div class="snav-row">
      <a href="#sec-season" class="snav-link" data-target="sec-season">今が行き時</a>
      <a href="#sec-features" class="snav-link" data-target="sec-features">季節・テーマ特集</a>
      <a href="#sec-compare" class="snav-link" data-target="sec-compare">都市を比べる</a>
      <a href="#sec-guides" class="snav-link" data-target="sec-guides">ガイド・早見表</a>
      <a href="#sec-cities" class="snav-link" data-target="sec-cities">全都市から探す</a>
    </div></div>
  </nav>

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
        <a href="#sec-features" class="intent-tile">
          <i data-lucide="calendar-days" class="w-5 h-5 shrink-0" style="color: var(--amber-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">季節・テーマ特集</strong><span class="text-[11px]" style="color: var(--text-muted);">時期や目的から選ぶ</span></span>
        </a>
        <a href="#sec-compare" class="intent-tile">
          <i data-lucide="scale" class="w-5 h-5 shrink-0" style="color: var(--accent-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">都市を比べる</strong><span class="text-[11px]" style="color: var(--text-muted);">迷う2都市を並べて確認</span></span>
        </a>
        <a href="#sec-guides" class="intent-tile">
          <i data-lucide="list-checks" class="w-5 h-5 shrink-0" style="color: var(--brand-esim-btn);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">ガイド・早見表</strong><span class="text-[11px]" style="color: var(--text-muted);">持ち物・時差・緊急時</span></span>
        </a>
        <a href="./features/first-time-safe/" class="intent-tile">
          <i data-lucide="shield-check" class="w-5 h-5 shrink-0" style="color: var(--sage-text);"></i>
          <span><strong class="block text-xs" style="color: var(--text-primary);">初めての海外</strong><span class="text-[11px]" style="color: var(--text-muted);">安心の12都市</span></span>
        </a>
      </div>

      <p class="text-[10.5px] leading-relaxed" style="color: var(--text-muted);">外務省の海外安全情報へのリンク付き ・ 為替の更新: %%RATES_UPDATED%% ・ 月別の気候カレンダー: %%CAL_COUNT%%都市</p>
    </section>

    <section id="sec-season" class="space-y-2.5 hidden scroll-mt">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold flex items-center gap-1.5" style="color: var(--text-primary);"><i data-lucide="sun" class="w-4 h-4"></i><span>今が行き時の都市</span></h2>
        <span class="text-[11px]" style="color: var(--text-muted);">気温・雨量から自動で選定</span>
      </div>
      <div id="season-tabs" class="hscroll"></div>
      <div id="season-list" class="grid grid-cols-2 sm:grid-cols-3 gap-2"></div>
      <p class="text-[10.5px] leading-relaxed" style="color: var(--text-muted);">月別の気温・降水量・湿度から算出した目安です（一部は編集部概算）。実際の天候は年によって異なります。各都市ページで1年のカレンダーを確認できます。</p>
    </section>

    <section id="sec-features" class="space-y-3 scroll-mt">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold flex items-center gap-1.5" style="color: var(--text-primary);"><i data-lucide="calendar-days" class="w-4 h-4"></i><span>季節・テーマ別の特集</span></h2>
        <a href="./features/" class="text-[11px] underline" style="color: var(--accent-text);">一覧を見る</a>
      </div>
      <p class="text-[11px]" style="color: var(--text-muted);">「いつ行くか」「どんな旅にしたいか」から選べます。気温・服装・時差・空港アクセスなどを表で比較できます。</p>
      <div class="hsnap">%%FEATURE_LINKS%%</div>
    </section>

    <section id="sec-compare" class="space-y-3 scroll-mt">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold flex items-center gap-1.5" style="color: var(--text-primary);"><i data-lucide="scale" class="w-4 h-4"></i><span>都市を比べる</span></h2>
        <a href="./compare/" class="text-[11px] underline" style="color: var(--accent-text);">一覧を見る</a>
      </div>
      <div class="pr-card pr-card--accent space-y-2.5">
        <p class="text-xs font-bold" style="color: var(--text-primary);">迷っている2都市を選ぶだけ</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
          <select id="cmp-a" aria-label="都市A" class="w-full rounded-lg px-3 py-2.5 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></select>
          <select id="cmp-b" aria-label="都市B" class="w-full rounded-lg px-3 py-2.5 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);"></select>
        </div>
        <p id="cmp-warn" class="hidden text-[11px] font-bold" style="color: var(--rose-text);">異なる2都市を選んでください</p>
        <a id="cmp-go" href="./compare/%%BASE_PAIR%%/" class="pr-cta" style="background: var(--accent); color: #ffffff;"><span>この2都市を比較する</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i></a>
      </div>
      <div class="space-y-1.5">
        <p class="text-[11px] font-semibold" style="color: var(--text-muted);">人気の比較</p>
        <div class="flex flex-wrap gap-1.5">%%COMPARE_LINKS%%</div>
      </div>
    </section>

    <section id="sec-guides" class="space-y-3 scroll-mt">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold flex items-center gap-1.5" style="color: var(--text-primary);"><i data-lucide="list-checks" class="w-4 h-4"></i><span>ガイド・早見表</span></h2>
        <a href="./guides/" class="text-[11px] underline" style="color: var(--accent-text);">一覧を見る</a>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">%%GUIDE_LINKS%%</div>
    </section>

    <section id="sec-cities" class="space-y-3 scroll-mt">
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

    %%SISTER%%
    %%SHARE%%

    <footer class="pt-6 text-center text-xs space-y-2" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline">たびレジ</a></p>
      <p><a href="./guides/" class="underline">ガイド・早見表</a> · <a href="./policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a> · <a href="./contact/" class="underline">お問い合わせ・情報修正依頼</a></p>
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

    // ---------- ヘッダー高さ（追従ナビの位置合わせ）----------
    const hdrEl = document.querySelector('.ed-header');
    function setHdrH() { if (hdrEl) document.documentElement.style.setProperty('--hdr-h', hdrEl.offsetHeight + 'px'); }
    setHdrH(); window.addEventListener('resize', setHdrH, { passive: true });

    // ---------- クイックナビ（現在位置の強調）----------
    const qLinks = Array.from(document.querySelectorAll('#quick-nav .snav-link'));
    const qTargets = qLinks.map((l) => document.getElementById(l.dataset.target)).filter(Boolean);
    function updateQuickNav() {
      // 画面上端から一定の位置（画面の約3割）を過ぎた最後のセクションを「現在地」とする
      const th = Math.max(220, window.innerHeight * 0.3);
      let cur = null;
      qTargets.forEach((sec) => { if (sec.offsetParent !== null && sec.getBoundingClientRect().top <= th) cur = sec.id; });
      qLinks.forEach((l) => l.classList.toggle('is-active', l.dataset.target === cur));
    }
    window.addEventListener('scroll', updateQuickNav, { passive: true });
    updateQuickNav();

    // ---------- 2都市比較ツール ----------
    const cmpA = document.getElementById('cmp-a');
    const cmpB = document.getElementById('cmp-b');
    const cmpGo = document.getElementById('cmp-go');
    const cmpWarn = document.getElementById('cmp-warn');
    const sortedSlugs = Object.keys(CITY_BRIEF).sort((x, y) => CITY_BRIEF[x].n.localeCompare(CITY_BRIEF[y].n, 'ja'));
    const optHtml = sortedSlugs.map((s) => `<option value="${s}">${CITY_BRIEF[s].n}（${CITY_BRIEF[s].c}）</option>`).join('');
    cmpA.innerHTML = optHtml; cmpB.innerHTML = optHtml;
    cmpA.value = '%%DEF_A%%'; cmpB.value = '%%DEF_B%%';
    function updateCmp() {
      const same = cmpA.value === cmpB.value;
      cmpWarn.classList.toggle('hidden', !same);
      cmpGo.href = same ? '#sec-compare' : `./compare/%%BASE_PAIR%%/?a=${encodeURIComponent(cmpA.value)}&b=${encodeURIComponent(cmpB.value)}`;
      cmpGo.style.opacity = same ? '.5' : '1';
    }
    cmpGo.addEventListener('click', (e) => { if (cmpA.value === cmpB.value) e.preventDefault(); });
    cmpA.addEventListener('change', updateCmp); cmpB.addEventListener('change', updateCmp); updateCmp();

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
        return `<a href="./${r.slug}/" class="ed-surface block p-2.5 space-y-0.5">
          <div class="flex items-baseline justify-between gap-1"><span class="font-bold text-[13px]" style="color: var(--text-primary);">${b.n}</span><span class="lab-chip lab-${r.lab}">${LAB_NAME[r.lab]}</span></div>
          <p class="text-[11px] tabular-nums" style="color: var(--text-muted);">${b.c} ・ ${r.tmin}〜${r.tmax}℃</p>
          ${b.v ? `<p class="hidden sm:block text-[11px] leading-relaxed clamp-2" style="color: var(--text-secondary);">${b.v}</p>` : ''}
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
        f'<a href="./features/{f["slug"]}/" class="ed-surface block p-3.5 space-y-1">'
        f'<span class="text-[10px] font-semibold px-2 py-0.5 rounded-full" style="background: var(--accent-soft); color: var(--accent-text);">{_esc(f["badge"])}</span>'
        f'<p class="text-xs font-bold mt-1.5 leading-snug" style="color: var(--text-primary);">{_esc(f["title"].split("｜")[0])}</p>'
        f'<p class="text-[11px] leading-relaxed clamp-2" style="color: var(--text-muted);">{_esc(f["desc"])}</p></a>'
        for f in FEATURE_PAGES
    )
    compare_links = "".join(
        f'<a href="./compare/{s1}-vs-{s2}/" class="text-[11px] px-2.5 py-1.5 rounded-full font-medium transition" style="background: var(--bg-tint); color: var(--text-secondary);">'
        f'{_esc(city_map[s1]["name_ja"].split("（")[0])} vs {_esc(city_map[s2]["name_ja"].split("（")[0])}</a>'
        for s1, s2, _ in featured_compare_pairs[:12] if s1 in city_map and s2 in city_map
    ) + '<a href="./compare/" class="text-[11px] px-2.5 py-1.5 rounded-full font-bold underline" style="color: var(--accent-text);">すべて見る →</a>'
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
        "%%BASE_PAIR%%": (f"{featured_compare_pairs[0][0]}-vs-{featured_compare_pairs[0][1]}" if featured_compare_pairs else ""),
        "%%DEF_A%%": (featured_compare_pairs[0][0] if featured_compare_pairs else ""), "%%DEF_B%%": (featured_compare_pairs[0][1] if featured_compare_pairs else ""),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


# ---------------------------------------------------------------------------
# お問い合わせページ（Formspree）
# ---------------------------------------------------------------------------
_CONTACT_TOPICS = ["情報の誤り・修正依頼", "掲載・取材・提携のご相談", "広告・PRのご相談", "サイトの不具合", "その他"]

_CONTACT_SCRIPT = r"""<script>
    (function () {
      var form = document.getElementById('contact-form');
      var okBox = document.getElementById('cf-success');
      var errBox = document.getElementById('cf-error');
      var btn = document.getElementById('cf-submit');
      var btnLabel = document.getElementById('cf-submit-label');
      var counter = document.getElementById('cf-count');
      var msg = document.getElementById('cf-message');
      var topicMap = { correction: '情報の誤り・修正依頼', partner: '掲載・取材・提携のご相談', ad: '広告・PRのご相談', bug: 'サイトの不具合', other: 'その他' };

      // 都市ページなどからのリンク（?topic=correction&page=ソウル）で内容を事前入力
      var params = new URLSearchParams(location.search);
      var t = params.get('topic');
      if (t && topicMap[t]) form.elements['topic'].value = topicMap[t];
      var pg = params.get('page');
      if (pg) form.elements['page'].value = pg.slice(0, 120);

      function updateCount() { counter.textContent = msg.value.length + ' / 3000'; }
      msg.addEventListener('input', updateCount); updateCount();

      function showError(text) { errBox.textContent = text; errBox.classList.remove('hidden'); okBox.classList.add('hidden'); }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        errBox.classList.add('hidden');
        form.elements['_subject'].value = '【%%SITE_NAME%%】' + form.elements['topic'].value;
        btn.disabled = true; btnLabel.textContent = '送信中…';
        fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
          .then(function (res) { return res.json().catch(function () { return {}; }).then(function (data) { return { ok: res.ok, data: data }; }); })
          .then(function (r) {
            if (r.ok) {
              form.reset(); updateCount();
              form.classList.add('hidden'); okBox.classList.remove('hidden');
              okBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
              var detail = (r.data && r.data.errors && r.data.errors.map(function (x) { return x.message; }).join(' / ')) || '';
              showError('送信できませんでした。' + (detail ? '（' + detail + '）' : '') + ' 時間をおいて、もう一度お試しください。');
            }
          })
          .catch(function () { showError('通信に失敗しました。ネットワーク環境をご確認のうえ、もう一度お試しください。'); })
          .then(function () { btn.disabled = false; btnLabel.textContent = '送信する'; });
      });
    })();
  </script>""".replace("%%SITE_NAME%%", SITE_NAME)


def build_contact_html() -> str:
    url = f"{SITE_URL}/contact/"
    title = f"お問い合わせ・情報修正のご連絡｜{SITE_NAME}"
    desc = f"{SITE_NAME}へのお問い合わせ、掲載情報の誤りのご指摘、提携・取材のご相談はこちらのフォームから。"
    topics = "".join(f'<option value="{_esc(t)}">{_esc(t)}</option>' for t in _CONTACT_TOPICS)
    input_style = 'style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);"'
    body = f"""
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-semibold uppercase tracking-wider" style="color: var(--accent-text);">CONTACT</span>
      <h1 class="text-xl sm:text-2xl font-bold">お問い合わせ・情報修正のご連絡</h1>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">掲載情報の誤り、最新状況への更新依頼、ご感想・ご提案などをお送りください。情報の修正は、公式情報を確認のうえ順次反映します。個別のご質問すべてに返信をお約束するものではありません。</p>
    </div>

    <div id="cf-success" class="hidden pr-card text-xs font-bold leading-relaxed" role="status" style="background: var(--sage-bg); border: 1px solid var(--sage-border); color: var(--sage-text);">
      送信ありがとうございます。お問い合わせを受け付けました。内容を確認のうえ、必要に応じてご連絡します。
    </div>
    <div id="cf-error" class="hidden pr-card text-xs font-bold leading-relaxed" role="alert" style="background: var(--rose-bg); border: 1px solid var(--rose-border); color: var(--rose-text);"></div>

    <form id="contact-form" action="{_esc(CONTACT_FORM_ENDPOINT)}" method="POST" class="ed-surface p-5 space-y-4 text-xs">
      <div>
        <label for="cf-topic" class="block font-bold mb-1" style="color: var(--text-primary);">お問い合わせの種類</label>
        <select id="cf-topic" name="topic" class="w-full rounded-lg px-3 py-2.5" {input_style}>{topics}</select>
      </div>
      <div>
        <label for="cf-page" class="block font-bold mb-1" style="color: var(--text-primary);">対象の都市・ページ <span class="font-normal" style="color: var(--text-muted);">（任意）</span></label>
        <input id="cf-page" name="page" type="text" maxlength="120" placeholder="例：ソウル、持ち物チェックリスト" class="w-full rounded-lg px-3 py-2.5" {input_style}>
      </div>
      <div>
        <label for="cf-message" class="block font-bold mb-1" style="color: var(--text-primary);">お問い合わせ内容 <span style="color: var(--rose-text);">（必須）</span></label>
        <textarea id="cf-message" name="message" rows="6" required minlength="10" maxlength="3000" placeholder="誤りのご指摘の場合は、該当箇所と、正しい内容・参考にした公式情報のURLがあると助かります。" class="w-full rounded-lg px-3 py-2.5 leading-relaxed" {input_style}></textarea>
        <p id="cf-count" class="text-[11px] text-right mt-0.5 tabular-nums" style="color: var(--text-muted);">0 / 3000</p>
      </div>
      <div>
        <label for="cf-email" class="block font-bold mb-1" style="color: var(--text-primary);">返信先メールアドレス <span class="font-normal" style="color: var(--text-muted);">（返信を希望する場合のみ）</span></label>
        <input id="cf-email" name="email" type="email" autocomplete="email" placeholder="example@example.com" class="w-full rounded-lg px-3 py-2.5" {input_style}>
      </div>

      <div style="display:none" aria-hidden="true">
        <label>このフィールドは空のままにしてください<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>
      </div>
      <input type="hidden" name="_subject" value="【{_esc(SITE_NAME)}】お問い合わせ">

      <label class="flex items-start gap-2 cursor-pointer">
        <input type="checkbox" name="consent" value="同意する" required class="mt-0.5">
        <span class="leading-relaxed" style="color: var(--text-secondary);"><a href="../policy/" target="_blank" rel="noopener" class="underline" style="color: var(--accent-text);">プライバシーポリシー</a>の内容（送信内容がフォーム送信サービスを通じて運営者に届くこと）に同意します。</span>
      </label>

      <button id="cf-submit" type="submit" class="pr-cta w-full sm:w-auto" style="background: var(--accent); color: #ffffff;">
        <span id="cf-submit-label">送信する</span>
        <i data-lucide="send" class="w-3.5 h-3.5"></i>
      </button>
      <p class="text-[11px] leading-relaxed" style="color: var(--text-muted);">※パスワードやカード番号など、機密性の高い情報は入力しないでください。</p>
    </form>"""
    crumb = '<nav class="text-[11px]" style="color: var(--text-muted);"><a href="../" class="underline">トップ</a> › お問い合わせ</nav>'
    return _guide_shell(title, desc, url, body, script=_CONTACT_SCRIPT, head_extra='<meta name="robots" content="noindex,follow">',
                        depth=1, active="contact", crumb_html=crumb)



# ---------------------------------------------------------------------------
# 特集一覧 / 比較一覧
# ---------------------------------------------------------------------------
def build_features_hub_html(cities: list) -> str:
    url = f"{SITE_URL}/features/"
    title = f"季節・テーマ別の特集一覧｜海外旅行先の選び方｜{SITE_NAME}"
    desc = "年末年始・春休み・GW・夏休み・秋休み、初めての海外・一人旅など、時期や目的から海外旅行先を選べる特集の一覧です。気温・服装・時差・空港アクセス・治安などを都市ごとに比較できます。"
    city_map = {c["slug"]: c for c in cities}
    cards = []
    for f in FEATURE_PAGES:
        names = "・".join(city_map[sl]["name_ja"].split("（")[0] for sl in f["cities"][:6] if sl in city_map)
        cards.append(
            f'<a href="./{f["slug"]}/" class="ed-surface block p-4 space-y-1.5">'
            f'<span class="text-[10px] font-semibold px-2 py-0.5 rounded-full" style="background: var(--accent-soft); color: var(--accent-text);">{_esc(f["badge"])}</span>'
            f'<p class="text-sm font-bold leading-snug" style="color: var(--text-primary);">{_esc(f["title"])}</p>'
            f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{_esc(f["desc"])}</p>'
            f'<p class="text-[11px]" style="color: var(--text-muted);">対象都市の例：{_esc(names)} ほか</p></a>'
        )
    body = _page_header("FEATURES", "季節・テーマ別の特集一覧", "「いつ行くか」「どんな旅にしたいか」から、行き先を選べます。気温・服装・時差・空港アクセス・治安などを、特集ごとに表で比べられます。") + \
        f'<section class="grid grid-cols-1 sm:grid-cols-2 gap-3">{"".join(cards)}</section>' + f"""
    <section class="ed-tint p-4 text-xs leading-relaxed" style="color: var(--text-secondary);">
      <strong style="color: var(--text-primary);">特集の見方：</strong>気温・降水日数は月別の気候データ（一部は編集部概算）から集計した目安です。実際の天候は年によって異なります。制度や料金は変わるため、渡航前に公式情報をご確認ください。
    </section>"""
    crumb = '<nav class="text-[11px]" style="color: var(--text-muted);"><a href="../" class="underline">トップ</a> › 季節・テーマ特集</nav>'
    return _guide_shell(title, desc, url, body, depth=1, active="features", crumb_html=crumb)


def build_compare_hub_html(cities: list, pairs: list) -> str:
    url = f"{SITE_URL}/compare/"
    title = f"都市を比べる｜2都市比較ツールと人気の比較一覧｜{SITE_NAME}"
    desc = "気になる2つの都市を選んで、時差・物価・ベスト月・空港アクセス・コンセント・チップ・治安をまとめて比較。人気の比較ペアの一覧もあります。"
    city_map = {c["slug"]: c for c in cities}
    base = f"{pairs[0][0]}-vs-{pairs[0][1]}" if pairs else ""
    cards = "".join(
        f'<a href="./{a}-vs-{b}/" class="ed-surface block p-3.5 space-y-1">'
        f'<span class="text-sm font-bold" style="color: var(--text-primary);">{_esc(city_map[a]["name_ja"].split("（")[0])} vs {_esc(city_map[b]["name_ja"].split("（")[0])}</span>'
        f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{_esc(summary)}</p></a>'
        for a, b, summary in pairs if a in city_map and b in city_map
    )
    options = "".join(f'<option value="{c["slug"]}">{_esc(c["name_ja"])}（{_esc(c["country_ja"])}）</option>' for c in cities)
    default_a = pairs[0][0] if pairs else cities[0]["slug"]
    default_b = pairs[0][1] if pairs else cities[1]["slug"]
    body = _page_header("COMPARE", "都市を比べる", "迷っている2都市を選ぶだけ。時差・物価・ベスト月・空港アクセス・コンセント・チップ・治安の違いをまとめて確認できます。") + f"""
    <section class="pr-card pr-card--accent space-y-2.5">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">好きな2都市を選んで比較</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">都市 A</label><select id="cmp-a" class="w-full rounded-lg px-3 py-2.5 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{options}</select></div>
        <div><label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">都市 B</label><select id="cmp-b" class="w-full rounded-lg px-3 py-2.5 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{options}</select></div>
      </div>
      <p id="cmp-warn" class="hidden text-[11px] font-bold" style="color: var(--rose-text);">異なる2都市を選んでください</p>
      <a id="cmp-go" href="./{base}/" class="pr-cta" style="background: var(--accent); color: #ffffff;"><span>この2都市を比較する</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i></a>
    </section>
    <section class="space-y-2.5">
      <h2 class="text-sm font-bold pb-1.5" style="color: var(--text-primary); border-bottom: 1px solid var(--divider);">人気の比較ペア</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">{cards}</div>
    </section>"""
    script = """<script>
    (function () {
      var a = document.getElementById('cmp-a'), b = document.getElementById('cmp-b'), go = document.getElementById('cmp-go'), warn = document.getElementById('cmp-warn');
      a.value = '%%A%%'; b.value = '%%B%%';
      function upd() {
        var same = a.value === b.value;
        warn.classList.toggle('hidden', !same);
        go.href = same ? '#' : './%%BASE%%/?a=' + encodeURIComponent(a.value) + '&b=' + encodeURIComponent(b.value);
        go.style.opacity = same ? '.5' : '1';
      }
      go.addEventListener('click', function (e) { if (a.value === b.value) e.preventDefault(); });
      a.addEventListener('change', upd); b.addEventListener('change', upd); upd();
    })();
  </script>""".replace("%%A%%", default_a).replace("%%B%%", default_b).replace("%%BASE%%", base)
    crumb = '<nav class="text-[11px]" style="color: var(--text-muted);"><a href="../" class="underline">トップ</a> › 都市を比べる</nav>'
    return _guide_shell(title, desc, url, body, script=script, depth=1, active="compare", crumb_html=crumb)



# ---------------------------------------------------------------------------
# 海外で困ったとき（緊急通報番号・大使館）
# ---------------------------------------------------------------------------
def build_emergency_html(cities: list) -> str:
    url = f"{SITE_URL}/guides/emergency/"
    title = f"【海外で困ったとき】国・地域別の緊急通報番号と日本大使館の連絡先｜{SITE_NAME}"
    desc = "海外で事故・病気・盗難・パスポート紛失などに遭ったときの基本の流れと、国・地域別の緊急通報番号、日本大使館・総領事館の連絡先をまとめました。番号は検索・コピーできます。"

    by_country = {}
    for c in cities:
        by_country.setdefault(c["country_ja"], []).append(c)
    cards = []
    for country, cl in sorted(by_country.items(), key=lambda kv: kv[0]):
        c0 = cl[0]
        search = " ".join([country] + [c["name_ja"] + " " + c["name_en"] for c in cl])
        cards.append(
            f'<div class="ed-surface p-4 space-y-1.5 em-card" data-search="{_esc(search.lower())}">'
            f'<div class="flex items-baseline justify-between gap-2 flex-wrap"><h3 class="text-sm font-bold" style="color: var(--text-primary);">{_esc(country)}</h3>'
            f'<button type="button" class="text-[11px] font-semibold px-2.5 py-1 rounded-full" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);" data-copy="{_esc(country)} 緊急通報: {_esc(c0["emergency_numbers"])} / {_esc(c0["embassy"])}">連絡先をコピー</button></div>'
            f'<p class="text-xs leading-relaxed"><strong style="color: var(--rose-text);">緊急通報：</strong><span style="color: var(--text-primary);">{_esc(c0["emergency_numbers"])}</span></p>'
            f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);"><strong style="color: var(--text-primary);">日本大使館・総領事館：</strong>{_esc(c0["embassy"])}</p>'
            f'<div class="text-[11px]">{_city_links(cl)}</div></div>'
        )

    steps = f"""
    <section class="ed-tint p-4 text-xs leading-relaxed space-y-2" style="color: var(--text-secondary);">
      <h2 class="text-sm font-bold" style="color: var(--text-primary);">困ったときの基本の流れ</h2>
      <p><strong style="color: var(--rose-text);">1. 命や安全に関わるとき（事故・急病・事件）：</strong>まず安全を確保し、現地の緊急通報番号（下の一覧）へ。入っている海外旅行保険の緊急連絡先（24時間デスク）にも連絡すると、病院の案内や支払いの手続きを助けてもらえます。</p>
      <p><strong style="color: var(--text-primary);">2. 盗難・紛失のとき：</strong>現地の警察に届け出て、盗難・紛失の証明書（届出番号）を受け取ります。クレジットカードはすぐにカード会社へ連絡して利用停止を。保険金の請求にも証明書が必要になることがあります。</p>
      <p><strong style="color: var(--text-primary);">3. パスポートをなくしたとき：</strong>警察への届出のあと、日本大使館・総領事館で手続きをします。新しいパスポートの発給や、帰国のための渡航書の発給など、必要な書類や日数は公館によって異なります。事前に外務省と在外公館の案内を確認してください。</p>
      <p><strong style="color: var(--text-primary);">4. 出発前にしておくこと：</strong>外務省の「たびレジ」に登録すると、渡航先の安全情報がメールで届きます。パスポートの写しやカード会社の連絡先は、スマホとは別の場所にも控えておくと安心です。</p>
      <p class="text-[11px]" style="color: var(--text-muted);">※番号や連絡先は変更されることがあります。必ず外務省「海外安全ホームページ」や在外公館の最新情報で確認してください。</p>
      <div class="flex flex-wrap gap-2 pt-1">
        <a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="pr-cta" style="background: var(--text-primary); color: var(--bg-canvas);"><span>外務省 海外安全ホームページ</span><i data-lucide="external-link" class="w-3.5 h-3.5"></i></a>
        <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="pr-cta" style="background: var(--sage-text); color: #ffffff;"><span>たびレジに登録する</span><i data-lucide="external-link" class="w-3.5 h-3.5"></i></a>
      </div>
    </section>"""
    body = _page_header("EMERGENCY GUIDE", "海外で困ったときの連絡先・手順",
        f"{len(by_country)}の国・地域の緊急通報番号と日本大使館・総領事館の連絡先を、検索してコピーできます。いざというときのために、出発前に渡航先を確認しておきましょう。") + steps + f"""
    <section class="space-y-2.5">
      <div class="flex items-baseline justify-between gap-2 flex-wrap pb-1.5" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">国・地域別の連絡先</h2>
        <span id="em-count" class="text-[11px]" style="color: var(--text-muted);">{len(by_country)}件</span>
      </div>
      <input id="em-search" type="search" autocomplete="off" placeholder="国名・都市名で絞り込み（例：タイ、パリ）" class="w-full rounded-lg px-3 py-2.5 text-xs" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
      <div id="em-list" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">{''.join(cards)}</div>
      <p id="em-empty" class="hidden text-xs text-center p-3" style="color: var(--text-muted);">該当する国・都市が見つかりませんでした。</p>
    </section>
    {render_telecom_box(custom_note="緊急時に連絡が取れるよう、渡航先で使える通信手段（eSIM・ローミングなど）を出発前に確認しておくと安心です。")}"""
    script = """<script>
    (function () {
      var input = document.getElementById('em-search'), cards = Array.prototype.slice.call(document.querySelectorAll('.em-card'));
      var count = document.getElementById('em-count'), empty = document.getElementById('em-empty');
      function hira(s) { return s.replace(/[\\u30a1-\\u30f6]/g, function (m) { return String.fromCharCode(m.charCodeAt(0) - 0x60); }); }
      function filter() {
        var q = hira(input.value.toLowerCase().trim()), n = 0;
        cards.forEach(function (c) { var ok = !q || hira(c.dataset.search).indexOf(q) !== -1; c.style.display = ok ? '' : 'none'; if (ok) n++; });
        count.textContent = n + '件'; empty.classList.toggle('hidden', n > 0);
      }
      input.addEventListener('input', filter);
      document.addEventListener('click', function (e) {
        var b = e.target.closest('[data-copy]'); if (!b) return;
        if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.copy).then(function () { if (typeof showToast === 'function') showToast('連絡先をコピーしました'); });
      });
    })();
  </script>"""
    return _guide_shell(title, desc, url, body, script=script, crumb=" › 海外で困ったとき")
