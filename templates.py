#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML・UIデザイン・テンプレート管理ファイル (templates.py)
- 都市別1年カレンダー（相対基準＋★＋月タップ詳細）
- バリ島等のエリア案内・小額通貨（1万IDR等）の読みやすい為替表示
- 秋休み特集：対象月基準の気温・雨・服装・ベスト月・秋の一言・夏時間注記
- ソウル vs 釜山等の同国ペア：旅のスタイル・移動・気候の違いと具体的な結論
- UX改善：不透明＆pointerdown遷移のサジェスト、追従検索バー、大きめホーム戻り、ブランドカラーPR枠
"""

import json
from config import (
    SITE_URL, SITE_NAME, GA4_ID, OGP_IMAGE_URL, FAVICON_URL,
    SISTER_SITE_URL, SISTER_SITE_NAME,
    AFFILIATE_ESIM_URL, AFFILIATE_VPN_URL, AFFILIATE_CARD_URL, AFFILIATE_WISE_URL,
    AFFILIATE_OOOH_URL, AFFILIATE_AGODA_URL,
    A8_PIXEL_URLS, FEATURE_PAGES
)

try:
    from climate_calendar import get_season_snapshot, season_tz_label
except Exception:
    get_season_snapshot = None
    season_tz_label = None


def format_rate_display(code: str, jpy_to_local: float) -> str:
    """IDRやVNDのような単位の小さい通貨は「1万単位」で実用的に表示"""
    if not jpy_to_local:
        return f"1{code} ≒ --円"
    unit_val = 1.0 / jpy_to_local
    if unit_val < 0.25:
        ten_k_jpy = round(10000.0 / jpy_to_local, 1)
        return f"1万{code} ≒ {ten_k_jpy:,}円"
    return f"1{code} ≒ {round(unit_val, 2)}円"


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


def format_water_status(city: dict) -> str:
    if city.get("water_note"):
        return city["water_note"]
    if city.get("slug") in ("seoul", "busan", "jeju", "incheon"):
        return "基準を満たすが市販水が無難"
    return "飲用可（目安）" if city.get("tap_water_safe") else "飲用不可（市販水推奨）"


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
      --font-sans: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", Meiryo, sans-serif;
      --font-editorial: "Georgia", "Times New Roman", "Hiragino Mincho ProN", "Yu Mincho", serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-full: 9999px;

      --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
      --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
      --ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);

      --bg-canvas: #f9f8f6;
      --bg-surface: #ffffff;
      --bg-tint: #f2f1ed;
      --bg-tint-hover: #e8e6e0;
      --text-primary: #18181b;
      --text-secondary: #3f3f46;
      --text-muted: #71717a;
      --divider: rgba(24, 24, 27, 0.08);
      --border-soft: rgba(24, 24, 27, 0.14);
      --shadow-hover: 0 8px 24px -6px rgba(24, 24, 27, 0.10);

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

      --brand-wise-bg: #f1fce5;
      --brand-wise-border: #a7e46f;
      --brand-wise-btn: #9fe870;
      --brand-wise-ink: #163300;

      --brand-epos-bg: #fdf2f4;
      --brand-epos-border: #f2bcc6;
      --brand-epos-btn: #c8102e;
      --brand-epos-ink: #7f0a1d;

      --brand-esim-bg: #eef7ff;
      --brand-esim-border: #b6d8f8;
      --brand-esim-btn: #0284c7;
      --brand-esim-ink: #075985;

      --brand-vpn-bg: #eef2ff;
      --brand-vpn-border: #c1cdf8;
      --brand-vpn-btn: #3b6ef5;
      --brand-vpn-ink: #1e3a8a;

      --brand-agoda-bg: #f5f2ff;
      --brand-agoda-border: #d4c6fa;
      --brand-agoda-btn: #6d28d9;
      --brand-agoda-ink: #4c1d95;

      --brand-oooh-bg: #eefaf7;
      --brand-oooh-border: #a8dfd3;
      --brand-oooh-btn: #0d9488;
      --brand-oooh-ink: #115e59;
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
      --border-soft: rgba(244, 244, 245, 0.16);
      --shadow-hover: 0 12px 30px -6px rgba(0, 0, 0, 0.55);

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

      --brand-wise-bg: rgba(159, 232, 112, 0.12);
      --brand-wise-border: rgba(159, 232, 112, 0.35);
      --brand-wise-btn: #9fe870;
      --brand-wise-ink: #163300;

      --brand-epos-bg: rgba(200, 16, 46, 0.14);
      --brand-epos-border: rgba(242, 116, 138, 0.35);
      --brand-epos-btn: #dc2626;
      --brand-epos-ink: #fecdd3;

      --brand-esim-bg: rgba(2, 132, 199, 0.14);
      --brand-esim-border: rgba(56, 189, 248, 0.35);
      --brand-esim-btn: #0ea5e9;
      --brand-esim-ink: #bae6fd;

      --brand-vpn-bg: rgba(70, 135, 255, 0.14);
      --brand-vpn-border: rgba(129, 168, 255, 0.35);
      --brand-vpn-btn: #4687ff;
      --brand-vpn-ink: #dbeafe;

      --brand-agoda-bg: rgba(109, 40, 217, 0.16);
      --brand-agoda-border: rgba(167, 139, 250, 0.35);
      --brand-agoda-btn: #7c3aed;
      --brand-agoda-ink: #ede9fe;

      --brand-oooh-bg: rgba(13, 148, 136, 0.15);
      --brand-oooh-border: rgba(94, 234, 212, 0.32);
      --brand-oooh-btn: #14b8a6;
      --brand-oooh-ink: #ccfbf1;
    }

    *, *::before, *::after { box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 112px; }
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
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseLive {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.45; transform: scale(0.85); }
    }

    .anim-enter { opacity: 0; animation: enterUp 0.6s var(--ease-out-expo) forwards; }
    .delay-1 { animation-delay: 60ms; }
    .delay-2 { animation-delay: 120ms; }

    .reveal-section {
      opacity: 0;
      transform: translateY(12px);
      transition: opacity 0.5s var(--ease-out-expo), transform 0.5s var(--ease-out-expo);
    }
    .reveal-section.is-visible { opacity: 1; transform: translateY(0); }

    .ed-header {
      position: sticky;
      top: 0;
      z-index: 45;
      background-color: color-mix(in srgb, var(--bg-canvas) 94%, transparent);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--divider);
    }

    .sticky-search-bar {
      position: sticky;
      top: 46px;
      z-index: 50;
      background-color: var(--bg-canvas);
      padding-top: 10px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--divider);
    }

    .suggest-dropdown {
      position: absolute;
      left: 0;
      right: 0;
      top: calc(100% + 6px);
      z-index: 80;
      background-color: var(--bg-surface);
      color: var(--text-primary);
      border: 1px solid var(--border-soft);
      border-radius: var(--radius-lg);
      box-shadow: 0 18px 40px -8px rgba(0, 0, 0, 0.22);
      max-height: 290px;
      overflow-y: auto;
      opacity: 1;
    }
    .suggest-item {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 11px 14px;
      font-size: 12.5px;
      text-align: left;
      background-color: var(--bg-surface);
      color: var(--text-primary);
      border: none;
      border-bottom: 1px solid var(--divider);
      cursor: pointer;
      transition: background-color 0.15s ease;
    }
    .suggest-item:last-child { border-bottom: none; }
    .suggest-item:hover, .suggest-item:active { background-color: var(--accent-soft); }

    .scroll-progress {
      position: absolute;
      top: 0;
      left: 0;
      height: 2px;
      width: 0%;
      background-color: var(--accent);
      transition: width 0.1s linear;
    }

    .toc-nav { position: relative; display: flex; gap: 20px; overflow-x: auto; scrollbar-width: none; }
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

    .ed-tint { background-color: var(--bg-tint); border-radius: var(--radius-md); transition: background-color 0.25s ease; }

    .pr-card {
      border-radius: var(--radius-lg);
      padding: 16px;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-out-expo);
    }
    .pr-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-hover); }
    .pr-card--accent { background-color: var(--accent-soft); border: 1px solid var(--accent-border); }
    .pr-card--wise { background-color: var(--brand-wise-bg); border: 1px solid var(--brand-wise-border); }
    .pr-card--epos { background-color: var(--brand-epos-bg); border: 1px solid var(--brand-epos-border); }
    .pr-card--esim { background-color: var(--brand-esim-bg); border: 1px solid var(--brand-esim-border); }
    .pr-card--vpn { background-color: var(--brand-vpn-bg); border: 1px solid var(--brand-vpn-border); }
    .pr-card--agoda { background-color: var(--brand-agoda-bg); border: 1px solid var(--brand-agoda-border); }
    .pr-card--oooh { background-color: var(--brand-oooh-bg); border: 1px solid var(--brand-oooh-border); }

    .pr-cta {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 10px 14px;
      border-radius: var(--radius-md);
      font-size: 12px;
      font-weight: 700;
      transition: transform 0.2s var(--ease-spring), opacity 0.2s ease;
    }
    .pr-cta:hover { transform: translateY(-1px); opacity: 0.94; }
    .pr-cta:active { transform: scale(0.98); }

    .ed-divider-list > div + div { border-top: 1px solid var(--divider); padding-top: 12px; margin-top: 12px; }

    .status-inline { display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 600; }
    .status-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
    .status-inline--ok { color: var(--sage-text); }
    .status-inline--ok .status-dot { background-color: var(--sage-text); }
    .status-inline--warn { color: var(--amber-text); }
    .status-inline--warn .status-dot { background-color: var(--amber-text); }
    .status-inline--danger { color: var(--rose-text); }
    .status-inline--danger .status-dot { background-color: var(--rose-text); }

    .live-dot { width: 6px; height: 6px; border-radius: 50%; background-color: #10b981; animation: pulseLive 2.2s infinite ease-in-out; }

    .month-tile {
      padding: 8px 6px;
      border-radius: var(--radius-sm);
      background-color: var(--bg-surface);
      border: 1px solid var(--divider);
      text-align: center;
      cursor: pointer;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-out-expo), border-color 0.2s ease;
    }
    .month-tile:hover, .month-tile.is-selected { transform: translateY(-2px); box-shadow: var(--shadow-hover); border-color: var(--accent); }
    .month-tile:active { transform: scale(0.96); }
    .month-tile--best { background-color: var(--sage-bg); border-color: var(--sage-border); color: var(--sage-text); }
    .month-tile--comfort { background-color: var(--accent-soft); border-color: var(--accent-border); color: var(--accent-text); }
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

    .accordion-content { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.4s var(--ease-out-expo); }
    .accordion-content.is-open { grid-template-rows: 1fr; }
    .accordion-inner { overflow: hidden; }

    .toast-msg {
      position: fixed; bottom: 24px; left: 50%;
      transform: translate(-50%, 24px) scale(0.92);
      opacity: 0; pointer-events: none; z-index: 90;
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
        <span class="text-[10px] font-semibold" style="color: var(--accent-text);">姉妹メディア · 長期滞在・留学・キャリア向け</span>
        <p class="text-xs sm:text-sm font-bold mt-0.5" style="color: var(--text-primary);">観光のその先へ：留学・ワーホリ・現地インターン情報【{SISTER_SITE_NAME}】</p>
        <p class="text-[11px] mt-0.5" style="color: var(--text-muted);">短期の渡航準備は当サイト、中長期滞在や現地コミュニティ・奨学金・キャリア情報は「{SISTER_SITE_NAME}」で役割を分けています。</p>
      </div>
      <a href="{SISTER_SITE_URL}/" target="_blank" rel="noopener" class="pr-cta shrink-0" style="background: var(--text-primary); color: var(--bg-canvas);">
        <span>{SISTER_SITE_NAME}を見る</span>
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
        return f"目安 {jpy_val:,}円（{loc_str} {code}）"

    return {
        "water": fmt_pair(water_jpy),
        "lunch": fmt_pair(lunch_jpy),
        "taxi": fmt_pair(taxi_jpy),
        "lunch_jpy": lunch_jpy,
        "taxi_jpy": taxi_jpy,
    }


def render_tip_split_calculator(city: dict, jpy_to_local: float, local_to_jpy: float) -> str:
    code = city["currency_code"]
    default_tip = 18 if city["tip_level"] == "required" else (10 if city["tip_level"] == "optional" else 0)
    bench = compute_price_benchmarks(city, jpy_to_local)

    return f"""
    <section id="sec-budget" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="calculator" class="w-4 h-4"></i>
          <span>物価の目安 ＆ チップ・割り勘計算機</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">現地予算ツール（目安）</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs tabular-nums">
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">水（500ml・商店目安）</span>
          <strong class="text-sm font-bold block mt-0.5" style="color: var(--text-primary);">{bench['water']}</strong>
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">昼食（食堂・カジュアル店目安）</span>
          <strong class="text-sm font-bold block mt-0.5" style="color: var(--text-primary);">{bench['lunch']}</strong>
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] block" style="color: var(--text-muted);">市内タクシー（短〜中距離目安）</span>
          <strong class="text-sm font-bold block mt-0.5" style="color: var(--text-primary);">{bench['taxi']}</strong>
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
              <option value="18" {"selected" if default_tip == 18 else ""}>18%（北米レストラン目安）</option>
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
            safety, safety_note = 4.6, "治安傾向が比較的安定（国・地域目安）"
        else:
            safety, safety_note = 4.2, "主要観光地は比較的安定（目安）"
    else:
        safety, safety_note = 3.4, "スリ・夜間行動に注意が必要（目安）"

    if city["special_ui"] in ("europe_cashless", "korea_nav", "us_tip_medical"):
        cashless, cashless_note = 4.8, "タッチ決済・カードが広く普及"
    elif city["special_ui"] == "china_vpn":
        cashless, cashless_note = 4.7, "QR決済主流（事前準備が便利）"
    else:
        cashless, cashless_note = 3.8, "カード＋少額現金の併用が安心"

    eng_high = ("アメリカ", "グアム・サイパン（米国準州）", "カナダ", "イギリス", "オーストラリア", "ニュージーランド", "シンガポール", "フィリピン", "マルタ", "オランダ", "スウェーデン", "ノルウェー", "デンマーク", "フィンランド", "アイスランド", "マレーシア", "アラブ首長国連邦（UAE）")
    eng_mid = ("韓国", "台湾", "タイ", "香港", "スイス", "ドイツ", "オーストリア", "ギリシャ", "クロアチア", "ポルトガル", "インド")
    if city["country_ja"] in eng_high:
        english, english_note = 4.8, "英語が広く通じやすい環境"
    elif city["country_ja"] in eng_mid:
        english, english_note = 4.0, "観光地・ホテルで英語が通じやすい"
    else:
        english, english_note = 3.3, "翻訳アプリや指差し併用が安心"

    cheap_curr = ("VND", "THB", "IDR", "PHP", "MYR", "INR", "LKR", "NPR", "EGP", "UZS", "MAD", "PLN", "HUF", "CZK")
    mid_curr = ("KRW", "TWD", "CNY", "TRY", "MXN", "PEN", "BRL", "ZAR")
    if city["currency_code"] in cheap_curr:
        cost, cost_note = 4.6, "日本より割安感がある水準（目安）"
    elif city["currency_code"] in mid_curr:
        cost, cost_note = 4.0, "日本と同等〜やや手頃な水準（目安）"
    else:
        cost, cost_note = 3.1, "外食や宿泊はやや高めの水準（目安）"

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
        <span class="font-bold text-sm" style="color: var(--text-primary);">{score:.1f} <span class="text-[11px] font-normal" style="color: var(--text-muted);">/ 5.0</span></span>
        <span class="text-[10px] font-semibold" style="color: {bar_color};">{level_tag}</span>
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
        <div class="flex items-center gap-2 flex-wrap">
          <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
            <i data-lucide="sparkles" class="w-4 h-4"></i>
            <span>{city['name_ja']}の渡航しやすさ評価（5段階・編集部目安）</span>
          </h2>
          <button id="rating-help-btn" type="button" class="text-[11px] font-semibold px-2 py-0.5 rounded-full inline-flex items-center gap-1" style="background: var(--bg-tint); color: var(--accent-text);" aria-expanded="false">
            <i data-lucide="help-circle" class="w-3 h-3"></i>
            <span>算出基準</span>
          </button>
        </div>
        <div class="text-xs font-bold tabular-nums" style="color: var(--accent-text);">総合 {r['avg']:.1f} / 5.0</div>
      </div>

      <div id="rating-help-panel" class="accordion-content">
        <div class="accordion-inner">
          <div class="ed-tint p-3 text-[11px] leading-relaxed space-y-1" style="color: var(--text-secondary);">
            <p><strong style="color: var(--text-primary);">評価の定義と注意点：</strong>治安・決済・英語・物価の4指標（各5.0点満点）の平均値です。国・地域単位の傾向や通貨水準をもとにした編集部目安であり、同じ都市でもエリアや時期によって体感は変わります。</p>
            <p style="color: var(--text-muted);">色分け基準：緑（4.2+ 比較的快適） / 青（3.5〜4.1 標準） / 琥珀（〜3.4 事前対策推奨）</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
        <div class="ed-surface p-3">
          <span class="text-[11px] font-medium block mb-1" style="color: var(--text-muted);">治安・観光安心度</span>
          {render_star_bar(r['safety'], r['safety_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-medium block mb-1" style="color: var(--text-muted);">キャッシュレス決済</span>
          {render_star_bar(r['cashless'], r['cashless_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-medium block mb-1" style="color: var(--text-muted);">英語・案内通用度</span>
          {render_star_bar(r['english'], r['english_note'])}
        </div>
        <div class="ed-surface p-3">
          <span class="text-[11px] font-medium block mb-1" style="color: var(--text-muted);">現地物価コスパ</span>
          {render_star_bar(r['cost'], r['cost_note'])}
        </div>
      </div>
    </section>"""


def render_annual_calendar_box(city: dict) -> str:
    cal = city.get("calendar")
    if not cal:
        return ""

    tile_cls_map = {
        "ベスト": "month-tile--best",
        "快適": "month-tile--comfort",
        "標準": "",
        "注意": "month-tile--caution",
    }

    month_cells = []
    for m in cal["months"]:
        cls = tile_cls_map.get(m["label"], "")
        tag_short = "・".join(m["tags"][:2]) if m["tags"] else "穏やか"
        best_mark = " ★" if m.get("city_best") else ""
        detail = (
            f"{m['month']}月：{m['label']}（平均 {m['tmin']}〜{m['tmax']}℃ / 降水量 {m['rain_mm']}mm・約{m['rain_days']}日 / 湿度{m['humidity']}%）。"
            f" 特徴：{tag_short}。服装目安：{m['outfit']}。"
        )
        detail_escaped = detail.replace('"', "&quot;")
        month_cells.append(
            f'<button type="button" class="month-tile {cls}" data-month="{m["month"]}月" data-detail="{detail_escaped}">'
            f'<div class="text-xs font-bold">{m["month"]}月{best_mark}</div>'
            f'<div class="text-[10.5px] font-bold mt-0.5">{m["label"]} <span class="font-normal opacity-80">{m["tmin"]}〜{m["tmax"]}℃</span></div>'
            f'<div class="text-[10px] opacity-85 truncate mt-0.5">{tag_short}</div>'
            f'</button>'
        )

    return f"""
    <section id="sec-calendar" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="calendar-days" class="w-4 h-4"></i>
          <span>{city['name_ja']}の1年気候カレンダー（月別気温・理由タグ・服装）</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">ベスト目安：{cal['best_months_str']}（月タップで詳細）</span>
      </div>

      <div class="grid grid-cols-3 sm:grid-cols-6 gap-1.5 tabular-nums">
        {''.join(month_cells)}
      </div>

      <div class="ed-tint p-3 text-xs space-y-1.5 leading-relaxed" style="color: var(--text-secondary);">
        <p id="calendar-month-detail"><strong style="color: var(--text-primary);">{city['name_ja']}の季節ポイント：</strong>{cal['summary_note']}</p>
        <p class="text-[10.5px]" style="color: var(--text-muted);">出典：{cal['source']}（基準 {cal['version']} / ★＝この街のベスト上位3か月）</p>
      </div>
    </section>"""


def render_sightseeing_and_agency_box(city: dict) -> str:
    spots = city.get("spots") or []
    section_title = f"{city['name_ja']}のエリア別特徴 ＆ 宿・現地手配" if city.get("slug") == "bali" else f"{city['name_ja']}の定番スポット ＆ 宿・現地手配"

    if not spots:
        return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="map-pin" class="w-4 h-4"></i>
          <span>{city['name_ja']}の宿・現地手配</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">PR / 予約・相談</span>
      </div>
      {render_agoda_and_oooh_box(city)}
    </section>"""

    spot_cards = ""
    for idx, sp in enumerate(spots[:4]):
        if isinstance(sp, str):
            sp_name, sp_desc, area, when, caution = sp, "", city["name_ja"], "", ""
        else:
            sp_name = sp.get("name", "")
            sp_desc = sp.get("desc", "")
            area = sp.get("area") or city["name_ja"]
            when = sp.get("best_time") or ""
            caution = sp.get("caution") or ""
        meta_line = f"{area} · {when}" if when else area
        spot_cards += (
            f'<div class="ed-surface p-3 space-y-1">'
            f'<div class="flex items-center justify-between gap-2">'
            f'<span class="text-[10px] font-semibold" style="color: var(--accent-text);">{meta_line}</span>'
            f'<span class="text-[10px]" style="color: var(--text-muted);">0{idx + 1}</span>'
            f'</div>'
            f'<p class="text-xs font-bold" style="color: var(--text-primary);">{sp_name}</p>'
            + (f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{sp_desc}</p>' if sp_desc else '')
            + (f'<p class="text-[10.5px] pt-0.5" style="color: var(--amber-text);">注意：{caution}</p>' if caution else '')
            + '</div>'
        )

    return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="map-pin" class="w-4 h-4"></i>
          <span>{section_title}</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">目安・PR</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">{spot_cards}</div>

      {render_agoda_and_oooh_box(city)}
    </section>"""


def render_wise_and_epos_affiliate(city: dict) -> str:
    return f"""
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-3">
        <div class="pr-card pr-card--wise flex flex-col justify-between gap-3">
          <div class="space-y-1">
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-extrabold px-2 py-0.5 rounded-full" style="background: var(--brand-wise-btn); color: var(--brand-wise-ink);">Wise · {city['currency_code']}</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold pt-1" style="color: var(--text-primary);">{city['name_ja']}の外貨決済・ATM引き出しに【Wise】</p>
            <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">
              外貨口座やデビットカードを活用したい人向けの選択肢です。<strong>両替コストや手数料を抑えたい人に向いています</strong>（対象通貨・手数料・利用上限は申込前に公式をご確認ください）。
            </p>
          </div>
          <a href="{AFFILIATE_WISE_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-wise-btn); color: var(--brand-wise-ink);">
            <span>Wise公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card pr-card--epos flex flex-col justify-between gap-3">
          <div class="space-y-1">
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="background: var(--brand-epos-btn); color: #ffffff;">年会費永年無料 · 海外旅行保険</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold pt-1" style="color: var(--text-primary);">{city['name_ja']}渡航の保険・タッチ決済に【エポスカード】</p>
            <p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">
              カード番号裏面記載＆Visaタッチ決済対応。<strong>※海外旅行傷害保険は「利用付帯」のため、空港までの交通費やツアー代金など対象費用を同カードで支払うこと</strong>が適用条件になります。
            </p>
          </div>
          <a href="{AFFILIATE_CARD_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-epos-btn); color: #ffffff;">
            <span>エポスカード詳細</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>"""


def render_detailed_rules_and_manners(city: dict) -> str:
    cc = city["country_ja"]
    curr = city["currency_code"]

    if city["special_ui"] == "china_vpn":
        payment_rule = f"中国本土では現金（{curr}）とあわせて「Alipay」や「WeChat Pay」が広く使われます。出発前にアプリを用意し、決済手段の紐付けや本人認証を確認しておくとスムーズです。"
    elif city["special_ui"] == "korea_nav":
        payment_rule = f"韓国はクレジットカードのタッチ決済が普及していますが、交通カードへのチャージや屋台・市場用に少額の現金（{curr}）もあると安心です。カード決済時は原則として現地通貨建て（{curr}）を選ぶと手数料面で有利になりやすいです。"
    elif city["special_ui"] == "europe_cashless":
        payment_rule = f"公共交通機関や店舗でタッチ決済が広く使われます。現金は最小限にとどめ、カード決済時に「円建て（JPY）」か「現地通貨建て（{curr}）」かを選べる場合は『現地通貨建て（{curr}）』を選ぶのが一般的です。"
    elif city["special_ui"] == "us_tip_medical":
        payment_rule = f"クレジットカード（タッチ決済）が広く使われます。ホテルのチェックイン時にはデポジット（保証金）としてカード提示が求められる場合があり、チップ用に少額紙幣を用意しておくと便利です。"
    else:
        payment_rule = f"ホテルや大型モールではクレジットカードが使えますが、ローカル店や移動・チップ用に現地通貨（{curr}）の現金もあると安心です。両替レートやATM手数料は事前に確認し、カード決済時は『現地通貨建て（{curr}）』を選ぶとわかりやすいです。"

    if cc in ("韓国", "台湾", "タイ", "ベトナム", "フィリピン", "インドネシア", "カンボジア", "中国", "ギリシャ", "トルコ", "エジプト", "モロッコ", "メキシコ", "ペルー", "ボリビア", "ブラジル"):
        toilet_rule = "配管や設備の事情により、紙を便器に流さず備え付けのゴミ箱へ入れる施設があるほか、紙が置かれていない公衆トイレも見られます。ポケットティッシュやウェットティッシュを持参すると安心です。"
    elif city["region"] == "ヨーロッパ":
        toilet_rule = "駅や観光地の公衆トイレは有料（カード決済や硬貨で入室）のケースが少なくありません。施設利用時やホテル・カフェで済ませておく計画を立てるとスムーズです。"
    else:
        toilet_rule = "トイレ事情は施設やエリアによって差があります。ショッピングモールやホテル、利用中の飲食店などを目安に済ませておくと安心です。"

    if cc in ("タイ", "シンガポール", "台湾", "香港", "マカオ", "インド"):
        taboo_rule = f"{cc}では電子タバコ・加熱式タバコの持ち込みや使用が厳しく規制されている場合があります。また駅構内での飲食や宗教施設での服装マナーなど、現地のルールを事前に確認してください。"
    elif cc in ("アラブ首長国連邦（UAE）", "カタール", "エジプト", "モロッコ", "トルコ", "マレーシア", "インドネシア", "モルディブ", "ウズベキスタン"):
        taboo_rule = "宗教施設を訪れる際は肌や髪の露出を抑えた服装が求められる場合があります。公共の場での飲酒マナーや、人物・施設への撮影ルールにも配慮してください。"
    elif cc in ("アメリカ", "カナダ", "オーストラリア", "ニュージーランド", "イギリス"):
        taboo_rule = "屋外での飲酒や禁煙エリアのルール、年齢確認のための顔写真付きID提示など、地域ごとの法律・条例が細かく定められています。"
    elif city["region"] == "ヨーロッパ":
        taboo_rule = "教会や史跡では服装・静粛マナーを守り、人混みやテラス席では貴重品管理に気を配ってください。日曜・祝日は店舗が休業や短縮営業になる地域もあります。"
    else:
        taboo_rule = "宗教施設や市場・繁華街では服装やマナー、貴重品の管理に気を配ってください。大型モールは営業していても、祝祭日や個人店は休業・時短になる場合があります。"

    return f"""
    <section id="sec-rules" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
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


def render_agoda_and_oooh_box(city: dict | None = None, context_label: str | None = None) -> str:
    label = context_label or (city["name_ja"] if city else "渡航先")
    hotel_title = f"{label}のホテルをエリア別に探す【アゴダ】"
    hotel_cta = f"アゴダで{label}の宿を見る"
    return f"""
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div class="pr-card pr-card--agoda flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="background: var(--brand-agoda-btn); color: #ffffff;">agoda · 宿泊予約</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold mt-2" style="color: var(--text-primary);">{hotel_title}</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              立地や口コミを見ながら宿を探したい人向けです。プランによってキャンセル条件や税・サービス料の扱いが異なるため、予約画面で最終条件をご確認ください。
            </p>
          </div>
          <a href="{AFFILIATE_AGODA_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-agoda-btn); color: #ffffff;">
            <span>{hotel_cta}</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card pr-card--oooh flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="background: var(--brand-oooh-btn); color: #ffffff;">Oooh · 日本語相談</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold mt-2" style="color: var(--text-primary);">送迎やツアーを現地会社に相談【Oooh】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              空港送迎や郊外・離島プランなどを日本語で相談したい人向けです。旅程や希望に合わせて現地側の手配可否を確認できます。
            </p>
          </div>
          <a href="{AFFILIATE_OOOH_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-oooh-btn); color: #ffffff;">
            <span>現地プロに相談する</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>"""


def render_telecom_box(city: dict | None = None, custom_note: str | None = None) -> str:
    ui = (city.get("special_ui", "standard") if city else "standard")
    vpn_badge = "NordVPN · 通信環境の確認を推奨" if ui == "china_vpn" else "NordVPN · 公衆Wi-Fi保護"
    note_text = custom_note or (
        city["telecom_note"]
        if city else
        "渡航先での地図や配車アプリ利用に向けて、eSIM・ローミング・レンタルWi-Fiなど自分の端末や旅程に合う通信手段を出発前に確認しておくと安心です。"
    )

    return f"""
    <section class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="wifi" class="w-4 h-4"></i>
          <span>現地の通信手段（eSIM）＆ 公衆Wi-Fi保護（VPN）</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">PR / 出発前準備</span>
      </div>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">{note_text}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div class="pr-card pr-card--esim flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="background: var(--brand-esim-btn); color: #ffffff;">Cross eSIM · 事前設定</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold mt-2" style="color: var(--text-primary);">海外向けeSIMプランを探す【Cross eSIM】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              物理SIMの入れ替えを減らしたい人向けの選択肢です。ご利用のスマホがeSIM対応・SIMロック解除済みか、対応国・容量条件を事前にご確認ください。
            </p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-esim-btn); color: #ffffff;">
            <span>Cross eSIM公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>

        <div class="pr-card pr-card--vpn flex flex-col justify-between gap-3">
          <div>
            <div class="flex items-center justify-between gap-1">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full" style="background: var(--brand-vpn-btn); color: #ffffff;">{vpn_badge}</span>
              <span class="text-[10px] font-semibold" style="color: var(--text-muted);">PR</span>
            </div>
            <p class="text-sm font-bold mt-2" style="color: var(--text-primary);">公衆Wi-Fiの通信暗号化に【NordVPN】</p>
            <p class="text-[11px] mt-1 leading-relaxed" style="color: var(--text-secondary);">
              空港・カフェ・ホテルなどの公衆Wi-Fi利用時に通信を暗号化したい人向けです。対応端末や返金保証などの条件は公式ページでご確認ください。
            </p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" target="_blank" rel="nofollow sponsored noopener" class="pr-cta w-full" style="background: var(--brand-vpn-btn); color: #ffffff;">
            <span>NordVPN公式サイトを見る</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>
        </div>
      </div>
    </section>"""


def render_city_comparison_section(city: dict, all_cities: list, city_compare_links: list) -> str:
    city_map = {c["slug"]: c for c in all_cities}
    nearby_slugs = city.get("nearby_slugs") or []
    nearby = [city_map[s] for s in nearby_slugs if s in city_map and s != city["slug"]][:3]
    if len(nearby) < 3:
        fallback = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"] and c not in nearby]
        nearby.extend(fallback[: 3 - len(nearby)])

    rows = ""
    for c in [city] + nearby:
        is_self = (c["slug"] == city["slug"])
        name_cell = f"<strong>{c['name_ja']}（当ページ）</strong>" if is_self else f'<a href="../{c["slug"]}/" class="underline font-bold" style="color: var(--accent-text);">{c["name_ja"]}</a>'
        rows += f"""
          <tr>
            <td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-primary);">{name_cell}</td>
            <td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c['country_ja']}</td>
            <td class="p-2.5 tabular-nums" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c.get('tz_diff_label', '-')}</td>
            <td class="p-2.5 tabular-nums" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{c['plug_type']} / {c['currency_code']}</td>
          </tr>"""

    comp_buttons = "".join([
        f'<a href="../compare/{pair_slug}/" class="text-xs font-semibold px-3 py-2 rounded-full transition inline-flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">'
        f'<span>{label} 比較</span><i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>'
        f'</a>'
        for pair_slug, label in city_compare_links
    ])

    return f"""
    <section id="sec-compare" class="space-y-3 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="scale" class="w-4 h-4"></i>
          <span>{city['name_ja']}と周辺・近隣都市の基本スペック比較</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">同国・近隣エリア優先</span>
      </div>
      <div class="ed-surface overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr style="background: var(--bg-tint); color: var(--text-muted);">
              <th class="p-2.5 font-semibold">都市名</th>
              <th class="p-2.5 font-semibold">国・地域</th>
              <th class="p-2.5 font-semibold">日本との時差</th>
              <th class="p-2.5 font-semibold">プラグ / 通貨</th>
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
    rate_display = format_rate_display(code, jpy_to_local)
    page_url = f"{SITE_URL}/{city['slug']}/"
    page_title = f"{city['name_ja']}の現地情報まとめ｜時差・天気/1年カレンダー・コンセント({city['plug_type']})・チップ・生活ルール"
    page_desc = f"{city['name_ja']}（{city['country_ja']}）の現在時刻・時差、現在の気温・1年カレンダー、コンセント（{city['plug_type']}）・電圧（{city['voltage']}）、チップ＆割り勘計算機、物価目安、お金・トイレ・マナー詳細を確認できます。"

    city_map = {c["slug"]: c for c in all_cities}
    nearby_objs = [city_map[s] for s in (city.get("nearby_slugs") or []) if s in city_map]
    other_region = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"] and c not in nearby_objs]
    related = (nearby_objs + other_region)[:14]
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
                "acceptedAnswer": {"@type": "Answer", "text": (city.get("calendar") or {}).get("summary_note") or city['climate']}
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

    water_label = format_water_status(city)

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
    <div class="max-w-[780px] mx-auto px-4 pt-2">
      <div class="flex items-center justify-between gap-2 pb-2">
        <a href="../" class="inline-flex items-center gap-2 py-1 pr-2 rounded-lg transition" style="color: var(--text-primary);">
          <i data-lucide="arrow-left" class="w-4 h-4 shrink-0" style="color: var(--accent-text);"></i>
          <img src="{FAVICON_URL}" alt="" width="22" height="22" class="w-5 h-5 rounded object-cover shrink-0" onerror="this.style.display='none'">
          <span class="font-extrabold text-sm sm:text-base tracking-tight">{SITE_NAME}</span>
          <span class="hidden sm:inline text-xs font-normal" style="color: var(--text-muted);">/ {city['region']}・{city['country_ja']}</span>
        </a>
        <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1 transition shrink-0" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
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
        <h1 class="text-2xl sm:text-3xl font-bold tracking-tight mt-0.5">
          {city['name_ja']}<span class="font-editorial-italic text-base font-normal ml-2.5" style="color: var(--text-muted);">{city['name_en']}</span>
        </h1>
      </div>

      <div class="ed-tint p-3.5 space-y-1.5 anim-enter delay-1">
        <div class="flex items-center justify-between gap-2 flex-wrap">
          <div class="flex items-center gap-2 flex-wrap">
            <i id="weather-icon" data-lucide="cloud-sun" class="w-4 h-4" style="color: var(--accent-text);"></i>
            <span class="text-xs font-medium" style="color: var(--text-muted);">現在の現地気温・天気:</span>
            <span id="weather-temp" class="text-sm font-bold tabular-nums" style="color: var(--text-primary);">取得中...</span>
            <button id="weather-retry-btn" type="button" class="hidden text-[10px] font-semibold px-2 py-0.5 rounded-full" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--accent-text);">再取得</button>
          </div>
          <span id="weather-meta" class="text-[10px] font-semibold flex items-center gap-1.5 tabular-nums" style="color: var(--text-muted);"><span class="live-dot"></span>LIVE · Open-Meteo</span>
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
          <div id="local-clock" class="text-xl font-mono font-bold tracking-tight tabular-nums">--:--:--</div>
          <div id="time-diff" class="text-[11px] font-semibold tabular-nums" style="color: var(--accent-text);">時差を計算中...</div>
        </div>

        <div class="p-3.5 flex flex-col justify-between gap-1.5 sm:border-b-0" style="border-bottom: 1px solid var(--divider);">
          <span class="text-[11px] font-medium flex items-center gap-1" style="color: var(--text-muted);"><i data-lucide="plug" class="w-3.5 h-3.5"></i>プラグ・電圧</span>
          <div class="flex items-center gap-2">
            <span style="color: var(--text-primary);">{render_plug_svg(city['plug_type'])}</span>
            <div>
              <div class="text-sm font-bold tabular-nums">{city['plug_type']} / {city['voltage']}</div>
              <div class="status-inline status-inline--ok"><span class="status-dot"></span>{'変圧器確認推奨' if city['transformer_needed'] else '対応機器は変圧器不要'}</div>
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
          <div class="text-[11px]" style="color: var(--text-muted);">水道水: {water_label}</div>
        </div>

        <div class="p-3.5 flex flex-col justify-between gap-1.5">
          <span class="text-[11px] font-medium flex items-center gap-1 tabular-nums" style="color: var(--text-muted);"><i data-lucide="arrow-left-right" class="w-3.5 h-3.5"></i>{rate_display}</span>
          <div class="flex items-center gap-1.5">
            <input id="jpy-input" type="number" value="1000" class="w-20 rounded-md px-2 py-1 text-xs font-bold tabular-nums" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);">
            <span class="text-[11px]" style="color: var(--text-muted);">円</span>
          </div>
          <div id="local-output" class="text-xs font-bold tabular-nums" style="color: var(--sage-text);">≒ {thousand_jpy_in_local} {code}</div>
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
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="plane" class="w-4 h-4"></i>
          <span>{city['airport_access']['airport_name']}から市内への移動</span>
        </h2>
        <span class="text-[11px]" style="color: var(--text-muted);">空港アクセス（目安）</span>
      </div>
      <div class="ed-surface p-4 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
        <div class="sm:grid sm:grid-cols-[120px_1fr] sm:gap-3 sm:items-baseline">
          <span class="font-bold" style="color: var(--accent-text);">時間重視・快適</span>
          <p>{city['airport_access']['fastest']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[120px_1fr] sm:gap-3 sm:items-baseline">
          <span class="font-bold" style="color: var(--sage-text);">費用重視・定番</span>
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
        <h2 class="text-base font-bold flex items-center gap-1.5" style="color: var(--text-primary);">
          <i data-lucide="shield-alert" class="w-4 h-4"></i>
          <span>安全・危険情報・日本大使館連絡先</span>
        </h2>
        <span class="status-inline status-inline--danger tabular-nums"><span class="status-dot"></span>緊急通報: {city['emergency_numbers']}</span>
      </div>

      <div class="ed-surface p-4 ed-divider-list text-xs leading-relaxed" style="color: var(--text-secondary);">
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">外務省 危険情報目安</p>
          <p><strong style="color: var(--text-primary);">{city['danger_level']}</strong> — <a href="{city['mofa_url']}" target="_blank" rel="noopener noreferrer" class="underline" style="color: var(--accent-text);">外務省公式ページで最新発出を確認</a></p>
        </div>
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">現地の治安・注意点</p>
          <p>{city['safety_note']}</p>
        </div>
        <div class="sm:grid sm:grid-cols-[180px_1fr] sm:gap-4 sm:items-baseline">
          <p class="font-bold" style="color: var(--text-primary);">日本大使館・総領事館</p>
          <div class="flex flex-wrap items-center gap-2">
            <span>{city['embassy']}</span>
            <button type="button" onclick="copyEmbassyInfo()" class="text-[11px] font-semibold px-2.5 py-1 rounded-full inline-flex items-center gap-1 transition" style="background: var(--bg-tint); border: 1px solid var(--border-soft); color: var(--text-primary);">
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
          <span>外務省「たびレジ」を確認する</span>
          <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </section>

    {render_city_comparison_section(city, all_cities, city_compare_links)}
    {render_share_buttons(page_url, page_title)}
    {render_sister_site_banner()}

    <section class="pt-1 reveal-section">
      <h3 class="text-xs font-bold mb-2" style="color: var(--text-muted);">{city['region']}・近隣の他の都市をチェック</h3>
      <div class="flex flex-wrap gap-1.5">{related_html}</div>
    </section>

    <footer class="pt-6 pb-4 text-center text-[11px] space-y-1.5" style="color: var(--text-muted); border-top: 1px solid var(--divider);">
      <p>※当ページはプロモーション（アフィリエイト広告）を含みます。制度・料金・治安情報等は変更される場合があるため、渡航前に外務省や各公式窓口の最新情報をご確認ください。</p>
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
      try {{
        const targetStr = now.toLocaleTimeString('ja-JP', {{ timeZone: targetTz, hour12: false }});
        document.getElementById('local-clock').textContent = targetStr;
        const baseTz = compareWithLocal ? Intl.DateTimeFormat().resolvedOptions().timeZone : 'Asia/Tokyo';
        const targetDate = new Date(now.toLocaleString('en-US', {{ timeZone: targetTz }}));
        const baseDate = new Date(now.toLocaleString('en-US', {{ timeZone: baseTz }}));
        let diffHours = Math.round((targetDate - baseDate) / 3600000);
        if (!compareWithLocal && citySlug === 'marrakech' && diffHours === -9) diffHours = -8;
        const sign = diffHours >= 0 ? '+' : '';
        const label = compareWithLocal ? '現在地との時差' : '日本との時差';
        document.getElementById('time-diff').textContent = `${{label}}: ${{sign}}${{diffHours}}時間`;
      }} catch (e) {{
        document.getElementById('local-clock').textContent = '--:--:--';
        document.getElementById('time-diff').textContent = 'タイムゾーン情報をご確認ください';
      }}
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
        countdownMsg.textContent = `出発まであと${{diffDays}}日（eSIM・保険・たびレジ確認期）`;
        highlightStep(stepMid);
      }} else if (diffDays >= 0) {{
        countdownMsg.textContent = diffDays === 0 ? '本日出発日です。安全なご渡航を！' : `出発まであと${{diffDays}}日（最終持ち物チェック期）`;
        highlightStep(stepFinal);
      }} else {{
        countdownMsg.textContent = '現地滞在中の時刻・為替・割り勘確認にご活用ください。';
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
        document.getElementById('calendar-month-detail').innerHTML = `<strong style="color: var(--text-primary);">${{tile.getAttribute('data-month')}}の気候・服装：</strong>${{detail.replace(/^[^：]+：/, '')}}`;
      }});
    }});

    const ratingHelpBtn = document.getElementById('rating-help-btn');
    const ratingHelpPanel = document.getElementById('rating-help-panel');
    if (ratingHelpBtn && ratingHelpPanel) {{
      ratingHelpBtn.addEventListener('click', () => {{
        const expanded = ratingHelpBtn.getAttribute('aria-expanded') === 'true';
        ratingHelpBtn.setAttribute('aria-expanded', String(!expanded));
        ratingHelpPanel.classList.toggle('is-open', !expanded);
      }});
    }}

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

    const weatherRetryBtn = document.getElementById('weather-retry-btn');
    if (weatherRetryBtn) {{
      weatherRetryBtn.addEventListener('click', () => {{
        document.getElementById('weather-temp').textContent = '再取得中...';
        weatherRetryBtn.classList.add('hidden');
        fetchWeather();
      }});
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
        if (temp >= 28) outfit = '服装目安：半袖・薄手の服（屋内冷房対策に薄手の羽織りがあると安心）';
        else if (temp >= 22) outfit = '服装目安：半袖または薄手の長袖シャツが快適';
        else if (temp >= 16) outfit = '服装目安：長袖＋カーディガンやジャケットなどの羽織りものがあると安心';
        else if (temp >= 10) outfit = '服装目安：コートやジャケット・ニットなどの防寒着がおすすめ';
        else outfit = '服装目安：冬物コートやダウンなどしっかりした防寒対策がおすすめ';

        const dryNote = humidity <= 40 ? '（乾燥注意）' : (humidity >= 80 ? '（高湿度）' : '');

        document.getElementById('weather-temp').textContent = `${{temp}}℃（${{desc}} / 湿度${{humidity}}%${{dryNote}}）`;
        document.getElementById('weather-outfit').textContent = outfit;
        if (weatherRetryBtn) weatherRetryBtn.classList.add('hidden');
        if (obsTime) {{
          document.getElementById('weather-meta').innerHTML = `<span class="live-dot"></span>現地 ${{obsTime}}観測 · Open-Meteo`;
        }}
      }} catch (e) {{
        setWeatherLucideIcon('cloud-sun');
        document.getElementById('weather-temp').textContent = '気象データを取得できませんでした（下の気候目安をご参照ください）';
        document.getElementById('weather-outfit').textContent = '通信環境をご確認のうえ、再取得ボタンを押すか気象情報をご確認ください';
        if (weatherRetryBtn) weatherRetryBtn.classList.remove('hidden');
      }}
    }}
    fetchWeather();
  </script>
</body>
</html>"""


def _city_style_verdict(c_target: dict, c_other: dict, s_t: dict, s_o: dict, b_t: dict, b_o: dict) -> str:
    """同じ国や別都市のペアでも、旅のスタイル・移動・性格の違いが伝わる結論を生成"""
    custom_verdicts = {
        "seoul": "王宮・ショッピング・夜の繁華街をコンパクトに楽しみたい人。仁川/金浦からの鉄道移動や最新トレンド巡りに向いています（4〜6月・9〜10月が好適）。",
        "busan": "海辺の景色・海鮮グルメ・落ち着いた街歩きを味わいたい人。ソウルとはKTX等で約2〜3時間の距離感で、港町ならではの開放感があります（4〜6月・9〜10月が好適）。",
        "sydney": "オペラハウスやハーバー・ビーチの開放感、フェリー移動を楽しみたい人（南半球の12〜2月は夏、6〜8月は冬）。",
        "melbourne": "路地裏のカフェ文化・アート・無料トラム中心の街歩きを楽しみたい人（南半球の6〜8月はシドニーより冷え込みやすい傾向）。",
    }
    if c_target["slug"] in custom_verdicts:
        return custom_verdicts[c_target["slug"]]

    rs = []
    if b_t["lunch_jpy"] < b_o["lunch_jpy"]:
        rs.append(f"現地物価のコスパ（昼食目安 {b_t['lunch_jpy']:,}円）を重視する人")
    if s_t["safety"] > s_o["safety"]:
        rs.append(f"治安面の安心感（評価 {s_t['safety']:.1f}/5.0）を優先したい人")
    if s_t["cashless"] > s_o["cashless"]:
        rs.append("キャッシュレス決済中心で身軽に動きたい人")
    tz_t, tz_o = c_target.get("tz_diff_hours"), c_other.get("tz_diff_hours")
    if tz_t is not None and tz_o is not None and abs(tz_t) < abs(tz_o):
        rs.append(f"時差を抑えたい人（日本との時差 {c_target.get('tz_diff_label')}）")
    if not rs:
        # 違いを示す根拠がないときは空文字を返し、結論ボックスごと非表示にする
        return ""
    bm = (c_target.get("calendar") or {}).get("best_months_str")
    suffix = f"（目安：{bm}）" if bm and bm != "特になし" else ""
    return "・".join(rs[:2]) + suffix


def _build_compare_payload(c1: dict, c2: dict, rates_data: dict) -> dict:
    s1 = compute_city_star_ratings(c1)
    s2 = compute_city_star_ratings(c2)
    r1 = rates_data["rates"].get(c1["currency_code"], 0.01)
    r2 = rates_data["rates"].get(c2["currency_code"], 0.01)
    b1 = compute_price_benchmarks(c1, r1)
    b2 = compute_price_benchmarks(c2, r2)
    cal1, cal2 = c1.get("calendar") or {}, c2.get("calendar") or {}

    same_country = (c1.get("country_ja") == c2.get("country_ja"))
    vibe_map = {
        "seoul": "王宮・ショッピング・夜の街が密集する大都市（日本から直行約2〜2.5時間目安）",
        "busan": "海辺・ビーチ・海鮮市場と落ち着いた街並みが魅力の港町（ソウルからKTX等で約2〜3時間目安）",
        "sydney": "ハーバー・ビーチ・フェリー移動が映える開放的な港湾都市",
        "melbourne": "路地裏のカフェ文化・アートと無料トラム中心の街歩きが楽しい都市",
    }
    style_map = {
        "seoul": "買い物・グルメ・歴史スポットをテンポよく巡る旅（4〜5日〜）",
        "busan": "海辺散策・海鮮・温泉やのんびり滞在を組み合わせる旅（3〜4日〜）",
    }

    common_items = []
    diff_rows = []

    if c1["slug"] in vibe_map and c2["slug"] in vibe_map:
        diff_rows.append((
            "街の個性・位置関係",
            vibe_map.get(c1["slug"], f"{c1['name_ja']}（{c1['country_ja']}）の中心エリア"),
            vibe_map.get(c2["slug"], f"{c2['name_ja']}（{c2['country_ja']}）の中心エリア"),
        ))
        if c1["slug"] in style_map or c2["slug"] in style_map:
            diff_rows.append((
                "旅のスタイル・日数目安",
                style_map.get(c1["slug"], f"{c1['name_ja']}中心の滞在"),
                style_map.get(c2["slug"], f"{c2['name_ja']}中心の滞在"),
            ))

    spec_checks = [
        ("日本との時差", c1.get("tz_diff_label", "-"), c2.get("tz_diff_label", "-"), c1.get("tz_diff_label") == c2.get("tz_diff_label"), f"日本との時差：{c1.get('tz_diff_label', '-')}"),
        ("物価目安（昼食 / タクシー）", f"昼食 {b1['lunch']} / タクシー {b1['taxi']}", f"昼食 {b2['lunch']} / タクシー {b2['taxi']}", (b1["lunch_jpy"] == b2["lunch_jpy"] and c1["currency_code"] == c2["currency_code"]), f"物価水準：昼食目安 {b1['lunch_jpy']:,}円前後"),
        ("ベスト月 / 注意月", f"ベスト：{cal1.get('best_months_str', '-')} ／ 注意：{cal1.get('caution_months_str', '-')}", f"ベスト：{cal2.get('best_months_str', '-')} ／ 注意：{cal2.get('caution_months_str', '-')}", (cal1.get("best_months_str") == cal2.get("best_months_str") and cal1.get("caution_months_str") == cal2.get("caution_months_str")), f"ベスト時期：{cal1.get('best_months_str', '-')}"),
        ("空港アクセス（最安・定番）", c1["airport_access"]["cheapest"], c2["airport_access"]["cheapest"], c1["airport_access"]["cheapest"] == c2["airport_access"]["cheapest"], None),
        ("空港アクセス（最速・快適）", c1["airport_access"]["fastest"], c2["airport_access"]["fastest"], c1["airport_access"]["fastest"] == c2["airport_access"]["fastest"], None),
        ("通貨・為替目安", f"{c1['currency_name']}（{format_rate_display(c1['currency_code'], r1)}）", f"{c2['currency_name']}（{format_rate_display(c2['currency_code'], r2)}）", c1["currency_code"] == c2["currency_code"], f"通貨：{c1['currency_name']}（{c1['currency_code']}）"),
        ("コンセント・電圧", f"{c1['plug_type']}タイプ（{c1['voltage']} / {c1['frequency']}）", f"{c2['plug_type']}タイプ（{c2['voltage']} / {c2['frequency']}）", (c1["plug_type"] == c2["plug_type"] and c1["voltage"] == c2["voltage"]), f"プラグ：{c1['plug_type']}（{c1['voltage']}）"),
        ("チップ習慣", f"{c1['tip_badge']}（{c1['tip_detail']}）", f"{c2['tip_badge']}（{c2['tip_detail']}）", (c1["tip_badge"] == c2["tip_badge"] and c1["tip_detail"] == c2["tip_detail"]), f"チップ：{c1['tip_badge']}"),
        ("水道水", format_water_status(c1), format_water_status(c2), format_water_status(c1) == format_water_status(c2), f"水道水：{format_water_status(c1)}"),
        ("外務省危険情報", c1["danger_level"], c2["danger_level"], c1["danger_level"] == c2["danger_level"], f"危険情報：{c1['danger_level'].split('（')[0]}"),
        ("総合評価（目安）", f"{s1['avg']:.1f} / 5.0", f"{s2['avg']:.1f} / 5.0", s1["avg"] == s2["avg"], f"総合目安：{s1['avg']:.1f} / 5.0"),
    ]

    if not (cal1 and cal2):
        spec_checks = [s for s in spec_checks if s[0] != "ベスト月 / 注意月"]

    for label, v1, v2, is_same, common_label in spec_checks:
        if is_same and common_label:
            common_items.append(common_label)
        else:
            diff_rows.append((label, v1, v2))

    diff_labels = [r[0] for r in diff_rows[:4]]
    diff_topic_str = "・".join(diff_labels) if diff_labels else "街の個性・空港アクセス"

    return {
        "common_items": common_items,
        "diff_rows": diff_rows,
        "diff_topic_str": diff_topic_str,
        "best1": _city_style_verdict(c1, c2, s1, s2, b1, b2),
        "best2": _city_style_verdict(c2, c1, s2, s1, b2, b1),
    }


def build_compare_html(c1: dict, c2: dict, summary_text: str, rates_data: dict, all_cities: list) -> str:
    pair_slug = f"{c1['slug']}-vs-{c2['slug']}"
    page_url = f"{SITE_URL}/compare/{pair_slug}/"
    payload = _build_compare_payload(c1, c2, rates_data)

    title = f"{c1['name_ja']}と{c2['name_ja']}を比較｜{payload['diff_topic_str']}の違い｜{SITE_NAME}"
    desc = f"{c1['name_ja']}（{c1['country_ja']}）と{c2['name_ja']}（{c2['country_ja']}）を{payload['diff_topic_str']}で比較。共通条件をまとめ、旅のスタイルに合わせた選び方を確認できます。"
    subtitle = f"{c1['name_ja']}と{c2['name_ja']}の「{payload['diff_topic_str']}」を中心に違いを整理しています。"

    compact_cities = []
    for c in all_cities:
        sr = compute_city_star_ratings(c)
        rc = rates_data["rates"].get(c["currency_code"], 0.01)
        bc = compute_price_benchmarks(c, rc)
        calc = c.get("calendar") or {}
        compact_cities.append({
            "slug": c["slug"],
            "name_ja": c["name_ja"],
            "country_ja": c["country_ja"],
            "tz_diff_label": c.get("tz_diff_label", "-"),
            "tz_diff_hours": c.get("tz_diff_hours"),
            "lunch": bc["lunch"],
            "taxi": bc["taxi"],
            "lunch_jpy": bc["lunch_jpy"],
            "best_months": calc.get("best_months_str", "-"),
            "caution_months": calc.get("caution_months_str", "-"),
            "plug_type": c["plug_type"],
            "voltage": c["voltage"],
            "frequency": c["frequency"],
            "tip_badge": c["tip_badge"],
            "tip_detail": c["tip_detail"],
            "currency_name": c["currency_name"],
            "currency_code": c["currency_code"],
            "rate_disp": format_rate_display(c["currency_code"], rc),
            "tap_water": format_water_status(c),
            "cheapest": c["airport_access"]["cheapest"],
            "fastest": c["airport_access"]["fastest"],
            "danger_level": c["danger_level"],
            "avg_star": sr["avg"],
            "safety": sr["safety"],
            "cashless": sr["cashless"],
        })

    options_1 = "".join([
        f'<option value="{c["slug"]}" {"selected" if c["slug"] == c1["slug"] else ""}>{c["name_ja"]}（{c["country_ja"]}）</option>'
        for c in all_cities
    ])
    options_2 = "".join([
        f'<option value="{c["slug"]}" {"selected" if c["slug"] == c2["slug"] else ""}>{c["name_ja"]}（{c["country_ja"]}）</option>'
        for c in all_cities
    ])

    common_badges = "".join([
        f'<span class="text-[11px] px-2.5 py-1 rounded-full font-medium" style="background: var(--bg-surface); border: 1px solid var(--divider); color: var(--text-secondary);">{item}</span>'
        for item in payload["common_items"]
    ])

    diff_rows_html = "".join([
        f"""
        <tr>
          <th class="p-3 font-semibold align-top" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">{lbl}</th>
          <td class="p-3 align-top leading-relaxed" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{v1}</td>
          <td class="p-3 align-top leading-relaxed" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">{v2}</td>
        </tr>"""
        for lbl, v1, v2 in payload["diff_rows"]
    ])

    both_label = f"{c1['name_ja']}・{c2['name_ja']}"

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
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-semibold uppercase tracking-wider" style="color: var(--accent-text);">2 CITY COMPARISON · {len(all_cities)}×{len(all_cities)}対応</span>
      <h1 id="comp-h1" class="text-xl sm:text-2xl font-bold">{c1['name_ja']} vs {c2['name_ja']} 違いと選び方比較</h1>
      <p id="comp-summary" class="text-xs leading-relaxed" style="color: var(--text-secondary);">{subtitle}</p>
    </div>

    <div id="comp-conclusion-box" class="pr-card pr-card--accent space-y-2 anim-enter delay-1 {'hidden' if not (payload['best1'] and payload['best2'] and payload['best1'] != payload['best2']) else ''}">
      <span class="text-[10px] font-bold" style="color: var(--accent-text);">選び方の目安（結論）</span>
      <div id="comp-conclusion-text" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs leading-relaxed" style="color: var(--text-primary);">
        <div class="p-3 rounded-lg" style="background: var(--bg-surface); border: 1px solid var(--divider);">
          <strong class="block mb-1" style="color: var(--accent-text);">{c1['name_ja']}が向いている人</strong>
          <p style="color: var(--text-secondary);">{payload['best1']}</p>
        </div>
        <div class="p-3 rounded-lg" style="background: var(--bg-surface); border: 1px solid var(--divider);">
          <strong class="block mb-1" style="color: var(--accent-text);">{c2['name_ja']}が向いている人</strong>
          <p style="color: var(--text-secondary);">{payload['best2']}</p>
        </div>
      </div>
    </div>

    <section class="ed-tint p-4 space-y-2.5 anim-enter delay-2">
      <p class="text-xs font-bold" style="color: var(--text-primary);">全{len(all_cities)}都市から好きな2都市を選んでその場で比較</p>
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

    <section id="comp-common-wrap" class="ed-tint p-3.5 space-y-2 reveal-section {'hidden' if not payload['common_items'] else ''}">
      <h2 class="text-xs font-bold" style="color: var(--text-primary);">2都市で共通の条件</h2>
      <div id="comp-common-list" class="flex flex-wrap gap-1.5">{common_badges}</div>
    </section>

    <section class="ed-surface overflow-x-auto reveal-section">
      <div class="px-3.5 py-2.5" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-xs font-bold" style="color: var(--text-primary);">違いが出る項目（比較表）</h2>
      </div>
      <table class="w-full text-left border-collapse text-xs">
        <thead>
          <tr style="background: var(--bg-tint); color: var(--text-primary);">
            <th class="p-3 w-1/4 font-bold">違いが出る項目</th>
            <th id="th-c1" class="p-3 w-[37.5%] font-bold" style="border-left: 1px solid var(--divider);"><a href="../../{c1['slug']}/" class="underline" style="color: var(--accent-text);">{c1['name_ja']}（{c1['country_ja']}）</a></th>
            <th id="th-c2" class="p-3 w-[37.5%] font-bold" style="border-left: 1px solid var(--divider);"><a href="../../{c2['slug']}/" class="underline" style="color: var(--accent-text);">{c2['name_ja']}（{c2['country_ja']}）</a></th>
          </tr>
        </thead>
        <tbody id="comp-diff-tbody" class="tabular-nums" style="color: var(--text-secondary);">
          {diff_rows_html}
        </tbody>
      </table>
    </section>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 reveal-section">
      <a id="btn-c1" href="../../{c1['slug']}/" class="pr-cta" style="background: var(--accent); color: #ffffff;">{c1['name_ja']}の生活ルール・詳細ページへ →</a>
      <a id="btn-c2" href="../../{c2['slug']}/" class="pr-cta" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">{c2['name_ja']}の生活ルール・詳細ページへ →</a>
    </div>

    {render_agoda_and_oooh_box(context_label=both_label)}
    {render_telecom_box(custom_note=f"{both_label}のどちらに渡航する場合も、現地での地図・配車アプリ利用に向けて出発前にeSIMやローミングなどの通信手段を確認しておくと安心です。")}
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

    function escHtml(str) {{
      return String(str || '').replace(/[&<>"']/g, s => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[s]));
    }}

    function buildVerdict(t, o) {{
      const map = {{
        seoul: '王宮・ショッピング・夜の街をコンパクトに楽しみたい人。仁川/金浦からの鉄道移動や最新トレンド巡りに向いています（4〜6月・9〜10月が好適）。',
        busan: '海辺の景色・海鮮グルメ・落ち着いた街歩きを味わいたい人。ソウルとはKTX等で約2〜3時間の距離感で、港町ならではの開放感があります（4〜6月・9〜10月が好適）。',
        sydney: 'オペラハウスやハーバー・ビーチの開放感、フェリー移動を楽しみたい人（南半球の12〜2月は夏、6〜8月は冬）。',
        melbourne: '路地裏のカフェ文化・アート・無料トラム中心の街歩きを楽しみたい人（南半球の6〜8月はシドニーより冷え込みやすい傾向）。'
      }};
      if (map[t.slug]) return map[t.slug];
      const rs = [];
      if (t.lunch_jpy < o.lunch_jpy) rs.push(`現地物価のコスパ（昼食目安 ${{t.lunch_jpy.toLocaleString()}}円）を重視する人`);
      if (t.safety > o.safety) rs.push(`治安面の安心感（評価 ${{t.safety.toFixed(1)}}/5.0）を優先したい人`);
      if (t.cashless > o.cashless) rs.push('キャッシュレス決済中心で身軽に動きたい人');
      if (t.tz_diff_hours !== null && o.tz_diff_hours !== null && Math.abs(t.tz_diff_hours) < Math.abs(o.tz_diff_hours)) {{
        rs.push(`時差を抑えたい人（日本との時差 ${{t.tz_diff_label}}）`);
      }}
      if (rs.length === 0) return '';
      const bm = t.best_months && t.best_months !== '-' ? `（目安：${{t.best_months}}）` : '';
      return rs.slice(0, 2).join('・') + bm;
    }}

    function renderDynamicCompare() {{
      const a = cityBySlug[sel1.value];
      const b = cityBySlug[sel2.value];
      if (!a || !b) return;

      const common = [];
      const diffs = [];
      const sameCountry = (a.country_ja === b.country_ja);
      const vibeMap = {{
        seoul: '王宮・ショッピング・夜の街が密集する大都市',
        busan: '海辺・ビーチ・海鮮市場と落ち着いた街並みが魅力の港町',
        sydney: 'ハーバー・ビーチ・フェリー移動が映える開放的な港湾都市',
        melbourne: '路地裏のカフェ文化・アートと無料トラム中心の街歩きが楽しい都市'
      }};
      if (vibeMap[a.slug] && vibeMap[b.slug]) {{
        diffs.push(['街の個性', vibeMap[a.slug] || a.name_ja, vibeMap[b.slug] || b.name_ja]);
      }}

      const specs = [
        ['日本との時差', a.tz_diff_label, b.tz_diff_label, a.tz_diff_label === b.tz_diff_label, `日本との時差：${{a.tz_diff_label}}`],
        ['物価目安（昼食 / タクシー）', `昼食 ${{a.lunch}} / タクシー ${{a.taxi}}`, `昼食 ${{b.lunch}} / タクシー ${{b.taxi}}`, (a.lunch_jpy === b.lunch_jpy && a.currency_code === b.currency_code), `物価水準：昼食目安 ${{a.lunch_jpy.toLocaleString()}}円前後`],
        ['ベスト月 / 注意月', `ベスト：${{a.best_months}} ／ 注意：${{a.caution_months}}`, `ベスト：${{b.best_months}} ／ 注意：${{b.caution_months}}`, (a.best_months === b.best_months && a.caution_months === b.caution_months), `ベスト時期：${{a.best_months}}`],
        ['空港アクセス（最安・定番）', a.cheapest, b.cheapest, a.cheapest === b.cheapest, null],
        ['空港アクセス（最速・快適）', a.fastest, b.fastest, a.fastest === b.fastest, null],
        ['通貨・為替目安', `${{a.currency_name}}（${{a.rate_disp}}）`, `${{b.currency_name}}（${{b.rate_disp}}）`, a.currency_code === b.currency_code, `通貨：${{a.currency_name}}（${{a.currency_code}}）`],
        ['コンセント・電圧', `${{a.plug_type}}タイプ（${{a.voltage}} / ${{a.frequency}}）`, `${{b.plug_type}}タイプ（${{b.voltage}} / ${{b.frequency}}）`, (a.plug_type === b.plug_type && a.voltage === b.voltage), `プラグ：${{a.plug_type}}（${{a.voltage}}）`],
        ['チップ習慣', `${{a.tip_badge}}（${{a.tip_detail}}）`, `${{b.tip_badge}}（${{b.tip_detail}}）`, (a.tip_badge === b.tip_badge && a.tip_detail === b.tip_detail), `チップ：${{a.tip_badge}}`],
        ['水道水', a.tap_water, b.tap_water, a.tap_water === b.tap_water, `水道水：${{a.tap_water}}`],
        ['外務省危険情報', a.danger_level, b.danger_level, a.danger_level === b.danger_level, `危険情報：${{a.danger_level.split('（')[0]}}`],
        ['総合評価（目安）', `${{a.avg_star.toFixed(1)}} / 5.0`, `${{b.avg_star.toFixed(1)}} / 5.0`, a.avg_star === b.avg_star, `総合目安：${{a.avg_star.toFixed(1)}} / 5.0`],
      ];

      specs.forEach(([lbl, v1, v2, isSame, cLbl]) => {{
        if (lbl === 'ベスト月 / 注意月' && (a.best_months === '-' || b.best_months === '-')) return;
        if (isSame && cLbl) common.push(cLbl);
        else diffs.push([lbl, v1, v2]);
      }});

      const topicStr = diffs.slice(0, 4).map(d => d[0]).join('・') || '街の個性・空港アクセス';
      document.getElementById('comp-h1').textContent = `${{a.name_ja}} vs ${{b.name_ja}} 違いと選び方比較`;
      document.getElementById('comp-summary').textContent = `${{a.name_ja}}と${{b.name_ja}}の「${{topicStr}}」を中心に違いを整理しています。`;

      const verdictA = buildVerdict(a, b);
      const verdictB = buildVerdict(b, a);
      document.getElementById('comp-conclusion-box').classList.toggle('hidden', !(verdictA && verdictB && verdictA !== verdictB));
      document.getElementById('comp-conclusion-text').innerHTML = `
        <div class="p-3 rounded-lg" style="background: var(--bg-surface); border: 1px solid var(--divider);">
          <strong class="block mb-1" style="color: var(--accent-text);">${{escHtml(a.name_ja)}}が向いている人</strong>
          <p style="color: var(--text-secondary);">${{escHtml(verdictA)}}</p>
        </div>
        <div class="p-3 rounded-lg" style="background: var(--bg-surface); border: 1px solid var(--divider);">
          <strong class="block mb-1" style="color: var(--accent-text);">${{escHtml(b.name_ja)}}が向いている人</strong>
          <p style="color: var(--text-secondary);">${{escHtml(verdictB)}}</p>
        </div>`;

      const commonWrap = document.getElementById('comp-common-wrap');
      const commonList = document.getElementById('comp-common-list');
      if (common.length > 0) {{
        commonWrap.classList.remove('hidden');
        commonList.innerHTML = common.map(item =>
          `<span class="text-[11px] px-2.5 py-1 rounded-full font-medium" style="background: var(--bg-surface); border: 1px solid var(--divider); color: var(--text-secondary);">${{escHtml(item)}}</span>`
        ).join('');
      }} else {{
        commonWrap.classList.add('hidden');
      }}

      document.getElementById('th-c1').innerHTML = `<a href="../../${{a.slug}}/" class="underline" style="color: var(--accent-text);">${{escHtml(a.name_ja)}}（${{escHtml(a.country_ja)}}）</a>`;
      document.getElementById('th-c2').innerHTML = `<a href="../../${{b.slug}}/" class="underline" style="color: var(--accent-text);">${{escHtml(b.name_ja)}}（${{escHtml(b.country_ja)}}）</a>`;
      document.getElementById('comp-diff-tbody').innerHTML = diffs.map(([lbl, v1, v2]) => `
        <tr>
          <th class="p-3 font-semibold align-top" style="background: var(--bg-tint); border-top: 1px solid var(--divider); color: var(--text-muted);">${{escHtml(lbl)}}</th>
          <td class="p-3 align-top leading-relaxed" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">${{escHtml(v1)}}</td>
          <td class="p-3 align-top leading-relaxed" style="border-top: 1px solid var(--divider); border-left: 1px solid var(--divider);">${{escHtml(v2)}}</td>
        </tr>`).join('');

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

    season_meta = {
        "graduation-spring": ([2, 3], "2〜3月（春休み）", "卒業旅行シーズンで航空券が混み合います。朝晩の冷え込みや防寒着も忘れずに。"),
        "spring-break": ([3], "3月（春休み）", "3月は卒業旅行シーズンで航空券が混み合います。朝晩の冷え込みに備えてください。"),
        "golden-week": ([4, 5], "4〜5月（GW）", "5月1日のメーデーは欧州を中心に休業施設が多く、日本の連休中は航空券・宿が高騰しやすい時期です。"),
        "summer-vacation": ([7, 8], "7〜8月（夏休み）", "北半球の夏や高地・北欧の過ごし方に加え、南半球の冬にあたる都市（シドニー・オークランド等）の気温差にご注意ください。"),
        "autumn-silverweek": (
            [9, 10, 11],
            "9〜11月（秋休み）",
            "欧州は10月最終日曜、米国は11月第1日曜に冬時間へ切り替わります。また中国の10月初旬（国慶節）や韓国の秋夕連休は混雑・料金上昇に注意が必要です。"
        ),
        "winter-newyear": ([12, 1, 2], "12〜2月（冬休み）", "12月25日・1月1日は欧米を中心に休業施設が多くなります。南半球は夏本番です。"),
        "first-time-safe": ([4, 5, 9, 10], "春秋目安", "公共交通やキャッシュレスが比較的整い、初めての海外でも動きやすい都市を集めています。"),
    }
    target_months, season_label, season_tip = season_meta.get(
        feat["slug"],
        (feat.get("target_months") or [9, 10, 11], feat.get("badge", "対象時期"), "")
    )

    autumn_reason_map = {
        "seoul": "夏の暑さや雨季が落ち着き、街歩き・ショッピング・グルメに心地よい秋シーズン。",
        "taipei": "猛暑や台風シーズンが和らぎ、夜市や街歩きを楽しみやすい秋が狙い目。",
        "shanghai": "過ごしやすい秋の一方、10月初旬（国慶節）は大型連休で混雑・料金上昇に注意。",
        "hanoi": "10〜11月は暑さと雨が落ち着き、街歩きがしやすい秋シーズン。",
        "kuala-lumpur": "通年高温多湿で秋はスコールが増える時期。雨具と冷房対策があると安心。",
        "new-york": "9〜10月は気候が落ち着き散策に好適。11月第1日曜に冬時間へ移行。",
        "boston": "秋は紅葉と涼しい空気が魅力。11月は肌寒くなるため上着が必要。",
        "paris": "9〜10月は暑さが和らぎ街歩きしやすい時期。10月最終日曜に冬時間へ移行。",
        "milan": "秋は街歩きや美術館巡りに心地よい季節。朝晩の冷え込みには羽織りを。",
        "madrid": "日中は穏やかな秋の日が多く、10月最終日曜に冬時間へ切り替わります。",
        "prague": "9〜10月は落ち着いた秋の街並み、11月はコートが活躍する肌寒さ。",
        "marrakech": "夏の猛暑が落ち着き観光しやすくなる秋。2026年9月20日からUTC+0固定（時差-9時間）。",
    }

    table_rows = []
    cards = []

    for c in selected:
        r = compute_city_star_ratings(c)
        snap = get_season_snapshot(c, target_months) if get_season_snapshot else None
        tz_label = season_tz_label(c, target_months) if season_tz_label else c.get("tz_diff_label", "-")
        if snap:
            temp_str = f"{snap['temp_str']}（雨 {snap['rain_days_str']}）"
            gear_str = snap["outfit"]
            tag_str = "・".join(snap["tags"]) if snap["tags"] else "穏やか"
            season_badge = f"{season_label}：{snap['label']} · {snap['temp_str']}（{snap['best_month_str']}）"
            autumn_note = autumn_reason_map.get(c["slug"], "") if feat["slug"] == "autumn-silverweek" else ""
            card_desc = (
                f"{season_label}は平均{snap['temp_str']}（降水目安 {snap['rain_days_str']}）で「{snap['label']}（{tag_str}）」。"
                f" {autumn_note}"
            ).strip()
        else:
            temp_str = "気候データ確認中"
            gear_str = "気温に応じた重ね着"
            season_badge = ""
            card_desc = c["climate"]

        airport_short = c["airport_access"]["cheapest"].split("（")[0]

        table_rows.append(
            f'<tr>'
            f'<td class="p-2.5 font-bold whitespace-nowrap" style="border-top: 1px solid var(--divider);"><a href="../../{c["slug"]}/" class="underline" style="color: var(--accent-text);">{c["name_ja"]}</a></td>'
            f'<td class="p-2.5 tabular-nums whitespace-nowrap" style="border-top: 1px solid var(--divider); color: var(--text-primary);">{temp_str}</td>'
            f'<td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{gear_str}</td>'
            f'<td class="p-2.5 tabular-nums whitespace-nowrap" style="border-top: 1px solid var(--divider); color: var(--text-secondary);">{tz_label}</td>'
            f'<td class="p-2.5" style="border-top: 1px solid var(--divider); color: var(--text-muted);">{airport_short}</td>'
            f'</tr>'
        )

        badge_html = (
            f'<span class="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full" style="background: var(--accent-soft); color: var(--accent-text);">{season_badge}</span>'
            if season_badge else ""
        )

        cards.append(
            f'<a href="../../{c["slug"]}/" class="ed-surface block p-4 space-y-2">'
            f'<div class="flex items-center justify-between gap-2">'
            f'<span class="font-bold text-sm" style="color: var(--text-primary);">{c["name_ja"]}</span>'
            f'<span class="text-[11px] font-semibold tabular-nums shrink-0" style="color: var(--accent-text);">{r["avg"]:.1f} / 5.0 <span class="text-[10px] font-normal ml-1" style="color: var(--text-muted);">{c["country_ja"]}</span></span>'
            f'</div>'
            + (f'<div>{badge_html}</div>' if badge_html else '')
            + f'<p class="text-[11px] leading-relaxed" style="color: var(--text-secondary);">{card_desc}</p>'
            f'<div class="text-[11px] flex flex-wrap gap-2 pt-1 tabular-nums" style="color: var(--text-muted); border-top: 1px solid var(--divider);">'
            f'<span>時差: {tz_label}</span><span>プラグ: {c["plug_type"]}</span><span>通貨: {c["currency_code"]}</span>'
            f'</div>'
            f'</a>'
        )

    season_tip_html = (
        f'<div class="ed-tint p-3.5 text-xs leading-relaxed" style="color: var(--text-secondary);">'
        f'<strong style="color: var(--text-primary);">{season_label}渡航の注意点：</strong>{season_tip}'
        f'</div>'
        if season_tip else ""
    )

    comparison_table_html = ""
    if selected:
        comparison_table_html = f"""
    <section class="space-y-2.5 reveal-section">
      <div class="flex items-baseline justify-between flex-wrap gap-1 pb-2" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm sm:text-base font-bold" style="color: var(--text-primary);">{season_label}の気温・服装・時差・空港アクセス比較表（全{len(selected)}都市）</h2>
        <span class="text-[11px]" style="color: var(--text-muted);">月別平年値から自動集計</span>
      </div>
      <div class="ed-surface overflow-x-auto">
        <table class="w-full text-left border-collapse text-xs">
          <thead>
            <tr style="background: var(--bg-tint); color: var(--text-muted);">
              <th class="p-2.5 font-semibold">都市</th>
              <th class="p-2.5 font-semibold">{season_label}の気温・雨</th>
              <th class="p-2.5 font-semibold">服装目安</th>
              <th class="p-2.5 font-semibold">日本との時差</th>
              <th class="p-2.5 font-semibold">空港アクセス目安</th>
            </tr>
          </thead>
          <tbody>{"".join(table_rows)}</tbody>
        </table>
      </div>
    </section>"""

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
    <div class="ed-surface p-5 space-y-2 anim-enter">
      <span class="text-[10px] font-semibold uppercase tracking-wider" style="color: var(--accent-text);">{feat['badge']}</span>
      <h1 class="text-xl sm:text-2xl font-bold">{feat['title']}</h1>
      <p class="text-xs leading-relaxed" style="color: var(--text-secondary);">{feat['desc']}</p>
    </div>

    {season_tip_html}
    {comparison_table_html}

    <section class="space-y-2.5">
      <div class="flex items-baseline justify-between pb-1.5" style="border-bottom: 1px solid var(--divider);">
        <h2 class="text-sm sm:text-base font-bold" style="color: var(--text-primary);">対象{len(selected)}都市の{season_label}ポイント</h2>
        <span class="text-[11px]" style="color: var(--text-muted);">タップで詳細へ</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">{"".join(cards)}</div>
    </section>

    {render_agoda_and_oooh_box(context_label=f"特集対象{len(selected)}都市")}
    {render_telecom_box(custom_note=f"特集の{len(selected)}都市へ渡航する際は、現地での地図・配車アプリ利用に向けて出発前にeSIMやローミングなどの通信手段を確認しておくとスムーズです。")}
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
    <div class="max-w-[780px] mx-auto px-4 py-2.5 flex items-center justify-between">
      <a href="../" class="inline-flex items-center gap-2 py-1 pr-2 rounded-lg" style="color: var(--text-primary);">
        <i data-lucide="arrow-left" class="w-4 h-4" style="color: var(--accent-text);"></i>
        <span class="font-extrabold text-sm sm:text-base">{SITE_NAME}</span>
      </a>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-6 space-y-6 text-xs sm:text-sm leading-relaxed" style="color: var(--text-secondary);">
    <h1 class="text-xl sm:text-2xl font-bold" style="color: var(--text-primary);">プライバシーポリシー・免責事項・運営者情報</h1>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">1. 免責事項（当サイトの情報について）</h2>
      <p>「{SITE_NAME}」（{SITE_URL}）に掲載している各国の時差、気象・気候データ、電圧・プラグ形状、チップ習慣、税金・免税制度、交通アクセス、為替レート、外務省危険情報・渡航情報等は、確認時点の調査データおよび外部APIをもとに作成しておりますが、最新性・正確性・完全性を保証するものではありません。</p>
      <p>ご渡航の際は、必ず<strong>外務省「海外安全ホームページ」</strong>、駐日各国大使館、およびご利用の航空会社・交通機関・宿泊施設等の公式最新情報をご自身でご確認ください。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">2. 広告の配信・アフィリエイトプログラムについて</h2>
      <p>当サイトは、第三者配信の広告サービス（Google AdSense）およびアフィリエイトプログラム（A8.net、Partnerize 等）に参加しており、提携リンク経由の申込・利用等により報酬を得る場合があります[cite: 3]。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">3. アクセス解析ツールについて</h2>
      <p>当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス（GA4）」を利用しています。データは匿名で収集されており、個人を特定するものではありません。</p>
    </section>
    <section class="ed-surface p-5 space-y-2">
      <h2 class="font-bold text-base" style="color: var(--text-primary);">4. 運営者情報・訂正のご連絡</h2>
      <p><strong>サイト名：</strong>{SITE_NAME} / <strong>URL：</strong>{SITE_URL} / <strong>運営：</strong>{SITE_NAME} 編集部</p>
      <p class="text-xs" style="color: var(--text-muted);">掲載情報の誤りや表記ゆれにお気づきの際は、運営窓口までお知らせいただけますと幸いです。</p>
    </section>
  </main>
  <script>lucide.createIcons();</script>
</body>
</html>"""


def build_index_html(cities: list, rates_data: dict, featured_compare_pairs: list) -> str:
    unique_regions = ["すべて"] + sorted(list({c["region"] for c in cities}))
    page_url = f"{SITE_URL}/"
    page_title = f"{SITE_NAME}｜世界{len(cities)}都市の時差・天気/1年カレンダー・コンセント・チップ・生活ルール"
    page_desc = f"海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・リアルタイム気温・1年カレンダー・コンセント・チップ計算機・生活マナー・最新為替・外務省危険情報を1画面で即解決。"
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
            vpn_badge = '<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--rose-bg); color: var(--rose-text);">通信確認推奨</span>'
        elif c["special_ui"] == "vpn_recommended":
            vpn_badge = '<span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--accent-soft); color: var(--accent-text);">VPN活用可</span>'
        else:
            vpn_badge = ""
        danger_dot = '<span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-semibold" style="background: var(--amber-bg); color: var(--amber-text);">注意喚起</span>' if c["danger_color"] != "emerald" else ""
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
            f'<div class="text-[10.5px] mt-1.5 flex items-center gap-x-2 gap-y-1 flex-wrap tabular-nums" style="color: var(--text-muted);">'
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
    .region-scroll-wrap {{ position: relative; display: flex; align-items: center; }}
    .region-scroll-wrap::after {{
      content: ""; position: absolute; top: 0; right: 0; bottom: 4px; width: 52px;
      background: linear-gradient(to right, transparent, var(--bg-canvas) 75%); pointer-events: none;
    }}
    .region-scroll-hint {{
      position: sticky; right: 2px; z-index: 2; display: inline-flex; align-items: center; justify-content: center;
      width: 20px; height: 20px; border-radius: 9999px; color: var(--text-muted); pointer-events: none; flex-shrink: 0;
    }}
    .sub-text-link {{
      display: inline-flex; align-items: center; gap: 4px; padding: 4px 2px; border-radius: var(--radius-sm);
      background-color: transparent; border: none; color: var(--text-muted); font-size: 11px; font-weight: 500;
      transition: color 0.15s ease;
    }}
    .sub-text-link:hover {{ color: var(--text-primary); }}
    .sub-text-link svg {{ transition: transform 0.3s var(--ease-out-expo); }}
    .sub-text-link[aria-expanded="true"] {{ color: var(--text-primary); font-weight: 600; }}
    .sub-text-link[aria-expanded="true"] svg {{ transform: rotate(180deg); }}
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
      <a href="./" class="font-extrabold text-sm flex items-center gap-2" style="color: var(--text-primary);">
        <img src="{FAVICON_URL}" alt="" width="22" height="22" class="w-5 h-5 rounded-md object-cover shrink-0" onerror="this.style.display='none'">
        <span>{SITE_NAME}</span>
      </a>
      <button id="theme-toggle" type="button" class="text-[11px] font-medium px-2.5 py-1 rounded-full flex items-center gap-1" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-secondary);">
        <i data-lucide="sun-moon" class="w-3.5 h-3.5"></i>
        <span id="theme-name">Light</span>
      </button>
    </div>
  </header>

  <main class="max-w-[780px] mx-auto px-4 pt-6 space-y-6">
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

    <div class="sticky-search-bar space-y-2.5 -mx-4 px-4">
      <div class="relative">
        <input id="search" type="text" autocomplete="off" placeholder="都市・国・ひらがな検索（例：ばり、ロンドン）"
          class="w-full p-3.5 rounded-xl text-sm focus:outline-none" style="background: var(--bg-surface); border: 1px solid var(--border-soft); color: var(--text-primary);">
        <div id="suggest-box" class="suggest-dropdown hidden"></div>
      </div>
      <div class="region-scroll-wrap">
        <div class="flex gap-1.5 overflow-x-auto pr-10 pb-1" style="scrollbar-width: none;">{region_buttons}</div>
        <span class="region-scroll-hint" aria-hidden="true"><i data-lucide="chevron-right" class="w-3.5 h-3.5"></i></span>
      </div>
    </div>

    <section class="space-y-3">
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
          <button type="button" class="suggest-item" data-href="./${{c.dataset.slug}}/">
            <span class="font-bold">${{c.dataset.name}}</span>
            <span style="color: var(--text-muted);">${{c.dataset.country}} →</span>
          </button>
        `).join('');
        suggestBox.classList.remove('hidden');
      }} else {{
        suggestBox.classList.add('hidden');
      }}
    }}

    suggestBox.addEventListener('pointerdown', (e) => {{
      const item = e.target.closest('.suggest-item');
      if (item && item.dataset.href) {{
        e.preventDefault();
        window.location.href = item.dataset.href;
      }}
    }});

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
