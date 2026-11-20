#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML・UIデザイン・テンプレート管理ファイル (templates.py)
- エディトリアル配色 × UI/UXアニメーション統合版
- 天気コード連動 Lucide アイコン ＋ 観測時刻表示
- 5段階評価バーの意味色分け（低彩度パレット）
- 気候実態に合わせた1年カレンダー見出し（雪目安 / 乾季・雨季目安）
- 出発日カウントダウン連動 3ステップ準備ガイド
- Wise ＆ エポスカードを含む視認性と誠実さを両立したPR・アフィリエイト導線
- スマホ表示バグ修正済み（reveal-section 最適化）
- OGP画像 (ogp.png) & ファビコン (youka.png) 全ページ完全対応
"""

import json
from config import (
    SITE_URL, SITE_NAME, GA4_ID, OGP_IMAGE_URL, FAVICON_URL,
    SISTER_SITE_URL, SISTER_SITE_NAME,
    AFFILIATE_ESIM_URL, AFFILIATE_VPN_URL, AFFILIATE_CARD_URL, AFFILIATE_WISE_URL,
    AFFILIATE_OOOH_URL, AFFILIATE_AGODA_URL,
    A8_PIXEL_URLS, FEATURE_PAGES
)


def render_plug_svg(plug_type: str) -> str:
    main_p = plug_type.split("/")[0]
    svgs = {
        "A": '<svg viewBox="0 0 64 64" class="w-10 h-10"><circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="2.5"/><rect x="21" y="20" width="4" height="24" rx="1" fill="currentColor"/><rect x="39" y="20" width="4" height="24" rx="1" fill="currentColor"/></svg>',
        "BF": '<svg viewBox="0 0 64 64" class="w-10 h-10"><circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="2.5"/><rect x="29" y="14" width="6" height="12" rx="1" fill="currentColor"/><rect x="16" y="36" width="11" height="5" rx="1" fill="currentColor"/><rect x="37" y="36" width="11" height="5" rx="1" fill="currentColor"/></svg>',
        "O": '<svg viewBox="0 0 64 64" class="w-10 h-10"><circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="2.5"/><rect x="20" y="18" width="4" height="14" transform="rotate(-30 22 25)" fill="currentColor"/><rect x="40" y="18" width="4" height="14" transform="rotate(30 42 25)" fill="currentColor"/><rect x="30" y="38" width="4" height="12" fill="currentColor"/></svg>',
        "C": '<svg viewBox="0 0 64 64" class="w-10 h-10"><circle cx="32" cy="32" r="28" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="22" cy="32" r="4.5" fill="currentColor"/><circle cx="42" cy="32" r="4.5" fill="currentColor"/></svg>'
    }
    return svgs.get(main_p, svgs["C"])


def tip_color_class(level: str) -> str:
    return {
        "none": "status-inline--ok",
        "optional": "status-inline--warn",
        "required": "status-inline--danger"
    }.get(level, "status-inline--warn")


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
  </script>
  <script src="https://unpkg.com/lucide@latest"></script>"""


def render_editorial_styles() -> str:
    return """<style>
    :root {
      --space-05: 4px;
      --space-1: 8px;
      --space-15: 12px;
      --space-2: 16px;
      --space-3: 24px;
      --space-4: 32px;
      --space-5: 44px;

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-full: 9999px;

      --font-sans: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
      --font-editorial: "Georgia", "Times New Roman", "Hiragino Mincho ProN", "Yu Mincho", serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
      --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
      --ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);

      --container-max: 780px;
      --bg-canvas: #f9f8f6;
      --bg-surface: #ffffff;
      --bg-tint: #f2f1ed;
      --bg-tint-hover: #e8e6e0;
      --text-primary: #18181b;
      --text-secondary: #3f3f46;
      --text-muted: #71717a;
      --divider: rgba(24, 24, 27, 0.08);
      --border-soft: rgba(24, 24, 27, 0.13);
      --shadow-hover: 0 8px 24px -6px rgba(24, 24, 27, 0.08);

      --accent: #274c77;
      --accent-soft: #eef2f6;
      --accent-border: rgba(39, 76, 119, 0.26);
      --accent-text: #1e3a5f;
      --sage-bg: #eef4f0;
      --sage-border: rgba(40, 82, 59, 0.25);
      --sage-text: #28523b;
      --amber-bg: #f8f2e7;
      --amber-border: rgba(124, 77, 18, 0.25);
      --amber-text: #8a5615;
      --rose-bg: #f9eded;
      --rose-border: rgba(136, 41, 41, 0.25);
      --rose-text: #882929;
    }

    :root[data-theme="dark"] {
      --bg-canvas: #111215;
      --bg-surface: #181a1f;
      --bg-tint: #21242b;
      --bg-tint-hover: #2a2e37;
      --text-primary: #f4f4f5;
      --text-secondary: #d4d4d8;
      --text-muted: #8e8e98;
      --divider: rgba(244, 244, 245, 0.09);
      --border-soft: rgba(244, 244, 245, 0.14);
      --shadow-hover: 0 10px 28px -6px rgba(0, 0, 0, 0.45);

      --accent: #6894c6;
      --accent-soft: rgba(104, 148, 198, 0.14);
      --accent-border: rgba(125, 162, 206, 0.35);
      --accent-text: #a5c2e6;
      --sage-bg: rgba(114, 168, 138, 0.14);
      --sage-border: rgba(151, 203, 176, 0.32);
      --sage-text: #97cbb0;
      --amber-bg: rgba(217, 173, 108, 0.14);
      --amber-border: rgba(228, 193, 141, 0.32);
      --amber-text: #e4c18d;
      --rose-bg: rgba(214, 118, 118, 0.15);
      --rose-border: rgba(230, 160, 160, 0.32);
      --rose-text: #e6a0a0;
    }

    *, *::before, *::after { box-sizing: border-box; }

    html {
      scroll-behavior: smooth;
      scroll-padding-top: 100px;
    }

    body {
      margin: 0;
      font-family: var(--font-sans);
      background-color: var(--bg-canvas);
      color: var(--text-primary);
      line-height: 1.65;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.35s var(--ease-smooth), color 0.35s var(--ease-smooth);
    }

    .tabular-nums { font-variant-numeric: tabular-nums; }
    .font-editorial-italic { font-family: var(--font-editorial); font-style: italic; }

    @keyframes enterUp {
      from { opacity: 0; transform: translateY(14px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseLive {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.45; transform: scale(0.85); }
    }

    .anim-enter { opacity: 0; animation: enterUp 0.65s var(--ease-out-expo) forwards; }
    .delay-1 { animation-delay: 60ms; }
    .delay-2 { animation-delay: 120ms; }

    .reveal-section {
      opacity: 0;
      transform: translateY(14px);
      transition: opacity 0.55s var(--ease-out-expo), transform 0.55s var(--ease-out-expo);
    }
    .reveal-section.is-visible { opacity: 1; transform: translateY(0); }

    .ed-header {
      position: sticky;
      top: 0;
      z-index: 40;
      background-color: color-mix(in srgb, var(--bg-canvas) 90%, transparent);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--divider);
    }

    .scroll-progress {
      position: absolute;
      top: 0;
      left: 0;
      height: 2px;
      width: 0%;
      background-color: var(--accent);
      transition: width 0.1s linear;
    }

    .toc-nav {
      position: relative;
      display: flex;
      gap: 20px;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .toc-nav::-webkit-scrollbar { display: none; }

    .toc-link {
      padding: 6px 0 9px;
      font-size: 12px;
      font-weight: 500;
      color: var(--text-muted);
      white-space: nowrap;
      transition: color 0.2s ease;
    }
    .toc-link:hover, .toc-link.is-active { color: var(--text-primary); font-weight: 700; }

    .toc-glider {
      position: absolute;
      bottom: 0;
      left: 0;
      height: 2px;
      width: 0;
      border-radius: 2px;
      background-color: var(--text-primary);
      transition: transform 0.35s var(--ease-out-expo), width 0.35s var(--ease-out-expo);
      pointer-events: none;
    }

    .ed-surface {
      background-color: var(--bg-surface);
      border: 1px solid var(--divider);
      border-radius: var(--radius-lg);
      transition: box-shadow 0.28s var(--ease-out-expo), border-color 0.2s ease;
    }
    .ed-surface:hover { box-shadow: var(--shadow-hover); }

    .ed-tint {
      background-color: var(--bg-tint);
      border-radius: var(--radius-md);
      transition: background-color 0.25s ease;
    }

    .pr-card {
      border-radius: var(--radius-lg);
      padding: 16px;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-out-expo);
    }
    .pr-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-hover);
    }
    .pr-card--accent {
      background-color: var(--accent-soft);
      border: 1px solid var(--accent-border);
    }
    .pr-card--sage {
      background-color: var(--sage-bg);
      border: 1px solid var(--sage-border);
    }
    .pr-card--amber {
      background-color: var(--amber-bg);
      border: 1px solid var(--amber-border);
    }
    .pr-card--rose {
      background-color: var(--rose-bg);
      border: 1px solid var(--rose-border);
    }

    .pr-cta {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px 14px;
      border-radius: var(--radius-md);
      font-size: 12px;
      font-weight: 800;
      transition: transform 0.2s var(--ease-spring), opacity 0.2s ease;
    }
    .pr-cta:hover { transform: translateY(-1px); opacity: 0.94; }
    .pr-cta:active { transform: scale(0.98); }

    .ed-divider-list > div + div {
      border-top: 1px solid var(--divider);
      padding-top: 12px;
      margin-top: 12px;
    }

    .status-inline { display: inline-flex; align-items: center; gap: 6px; font-size: 11px; font-weight: 700; }
    .status-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
    .status-inline--ok { color: var(--sage-text); }
    .status-inline--ok .status-dot { background-color: var(--sage-text); }
    .status-inline--warn { color: var(--amber-text); }
    .status-inline--warn .status-dot { background-color: var(--amber-text); }
    .status-inline--danger { color: var(--rose-text); }
    .status-inline--danger .status-dot { background-color: var(--rose-text); }

    .live-dot {
      width: 6px; height: 6px; border-radius: 50%; background-color: #10b981;
      animation: pulseLive 2.2s infinite ease-in-out;
    }

    .month-tile {
      padding: 8px 6px;
      border-radius: var(--radius-sm);
      background-color: var(--bg-surface);
      border: 1px solid var(--divider);
      text-align: center;
      cursor: pointer;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-out-expo), border-color 0.2s ease;
    }
    .month-tile:hover, .month-tile.is-selected {
      transform: translateY(-2px);
      box-shadow: var(--shadow-hover);
      border-color: var(--accent);
    }
    .month-tile:active { transform: scale(0.96); }
    .month-tile--best { background-color: var(--accent-soft); border-color: var(--accent-border); color: var(--accent-text); }
    .month-tile--quiet { background-color: var(--sage-bg); border-color: var(--sage-border); color: var(--sage-text); }
    .month-tile--caution { background-color: var(--amber-bg); border-color: var(--amber-border); color: var(--amber-text); }

    .accordion-trigger {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 6px 12px; border-radius: var(--radius-full);
      background-color: var(--bg-tint); color: var(--accent-text);
      font-size: 12px; font-weight: 700;
      transition: background-color 0.2s ease, transform 0.2s var(--ease-spring);
    }
    .accordion-trigger:hover { background-color: var(--bg-tint-hover); transform: translateY(-1px); }
    .accordion-trigger svg { transition: transform 0.35s var(--ease-out-expo); }
    .accordion-trigger[aria-expanded="true"] svg { transform: rotate(180deg); }

    .accordion-content {
      display: grid; grid-template-rows: 0fr;
      transition: grid-template-rows 0.4s var(--ease-out-expo);
    }
    .accordion-content.is-open { grid-template-rows: 1fr; }
    .accordion-inner { overflow: hidden; }

    .toast-msg {
      position: fixed; bottom: 24px; left: 50%;
      transform: translate(-50%, 24px) scale(0.92);
      opacity: 0; pointer-events: none; z-index: 60;
      display: inline-flex; align-items: center; gap: 8px;
      padding: 10px 18px; border-radius: var(--radius-full);
      background-color: var(--text-primary); color: var(--bg-canvas);
      font-size: 12px; font-weight: 700;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.22);
      transition: transform 0.4s var(--ease-spring), opacity 0.25s ease;
    }
    .toast-msg.is-shown { opacity: 1; transform: translate(-50%, 0) scale(1); }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
      .anim-enter, .reveal-section { opacity: 1 !important; transform: none !important; }
    }
  </style>"""


