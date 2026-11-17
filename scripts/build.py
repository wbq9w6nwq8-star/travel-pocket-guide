import json
from pathlib import Path

SITE_URL = "https://example.com"  # 独自ドメイン取得後にここを書き換える

DATA_CITIES = Path("data/cities.json")
DATA_RATES = Path("data/rates.json")
DIST_DIR = Path("dist")

def render_plug_svg(plug_type: str) -> str:
    # 代表的なプラグ形状のシンプルなSVGアイコンを返す
    svgs = {
        "A": '<svg viewBox="0 0 64 64" class="w-12 h-12 mx-auto"><circle cx="32" cy="32" r="28" fill="#f1f5f9" stroke="#334155" stroke-width="3"/><rect x="21" y="20" width="4" height="24" rx="1" fill="#0f172a"/><rect x="39" y="20" width="4" height="24" rx="1" fill="#0f172a"/></svg>',
        "BF": '<svg viewBox="0 0 64 64" class="w-12 h-12 mx-auto"><circle cx="32" cy="32" r="28" fill="#f1f5f9" stroke="#334155" stroke-width="3"/><rect x="29" y="14" width="6" height="12" rx="1" fill="#0f172a"/><rect x="17" y="36" width="10" height="5" rx="1" fill="#0f172a"/><rect x="37" y="36" width="10" height="5" rx="1" fill="#0f172a"/></svg>',
        "C": '<svg viewBox="0 0 64 64" class="w-12 h-12 mx-auto"><circle cx="32" cy="32" r="28" fill="#f1f5f9" stroke="#334155" stroke-width="3"/><circle cx="22" cy="32" r="4.5" fill="#0f172a"/><circle cx="42" cy="32" r="4.5" fill="#0f172a"/></svg>'
    }
    return svgs.get(plug_type, svgs["C"])

def tip_color_class(level: str) -> str:
    return {
        "none": "bg-emerald-100 text-emerald-800 border-emerald-300",
        "optional": "bg-amber-100 text-amber-800 border-amber-300",
        "required": "bg-rose-100 text-rose-800 border-rose-300"
    }.get(level, "bg-slate-100 text-slate-800")

