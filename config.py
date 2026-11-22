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

FAVICON_FILENAME = "youka.png"
FAVICON_URL = f"{SITE_URL}/{FAVICON_FILENAME}"

# 姉妹サイト
SISTER_SITE_URL = "https://ryugaku-intern.com"
SISTER_SITE_NAME = "Atrium（海外留学・キャリア・現地リアル情報）"

# A8.net アフィリエイトリンク
AFFILIATE_ESIM_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+16VZM+2W74+NTJWY"
AFFILIATE_VPN_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+7QNN6+3YFI+674EQ"
AFFILIATE_CARD_URL = "https://px.a8.net/svt/ejp?a8mat=4BGO4G+BB99U+38L8+62MDE"
AFFILIATE_OOOH_URL = "https://px.a8.net/svt/ejp?a8mat=4BGOWJ+5YCTU+5OEM+5YRHE"
AFFILIATE_AGODA_URL = "https://px.a8.net/svt/ejp?a8mat=4BGOWK+1HL182+4X1W+5YRHE"
AFFILIATE_WISE_URL = "https://wise.prf.hn/click/camref:1011l6vLmr"

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

# 季節・テーマ別まとめハブページ定義（6特集）
# 任意キー: columns（比較表の列）, table_title, tip_title, card_title, card_mode("safety" で治安中心のカード）
FEATURE_PAGES = [
    {
        "slug": "winter-newyear",
        "title": "【年末年始・冬休み】海外旅行先おすすめ12都市｜気温・服装・時差・空港アクセス比較",
        "badge": "12月〜2月渡航",
        "desc": "年末年始や冬休みに人気の「暖かい常夏リゾート」と「冬のイルミネーション・街並みを楽しめる都市」を厳選。12〜2月の気温、服装の目安、日本との時差、空港アクセスを一覧で比較できます。",
        "cities": ["honolulu", "bangkok", "taipei", "singapore", "cebu", "bali", "sydney", "dubai", "london", "paris", "vienna", "new-york"],
    },
    {
        "slug": "graduation-spring",
        "title": "【卒業旅行・春休み】学生＆初海外におすすめ12都市｜気温・治安・時差・空港アクセス比較",
        "badge": "2月〜3月渡航",
        "desc": "卒業旅行や春休みの海外渡航で選ばれている世界12都市をピックアップ。2〜3月の気温と服装、治安の目安、日本との時差、空港アクセスを一覧で確認できます。",
        "cities": ["seoul", "taipei", "bangkok", "da-nang", "guam", "honolulu", "paris", "rome", "barcelona", "london", "los-angeles", "madrid"],
        "columns": ["climate", "dress", "safety", "tz", "airport"],
    },
    {
        "slug": "golden-week",
        "title": "【GW（ゴールデンウィーク）】4〜5月に過ごしやすい海外12都市｜気温・時差・空港アクセス比較",
        "badge": "4月〜5月渡航",
        "desc": "ヨーロッパの春やアジアの乾季など、4月末〜5月の大型連休に気候が過ごしやすい12都市を厳選。4〜5月の気温、日本との時差、空港アクセスを一覧で比較できます。",
        "cities": ["seoul", "taipei", "hong-kong", "lisbon", "bali", "honolulu", "paris", "rome", "london", "barcelona", "istanbul", "vancouver"],
    },
    {
        "slug": "summer-vacation",
        "title": "【夏休み・お盆】7〜8月に爽やかな都市＆乾季リゾート12選｜気温・服装・時差・空港アクセス比較",
        "badge": "7月〜8月渡航",
        "desc": "日本の猛暑を避けて涼しく過ごせる北欧・カナダや、夏が乾季のバリ島・ハワイなど12都市の7〜8月の気温、服装、時差、空港アクセスをまとめました。南半球は冬にあたる都市も含みます。",
        "cities": ["bali", "honolulu", "singapore", "vancouver", "banff", "london", "helsinki", "stockholm", "zurich", "munich", "sydney", "auckland"],
    },
    {
        "slug": "autumn-silverweek",
        "title": "【秋休み・9〜11月】気候が過ごしやすいおすすめ海外12都市｜気温・服装・時差・チップ比較",
        "badge": "9月〜11月渡航",
        "desc": "暑さが落ち着き、街歩きやグルメに向く秋シーズンのおすすめ都市。9〜11月の気温・服装・時差と、各国のチップ習慣をまとめてチェックできます。",
        "cities": ["seoul", "taipei", "shanghai", "hanoi", "istanbul", "new-york", "boston", "paris", "milan", "madrid", "prague", "marrakech"],
        "columns": ["climate", "dress", "tz", "tip", "airport"],
    },
    {
        "slug": "first-time-safe",
        "title": "【初海外・一人旅】治安が安定＆移動がわかりやすい世界の安心12都市まとめ",
        "badge": "初心者・一人旅向け",
        "desc": "初めての海外旅行や一人旅でも安心感が高い都市を、治安評価・外務省危険情報・緊急通報番号・空港アクセス・英語の通じやすさで比較。公共交通やキャッシュレスが整った12都市です。",
        "cities": ["taipei", "seoul", "singapore", "honolulu", "guam", "sydney", "melbourne", "auckland", "vancouver", "zurich", "vienna", "helsinki"],
        "columns": ["safety", "danger", "emergency", "airport", "english"],
        "table_title": "治安・危険情報・緊急通報・空港アクセス・英語の比較表",
        "tip_title": "選び方のポイント",
        "card_title": "対象12都市の安心ポイント",
        "card_mode": "safety",
    },
]