def render_pr_banner() -> str:
    return """<div style="background: var(--bg-tint); border-bottom: 1px solid var(--divider); text-align: center; padding: 4px 12px; font-size: 10px; color: var(--text-muted);">
    【PR】当サイトはアフィリエイト広告を利用しています
  </div>"""


def render_pixels() -> str:
    return "\n  ".join([
        f'<img border="0" width="1" height="1" src="{url}" alt="" style="display:none;">'
        for url in A8_PIXEL_URLS
    ])


def render_share_buttons(page_url: str, share_title: str) -> str:
    return f"""
    <div class="ed-surface p-3.5 flex flex-wrap items-center justify-between gap-2 reveal-section">
      <span class="text-xs font-bold" style="color: var(--text-primary);">このページの渡航情報を同行者に共有</span>
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
          class="ed-tint text-[11px] font-bold px-3 py-1.5 rounded-lg transition" style="color: var(--text-secondary); border: 1px solid var(--border-soft);">
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
          if (typeof showToast === 'function') showToast('ページのURLをコピーしました');
        });
      }
    }"""


def render_theme_and_toast_script() -> str:
    return """
    const rootEl = document.documentElement;
    const savedTheme = localStorage.getItem('tokou_theme') || 'light';
    rootEl.setAttribute('data-theme', savedTheme);
    const themeNameEl = document.getElementById('theme-name');
    if (themeNameEl) themeNameEl.textContent = savedTheme === 'dark' ? 'Dark' : 'Light';

    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const next = rootEl.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
        rootEl.setAttribute('data-theme', next);
        localStorage.setItem('tokou_theme', next);
        if (themeNameEl) themeNameEl.textContent = next === 'light' ? 'Light' : 'Dark';
      });
    }

    const toastEl = document.getElementById('toast');
    const toastTextEl = document.getElementById('toast-text');
    let toastTimer;
    function showToast(msg) {
      if (!toastEl || !toastTextEl) return;
      toastTextEl.textContent = msg;
      toastEl.classList.add('is-shown');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => toastEl.classList.remove('is-shown'), 2400);
    }

    function animateNumber(el, targetVal, decimals = 0, prefix = '', suffix = '') {
      if (!el) return;
      const startVal = parseFloat(el.dataset.val ?? el.textContent.replace(/[^\\d.-]/g, '')) || 0;
      el.dataset.val = targetVal;
      const duration = 260;
      const startTime = performance.now();
      function step(now) {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = startVal + (targetVal - startVal) * eased;
        el.textContent = prefix + (decimals > 0 ? current.toFixed(decimals) : Math.round(current).toLocaleString()) + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -20px 0px' });
    document.querySelectorAll('.reveal-section').forEach((sec) => revealObserver.observe(sec));
    setTimeout(() => {
      document.querySelectorAll('.reveal-section').forEach((sec) => sec.classList.add('is-visible'));
    }, 900);
    """


def render_sister_site_banner() -> str:
    return f"""
    <div class="ed-surface p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 reveal-section">
      <div>
        <span class="text-[10px] font-bold" style="color: var(--accent-text);">姉妹メディア · 長期滞在・留学・キャリア向け</span>
        <p class="text-xs sm:text-sm font-extrabold mt-0.5" style="color: var(--text-primary);">観光のその先へ：留学・ワーホリ・現地インターン情報【Atrium】</p>
        <p class="text-[11px] mt-0.5" style="color: var(--text-muted);">短期旅行は当サイト、中長期滞在や現地コミュニティ・奨学金・就活ニュースは姉妹メディア「Atrium」で役割を分けて発信しています。</p>
      </div>
      <a href="{SISTER_SITE_URL}/" target="_blank" rel="noopener" class="pr-cta shrink-0" style="background: var(--text-primary); color: var(--bg-canvas);">
        <span>Atriumを見る</span>
        <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
      </a>
    </div>"""


def render_countdown_calendar(city: dict) -> str:
    return f"""
    <section class="ed-surface p-3.5 space-y-2.5 reveal-section">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <div class="flex items-center gap-2">
          <i data-lucide="calendar" class="w-4 h-4" style="color: var(--accent-text);"></i>
          <span class="text-xs font-bold" style="color: var(--text-primary);">{city['name_ja']}への出発日:</span>
          <input id="trip-date-input" type="date" class="text-xs rounded-lg px-2.5 py-1 font-bold tabular-nums" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);">
        </div>
        <div id="trip-countdown-msg" class="text-xs font-bold tabular-nums" style="color: var(--accent-text);">出発日を入れると残り日数と準備ステップを表示</div>
      </div>
      <div id="trip-checklist" class="hidden grid grid-cols-1 sm:grid-cols-3 gap-2 pt-2 text-[11px]" style="border-top: 1px solid var(--divider);">
        <div id="step-early" class="p-2 rounded-lg" style="background: var(--bg-tint); color: var(--text-secondary);">
          <strong class="block" style="color: var(--text-primary);">〜2週間前</strong>
          パスポート残存・宿・ビザ要件の確認
        </div>
        <div id="step-mid" class="p-2 rounded-lg" style="background: var(--bg-tint); color: var(--text-secondary);">
          <strong class="block" style="color: var(--text-primary);">2週間〜3日前</strong>
          eSIM・海外保険・外務省「たびレジ」登録
        </div>
        <div id="step-final" class="p-2 rounded-lg" style="background: var(--bg-tint); color: var(--text-secondary);">
          <strong class="block" style="color: var(--text-primary);">出発前日〜当日</strong>
          {city['plug_type']}変換プラグ・配車アプリ・常備薬
        </div>
      </div>
    </section>"""


def compute_price_benchmarks(city: dict, jpy_to_local: float) -> dict:
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
    bench = compute_price_benchmarks(city, jpy_to_local)

    return f"""
    <section id="sec-budget" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="calculator" class="w-4 h-4"></i>
          <span>ざっくり物価目安 ＆ チップ・割り勘計算機</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">現地予算ツール</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs tabular-nums">
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">水（500ml・商店目安）</span>
          <strong class="text-sm font-extrabold block mt-0.5" style="color: var(--text-primary);">{bench['water']}</strong>
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">昼食（食堂・カジュアル店）</span>
          <strong class="text-sm font-extrabold block mt-0.5" style="color: var(--text-primary);">{bench['lunch']}</strong>
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">市内タクシー（短〜中距離目安）</span>
          <strong class="text-sm font-extrabold block mt-0.5" style="color: var(--text-primary);">{bench['taxi']}</strong>
        </div>
      </div>

      <div class="ed-tint p-4 space-y-3">
        <div class="flex items-center justify-between flex-wrap gap-2 text-[11px]">
          <span class="font-bold" style="color: var(--text-secondary);">会計割り勘・チップ計算</span>
          <label class="inline-flex items-center gap-1.5 cursor-pointer font-semibold" style="color: var(--accent-text);">
            <input id="bill-sc-included" type="checkbox" class="rounded">
            <span>伝票にサービス料(SC)込み（チップ0%にする）</span>
          </label>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
          <div>
            <label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">1. お会計金額（{code}）</label>
            <input id="bill-amount" type="number" value="100" class="w-full rounded-lg px-3 py-1.5 font-bold text-sm tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
          </div>
          <div>
            <label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">2. チップ率（目安: {city['tip_badge']}）</label>
            <select id="bill-tip" class="w-full rounded-lg px-2.5 py-2 font-bold text-xs tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
              <option value="0" {"selected" if default_tip == 0 else ""}>0%（チップ不要・SC込）</option>
              <option value="5">5%（端数・気持ち程度）</option>
              <option value="10" {"selected" if default_tip == 10 else ""}>10%（一般的な目安）</option>
              <option value="15">15%（標準サービス）</option>
              <option value="18" {"selected" if default_tip == 18 else ""}>18%（北米レストラン標準）</option>
              <option value="20">20%（良いサービス）</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">3. 割り勘する人数</label>
            <select id="bill-split" class="w-full rounded-lg px-2.5 py-2 font-bold text-xs tabular-nums" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
              <option value="1">1人（割り勘なし）</option>
              <option value="2" selected>2人で割り勘</option>
              <option value="3">3人で割り勘</option>
              <option value="4">4人で割り勘</option>
              <option value="5">5人で割り勘</option>
              <option value="6">6人で割り勘</option>
            </select>
          </div>
        </div>
        <div class="pt-2.5 flex flex-wrap items-baseline justify-between gap-2 text-xs tabular-nums" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">
          <div>
            <span>チップ込総額: <strong id="bill-total-local" style="color: var(--text-primary);">-- {code}</strong></span>
            <span class="text-[11px] ml-1" style="color: var(--text-muted);">（約 <span id="bill-total-jpy">--</span> 円）</span>
          </div>
          <div>
            <span>1人あたり: <strong id="bill-per-local" class="text-sm" style="color: var(--accent-text);">-- {code}</strong>（約 <span id="bill-per-jpy">--</span> 円）</span>
          </div>
        </div>
      </div>
    </section>"""


