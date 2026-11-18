#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定・アフィリエイト・特集定義ファイル (config.py)
"""

SITE_URL = "https://tokou-pocket.com"
SITE_NAME = "渡航ポケット辞典"
GA4_ID = "G-2Q2NX4NSVQ"

# 姉妹サイト（相互リンク・SEO強化＆留学・長期滞在層の送客用）
SISTER_SITE_URL = "https://ryugaku-intern.com"
SISTER_SITE_NAME = "Atrium（海外留学・キャリア・現地リアル情報）"

# A8.net アフィリエイトリンク（5大案件完備）
AFFILIATE_ESIM_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+16VZM+2W74+NTJWY"
AFFILIATE_VPN_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+7QNN6+3YFI+674EQ"
AFFILIATE_CARD_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+BB99U+38L8+62MDE"
AFFILIATE_OOOH_URL = "https://px.a8.net/svt/ejp?a8mat=4BGOWJ+5YCTU+5OEM+5YRHE"
AFFILIATE_AGODA_URL = "https://px.a8.net/svt/ejp?a8mat=4BGOWK+1HL182+4X1W+5YRHE"

# A8.net インプレッション計測用ピクセルURL
A8_PIXEL_URLS = [
    "https://www16.a8.net/0.gif?a8mat=4BGO4G+7QNN6+3YFI+674EQ",
    "https://www11.a8.net/0.gif?a8mat=4BGO4G+16VZM+2W74+NTJWY",
    "https://www13.a8.net/0.gif?a8mat=4BGO4G+BB99U+38L8+62MDE",
    "https://www13.a8.net/0.gif?a8mat=4BGOWJ+5YCTU+5OEM+5YRHE",
    "https://www14.a8.net/0.gif?a8mat=4BGOWK+1HL182+4X1W+5YRHE",
]

# 自動生成する「人気2都市比較ページ」のペア定義
COMPARE_PAIRS = [
    ("seoul", "taipei", "アジア週末旅行の2大巨頭！物価・プラグ・治安・移動のしやすさを徹底比較"),
    ("bangkok", "singapore", "東南アジア人気トップ2！コスパ重視のバンコクか、快適・近未来のシンガポールか"),
    ("honolulu", "guam", "王道ビーチリゾート対決！時差・フライト・チップ・現地予算の違いまとめ"),
    ("london", "paris", "ヨーロッパ周遊の2大拠点！ユーロスターで繋がる2都市の物価・治安・電源比較"),
    ("rome", "barcelona", "南欧の人気観光都市対決！スリ対策・免税・気候・空港アクセスの違い"),
    ("los-angeles", "new-york", "アメリカ東西2大都市！時差・チップ・地下鉄/配車移動・気候の違いを即チェック"),
    ("bali", "phuket", "アジア屈指のアイランドリゾート対決！ベストシーズン・乾季と雨季・物価比較"),
    ("shanghai", "hong-kong", "中華圏の人気都市比較！ネット検閲（VPN必要性）・決済手段・電源の違い"),
    ("sydney", "auckland", "オセアニアの人気都市比較！治安・キャッシュレス・自然＆都市観光の違い"),
    ("dubai", "istanbul", "中東・ターキッシュの人気ハブ都市対決！気候・服装マナー・乗り継ぎ観光比較"),
]

# 自動生成する「季節・テーマ別まとめハブページ」の定義
FEATURE_PAGES = [
    {
        "slug": "winter-newyear",
        "title": "【年末年始・冬休み】海外旅行先おすすめ12都市｜気温・服装・電源・治安比較",
        "badge": "12月〜2月渡航向け",
        "desc": "年末年始や冬休みに人気の「暖かい常夏リゾート」「本場の冬・クリスマス街並みを楽しめる都市」を厳選。各都市の気候・コンセント・チップ・外務省危険情報を一覧で比較できます。",
        "cities": ["honolulu", "bangkok", "taipei", "singapore", "cebu", "bali", "sydney", "dubai", "london", "paris", "vienna", "new-york"]
    },
    {
        "slug": "graduation-spring",
        "title": "【卒業旅行・春休み】学生＆初海外におすすめ12都市｜予算・治安・事前準備まとめ",
        "badge": "2月〜3月・春渡航向け",
        "desc": "学生の卒業旅行や春休みの海外旅行で選ばれている世界12都市をピックアップ。初めての海外でも失敗しないホテル予約・通信（eSIM/VPN）・クレカ保険・プラグ形状を一括チェック！",
        "cities": ["seoul", "taipei", "bangkok", "da-nang", "guam", "honolulu", "paris", "rome", "barcelona", "london", "los-angeles", "cairo"]
    }
]