def build_city_page(city: dict, rates_data: dict) -> str:
    code = city["currency_code"]
    jpy_to_local = rates_data["rates"].get(code, 0.01)
    local_to_jpy = round(1 / jpy_to_local, 2) if jpy_to_local else 0
    thousand_jpy_in_local = round(1000 * jpy_to_local, 2)

    # 悩み直結アフィリエイトの出し分け
    context_affiliate = ""
    if not city["tap_water_safe"]:
        context_affiliate = f"""
        <div class="p-4 rounded-xl bg-amber-50 border border-amber-200 mt-4">
          <p class="text-xs font-bold text-amber-800">⚠️ {city['name_ja']}は水道水の飲用不可</p>
          <p class="text-sm text-slate-700 mt-1">現地の病院は高額になりがちです。キャッシュレス診療付きの海外旅行保険（またはクレカ付帯保険）の事前確認がおすすめです。</p>
          <a href="#YOUR_INSURANCE_AFFILIATE_LINK" class="inline-block mt-2 text-sm font-bold text-blue-600 underline">→ {city['country_ja']}対応の海外旅行保険を比較する</a>
        </div>
        """
    elif city["tip_level"] == "required":
        context_affiliate = f"""
        <div class="p-4 rounded-xl bg-rose-50 border border-rose-200 mt-4">
          <p class="text-xs font-bold text-rose-800">💳 {city['name_ja']}はカード決済＋チップ社会</p>
          <p class="text-sm text-slate-700 mt-1">一般的な日本のクレカは海外事務手数料（約2.2〜3.85%）がかかります。手数料の安いカードやWiseデビットを使うと数千円単位で節約できます。</p>
          <a href="#YOUR_CARD_AFFILIATE_LINK" class="inline-block mt-2 text-sm font-bold text-blue-600 underline">→ 海外決済でお得なカード一覧を見る</a>
        </div>
        """

    # FAQ構造化データ（Google検索結果にQ&Aを出す）
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{city['name_ja']}のコンセント形状と電圧は？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{city['name_ja']}（{city['country_ja']}）のコンセントは{city['plug_type']}タイプ、電圧は{city['voltage']}です。{city['transformer_note']}"
                }
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}でチップは必要ですか？相場は？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{city['tip_badge']}です。{city['tip_detail']}"
                }
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}の水道水は飲めますか？",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": city["tap_water_note"]
                }
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{city['name_ja']}の現地情報まとめ｜時差・コンセント({city['plug_type']})・チップ・為替を1画面で即答</title>
  <meta name="description" content="{city['name_ja']}（{city['country_ja']}）の現在時刻・日本との時差、コンセントのプラグ形状（{city['plug_type']}タイプ）・電圧（{city['voltage']}）、チップ相場、最新為替レート、空港からの移動手段をスクロールなしで即確認。">
  <link rel="canonical" href="{SITE_URL}/{city['slug']}/">
  <link rel="manifest" href="/manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased">
  <header class="bg-white border-b border-slate-200 sticky top-0 z-10">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="/" class="font-bold text-slate-800 text-sm">🌐 渡航ポケット辞典</a>
      <span class="text-xs text-slate-500">{city['region']} / {city['country_ja']}</span>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 py-5 space-y-5">
    <div>
      <h1 class="text-2xl font-extrabold tracking-tight">{city['name_ja']} <span class="text-base font-normal text-slate-500">{city['name_en']}</span></h1>
      <p class="text-xs text-slate-500 mt-1">最終レート更新: {rates_data['updated_at']}</p>
    </div>

    <!-- ファーストビュー：4分割即答ダッシュボード -->
    <section class="grid grid-cols-2 gap-3">
      <!-- 1. 現地時刻 -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <div class="flex items-center justify-between">
          <span class="text-xs font-bold text-slate-500">🕒 現地時刻</span>
          <button id="tz-toggle" class="text-[10px] bg-slate-100 px-2 py-0.5 rounded text-slate-600">vs 日本</button>
        </div>
        <div id="local-clock" class="text-2xl font-mono font-bold mt-2">--:--:--</div>
        <div id="time-diff" class="text-xs font-medium text-blue-600 mt-1">時差を計算中...</div>
      </div>

      <!-- 2. コンセント -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 text-center">
        <span class="text-xs font-bold text-slate-500 block text-left">🔌 プラグ・電圧</span>
        <div class="my-1">{render_plug_svg(city['plug_type'])}</div>
        <div class="text-sm font-bold">{city['plug_type']}タイプ / {city['voltage']}</div>
        <div class="text-[11px] text-slate-500">{'変圧器が必要' if city['transformer_needed'] else 'スマホ変圧器不要'}</div>
      </div>

      <!-- 3. チップ判定 -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">💵 チップ習慣</span>
        <div class="my-2">
          <span class="inline-block px-2.5 py-1 rounded-lg text-xs font-bold border {tip_color_class(city['tip_level'])}">
            {city['tip_badge']}
          </span>
        </div>
        <div class="text-[11px] text-slate-500">詳細は下部のマナー欄へ</div>
      </div>

      <!-- 4. クイック通貨換算 -->
      <div class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 flex flex-col justify-between">
        <span class="text-xs font-bold text-slate-500">💱 1{code} ≒ {local_to_jpy}円</span>
        <div class="mt-2">
          <div class="flex items-center border border-slate-300 rounded-lg px-2 py-1 bg-slate-50">
            <input id="jpy-input" type="number" value="1000" class="w-full bg-transparent text-sm font-bold focus:outline-none">
            <span class="text-xs text-slate-500 ml-1">円</span>
          </div>
          <div id="local-output" class="text-sm font-bold text-emerald-700 mt-1">≒ {thousand_jpy_in_local} {code}</div>
        </div>
      </div>
    </section>

    <!-- 通信＆eSIM枠（全都市共通の高収益枠） -->
    <section class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
      <h2 class="text-base font-bold flex items-center gap-1.5">📶 通信・ネット環境</h2>
      <p class="text-sm text-slate-700 mt-2 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 p-3.5 rounded-xl bg-blue-50 border border-blue-200">
        <p class="text-xs font-bold text-blue-900">✈️ 空港に着いた瞬間からネットを使うなら</p>
        <p class="text-xs text-slate-700 mt-1">物理SIMの入れ替え不要。日本でQRコードを読み込むだけの{city['country_ja']}対応eSIMが最安・最速です。</p>
        <a href="#YOUR_ESIM_AFFILIATE_LINK" class="inline-block mt-2 bg-blue-600 text-white text-xs font-bold px-3 py-2 rounded-lg">
          {city['name_ja']}で使えるおすすめeSIMを見る →
        </a>
      </div>
    </section>

    <!-- 電気・お金・マナー詳細 -->
    <section class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 space-y-4">
      <h2 class="text-base font-bold">⚡ 電気・お金・税金のルール</h2>
      <div class="text-sm space-y-2.5 text-slate-700">
        <p><strong class="text-slate-900">変圧器の目安：</strong>{city['transformer_note']}</p>
        <p><strong class="text-slate-900">チップの相場：</strong>{city['tip_detail']}</p>
        <p><strong class="text-slate-900">税金・免税：</strong>{city['tax_note']}</p>
        <p><strong class="text-slate-900">サマータイム：</strong>{city['dst_note']}</p>
      </div>
      {context_affiliate}
    </section>

    <!-- 空港アクセス・緊急時メモ -->
    <section class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <h2 class="text-base font-bold">🚕 空港アクセス＆緊急時メモ</h2>
      <div class="text-sm space-y-2 text-slate-700">
        <p><strong class="text-slate-900">{city['airport_access']['airport_name']}（最速）：</strong>{city['airport_access']['fastest']}</p>
        <p><strong class="text-slate-900">{city['airport_access']['airport_name']}（最安）：</strong>{city['airport_access']['cheapest']}</p>
        <p><strong class="text-slate-900">必須移動アプリ：</strong>{', '.join(city['transport_apps'])}</p>
        <p><strong class="text-slate-900">水道水：</strong>{city['tap_water_note']}</p>
        <p class="text-rose-700 font-bold">🚨 緊急連絡先（警察・救急・消防）：{city['emergency_numbers']['police_ambulance_fire']}</p>
      </div>
    </section>
  </main>

  <script>
    // 1. リアルタイム現地時刻＆時差計算
    const targetTz = "{city['timezone']}";
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

    // 2. クイック為替計算機
    const rate = {jpy_to_local};
    const jpyInput = document.getElementById('jpy-input');
    const localOutput = document.getElementById('local-output');
    jpyInput.addEventListener('input', () => {{
      const val = parseFloat(jpyInput.value) || 0;
      localOutput.textContent = `≒ ${{(val * rate).toFixed(2)}} {code}`;
    }});

    // 3. オフライン閲覧用 Service Worker 登録
    if ('serviceWorker' in navigator) {{
      navigator.serviceWorker.register('/sw.js').catch(() => {{}});
    }}
  </script>