def compute_city_star_ratings(city: dict) -> dict:
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
    pct = int((score / 5.0) * 100)
    if score >= 4.2:
        bar_color, level_tag = "var(--sage-text)", "好適"
    elif score >= 3.5:
        bar_color, level_tag = "var(--accent)", "標準"
    else:
        bar_color, level_tag = "var(--amber-text)", "要注意"
    return f"""
      <div class="flex items-center justify-between gap-1 tabular-nums">
        <span class="font-extrabold text-sm" style="color: var(--text-primary);">{score:.1f} <span class="text-[11px] font-normal" style="color: var(--text-muted);">/ 5.0</span></span>
        <span class="text-[10px] font-bold" style="color: {bar_color};">{level_tag}</span>
      </div>
      <div class="w-full h-1.5 rounded-full overflow-hidden mt-1.5" style="background: var(--bg-tint);">
        <div class="h-full rounded-full" style="width: {pct}%; background: {bar_color};"></div>
      </div>
      <p class="text-[11px] mt-1.5" style="color: var(--text-muted);">{note}</p>"""


def render_city_rating_box(city: dict) -> str:
    r = compute_city_star_ratings(city)
    return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-2 pb-2" style="border-bottom: 1px solid var(--divider);">
        <div>
          <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>{city['name_ja']}の渡航しやすさ評価（5段階）</span>
          </h2>
          <p class="text-[11px] mt-0.5" style="color: var(--text-muted);">色分け基準：緑（4.2+ 好適） / 青（3.5〜4.1 標準） / 琥珀（〜3.4 事前対策推奨）</p>
        </div>
        <div class="text-xs font-extrabold tabular-nums" style="color: var(--accent-text);">総合 {r['avg']:.1f} / 5.0</div>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
        <div class="ed-surface p-3">
          <span class="text-[11px] font-semibold block mb-1" style="color: var(--text-muted);">治安・観光安心度</span>
          {render_star_bar(r['safety'], r['safety_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-semibold block mb-1" style="color: var(--text-muted);">キャッシュレス決済</span>
          {render_star_bar(r['cashless'], r['cashless_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-semibold block mb-1" style="color: var(--text-muted);">英語・案内通用度</span>
          {render_star_bar(r['english'], r['english_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-semibold block mb-1" style="color: var(--text-muted);">現地物価コスパ</span>
          {render_star_bar(r['cost'], r['cost_note'])}
        </div>
      </div>
    </section>"""


def render_annual_calendar_box(city: dict) -> str:
    region = city["region"]
    climate = city["climate"]
    slug = city["slug"]

    snow_cities = {
        "zurich", "geneva", "basel", "bern", "lucerne", "interlaken", "zermatt",
        "vienna", "salzburg", "innsbruck", "munich", "berlin", "hamburg", "frankfurt",
        "prague", "budapest", "warsaw", "krakow",
        "oslo", "stockholm", "helsinki", "copenhagen", "reykjavik", "tallinn", "riga", "vilnius",
        "new-york", "boston", "chicago", "washington-dc", "philadelphia",
        "toronto", "vancouver", "montreal", "calgary", "banff", "quebec-city",
        "seoul", "busan", "beijing", "harbin", "almaty", "astana", "tbilisi", "queenstown"
    }
    has_real_snow = slug in snow_cities
    cal_subtitle = "季節の魅力・穴場・雪目安" if has_real_snow else "乾季・雨季・穴場・気候目安"

    if slug in ("zurich", "geneva", "interlaken", "zermatt", "lucerne", "bern"):
        unique_season_note = "夏（6〜8月）はアルプスの緑と湖畔ハイキングが映え、冬（12〜2月）は雪山・スキーや冬の澄んだ景色が魅力です。"
    elif region == "オセアニア":
        unique_season_note = "南半球のため季節が逆転し、12〜2月は日照時間が長く夏本番のアクティビティに最適。6〜8月は落ち着いた気候で街歩きが楽しめます。"
    elif has_real_snow:
        unique_season_note = "春〜初夏や秋は街歩きや文化巡りに適し、冬（12〜2月）は雪景色・ウィンターシーズンや冬の街並みといった季節ならではの風景が楽しめます。"
    else:
        unique_season_note = "年間を通して降雪はなく、乾季や温暖な時期ほど青空・海・街歩きやローカルグルメの快適さが際立ちます。雨季や真夏はスコール・日差し対策を前提に組み立てるのがおすすめです。"

    month_cells = []
    for m in range(1, 13):
        if region == "オセアニア":
            if m in (11, 12, 1, 2):
                tag, cls = "好適・夏期", "month-tile--best"
                detail = f"{m}月：日照が長くアウトドアや街歩きに好適なシーズンです。"
            elif m in (5, 6, 8):
                tag, cls = "穴場・落ち着き", "month-tile--quiet"
                detail = f"{m}月：繁忙期を外して落ち着いた雰囲気で過ごしやすい時期です。"
            else:
                tag, cls = "散策向き", ""
                detail = f"{m}月：気温差に備えつつ街歩きやグルメを楽しめる時期です。"
        elif has_real_snow:
            if m in (5, 6, 9, 10):
                tag, cls = "快適ベスト", "month-tile--best"
                detail = f"{m}月：気候が安定し、街歩き・公園散策・観光に最も過ごしやすい時期です。"
            elif m in (12, 1, 2):
                tag, cls = "雪・冬景色", "month-tile--quiet"
                detail = f"{m}月：雪景色や冬の街並み・ウィンターシーズンを体感できる時期（防寒対策必須）。"
            elif m in (3, 4, 11):
                tag, cls = "穴場・変わり目", ""
                detail = f"{m}月：観光客が比較的落ち着き、季節の移り変わりを感じられる時期です。"
            else:
                tag, cls = "日照長め", "month-tile--caution"
                detail = f"{m}月：日没が遅く一日を長く使えますが、混雑や暑さ・天候変化に注意が必要です。"
        else:
            if m in (11, 12, 1, 2, 3):
                tag, cls = "快適・乾季目安", "month-tile--best"
                detail = f"{m}月：雨が少なく比較的過ごしやすい観光の狙い目シーズンです。"
            elif m in (5, 6, 9, 10):
                tag, cls = "穴場・空く時期", "month-tile--quiet"
                detail = f"{m}月：大型連休を外した比較的落ち着いた時期。旅費や人混みを抑えやすいです。"
            else:
                tag, cls = "雨・暑さ注意", "month-tile--caution"
                detail = f"{m}月：スコールや蒸し暑さ・台風/日差しに備え、屋内プランも交えると快適です。"

        month_cells.append(
            f'<button type="button" class="month-tile {cls}" data-month="{m}月" data-detail="{detail}">'
            f'<div class="text-xs font-extrabold">{m}月</div>'
            f'<div class="text-[11px] font-semibold mt-0.5">{tag}</div>'
            f'</button>'
        )

    return f"""
    <section id="sec-calendar" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="calendar-days" class="w-4 h-4"></i>
          <span>{city['name_ja']}の1年カレンダー（{cal_subtitle}）</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">月をタップで詳細</span>
      </div>

      <div class="grid grid-cols-3 sm:grid-cols-6 gap-1.5 tabular-nums">
        {''.join(month_cells)}
      </div>

      <div class="ed-tint p-3 text-xs space-y-1.5 leading-relaxed" style="color: var(--text-secondary);">
        <p id="calendar-month-detail"><strong style="color: var(--text-primary);">この街ならではの季節の見どころ：</strong>{unique_season_note}</p>
        <p class="text-[11px]" style="color: var(--text-muted);">{climate}</p>
      </div>
    </section>"""


def render_sightseeing_and_agency_box(city: dict) -> str:
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
            "title": f"{name}の展望スポット・公園／水辺エリア",
            "desc": "街全体の景色や夕景を楽しめる開放的なエリア。移動ルートに合わせて組み込むと旅程のメリハリがつきやすくなります。"
        }
    ]

    spot_cards = "".join([
        f'<div class="ed-surface p-3 space-y-1">'
        f'<div class="flex items-center justify-between gap-2">'
        f'<span class="text-[10px] font-bold" style="color: var(--accent-text);">定番スポット 0{idx + 1}</span>'
        f'<span class="text-[10px]" style="color: var(--text-muted);">{region}</span>'
        f'</div>'
        f'<p class="text-xs font-extrabold" style="color: var(--text-primary);">{sp["title"]}</p>'
        f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{sp["desc"]}</p>'
        f'</div>'
        for idx, sp in enumerate(spots)
    ])

    return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="map-pin" class="w-4 h-4"></i>
          <span>{name}の定番エリア目安 ＆ 宿・現地手配</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">軽量テキスト表示</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">{spot_cards}</div>

      {render_agoda_and_oooh_box(city)}
    </section>"""


def render_wise_and_epos_affiliate(city: dict) -> str:
    return f"""
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-3">
        <div class="pr-card pr-card--accent flex flex-col justify-between gap-3">
          <div class="space-y-1">
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--accent); color: #ffffff;">リアルレート両替 · {city['currency_code']}</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold pt-1" style="color: var(--text-primary);">{city['name_ja']}の決済・ATM引き出しに【Wise】</p>
            <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">
              マルチカレンシー口座＆デビットカードで外貨決済や現地ATM引き出しの手数料を抑えやすいのが魅力。<strong>両替コストや為替手数料をシビアに抑えたい人向け</strong>です（利用上限や手数料体系は申込前に公式をご確認ください）。
            </p>
          </div>
          <a href="{AFFILIATE_WISE_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: var(--accent); color: #ffffff;">
            <span>Wise公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card pr-card--amber flex flex-col justify-between gap-3">
          <div class="space-y-1">
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--amber-text); color: #ffffff;">年会費永年無料 · 海外旅行保険</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold pt-1" style="color: var(--text-primary);">{city['name_ja']}渡航の保険・防犯に【エポスカード】</p>
            <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">
              カード番号裏面記載＆タッチ決済対応で安心。<strong>※海外旅行傷害保険は「利用付帯」のため、空港までの交通費やツアー代金など対象費用を同カードで支払うこと</strong>が適用条件になります。
            </p>
          </div>
          <a href="{AFFILIATE_CARD_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: var(--amber-text); color: #ffffff;">
            <span>エポスカード詳細</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>"""


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
    elif city["region"] == "ヨーロッパ":
        taboo_rule = "教会や大聖堂に入る際は帽子を脱ぎ、肩や膝が露出する服装は避けてください。またスリ防犯のためズボンの後ろポケットに財布やスマホを入れず、テーブル上にスマホを置いたままにしないことが重要です。日曜日・祝日はスーパーや商業施設が休業・時短となる都市が多いため、買い出しは土曜までに済ませると安心です。"
    else:
        taboo_rule = "教会・寺院などの宗教施設に入る際は、肩や膝の露出を控えた服装が基本です。都市部の大型ショッピングモールは日曜も営業していますが、祝祭日やローカル個人店は休業・時短となる場合があります。また人混みや市場ではバッグを体の前に持ち、テーブル上にスマホを置いたままにしないよう注意してください。"

    return f"""
    <section id="sec-rules" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="book-open-check" class="w-4 h-4"></i>
          <span>{city['name_ja']}のお金・マナー・生活ルール詳細ガイド</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">現地実用辞典</span>
      </div>

      <div class="ed-surface p-4 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
        <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">チップの相場と渡し方（{city['tip_badge']}）</p>
          <p>{city['tip_detail']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">両替・カード決済・ATM（{city['currency_name']} / {curr}）</p>
          <p>{payment_rule}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">トイレ事情・衛生ルール</p>
          <p>{toilet_rule}</p>
        </div>
      </div>

      <div>
        <button id="rules-accordion-btn" type="button" class="accordion-trigger" aria-expanded="false" aria-controls="rules-accordion-panel">
          <span id="rules-accordion-label">その他のルールを開く（税金・変圧器・水道水・マナー・夏時間）</span>
          <i data-lucide="chevron-down" class="w-3.5 h-3.5"></i>
        </button>
        <div id="rules-accordion-panel" class="accordion-content">
          <div class="accordion-inner">
            <div class="ed-surface p-4 mt-2 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
              <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
                <p class="font-bold" style="color: var(--text-primary);">税金・免税手続き（Tax Free）</p>
                <p>{city['tax_note']}</p>
              </div>
              <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
                <p class="font-bold" style="color: var(--text-primary);">コンセント（{city['plug_type']}）・電圧（{city['voltage']}）</p>
                <p>{city['transformer_note']}</p>
              </div>
              <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
                <p class="font-bold" style="color: var(--text-primary);">水道水・氷・水注文</p>
                <p>{city['tap_water_note']}</p>
              </div>
              <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
                <p class="font-bold" style="color: var(--text-primary);">現地マナー・法律規制</p>
                <p>{taboo_rule}</p>
              </div>
              <div class="sm:grid sm:grid-cols-[200px_1fr] sm:gap-4 sm:items-baseline">
                <p class="font-bold" style="color: var(--text-primary);">サマータイム（夏時間）制度</p>
                <p>{city['dst_note']}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {render_wise_and_epos_affiliate(city)}
    </section>"""


def render_agoda_and_oooh_box(city: dict) -> str:
    return f"""
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div class="pr-card pr-card--accent flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--accent); color: #ffffff;">最大80%OFF · 宿泊予約</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold mt-2" style="color: var(--text-primary);">{city['name_ja']}のホテルをエリア別に探す【アゴダ】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              治安が安定した中心部や空港アクセス重視のホテルを格安比較。<strong>自分でエリアや口コミを見てサクッと予約したい人向け</strong>（税・サービス料込みの最終金額を予約前に確認してください）。
            </p>
          </div>
          <a href="{AFFILIATE_AGODA_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: var(--accent); color: #ffffff;">
            <span>アゴダで{city['name_ja']}の宿を見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card pr-card--sage flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--sage-text); color: #ffffff;">日本語チャット無料 · 現地手配</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold mt-2" style="color: var(--text-primary);">専用車・ツアーを現地プロに相談【Oooh】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              空港送迎や離島・郊外ツアーを現地旅行会社に日本語チャットで直接手配。<strong>初訪問・子連れ・移動の不安をプロに任せたい人向け</strong>です。
            </p>
          </div>
          <a href="{AFFILIATE_OOOH_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: var(--sage-text); color: #ffffff;">
            <span>無料で現地プロに相談する</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>"""


def render_telecom_box(city: dict) -> str:
    ui = city.get("special_ui", "standard")
    vpn_card_cls = "pr-card--rose" if ui == "china_vpn" else "pr-card--accent"
    vpn_btn_bg = "var(--rose-text)" if ui == "china_vpn" else "var(--text-primary)"
    vpn_btn_color = "#ffffff" if ui == "china_vpn" else "var(--bg-canvas)"
    vpn_badge = "中国渡航は事前準備必須" if ui == "china_vpn" else "フリーWi-Fi暗号化・30日返金保証"

    return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="wifi" class="w-4 h-4"></i>
          <span>現地のネット通信（eSIM）＆ Wi-Fi保護（VPN）</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">PR / 出発前準備</span>
      </div>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">{city['telecom_note']}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div class="pr-card pr-card--accent flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--accent); color: #ffffff;">最短3分・QRで即開通</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold mt-2" style="color: var(--text-primary);">世界125以上の国・地域対応【Cross eSIM】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              SIM差し替え・空港受取不要で到着直後から通信可能。<strong>事前に端末がeSIM対応＆SIMフリーかだけ確認</strong>して購入するとスムーズです。
            </p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: var(--accent); color: #ffffff;">
            <span>Cross eSIM公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card {vpn_card_cls} flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: {vpn_btn_bg}; color: {vpn_btn_color};">{vpn_badge}</span>
              <span class="text-[10px] font-bold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-extrabold mt-2" style="color: var(--text-primary);">海外Wi-Fi保護＆制限回避【NordVPN】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              空港・カフェ・ホテルの無料Wi-Fiでのカード入力やネット銀行操作を暗号化。海外から日本の動画サービスを見たい人にも向いています。
            </p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow noopener" class="pr-cta w-full" style="background: {vpn_btn_bg}; color: {vpn_btn_color};">
            <span>NordVPN公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>
    </section>"""


def render_city_comparison_section(city: dict, all_cities: list, city_compare_links: list) -> str:
    same_region = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:3]
    if not same_region:
        same_region = [c for c in all_cities if c["slug"] != city["slug"]][:3]

    rows = ""
    for c in [city] + same_region:
        is_self = (c["slug"] == city["slug"])
        name_cell = f"<strong>{c['name_ja']}（当ページ）</strong>" if is_self else f'<a href="../{c["slug"]}/" class="underline font-bold" style="color: var(--accent-text);">{c["name_ja"]}</a>'
        rows += f"""
          <tr>
            <td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-primary);">{name_cell}</td>
            <td class="p-2.5 tabular-nums" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c['plug_type']} / {c['voltage']}</td>
            <td class="p-2.5 tabular-nums" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c['currency_code']}</td>
            <td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c['tip_badge'].split('（')[0]}</td>
          </tr>"""

    comp_buttons = "".join([
        f'<a href="../compare/{pair_slug}/" class="text-xs font-bold px-3 py-2 rounded-full transition inline-flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">'
        f'<span>{label} 徹底比較</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>'
        f'</a>'
        for pair_slug, label in city_compare_links
    ])

    return f"""
    <section id="sec-compare" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="scale" class="w-4 h-4"></i>
          <span>{city['name_ja']}と周辺・人気都市のスペック比較</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">周遊や候補選びに</span>
      </div>
      <div class="ed-surface overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr style="background: var(--bg-tint); color: var(--text-muted);">
              <th class="p-2.5 font-semibold">都市名</th>
              <th class="p-2.5 font-semibold">プラグ / 電圧</th>
              <th class="p-2.5 font-semibold">通貨</th>
              <th class="p-2.5 font-semibold">チップ</th>
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
        f'<a href="../{c["slug"]}/" class="text-xs px-3 py-1.5 rounded-full transition" style="background: var(--bg-surface); border: 1px solid var(--divider); color: var(--text-secondary);">{c["name_ja"]}</a>'
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
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url)}
  {render_editorial_styles()}
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <link rel="canonical" href="{page_url}">
  <link rel="manifest" href="../manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="pb-14">
  {render_pr_banner()}
  <header class="ed-header">
    <div id="scroll-progress" class="scroll-progress"></div>
    <div class="max-w-[780px] mx-auto px-4 pt-2.5">
      <div class="flex items-center justify-between gap-2 pb-2">
        <a href="../" class="font-bold text-xs flex items-center gap-1.5 transition" style="color: var(--text-primary);">
          <img src="{FAVICON_URL}" alt="" width="18" height="18" class="w-4.5 h-4.5 rounded object-cover shrink-0" onerror="this.style.display='none'">
          <span>{SITE_NAME}</span>
          <span class="font-normal" style="color: var(--text-muted);">/ {city['region']}・{city['country_ja']}</span>
        </a>
        <button id="theme-toggle" type="button" class="text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1 transition" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
          <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
          <span id="theme-name">Light</span>
        </button>
      </div>
      <nav id="toc-nav" class="toc-nav" aria-label="ページ内クイック移動">
        <a href="#sec-top" class="toc-link is-active">基本スペック</a>
        <a href="#sec-calendar" class="toc-link">1年カレンダー</a>
        <a href="#sec-rules" class="toc-link">お金・生活ルール</a>
        <a href="#sec-budget" class="toc-link">物価・割り勘</a>
        <a href="#sec-safety" class="toc-link">治安・大使館</a>
        <a href="#sec-compare" class="toc-link">他都市比較</a>
        <div id="toc-glider" class="toc-glider"></div>
      </nav>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-9">
    <section id="sec-top" class="space-y-3">
      <div class="anim-enter">
        <div class="flex items-center justify-between flex-wrap gap-1 text-[11px]" style="color: var(--text-muted);">
          <span>{city['country_ja']} · {city['region']}</span>
          <span class="tabular-nums">為替更新: {rates_data['updated_at']}</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight mt-0.5">
          {city['name_ja']}<span class="font-editorial-italic text-base font-normal ml-2.5" style="color: var(--text-muted);">{city['name_en']}</span>
        </h1>
      </div>

      <div class="ed-tint p-3.5 space-y-1.5 anim-enter delay-1">
        <div class="flex items-center justify-between gap-2 flex-wrap">
          <div class="flex items-center gap-2 flex-wrap">
            <i id="weather-icon" data-lucide="cloud-sun" class="w-4 h-4" style="color: var(--accent-text);"></i>
            <span class="text-xs font-semibold" style="color: var(--text-muted);">現在の現地気温・天気:</span>
            <span id="weather-temp" class="text-sm font-extrabold tabular-nums" style="color: var(--text-primary);">取得中...</span>
          </div>
          <span id="weather-meta" class="text-[10px] font-bold flex items-center gap-1.5 tabular-nums" style="color: var(--text-muted);"><span class="live-dot"></span>LIVE · Open-Meteo</span>
        </div>
        <p id="weather-outfit" class="text-xs leading-relaxed" style="color: var(--text-secondary);">現地の気象データから服装の目安を計算しています...</p>
        <p class="text-[11px] leading-relaxed pt-1" style="color: var(--text-muted); border-top: 1px solid var(--divider);">{city['climate']}</p>
      </div>

      <div class="ed-surface grid grid-cols-2 sm:grid-cols-4 overflow-hidden anim-enter delay-2">
        <div class="p-3.5 flex flex-col justify-between gap-1.5" style="border-bottom: 1px solid var(--divider); border-right: 1px solid var(--divider);">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-medium flex items-center gap-1" style="color: var(--text-muted);"><i data-lucide="clock" class="w-3.5 h-3.5"></i>現地時刻</span>
            <button id="tz-toggle" type="button" class="text-[10px] px-1.5 py-0.5 rounded font-semibold" style="background: var(--bg-tint); color: var(--text-secondary);">vs 日本</button>
          </div>
          <div id="local-clock" class="text-xl font-mono font-extrabold tracking-tight tabular-nums">--:--:--</div>
          <div id="time-diff" class="text-[11px] font-bold tabular-nums" style="color: var(--accent-text);">時差を計算中...</div>
        </div>

        <div class="p-3.5 flex flex-col justify-between gap-1.5 sm:border-b-0" style="border-bottom: 1px solid var(--divider);">
          <span class="text-[11px] font-medium flex items-center gap-1" style="color: var(--text-muted);"><i data-lucide="plug" class="w-3.5 h-3.5"></i>プラグ・電圧</span>
          <div class="flex items-center gap-2">
            <span style="color: var(--text-primary);">{render_plug_svg(city['plug_type'])}</span>
            <div>
              <div class="text-sm font-extrabold tabular-nums">{city['plug_type']} / {city['voltage']}</div>
              <div class="status-inline status-inline--ok"><span class="status-dot"></span>{'変圧器要' if city['transformer_needed'] else 'スマホ変圧器不要'}</div>
            </div>
          </div>
        </div>

        <div class="p-3.5 flex flex-col justify-between gap-1.5" style="border-right: 1px solid var(--divider);">
          <span class="text-[11px] font-medium flex items-center gap-1" style="color: var(--text-muted);"><i data-lucide="coins" class="w-3.5 h-3.5"></i>チップ習慣</span>
          <div>
            <span class="status-inline {tip_color_class(city['tip_level'])}">
              <span class="status-dot"></span>{city['tip_badge']}
            </span>
          </div>
          <div class="text-[11px]" style="color: var(--text-muted);">水道水: {'飲用可' if city['tap_water_safe'] else '飲用不可（市販水推奨）'}</div>
        </div>

        <div class="p-3.5 flex flex-col justify-between gap-1.5">
          <span class="text-[11px] font-medium flex items-center gap-1 tabular-nums" style="color: var(--text-muted);"><i data-lucide="arrow-left-right" class="w-3.5 h-3.5"></i>1{code} ≒ {local_to_jpy}円</span>
          <div class="flex items-center gap-1.5">
            <input id="jpy-input" type="number" value="1000" class="w-20 rounded-md px-2 py-1 text-xs font-extrabold tabular-nums" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);">
            <span class="text-[11px]" style="color: var(--text-muted);">円</span>
          </div>
          <div id="local-output" class="text-xs font-extrabold tabular-nums" style="color: var(--sage-text);">≒ {thousand_jpy_in_local} {code}</div>
        </div>
      </div>
    </section>

    {render_countdown_calendar(city)}

    {render_city_rating_box(city)}

    {render_annual_calendar_box(city)}

    {render_detailed_rules_and_manners(city)}

    {render_tip_split_calculator(city, jpy_to_local, local_to_jpy)}

    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="plane" class="w-4 h-4"></i>
          <span>{city['airport_access']['airport_name']}から市内への移動</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">空港アクセス</span>
      </div>
      <div class="ed-surface p-4 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
        <div class="sm:grid sm:grid-cols-[120px_1fr] sm:gap-3 sm:items-baseline">
          <span class="font-bold" style="color: var(--accent-text);">最速・快適</span>
          <p>{city['airport_access']['fastest']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[120px_1fr] sm:gap-3 sm:items-baseline">
          <span class="font-bold" style="color: var(--sage-text);">最安・定番</span>
          <p>{city['airport_access']['cheapest']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[120px_1fr] sm:gap-3 sm:items-baseline">
          <span class="font-bold" style="color: var(--text-primary);">配車・移動アプリ</span>
          <p>{', '.join(city['transport_apps'])}</p>
        </div>
      </div>
    </section>

    {render_sightseeing_and_agency_box(city)}

    {render_telecom_box(city)}

    <section id="sec-safety" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-2 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-extrabold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="shield-alert" class="w-4 h-4"></i>
          <span>安全・危険情報・日本大使館連絡先</span>
        </h2>
        <span class="status-inline status-inline--danger tabular-nums"><span class="status-dot"></span>緊急通報: {city['emergency_numbers']}</span>
      </div>

      <div class="ed-surface p-4 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">外務省 危険情報目安</p>
          <p><strong style="color: var(--text-primary);">{city['danger_level']}</strong> — <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="underline" style="color: var(--accent-text);">外務省公式ページを見る</a></p>
        </div>
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">現地の治安・注意点</p>
          <p>{city['safety_note']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">日本大使館・総領事館</p>
          <div class="flex flex-wrap items-center gap-2">
            <span>{city['embassy']}</span>
            <button type="button" onclick="copyEmbassyInfo()" class="text-[11px] font-bold px-2.5 py-1 rounded-full inline-flex items-center gap-1 transition" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);">
              <i data-lucide="copy" class="w-3 h-3"></i>
              <span>公館情報をコピー</span>
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="pr-cta" style="background: var(--text-primary); color: var(--bg-canvas);">
          <span>外務省「{city['country_ja']}」安全情報</span>
          <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
        </a>
        <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="pr-cta" style="background: var(--sage-text); color: #ffffff;">
          <span>外務省「たびレジ」に登録する（無料）</span>
          <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </section>

    {render_city_comparison_section(city, all_cities, city_compare_links)}

    {render_share_buttons(page_url, page_title)}

    {render_sister_site_banner()}

    <section class="pt-1 reveal-section">
      <h3 class="text-xs font-bold mb-2" style="color: var(--text-muted);">{city['region']}の他の都市をチェック</h3>
      <div class="flex flex-wrap gap-1.5">{related_html}</div>
    </section>

    <footer class="pt-6 pb-4 text-center text-[11px] space-y-1.5" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>※本ページはプロモーション（アフィリエイト広告）が含まれています。渡航前に必ず外務省・各国大使館の最新公式情報をご確認ください。</p>
      <p><a href="../policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a></p>
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

    const citySlug = "{city['slug']}";
    const targetTz = "{city['timezone']}";
    const cityNameEn = "{city['name_en']}";
    const embassyRawText = {json.dumps(f"{city['name_ja']} 日本大使館・総領事館: {city['embassy']} / 緊急通報: {city['emergency_numbers']}", ensure_ascii=False)};
    let compareWithLocal = false;

    function copyEmbassyInfo() {{
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(embassyRawText).then(() => showToast('大使館・緊急連絡先をコピーしました'));
      }}
    }}

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
    localOutput.dataset.val = (1000 * rate).toFixed(2);
    jpyInput.addEventListener('input', () => {{
      const val = parseFloat(jpyInput.value) || 0;
      animateNumber(localOutput, val * rate, 2, '≒ ', ' {code}');
    }});

    const billAmount = document.getElementById('bill-amount');
    const billTip = document.getElementById('bill-tip');
    const billSplit = document.getElementById('bill-split');
    const billScCheck = document.getElementById('bill-sc-included');
    const outTotalLocal = document.getElementById('bill-total-local');
    const outTotalJpy = document.getElementById('bill-total-jpy');
    const outPerLocal = document.getElementById('bill-per-local');
    const outPerJpy = document.getElementById('bill-per-jpy');
    let prevTipVal = billTip.value;

    billScCheck.addEventListener('change', () => {{
      if (billScCheck.checked) {{
        prevTipVal = billTip.value;
        billTip.value = '0';
      }} else {{
        billTip.value = prevTipVal;
      }}
      updateBillCalc(false);
    }});

    function updateBillCalc(instant = false) {{
      const amt = parseFloat(billAmount.value) || 0;
      const tipPct = parseFloat(billTip.value) || 0;
      const split = parseInt(billSplit.value, 10) || 1;
      const totalLocal = amt * (1 + tipPct / 100);
      const totalJpy = Math.round(totalLocal * localToJpy);
      const perLocal = totalLocal / split;
      const perJpy = Math.round(totalJpy / split);

      if (instant) {{
        outTotalLocal.textContent = `${{totalLocal.toFixed(1)}} {code}`;
        outTotalJpy.textContent = totalJpy.toLocaleString();
        outPerLocal.textContent = `${{perLocal.toFixed(1)}} {code}`;
        outPerJpy.textContent = perJpy.toLocaleString();
        outTotalLocal.dataset.val = totalLocal.toFixed(1);
        outTotalJpy.dataset.val = String(totalJpy);
        outPerLocal.dataset.val = perLocal.toFixed(1);
        outPerJpy.dataset.val = String(perJpy);
      }} else {{
        animateNumber(outTotalLocal, totalLocal, 1, '', ` ${{code}}`);
        animateNumber(outTotalJpy, totalJpy, 0);
        animateNumber(outPerLocal, perLocal, 1, '', ` ${{code}}`);
        animateNumber(outPerJpy, perJpy, 0);
      }}
    }}
    [billAmount, billTip, billSplit].forEach(el => el.addEventListener('input', () => {{
      if (el === billTip && billTip.value !== '0') billScCheck.checked = false;
      updateBillCalc(false);
    }}));
    updateBillCalc(true);

    const dateInput = document.getElementById('trip-date-input');
    const countdownMsg = document.getElementById('trip-countdown-msg');
    const checklistBox = document.getElementById('trip-checklist');
    const stepEarly = document.getElementById('step-early');
    const stepMid = document.getElementById('step-mid');
    const stepFinal = document.getElementById('step-final');
    const savedDate = localStorage.getItem('trip_date_' + citySlug) || localStorage.getItem('trip_date_global');
    if (savedDate) dateInput.value = savedDate;

    function highlightStep(activeEl) {{
      [stepEarly, stepMid, stepFinal].forEach((el) => {{
        if (!el) return;
        el.style.background = 'var(--bg-tint)';
        el.style.border = '1px solid transparent';
      }});
      if (activeEl) {{
        activeEl.style.background = 'var(--accent-soft)';
        activeEl.style.border = '1px solid var(--accent-border)';
      }}
    }}

    function updateCountdown() {{
      if (!dateInput.value) return;
      localStorage.setItem('trip_date_' + citySlug, dateInput.value);
      localStorage.setItem('trip_date_global', dateInput.value);
      const today = new Date();
      today.setHours(0,0,0,0);
      const target = new Date(dateInput.value + 'T00:00:00');
      const diffDays = Math.round((target - today) / 86400000);
      checklistBox.classList.remove('hidden');

      if (diffDays > 14) {{
        countdownMsg.textContent = `出発まであと${{diffDays}}日（宿・パスポート確認期）`;
        highlightStep(stepEarly);
      }} else if (diffDays >= 3) {{
        countdownMsg.textContent = `出発まであと${{diffDays}}日（eSIM・保険・たびレジ登録期）`;
        highlightStep(stepMid);
      }} else if (diffDays >= 0) {{
        countdownMsg.textContent = diffDays === 0 ? '本日出発日です。安全なご渡航を！' : `出発まであと${{diffDays}}日（最終持ち物チェック期）`;
        highlightStep(stepFinal);
      }} else {{
        countdownMsg.textContent = `現地滞在中の時刻・為替・割り勘確認にご活用ください。`;
        highlightStep(null);
      }}
    }}
    dateInput.addEventListener('change', updateCountdown);
    updateCountdown();

    document.querySelectorAll('.month-tile').forEach((tile) => {{
      tile.addEventListener('click', () => {{
        document.querySelectorAll('.month-tile').forEach((t) => t.classList.remove('is-selected'));
        tile.classList.add('is-selected');
        const detail = tile.getAttribute('data-detail');
        document.getElementById('calendar-month-detail').innerHTML = `<strong style="color: var(--text-primary);">${{tile.getAttribute('data-month')}}の目安：</strong>${{detail.replace(/^[^：]+：/, '')}}`;
      }});
    }});

    const rulesAccBtn = document.getElementById('rules-accordion-btn');
    const rulesAccLabel = document.getElementById('rules-accordion-label');
    const rulesAccPanel = document.getElementById('rules-accordion-panel');
    if (rulesAccBtn && rulesAccPanel) {{
      rulesAccBtn.addEventListener('click', () => {{
        const expanded = rulesAccBtn.getAttribute('aria-expanded') === 'true';
        rulesAccBtn.setAttribute('aria-expanded', String(!expanded));
        rulesAccPanel.classList.toggle('is-open', !expanded);
        rulesAccLabel.textContent = !expanded
          ? 'その他のルールを閉じる'
          : 'その他のルールを開く（税金・変圧器・水道水・マナー・夏時間）';
      }});
    }}

    const progressBar = document.getElementById('scroll-progress');
    const tocNav = document.getElementById('toc-nav');
    const tocLinks = Array.from(document.querySelectorAll('#toc-nav .toc-link'));
    const tocGlider = document.getElementById('toc-glider');
    const tocSections = tocLinks.map((l) => document.querySelector(l.getAttribute('href'))).filter(Boolean);

    function moveGlider(activeLink) {{
      if (!activeLink || !tocGlider) return;
      tocGlider.style.width = `${{activeLink.offsetWidth}}px`;
      tocGlider.style.transform = `translateX(${{activeLink.offsetLeft}}px)`;
    }}
    window.addEventListener('resize', () => moveGlider(tocNav?.querySelector('.toc-link.is-active')));
    moveGlider(tocLinks[0]);

    window.addEventListener('scroll', () => {{
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (progressBar && docHeight > 0) {{
        progressBar.style.width = `${{Math.min((window.scrollY / docHeight) * 100, 100)}}%`;
      }}
      const scrollPos = window.scrollY + 140;
      let currentId = tocSections[0]?.id;
      for (const sec of tocSections) {{
        if (sec.offsetTop <= scrollPos) currentId = sec.id;
      }}
      tocLinks.forEach((link) => {{
        const isCurrent = link.getAttribute('href') === `#${{currentId}}`;
        if (isCurrent && !link.classList.contains('is-active')) {{
          link.classList.add('is-active');
          moveGlider(link);
        }} else if (!isCurrent) {{
          link.classList.remove('is-active');
        }}
      }});
    }}, {{ passive: true }});

    function setWeatherLucideIcon(iconName) {{
      const iconEl = document.getElementById('weather-icon');
      if (!iconEl) return;
      iconEl.outerHTML = `<i id="weather-icon" data-lucide="${{iconName}}" class="w-4 h-4" style="color: var(--accent-text);"></i>`;
      if (window.lucide) lucide.createIcons();
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
        const wCode = wData.current.weather_code;
        const obsTime = (wData.current.time || '').split('T')[1] || '';

        let desc = '晴れ';
        let lucideIcon = 'sun';
        if (wCode === 0) {{ desc = '快晴・晴れ'; lucideIcon = 'sun'; }}
        else if (wCode >= 1 && wCode <= 2) {{ desc = '晴れ時々曇り'; lucideIcon = 'cloud-sun'; }}
        else if (wCode === 3) {{ desc = '曇り'; lucideIcon = 'cloud'; }}
        else if (wCode >= 45 && wCode <= 48) {{ desc = '霧'; lucideIcon = 'cloud-fog'; }}
        else if ((wCode >= 51 && wCode <= 67) || (wCode >= 80 && wCode <= 82)) {{ desc = wCode >= 80 ? 'にわか雨' : '雨'; lucideIcon = 'cloud-rain'; }}
        else if (wCode >= 71 && wCode <= 77) {{ desc = '雪'; lucideIcon = 'snowflake'; }}
        else if (wCode >= 95) {{ desc = '雷雨'; lucideIcon = 'cloud-lightning'; }}

        setWeatherLucideIcon(lucideIcon);

        let outfit = '';
        if (temp >= 28) outfit = '服装目安：半袖・薄手の服（屋内冷房対策に薄手の羽織りを1枚）';
        else if (temp >= 22) outfit = '服装目安：半袖または薄手の長袖シャツが快適';
        else if (temp >= 16) outfit = '服装目安：長袖＋カーディガンやジャケットなど羽織りもの必須';
        else if (temp >= 10) outfit = '服装目安：コートやジャケット・ニットが必要';
        else outfit = '服装目安：冬物コート・ダウンなど防寒対策が必須';

        const dryNote = humidity <= 40 ? '（乾燥注意）' : (humidity >= 80 ? '（高湿度）' : '');

        document.getElementById('weather-temp').textContent = `${{temp}}℃（${{desc}} / 湿度${{humidity}}%${{dryNote}}）`;
        document.getElementById('weather-outfit').textContent = outfit;
        if (obsTime) {{
          document.getElementById('weather-meta').innerHTML = `<span class="live-dot"></span>現地 ${{obsTime}}観測 · Open-Meteo`;
        }}
      }} catch (e) {{
        setWeatherLucideIcon('cloud-sun');
        document.getElementById('weather-temp').textContent = '下の年間気候目安をご参照ください';
        document.getElementById('weather-outfit').textContent = '渡航前に気象アプリ等で最新気温をご確認ください';
      }}
    }}
    fetchWeather();
  </script>