# 近隣都市ロジック修正（座標追加）前に公開されていた比較ページのうち、現在は生成されないURL。
# 旧URLにアクセスした人・検索エンジン向けに、移動案内ページ（meta refresh + canonical）を出力する。
LEGACY_COMPARE_SLUGS = [
    "adelaide-vs-sydney",
    "almaty-vs-seoul",
    "ankara-vs-istanbul",
    "antalya-vs-istanbul",
    "athens-vs-santorini",
    "atlanta-vs-honolulu",
    "auckland-vs-queenstown",
    "bath-vs-london",
    "bengaluru-vs-delhi",
    "berlin-vs-frankfurt",
    "bologna-vs-rome",
    "boracay-vs-cebu",
    "bordeaux-vs-paris",
    "boston-vs-honolulu",
    "brisbane-vs-sydney",
    "budapest-vs-london",
    "buenos-aires-vs-cancun",
    "cairns-vs-sydney",
    "cappadocia-vs-istanbul",
    "chengdu-vs-shanghai",
    "chiang-mai-vs-bangkok",
    "chiang-rai-vs-bangkok",
    "chicago-vs-honolulu",
    "chongqing-vs-shanghai",
    "christchurch-vs-auckland",
    "cologne-vs-frankfurt",
    "colombo-vs-seoul",
    "copenhagen-vs-london",
    "daegu-vs-seoul",
    "dalian-vs-shanghai",
    "dallas-vs-honolulu",
    "delhi-vs-mumbai",
    "doha-vs-dubai",
    "dusseldorf-vs-frankfurt",
    "edinburgh-vs-london",
    "fes-vs-marrakech",
    "florence-vs-rome",
    "gold-coast-vs-sydney",
    "granada-vs-barcelona",
    "guangzhou-vs-shanghai",
    "gyeongju-vs-seoul",
    "hamburg-vs-frankfurt",
    "hangzhou-vs-shanghai",
    "harbin-vs-shanghai",
    "hobart-vs-sydney",
    "houston-vs-honolulu",
    "hualien-vs-taipei",
    "hue-vs-ho-chi-minh",
    "innsbruck-vs-vienna",
    "interlaken-vs-zurich",
    "jaipur-vs-delhi",
    "jakarta-vs-bali",
    "jeju-vs-seoul",
    "johor-bahru-vs-kuala-lumpur",
    "kathmandu-vs-seoul",
    "koh-samui-vs-bangkok",
    "kona-vs-honolulu",
    "kota-kinabalu-vs-kuala-lumpur",
    "krabi-vs-bangkok",
    "langkawi-vs-kuala-lumpur",
    "las-vegas-vs-honolulu",
    "liverpool-vs-london",
    "lucerne-vs-zurich",
    "lyon-vs-paris",
    "madrid-vs-barcelona",
    "malaga-vs-barcelona",
    "male-vs-seoul",
    "manchester-vs-london",
    "manila-vs-cebu",
    "marseille-vs-paris",
    "maui-vs-honolulu",
    "miami-vs-honolulu",
    "milan-vs-rome",
    "montreal-vs-vancouver",
    "mykonos-vs-athens",
    "nadi-vs-sydney",
    "nice-vs-paris",
    "noumea-vs-sydney",
    "orlando-vs-honolulu",
    "palawan-vs-cebu",
    "palermo-vs-rome",
    "penang-vs-kuala-lumpur",
    "perth-vs-sydney",
    "prague-vs-london",
    "qingdao-vs-shanghai",
    "quebec-city-vs-vancouver",
    "reykjavik-vs-london",
    "san-diego-vs-honolulu",
    "san-francisco-vs-honolulu",
    "san-sebastian-vs-barcelona",
    "santiago-vs-cancun",
    "seattle-vs-honolulu",
    "seville-vs-barcelona",
    "shenzhen-vs-shanghai",
    "stockholm-vs-london",
    "strasbourg-vs-paris",
    "surabaya-vs-bali",
    "suzhou-vs-shanghai",
    "tahiti-vs-sydney",
    "taichung-vs-taipei",
    "tainan-vs-taipei",
    "tashkent-vs-seoul",
    "uluru-vs-sydney",
    "uyuni-vs-cancun",
    "valencia-vs-barcelona",
    "valletta-vs-london",
    "venice-vs-rome",
    "washington-dc-vs-honolulu",
    "wellington-vs-auckland",
    "xiamen-vs-shanghai",
    "xian-vs-shanghai",
    "yogyakarta-vs-bali",
    "zagreb-vs-dubrovnik",
    "zermatt-vs-zurich",
    "zurich-vs-geneva",
]

# 自動生成した比較ページ（COMPARE_PAIRS以外）を検索に出すか。
# False の間は、両都市に city_vibe/best_for（手書きの個性文）がある場合だけ index 対象にする。
INDEX_AUTO_COMPARE_PAGES = False
