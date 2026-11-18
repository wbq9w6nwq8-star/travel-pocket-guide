#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定・アフィリエイト・特集・比較ペア定義ファイル (config.py)
"""

SITE_URL = "https://tokou-pocket.com"
SITE_NAME = "渡航ポケット辞典"
GA4_ID = "G-2Q2NX4NSVQ"

# OGP共有サムネイル画像ファイル名（リポジトリ直下に ogp.png として配置）
OGP_IMAGE_FILENAME = "ogp.png"
OGP_IMAGE_URL = f"{SITE_URL}/{OGP_IMAGE_FILENAME}"

# 姉妹サイト
SISTER_SITE_URL = "https://ryugaku-intern.com"
SISTER_SITE_NAME = "Atrium（海外留学・キャリア・現地リアル情報）"

# A8.net アフィリエイトリンク
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

# 主要2都市比較ページ定義（20ペア＋全都市自動ペアリングと連動）
COMPARE_PAIRS = [
    ("seoul", "taipei", "アジア週末旅行の2大定番。物価・プラグ・治安・移動アプリの使い勝手を比較"),
    ("seoul", "busan", "韓国2大都市比較。空港アクセス・都市規模・グルメ・観光日数の目安"),
    ("taipei", "kaohsiung", "台湾2大都市比較。気候の違い・MRT移動・夜市・滞在費用の目安"),
    ("bangkok", "singapore", "東南アジア人気トップ2。物価コスパのバンコクとインフラ最先端のシンガポールを比較"),
    ("bangkok", "ho-chi-minh", "東南アジア活気都市対決。配車アプリ・屋台グルメ・物価・ベストシーズン比較"),
    ("hanoi", "ho-chi-minh", "ベトナム南北2大都市。四季のあるハノイと常夏のホーチミンの気候・移動比較"),
    ("da-nang", "cebu", "アジア近距離ビーチリゾート対決。フライト時間・物価・乾季と雨季の違い"),
    ("bali", "phuket", "本格アイランドリゾート比較。ベストシーズン（乾季のズレ）・物価・移動手段"),
    ("kuala-lumpur", "singapore", "マレー半島2大都市。ホテル価格差・プラグ・治安・周遊アクセスの違い"),
    ("hong-kong", "macau", "フェリーや橋で繋がる2都市比較。通貨・電源・ネット環境・観光スタイルの違い"),
    ("shanghai", "beijing", "中国2大都市比較。ネット検閲対策・決済アプリ・気候・空港アクセスの違い"),
    ("honolulu", "guam", "王道ビーチリゾート比較。時差・フライト時間・チップ・現地物価の違い"),
    ("los-angeles", "new-york", "アメリカ東西2大都市。時差・チップ・地下鉄と配車移動・気候の違い"),
    ("vancouver", "toronto", "カナダ東西2大都市。冬の寒さ・時差・治安・空港からの鉄道アクセス比較"),
    ("london", "paris", "ヨーロッパ周遊の2大拠点。ユーロスター移動・プラグ形状・物価・スリ対策比較"),
    ("rome", "barcelona", "南欧の人気観光都市対決。免税制度・スリ対策・気候・食事マナーの違い"),
    ("paris", "rome", "欧州王道2大都市。電圧・水道水・チップ・美術館＆遺跡観光の移動比較"),
    ("frankfurt", "munich", "ドイツ2大拠点比較。空港直結アクセス・治安・日曜営業ルールの確認"),
    ("sydney", "melbourne", "オーストラリア2大都市。気候・空港鉄道/バス・カフェ文化・キャッシュレス比較"),
    ("dubai", "istanbul", "中東・トルコの人気ハブ都市対決。通信規制・服装マナー・ベストシーズン比較"),
]

# 季節・テーマ別まとめハブページ定義（6特集に拡充）
FEATURE_PAGES = [
    {
        "slug": "winter-newyear",
        "title": "【年末年始・冬休み】海外旅行先おすすめ12都市｜気温・服装・電源・治安比較",
        "badge": "12月〜2月渡航",
        "desc": "年末年始や冬休みに人気の「暖かい常夏リゾート」と「冬のイルミネーション・街並みを楽しめる都市」を厳選。気候・コンセント・チップ・外務省危険情報を一覧で比較できます。",
        "cities": ["honolulu", "bangkok", "taipei", "singapore", "cebu", "bali", "sydney", "dubai", "london", "paris", "vienna", "new-york"]
    },
    {
        "slug": "graduation-spring",
        "title": "【卒業旅行・春休み】学生＆初海外におすすめ12都市｜予算・治安・事前準備まとめ",
        "badge": "2月〜3月渡航",
        "desc": "卒業旅行や春休みの海外渡航で選ばれている世界12都市をピックアップ。ホテル予約・通信（eSIM/VPN）・カード保険・プラグ形状を一括確認できます。",
        "cities": ["seoul", "taipei", "bangkok", "da-nang", "guam", "honolulu", "paris", "rome", "barcelona", "london", "los-angeles", "cairo"]
    },
    {
        "slug": "golden-week",
        "title": "【GW（ゴールデンウィーク）】4〜5月がベストシーズンの海外12都市｜気候・時差・移動比較",
        "badge": "4月〜5月渡航",
        "desc": "ヨーロッパの春やアジアの乾季など、4月末〜5月の大型連休に気候が最も安定する12都市を厳選。休みの日数に合わせた時差・空港アクセス一覧です。",
        "cities": ["seoul", "taipei", "hong-kong", "bangkok", "bali", "honolulu", "paris", "rome", "london", "barcelona", "istanbul", "vancouver"]
    },
    {
        "slug": "summer-vacation",
        "title": "【夏休み・お盆】7〜8月に爽やかな都市＆乾季リゾート12選｜紫外線・冷房・服装対策",
        "badge": "7月〜8月渡航",
        "desc": "日本の猛暑を避けて涼しく過ごせる北欧・カナダ・オセアニアや、夏が乾季ベストシーズンのバリ島・ハワイなど12都市の気候・電源・治安まとめ。",
        "cities": ["bali", "honolulu", "singapore", "vancouver", "banff", "london", "helsinki", "stockholm", "zurich", "munich", "sydney", "auckland"]
    },
    {
        "slug": "autumn-silverweek",
        "title": "【秋休み・9〜11月】気候快適＆旅費が落ち着くおすすめ海外12都市｜マナー・免税比較",
        "badge": "9月〜11月渡航",
        "desc": "台風や猛暑が落ち着き、街歩きやグルメに最適な秋シーズンのおすすめ都市。各国の免税（Tax Free）基準額やチップ習慣もまとめてチェック。",
        "cities": ["seoul", "taipei", "shanghai", "hanoi", "kuala-lumpur", "new-york", "boston", "paris", "milan", "madrid", "prague", "marrakech"]
    },
    {
        "slug": "first-time-safe",
        "title": "【初海外・一人旅】治安が安定＆移動がわかりやすい世界の安心12都市まとめ",
        "badge": "初心者・一人旅向け",
        "desc": "初めての海外旅行や一人旅でも安心感が高い、外務省危険情報レベル0・公共交通とキャッシュレスが発達した12都市の生活ルール・緊急連絡先一覧。",
        "cities": ["taipei", "seoul", "singapore", "honolulu", "guam", "sydney", "melbourne", "auckland", "vancouver", "zurich", "vienna", "helsinki"]
    }
]