</body>
</html>"""


def build_compare_html(c1: dict, c2: dict, summary_text: str, rates_data: dict, all_cities: list) -> str:
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
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(title, desc, page_url)}
  {render_editorial_styles()}
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="pb-14">
  {render_pr_banner()}
  <header class="ed-header">
    <div class="max-w-[780px] mx-auto px-4 py-3 flex items-center justify-between gap-2">
      <a href="../../" class="font-bold text-xs flex items-center gap-1.5" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        <span>{SITE_NAME}（トップへ戻る）</span>
      </a>
      <button id="theme-toggle" type="button" class="text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-6">
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-extrabold uppercase tracking-wider" style="color: var(--accent-text);">2 CITY COMPARISON · {len(all_cities)}×{len(all_cities)}対応</span>
      <h1 id="comp-h1" class="text-xl sm:text-2xl font-extrabold">{c1['name_ja']} vs {c2['name_ja']} 現地情報・渡航スペック比較</h1>
      <p id="comp-summary" class="text-xs leading-relaxed" style="color: var(--text-secondary);">{summary_text}</p>
    </div>

    <section class="ed-tint p-4 space-y-2.5 anim-enter delay-1">
      <p class="text-xs font-extrabold" style="color: var(--text-primary);">全{len(all_cities)}都市から好きな2都市を選んでその場で比較</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
        <div>
          <label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">比較する都市 A</label>
          <select id="sel-city-1" class="w-full rounded-lg px-3 py-2 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{options_1}</select>
        </div>
        <div>
          <label class="block text-[11px] font-semibold mb-1" style="color: var(--text-muted);">比較する都市 B</label>
          <select id="sel-city-2" class="w-full rounded-lg px-3 py-2 font-bold" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{options_2}</select>
        </div>
      </div>
    </section>

    <div class="ed-surface overflow-x-auto anim-enter delay-2">
      <table class="w-full text-left border-collapse text-xs">
        <thead>
          <tr style="background: var(--bg-tint); color: var(--text-primary);">
            <th class="p-3 w-1/4 font-bold">比較項目</th>
            <th id="th-c1" class="p-3 w-[37.5%] font-bold" style="border-left: 1px solid var(--divider);"><a href="../../{c1['slug']}/" class="underline" style="color: var(--accent-text);">{c1['name_ja']}（{c1['country_ja']}）</a></th>
            <th id="th-c2" class="p-3 w-[37.5%] font-bold" style="border-left: 1px solid var(--divider);"><a href="../../{c2['slug']}/" class="underline" style="color: var(--accent-text);">{c2['name_ja']}（{c2['country_ja']}）</a></th>
          </tr>
        </thead>
        <tbody class="tabular-nums" style="color: var(--text-secondary);">
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">総合評価</th>
            <td id="td-star-1" class="p-3 font-extrabold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider); color: var(--accent-text);">{s1['avg']:.1f} / 5.0</td>
            <td id="td-star-2" class="p-3 font-extrabold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider); color: var(--accent-text);">{s2['avg']:.1f} / 5.0</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">コンセント・電圧</th>
            <td id="td-plug-1" class="p-3 font-bold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider); color: var(--text-primary);">{c1['plug_type']}タイプ（{c1['voltage']} / {c1['frequency']}）</td>
            <td id="td-plug-2" class="p-3 font-bold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider); color: var(--text-primary);">{c2['plug_type']}タイプ（{c2['voltage']} / {c2['frequency']}）</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">チップ習慣</th>
            <td id="td-tip-1" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);"><strong>{c1['tip_badge']}</strong><br><span class="text-[11px]" style="color: var(--text-muted);">{c1['tip_detail']}</span></td>
            <td id="td-tip-2" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);"><strong>{c2['tip_badge']}</strong><br><span class="text-[11px]" style="color: var(--text-muted);">{c2['tip_detail']}</span></td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">通貨・為替目安</th>
            <td id="td-curr-1" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c1['currency_name']}（1{c1['currency_code']} ≒ {jpy1}円）</td>
            <td id="td-curr-2" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c2['currency_name']}（1{c2['currency_code']} ≒ {jpy2}円）</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">水道水</th>
            <td id="td-water-1" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{'飲用可' if c1['tap_water_safe'] else '飲用不可（市販水推奨）'}</td>
            <td id="td-water-2" class="p-3" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{'飲用可' if c2['tap_water_safe'] else '飲用不可（市販水推奨）'}</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">気候・季節感</th>
            <td id="td-clim-1" class="p-3 text-[11px]" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c1['climate']}</td>
            <td id="td-clim-2" class="p-3 text-[11px]" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c2['climate']}</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">空港アクセス</th>
            <td id="td-air-1" class="p-3 text-[11px]" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c1['airport_access']['fastest']}</td>
            <td id="td-air-2" class="p-3 text-[11px]" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c2['airport_access']['fastest']}</td>
          </tr>
          <tr>
            <th class="p-3 font-semibold" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">外務省危険情報</th>
            <td id="td-dan-1" class="p-3 text-[11px] font-bold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c1['danger_level']}</td>
            <td id="td-dan-2" class="p-3 text-[11px] font-bold" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{c2['danger_level']}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 reveal-section">
      <a id="btn-c1" href="../../{c1['slug']}/" class="pr-cta" style="background: var(--accent); color: #ffffff;">{c1['name_ja']}の生活ルール・詳細ページへ →</a>
      <a id="btn-c2" href="../../{c2['slug']}/" class="pr-cta" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{c2['name_ja']}の生活ルール・詳細ページへ →</a>
    </div>

    {render_sightseeing_and_agency_box(c1)}
    {render_telecom_box(c1)}
    {render_share_buttons(page_url, title)}
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
      document.getElementById('th-c1').innerHTML = `<a href="../../${{a.slug}}/" class="underline" style="color: var(--accent-text);">${{a.name_ja}}（${{a.country_ja}}）</a>`;
      document.getElementById('th-c2').innerHTML = `<a href="../../${{b.slug}}/" class="underline" style="color: var(--accent-text);">${{b.name_ja}}（${{b.country_ja}}）</a>`;
      document.getElementById('td-star-1').textContent = `${{a.avg_star.toFixed(1)}} / 5.0`;
      document.getElementById('td-star-2').textContent = `${{b.avg_star.toFixed(1)}} / 5.0`;
      document.getElementById('td-plug-1').textContent = `${{a.plug_type}}タイプ（${{a.voltage}} / ${{a.frequency}}）`;
      document.getElementById('td-plug-2').textContent = `${{b.plug_type}}タイプ（${{b.voltage}} / ${{b.frequency}}）`;
      document.getElementById('td-tip-1').innerHTML = `<strong>${{a.tip_badge}}</strong><br><span class="text-[11px]" style="color: var(--text-muted);">${{a.tip_detail}}</span>`;
      document.getElementById('td-tip-2').innerHTML = `<strong>${{b.tip_badge}}</strong><br><span class="text-[11px]" style="color: var(--text-muted);">${{b.tip_detail}}</span>`;
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
            f'<a href="../../{c["slug"]}/" class="ed-surface block p-4 space-y-1.5">'
            f'<div class="flex items-center justify-between">'
            f'<span class="font-extrabold text-sm" style="color: var(--text-primary);">{c["name_ja"]}</span>'
            f'<span class="text-[11px] font-bold tabular-nums" style="color: var(--accent-text);">{r["avg"]:.1f} / 5.0 <span class="text-[10px] font-normal ml-1" style="color: var(--text-muted);">{c["country_ja"]}</span></span>'
            f'</div>'
            f'<p class="text-[11px] line-clamp-2" style="color: var(--text-secondary);">{c["climate"]}</p>'
            f'<div class="text-[11px] flex flex-wrap gap-2 pt-1 tabular-nums" style="color: var(--text-muted);">'
            f'<span>プラグ: {c["plug_type"]}</span><span>チップ: {c["tip_badge"].split("（")[0]}</span><span>通貨: {c["currency_code"]}</span>'
            f'</div>'
            f'</a>'
        )

    return f"""<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, feat['desc'], page_url)}
  {render_editorial_styles()}
  <title>{page_title}</title>
  <meta name="description" content="{feat['desc']}">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="pb-14">
  {render_pr_banner()}
  <header class="ed-header">
    <div class="max-w-[780px] mx-auto px-4 py-3 flex items-center justify-between gap-2">
      <a href="../../" class="font-bold text-xs flex items-center gap-1.5" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        <span>{SITE_NAME}（全150都市一覧へ）</span>
      </a>
      <button id="theme-toggle" type="button" class="text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-5 space-y-6">
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-extrabold uppercase tracking-wider" style="color: var(--accent-text);">{feat['badge']}</span>
      <h1 class="text-xl sm:text-2xl font-extrabold">{feat['title']}</h1>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">{feat['desc']}</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">{cards}</div>

    {render_sightseeing_and_agency_box(selected[0])}
    {render_telecom_box(selected[0])}
    {render_share_buttons(page_url, feat['title'])}
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
</body>
</html>"""


def build_policy_html() -> str:
    page_url = f"{SITE_URL}/policy/"
    page_title = f"プライバシーポリシー・免責事項・運営者情報｜{SITE_NAME}"
    page_desc = f"{SITE_NAME}のプライバシーポリシー、免責事項、運営者情報。"
    return f"""<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url)}
  {render_editorial_styles()}
  <title>{page_title}</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="pb-16">
  {render_pr_banner()}
  <header class="ed-header">
    <div class="max-w-[780px] mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-xs flex items-center gap-1.5" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4"></i>
        <span>{SITE_NAME}（トップへ戻る）</span>
      </a>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-6 space-y-6 text-xs sm:text-sm leading-relaxed" style="color: var(--text-secondary);">
    <h1 class="text-xl sm:text-2xl font-extrabold" style="color: var(--text-primary);">プライバシーポリシー・免責事項・運営者情報</h1>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">1. 免責事項（当サイトの情報について）</h2>
      <p>「{SITE_NAME}」（{SITE_URL}）に掲載している各国の時差、気象・気候データ、電圧・プラグ形状、チップ習慣、税金・免税制度、交通アクセス、為替レート、外務省危険情報・渡航情報等は、執筆・更新時点の調査データおよび外部APIをもとに作成しておりますが、その正確性・最新性・完全性を保証するものではありません。</p>
      <p>ご渡航の際は、必ず<strong>外務省「海外安全ホームページ」</strong>、駐日各国大使館、およびご利用の航空会社等の公式最新情報をご自身でご確認ください。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">2. 広告の配信・アフィリエイトプログラムについて</h2>
      <p>当サイトは、第三者配信の広告サービス（Google AdSense）およびアフィリエイトプログラム（A8.net 等）に参加しており、適格販売・申込により収入を得る場合があります。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">3. アクセス解析ツールについて</h2>
      <p>当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス（GA4）」を利用しています。データは匿名で収集されており、個人を特定するものではありません。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">4. 運営者情報</h2>
      <p><strong>サイト名：</strong>{SITE_NAME} / <strong>URL：</strong>{SITE_URL} / <strong>運営：</strong>{SITE_NAME} 編集部</p>
    </section>
  </main>
  <script>lucide.createIcons();</script>