</body>
</html>"""

def main():
    cities = json.loads(DATA_CITIES.read_text(encoding="utf-8"))
    rates_data = json.loads(DATA_RATES.read_text(encoding="utf-8"))
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    urls = [f"{SITE_URL}/"]

    for city in cities:
        city_dir = DIST_DIR / city["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        html = build_city_page(city, rates_data)
        (city_dir / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"{SITE_URL}/{city['slug']}/")

    # トップページ（検索フィルター付き都市一覧）生成
    cards_html = "\n".join([
        f'<a href="/{c["slug"]}/" data-name="{c["name_ja"]} {c["name_en"]} {c["country_ja"]}" class="city-card block bg-white p-4 rounded-xl border border-slate-200 hover:border-blue-400 transition">'
        f'<div class="font-bold text-base">{c["name_ja"]}</div>'
        f'<div class="text-xs text-slate-500 mt-0.5">{c["country_ja"]}・プラグ{c["plug_type"]}・{c["currency_code"]}</div>'
        f'</a>'
        for c in cities
    ])

    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>渡航ポケット辞典｜海外都市の時差・コンセント・チップ・為替を1画面で即答</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900">
  <main class="max-w-2xl mx-auto px-4 py-8 space-y-6">
    <div class="text-center space-y-2">
      <h1 class="text-2xl font-extrabold">🌐 渡航ポケット辞典</h1>
      <p class="text-sm text-slate-600">空港や渡航前に知りたい「時差・プラグ・チップ・為替」を1画面で即解決</p>
    </div>
    <input id="search" type="text" placeholder="都市名・国名で検索（例：ロンドン、アメリカ）" class="w-full p-3.5 rounded-xl border border-slate-300 bg-white shadow-sm text-sm">
    <div id="grid" class="grid grid-cols-2 gap-3">{cards_html}</div>
  </main>
  <script>
    document.getElementById('search').addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('.city-card').forEach(card => {{
        card.style.display = card.dataset.name.toLowerCase().includes(q) ? 'block' : 'none';
      }});
    }});
  </script>
</body>
</html>"""
    (DIST_DIR / "index.html").write_text(index_html, encoding="utf-8")

    # sitemap.xml 自動生成
    sitemap_items = "\n".join([f"  <url><loc>{u}</loc></url>" for u in urls])
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}
</urlset>"""
    (DIST_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    print(f"Built {len(cities)} city pages + index + sitemap!")

if __name__ == "__main__":
    main()