</body>
</html>"""


def build_index_html(cities: list, rates_data: dict, featured_compare_pairs: list) -> str:
    unique_regions = ["すべて"] + sorted(list({c["region"] for c in cities}))
    page_url = f"{SITE_URL}/"
    page_title = f"{SITE_NAME}｜世界{len(cities)}都市の時差・天気/1年カレンダー・コンセント・チップ・生活ルール"
    page_desc = f"海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・リアルタイム気温・1年カレンダー・コンセント・チップ計算機・生活マナー・最新為替を1画面で即解決。"
    city_map = {c["slug"]: c for c in cities}

    region_buttons = "".join([
        f'<button type="button" data-region="{r}" class="region-btn shrink-0 px-3 py-1 rounded-full text-xs transition" '
        f'style="{"background: var(--accent); color: #ffffff; font-weight: 700; border: 1px solid var(--accent);" if r == "すべて" else "background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary); font-weight: 500;"}">{r}</button>'
        for r in unique_regions
    ])

    card_list = []
    for c in cities:
        r = compute_city_star_ratings(c)
        if c["special_ui"] == "china_vpn":
            vpn_badge = '<span class="status-inline status-inline--danger"><span class="status-dot"></span>要VPN/eSIM</span>'
        elif c["special_ui"] == "vpn_recommended":
            vpn_badge = '<span class="text-[10px] font-semibold" style="color: var(--accent-text);">VPN推奨</span>'
        else:
            vpn_badge = ""
        danger_dot = '<span class="status-inline status-inline--warn"><span class="status-dot"></span>注意喚起</span>' if c["danger_color"] != "emerald" else ""
        tip_short = c["tip_badge"].split("（")[0]
        search_str = f'{c["name_ja"]} {c["kana_kw"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}'
        card_list.append(
            f'<a href="./{c["slug"]}/" data-region="{c["region"]}" '
            f'data-name="{c["name_ja"]}" data-country="{c["country_ja"]}" data-slug="{c["slug"]}" '
            f'data-search="{search_str}" '
            f'class="city-card ed-surface block px-3.5 py-3">'
            f'<div class="flex items-baseline justify-between gap-2">'
            f'<span class="font-bold text-sm" style="color: var(--text-primary);">{c["name_ja"]}</span>'
            f'<span class="text-[11px] tabular-nums shrink-0" style="color: var(--text-muted);"><strong class="font-bold" style="color: var(--accent-text);">{r["avg"]:.1f}</strong> / {c["country_ja"]}</span>'
            f'</div>'
            f'<div class="text-[10.5px] mt-1 flex items-center gap-2 flex-wrap tabular-nums" style="color: var(--text-muted); opacity: 0.88;">'
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
        f'<a href="./features/{f["slug"]}/" class="ed-surface block p-3.5">'
        f'<span class="text-[10px] font-medium tracking-wide block" style="color: var(--text-muted);">{f["badge"]}</span>'
        f'<p class="text-xs font-semibold mt-1 leading-relaxed" style="color: var(--text-primary);">{f["title"]}</p>'
        f'</a>'
        for f in FEATURE_PAGES
    ])

    compare_links = "".join([
        f'<a href="./compare/{s1}-vs-{s2}/" class="text-[11px] px-2.5 py-1 rounded-full font-medium transition" style="background: var(--bg-tint); color: var(--text-secondary);">'
        f'{city_map[s1]["name_ja"]} vs {city_map[s2]["name_ja"]}'
        f'</a>'
        for s1, s2, _ in featured_compare_pairs if s1 in city_map and s2 in city_map
    ])

    return f"""<!DOCTYPE html>
<html lang="ja" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_common_head(page_title, page_desc, page_url, og_type="website")}
  {render_editorial_styles()}
  <style>
    .region-scroll-wrap {{
      position: relative;
      display: flex;
      align-items: center;
    }}
    .region-scroll-wrap::after {{
      content: "";
      position: absolute;
      top: 0;
      right: 0;
      bottom: 4px;
      width: 52px;
      background: linear-gradient(to right, transparent, var(--bg-canvas) 75%);
      pointer-events: none;
    }}
    .region-scroll-hint {{
      position: sticky;
      right: 2px;
      z-index: 2;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 20px;
      height: 20px;
      border-radius: 9999px;
      color: var(--text-muted);
      pointer-events: none;
      flex-shrink: 0;
    }}
    .sub-text-link {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 2px;
      border-radius: var(--radius-sm);
      background-color: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 11px;
      font-weight: 500;
      transition: color 0.15s ease;
    }}
    .sub-text-link:hover {{
      color: var(--text-primary);
    }}
    .sub-text-link svg {{
      transition: transform 0.3s var(--ease-out-expo);
    }}
    .sub-text-link[aria-expanded="true"] {{
      color: var(--text-primary);
      font-weight: 600;
    }}
    .sub-text-link[aria-expanded="true"] svg {{
      transform: rotate(180deg);
    }}
  </style>
  <title>{page_title}</title>
  <meta name="description" content="{page_desc}">
  <link rel="canonical" href="{page_url}">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="pb-16">
  {render_pr_banner()}
  <header class="ed-header">
    <div id="scroll-progress" class="scroll-progress"></div>
    <div class="max-w-[780px] mx-auto px-4 py-2.5 flex items-center justify-between gap-2">
      <span class="font-bold text-xs flex items-center gap-2" style="color: var(--text-primary);">
        <img src="{FAVICON_URL}" alt="" width="20" height="20" class="w-5 h-5 rounded-md object-cover shrink-0" onerror="this.style.display='none'">
        <span>{SITE_NAME}</span>
      </span>
      <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-6 space-y-7">
    <div class="space-y-1.5 anim-enter">
      <div class="flex items-center gap-2 text-[11px] tracking-wider" style="color: var(--text-muted);">
        <span>WORLD TRAVEL POCKET DICTIONARY · {len(cities)} CITIES</span>
      </div>
      <div class="flex items-center gap-2.5">
        <img src="{FAVICON_URL}" alt="{SITE_NAME}" width="32" height="32" class="w-8 h-8 rounded-lg object-cover shrink-0" style="border: 1px solid var(--divider);" onerror="this.style.display='none'">
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight">{SITE_NAME}</h1>
      </div>
      <p class="text-xs sm:text-sm leading-relaxed" style="color: var(--text-secondary);">世界{len(cities)}都市の時差・気温/1年カレンダー・コンセント・チップ計算・生活マナー・為替・外務省危険情報を1画面で即答</p>
    </div>

    <div class="space-y-2.5 anim-enter delay-1">
      <div class="relative">
        <input id="search" type="text" autocomplete="off" placeholder="都市・国・ひらがな検索（例：ばり、ロンドン）"
          class="w-full p-3.5 rounded-xl text-sm focus:outline-none" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
        <div id="suggest-box" class="ed-surface hidden absolute left-0 right-0 mt-1 max-h-64 overflow-y-auto z-40" style="box-shadow: var(--shadow-hover);"></div>
      </div>
      <div class="region-scroll-wrap">
        <div class="flex gap-1.5 overflow-x-auto pr-10 pb-1" style="scrollbar-width: none;">{region_buttons}</div>
        <span class="region-scroll-hint" aria-hidden="true"><i data-lucide="chevron-right" class="w-3.5 h-3.5"></i></span>
      </div>
    </div>

    <section class="space-y-3 anim-enter delay-2">
      <div class="flex items-baseline justify-between pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">季節・テーマ別特集</h2>
        <span class="text-[11px] tabular-nums" style="color: var(--text-muted);">{len(cities)}×{len(cities)}比較対応</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">{feature_links}</div>
      <div class="pt-0.5">
        <button id="comp-toggle-btn" type="button" class="sub-text-link" aria-expanded="false">
          <span>2都市比較ページ一覧を開く</span>
          <i data-lucide="chevron-down" class="w-3 h-3"></i>
        </button>
        <div id="comp-toggle-panel" class="accordion-content">
          <div class="accordion-inner">
            <div class="flex flex-wrap gap-1.5 pt-2.5">{compare_links}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="space-y-2.5">
      <div class="flex items-baseline justify-between pb-1.5" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm font-bold" style="color: var(--text-primary);">都市一覧</h2>
        <span id="index-city-count" class="text-[11px] tabular-nums" style="color: var(--text-muted);">{len(cities)}都市</span>
      </div>
      <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">{cards_html}</div>
    </section>

    {render_sister_site_banner()}

    {render_share_buttons(page_url, page_title)}

    <footer class="pt-6 text-center text-xs space-y-2" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline">たびレジ</a></p>
      <p><a href="./policy/" class="underline">プライバシーポリシー・免責事項・運営者情報</a></p>
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

    const compBtn = document.getElementById('comp-toggle-btn');
    const compPanel = document.getElementById('comp-toggle-panel');
    if (compBtn && compPanel) {{
      compBtn.addEventListener('click', () => {{
        const expanded = compBtn.getAttribute('aria-expanded') === 'true';
        compBtn.setAttribute('aria-expanded', String(!expanded));
        compPanel.classList.toggle('is-open', !expanded);
      }});
    }}

    function syncSearchPlaceholder() {{
      const inputEl = document.getElementById('search');
      if (!inputEl) return;
      inputEl.placeholder = window.innerWidth >= 640
        ? 'ひらがな・都市名・国名で予測検索（例：ばり、ぷさん、ロンドン、たいわん）'
        : '都市・国・ひらがな検索（例：ばり、ロンドン）';
    }}
    syncSearchPlaceholder();
    window.addEventListener('resize', syncSearchPlaceholder, {{ passive: true }});

    const progressBar = document.getElementById('scroll-progress');
    window.addEventListener('scroll', () => {{
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      if (progressBar && docHeight > 0) {{
        progressBar.style.width = `${{Math.min((window.scrollY / docHeight) * 100, 100)}}%`;
      }}
    }}, {{ passive: true }});

    let currentRegion = 'すべて';
    const searchInput = document.getElementById('search');
    const suggestBox = document.getElementById('suggest-box');
    const cards = Array.from(document.querySelectorAll('.city-card'));
    const regionBtns = document.querySelectorAll('.region-btn');
    const countEl = document.getElementById('index-city-count');

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
      let visibleCount = 0;

      cards.forEach(card => {{
        const haystack = normalizeText(card.dataset.search);
        const matchSearch = !q || haystack.includes(q);
        const matchRegion = (currentRegion === 'すべて' || card.dataset.region === currentRegion);
        const visible = matchSearch && matchRegion;
        card.style.display = visible ? 'block' : 'none';
        if (visible) visibleCount += 1;
        if (q && matchSearch) matchedCards.push(card);
      }});

      if (countEl) countEl.textContent = `${{visibleCount}}都市`;

      if (q.length > 0 && matchedCards.length > 0) {{
        suggestBox.innerHTML = matchedCards.slice(0, 8).map(c => `
          <a href="./${{c.dataset.slug}}/" class="flex items-center justify-between px-4 py-2.5 text-xs" style="border-bottom: 1px solid var(--divider);">
            <span class="font-bold" style="color: var(--text-primary);">${{c.dataset.name}}</span>
            <span style="color: var(--text-muted);">${{c.dataset.country}} →</span>
          </a>
        `).join('');
        suggestBox.classList.remove('hidden');
      }} else {{
        suggestBox.classList.add('hidden');
      }}
    }}

    searchInput.addEventListener('input', filterCards);
    document.addEventListener('click', (e) => {{
      if (!searchInput.contains(e.target) && !suggestBox.contains(e.target)) suggestBox.classList.add('hidden');
    }});
    searchInput.addEventListener('focus', () => {{
      if (searchInput.value.trim().length > 0) filterCards();
    }});

    regionBtns.forEach(btn => {{
      btn.addEventListener('click', () => {{
        currentRegion = btn.dataset.region;
        regionBtns.forEach(b => {{
          b.style.background = 'var(--bg-surface)';
          b.style.border = '1px solid var(--border-soft)';
          b.style.color = 'var(--text-secondary)';
          b.style.fontWeight = '500';
        }});
        btn.style.background = 'var(--accent)';
        btn.style.border = '1px solid var(--accent)';
        btn.style.color = '#ffffff';
        btn.style.fontWeight = '700';
        filterCards();
      }});
    }});
  </script>
</body>
</html>"""
