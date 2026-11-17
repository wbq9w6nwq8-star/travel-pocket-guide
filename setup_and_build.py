#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渡航ポケット辞典（世界130都市プログラムSEOサイト）オールインワン生成スクリプト
- GTM (GTM-TJ4RTPWB) 完全組込済み
- 130都市対応・ひらがな＆予測変換サジェスト検索対応
- 国・地域別カスタムUI（中国VPNカード、欧米キャッシュレス＆チップ、水道水＆医療保険）
- 外務省「海外安全ホームページ」・たびレジ・現地日本大使館/領事館情報搭載
"""

import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ==========================================
# 1. 基本設定・アフィリエイトリンク設定
# ==========================================
SITE_URL = "https://tokou-pocket.com"
SITE_NAME = "渡航ポケット辞典"
GTM_ID = "GTM-TJ4RTPWB"

AFFILIATE_ESIM_URL = "#YOUR_ESIM_AFFILIATE_LINK"
AFFILIATE_VPN_URL = "#YOUR_VPN_AFFILIATE_LINK"
AFFILIATE_CARD_URL = "#YOUR_CARD_AFFILIATE_LINK"
AFFILIATE_INSURANCE_URL = "#YOUR_INSURANCE_AFFILIATE_LINK"

# ==========================================
# 2. 国・地域別ベースプロファイル（外務省・大使館・地域特性UI対応）
# ==========================================
COUNTRY_PROFILES = {
    "KR": {
        "country_ja": "韓国", "country_kana": "かんこく コリア", "region": "アジア",
        "plug": "C/SE", "voltage": "220V", "freq": "60Hz", "trans": False,
        "curr": "KRW", "curr_ja": "ウォン", "sym": "₩",
        "tip": "none", "tip_badge": "不要", "tip_detail": "韓国にチップの習慣はありません。高級ホテルや一部レストランではサービス料10%が自動加算される場合があります。",
        "tax": "付加価値税(VAT)10%。Tax Free加盟店で15,000ウォン以上購入時、パスポート提示で即時還付または空港キオスク還付が可能。",
        "water": False, "water_note": "水道水はそのまま飲まず市販のミネラルウォーター推奨。飲食店の無料の水は浄水器の水なので安心です。",
        "emerg": "警察112 / 救急・消防119 / 観光通訳案内1330（日本語対応）",
        "apps": ["NAVERマップ（必須・Googleマップ徒歩ナビ非対応）", "Kakao T（タクシー）", "WOWPASS / NAMANE"],
        "embassy": "在大韓民国日本国大使館（ソウル）/ 在釜山総領事館 / 在済州総領事館（代表: +82-2-2170-5200）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_003.html",
        "safety_note": "全体的に治安は良好ですが、繁華街（弘大・梨泰院・明洞等）での夜間の一人歩きやぼったくりタクシー、大規模集会・デモ周辺への接近に注意してください。",
        "special_ui": "korea_nav"
    },
    "TW": {
        "country_ja": "台湾", "country_kana": "たいわん たいぺい", "region": "アジア",
        "plug": "A", "voltage": "110V", "freq": "60Hz", "trans": False,
        "curr": "TWD", "curr_ja": "ニュー台湾ドル", "sym": "NT$",
        "tip": "none", "tip_badge": "不要", "tip_detail": "基本的に不要。レストランでは会計に10%のサービス料が含まれることが多いです。",
        "tax": "営業税5%。特定マークのある店舗で同日2,000台湾ドル以上購入すると空港等で還付申請が可能。",
        "water": False, "water_note": "水道水の直接飲用は不可。必ずミネラルウォーターを購入するか煮沸してください。",
        "emerg": "警察110 / 救急・消防119",
        "apps": ["Uber", "Googleマップ", "台湾公車通（バス）"],
        "embassy": "日本台湾交流協会 台北事務所（+886-2-2713-8000）/ 高雄事務所（+886-7-771-4008）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_006.html",
        "safety_note": "治安は非常に良好ですが、夜市など混雑場所でのスリや、バイクのすり抜け・交通マナーの違いによる接触事故に十分注意してください。",
        "special_ui": "standard"
    },
    "TH": {
        "country_ja": "タイ", "country_kana": "たい ばんこく", "region": "アジア",
        "plug": "A/B3/C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "THB", "curr_ja": "バーツ", "sym": "฿",
        "tip": "optional", "tip_badge": "気持ち程度（20〜100B）", "tip_detail": "屋台や食堂は不要。マッサージは50〜100バーツ、ホテルのポーターやベッドメイクは20〜50バーツ程度がスマート。",
        "tax": "VAT 7%。VAT Refund加盟店で同日2,000バーツ以上購入すると空港で還付手続き可能。",
        "water": False, "water_note": "水道水は飲用不可。屋台の氷も衛生的な店舗以外は注意が必要です。",
        "emerg": "観光警察1155（日本語通訳あり）/ 警察191 / 救急1669",
        "apps": ["Grab（配車・デリバリー必須）", "Bolt（Grabより安い配車）", "Googleマップ"],
        "embassy": "在タイ日本国大使館（バンコク: +66-2-207-8500）/ 在チェンマイ総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_007.html",
        "safety_note": "王室に対する不敬言動は厳罰の対象となります。また電子タバコの持ち込み・所持は法律で厳しく禁止されており高額な罰金・逮捕対象となるため絶対持ち込まないでください。",
        "special_ui": "standard"
    },
    "SG": {
        "country_ja": "シンガポール", "country_kana": "しんがぽーる", "region": "アジア",
        "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "SGD", "curr_ja": "シンガポールドル", "sym": "S$",
        "tip": "none", "tip_badge": "不要（サ料10%込）", "tip_detail": "原則不要。ほとんどのレストランやホテルで10%のサービス料が自動で加算されます。",
        "tax": "GST 9%。加盟店で100S$以上購入時、チャンギ空港の電子キオスク(eTRS)で簡単に免税還付が可能。",
        "water": True, "water_note": "水道水はWHO基準を満たしておりそのまま飲用可能ですが、気になる場合は市販水を推奨。",
        "emerg": "警察999 / 救急・消防995",
        "apps": ["Grab", "Gojek", "Citymapper"],
        "embassy": "在シンガポール日本国大使館（+65-6235-8855）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_005.html",
        "safety_note": "世界トップクラスの治安ですが、チューインガムの持ち込み禁止、電子タバコの所持禁止、指定場所以外での喫煙・ポイ捨て・横断歩道外の横断に対する高額罰金に注意してください。",
        "special_ui": "standard"
    },
    "VN": {
        "country_ja": "ベトナム", "country_kana": "べとなむ", "region": "アジア",
        "plug": "A/C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "VND", "curr_ja": "ドン", "sym": "₫",
        "tip": "optional", "tip_badge": "気持ち程度（スパ・高級店）", "tip_detail": "ローカル店は不要。スパやマッサージでは50,000〜100,000ドン程度渡すのが一般的。",
        "tax": "VAT 8〜10%。対象店舗で200万ドン以上購入時、国際空港で85%相当のVAT還付が可能。",
        "water": False, "water_note": "水道水は飲用不可。歯磨きやうがいもミネラルウォーターを使う方が安心です。",
        "emerg": "警察113 / 消防114 / 救急115",
        "apps": ["Grab（ぼったくり防止に絶対必須）", "Be", "Googleマップ"],
        "embassy": "在ベトナム日本国大使館（ハノイ: +84-24-3846-3000）/ 在ホーチミン総領事館 / 在ダナン総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_015.html",
        "safety_note": "バイクによるスマホのひったくり（歩きスマホ厳禁）や、流しの白タク・シクロによる法外な料金請求が多発しています。移動は必ずGrabアプリを利用してください。",
        "special_ui": "standard"
    },
    "PH": {
        "country_ja": "フィリピン", "country_kana": "ふぃりぴん", "region": "アジア",
        "plug": "A/B/C", "voltage": "220V", "freq": "60Hz", "trans": False,
        "curr": "PHP", "curr_ja": "ペソ", "sym": "₱",
        "tip": "optional", "tip_badge": "10%程度（サ料別の場合）", "tip_detail": "レシートにService Charge(SC)が含まれていなければ会計の10%程度。マッサージやポーターは20〜50ペソ。",
        "tax": "VAT 12%。観光客向けの免税還付制度は限定的。",
        "water": False, "water_note": "水道水は飲用不可。市販のペットボトル水を必ず購入してください。",
        "emerg": "緊急通報911（警察・救急・消防共通）",
        "apps": ["Grab（安全移動に絶対必須）", "JoyRide", "Googleマップ"],
        "embassy": "在フィリピン日本国大使館（マニラ: +63-2-8551-5710）/ 在セブ総領事館（+63-32-231-7321）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_013.html",
        "safety_note": "流しのタクシーやジプニーでの強盗・ぼったくり被害や、スリ・睡眠薬強盗に厳重注意。移動は流しのタクシーを避け、必ずGrabアプリで配車してください。",
        "special_ui": "standard"
    },
    "MY": {
        "country_ja": "マレーシア", "country_kana": "まれーしあ", "region": "アジア",
        "plug": "BF", "voltage": "240V", "freq": "50Hz", "trans": False,
        "curr": "MYR", "curr_ja": "リンギット", "sym": "RM",
        "tip": "none", "tip_badge": "不要", "tip_detail": "基本的に不要。レストランやホテルでは10%のサービス料が含まれています。",
        "tax": "SST（売上・サービス税）6〜8%。原則として旅行者向けの免税還付制度はなし。",
        "water": False, "water_note": "水道水は配管が古い場合があるため、そのまま飲まずミネラルウォーターまたは煮沸を推奨。",
        "emerg": "警察・救急999 / 消防994",
        "apps": ["Grab（圧倒的シェア・必須）", "AirAsia MOVE", "Googleマップ"],
        "embassy": "在マレーシア日本国大使館（クアラルンプール: +60-3-2177-2600）/ 在ペナン総領事館 / 在コタキナバル領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_017.html",
        "safety_note": "比較的治安は安定していますが、歩道側からのバイクによるバッグひったくりに注意。車道側と反対の手にカバンを持つようにしてください。",
        "special_ui": "standard"
    },
    "ID": {
        "country_ja": "インドネシア", "country_kana": "いんどねしあ", "region": "アジア",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "IDR", "curr_ja": "ルピア", "sym": "Rp",
        "tip": "optional", "tip_badge": "気持ち程度（5〜10%）", "tip_detail": "サービス料込のレストランは不要。スパやドライバー、ポーターには10,000〜50,000ルピア程度渡すと喜ばれます。",
        "tax": "VAT 11%。「VAT Refund for Tourists」加盟店で一定額以上購入すると主要空港で還付可能。",
        "water": False, "water_note": "水道水は絶対に飲用不可（バリ腹の原因になります）。うがいや歯磨きもペットボトル水を推奨。",
        "emerg": "総合緊急112 / 警察110 / 救急118",
        "apps": ["Grab", "Gojek（バイク・車・配達すべて対応）", "Bluebird（信頼できるタクシー）"],
        "embassy": "在インドネシア日本国大使館（ジャカルタ: +62-21-3192-4308）/ 在デンパサール（バリ）総領事館（+62-361-227628）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_002.html",
        "safety_note": "街中の無認可両替所での紙幣抜き取り詐欺（高レートで誘う手口）や、バイクによるスマホひったくりが多発。両替は銀行または公認両替所を利用してください。",
        "special_ui": "standard"
    },
    "HK": {
        "country_ja": "香港", "country_kana": "ほんこん", "region": "アジア",
        "plug": "BF", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "HKD", "curr_ja": "香港ドル", "sym": "HK$",
        "tip": "optional", "tip_badge": "端数〜10%（サ料別の場合）", "tip_detail": "多くの飲食店で10%のサービス料（加一服務費）が加算されます。タクシーは端数切り上げ、ポーターは10〜20HKD。",
        "tax": "香港は消費税・付加価値税がないフリーポートのため、街中すべての買い物が最初から免税価格です。",
        "water": False, "water_note": "水道水は基準を満たしていますが、ビル配管の都合上、煮沸するかミネラルウォーターの購入が一般的です。",
        "emerg": "警察・救急・消防 999",
        "apps": ["MTR Mobile", "Uber", "オクトパス（Octopus for Tourists）"],
        "embassy": "在香港日本国総領事館（+852-2522-1184）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_016.html",
        "safety_note": "治安は良好ですが、政治的な集会や撮影禁止エリアの撮影には十分注意してください。また加熱式・電子タバコの持ち込みは法律で禁止されています。",
        "special_ui": "standard"
    },
    "MO": {
        "country_ja": "マカオ", "country_kana": "まかお", "region": "アジア",
        "plug": "BF", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "MOP", "curr_ja": "パタカ（香港ドルも流通）", "sym": "MOP$",
        "tip": "optional", "tip_badge": "端数〜10%", "tip_detail": "香港と同様、10%のサービス料が含まれる店舗が多数。香港ドルがほぼ1:1でそのまま使えます。",
        "tax": "消費税はなく、全域で免税価格での買い物が可能です。",
        "water": False, "water_note": "水道水の直接飲用は避け、ホテルの無料ボトル水や市販水を利用してください。",
        "emerg": "警察・救急・消防 999",
        "apps": ["マカオ電召（タクシー）", "巴士報站（バス）"],
        "embassy": "在香港日本国総領事館（マカオ兼轄: +852-2522-1184）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_016.html",
        "safety_note": "カジノ周辺を含め治安は良好ですが、スリや置き引きには基本的な注意を払ってください。",
        "special_ui": "standard"
    },
    "CN": {
        "country_ja": "中国", "country_kana": "ちゅうごく チャイナ", "region": "アジア",
        "plug": "A/O", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "CNY", "curr_ja": "人民元", "sym": "元",
        "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。現金よりもAlipayやWeChat Payの事前登録（日本のクレカ紐付け）が絶対必須です。",
        "tax": "増値税13%。Tax Free指定店で500元以上購入時、空港で還付手続きが可能。",
        "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。",
        "emerg": "警察110 / 救急120 / 消防119",
        "apps": ["Alipay（決済・DiDi配車・地下鉄すべて完結）", "WeChat（微信）", "高徳地図 / 百度地図（Googleマップはズレるため必須）"],
        "embassy": "在中国日本国大使館（北京: +86-10-8531-9800）/ 上海・広州・瀋陽・重慶・青島・大連の各総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_009.html",
        "safety_note": "【重要】ネット検閲（グレートファイアウォール）により、現地のWi-Fiや一般SIMではLINE・Google・Instagram・YouTube・X等が一切使えません。必ず日本出発前に「ローミング型eSIM」または「中国対応VPN」を準備してください。また軍事施設等の撮影は厳禁です。",
        "special_ui": "china_vpn"
    },
    "IN": {
        "country_ja": "インド", "country_kana": "いんど", "region": "アジア",
        "plug": "C/BF/B3", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "INR", "curr_ja": "インドルピー", "sym": "₹",
        "tip": "optional", "tip_badge": "5〜10%（高級店・ドライバー）", "tip_detail": "中級〜高級レストランでサービス料が含まれない場合は会計の5〜10%。ポーターや専属ドライバーには50〜200ルピー程度。",
        "tax": "GST 5〜28%（品目により異なる）。",
        "water": False, "water_note": "水道水は厳禁。ペットボトル購入時もキャップが未開封（密閉されているか）必ず確認してください。",
        "emerg": "総合緊急112 / 警察100 / 救急102",
        "apps": ["Uber（オートリキシャも呼べて交渉不要）", "Ola", "Googleマップ"],
        "embassy": "在インド日本国大使館（ニューデリー: +91-11-4610-4610）/ 在ムンバイ・チェンナイ・コルカタ・ベンガルール各総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_001.html",
        "safety_note": "空港や主要駅での悪質な客引き（「ホテルが閉鎖された」「チケット売り場はこっち」等の詐欺）に厳重注意。見知らぬ人から勧められた飲食物は睡眠薬強盗の危険があるため絶対に口にしないでください。",
        "special_ui": "standard"
    },
    "KH": {
        "country_ja": "カンボジア", "country_kana": "かんぼじあ", "region": "アジア",
        "plug": "A/C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "USD", "curr_ja": "米ドル（現地通貨リエル併用）", "sym": "$",
        "tip": "optional", "tip_badge": "1〜2ドル程度", "tip_detail": "ホテルのポーターやマッサージ、遺跡ガイドには1〜5米ドル程度。街中では米ドル紙幣が流通（少しでも破れや汚れがあるドル札は受取拒否されるため新札を用意）。",
        "tax": "VAT 10%。",
        "water": False, "water_note": "水道水は飲用不可。ミネラルウォーターを常備してください。",
        "emerg": "警察117 / 消防118 / 救急119",
        "apps": ["Grab（トゥクトゥクも定額で呼べる）", "PassApp"],
        "embassy": "在カンボジア日本国大使館（プノンペン: +855-23-217-161）/ 在シェムリアップ領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_004.html",
        "safety_note": "トゥクトゥク乗車中に外側からカバンやスマホをバイクにひったくられる被害が多発しています。乗車中はスマホを道路側に出さないでください。",
        "special_ui": "standard"
    },
    "LK": {
        "country_ja": "スリランカ", "country_kana": "すりらんか", "region": "アジア",
        "plug": "BF/B3/C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "LKR", "curr_ja": "スリランカルピー", "sym": "Rs",
        "tip": "optional", "tip_badge": "10%程度", "tip_detail": "ポーターやドライバー、ベッドメイクには100〜500ルピー程度渡す習慣があります。",
        "tax": "VAT 18%。",
        "water": False, "water_note": "水道水は飲用不可。市販のボトル水を利用してください。",
        "emerg": "警察119 / 救急1990",
        "apps": ["PickMe（スリランカ版Grab）", "Uber"],
        "embassy": "在スリランカ日本国大使館（コロンボ: +94-11-2693831）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_006.html",
        "safety_note": "仏像に背を向けて記念撮影する行為は不敬とされトラブルになるため禁止されています。スリーウィーラー利用時は配車アプリPickMeが安全です。",
        "special_ui": "standard"
    },
    "NP": {
        "country_ja": "ネパール", "country_kana": "ねぱーる", "region": "アジア",
        "plug": "C/B3", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "NPR", "curr_ja": "ネパールルピー", "sym": "Rs",
        "tip": "optional", "tip_badge": "10%程度（ガイド・高級店）", "tip_detail": "トレッキングのガイドやポーター、観光客向けレストランでは10%程度のチップが一般的です。",
        "tax": "VAT 13%。",
        "water": False, "water_note": "水道水は飲用不可。必ず密閉されたミネラルウォーターを購入してください。",
        "emerg": "警察100 / 救急102 / 観光警察1144",
        "apps": ["Pathao", "InDrive"],
        "embassy": "在ネパール日本国大使館（カトマンズ: +977-1-4426680）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_010.html",
        "safety_note": "高地トレッキング時は高山病とヘリコプター救援に対応した海外旅行保険への加入が必須です。",
        "special_ui": "standard"
    },
    "MV": {
        "country_ja": "モルディブ", "country_kana": "もるでぃぶ", "region": "アジア",
        "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "USD", "curr_ja": "米ドル（現地通貨ルフィヤ）", "sym": "$",
        "tip": "optional", "tip_badge": "1〜5ドル（リゾート内）", "tip_detail": "リゾートホテルでは10%のサービス料が加算されますが、バトラーやハウスキーピングに1日2〜5米ドル程度渡すのが一般的。",
        "tax": "TGST（観光財サービス税）16%。",
        "water": False, "water_note": "リゾート内では毎日無料のミネラルウォーターが補充されます。",
        "emerg": "警察119 / 救急102",
        "apps": ["リゾート専用アプリ", "RTL Travel"],
        "embassy": "在モルディブ日本国大使館（マレ: +960-330-0087）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_019.html",
        "safety_note": "イスラム教国のため、アルコール類や豚肉製品の持ち込みは厳禁です（リゾート島内での飲酒は可）。またローカル島では肌の露出を控えてください。",
        "special_ui": "standard"
    },
    "UZ": {
        "country_ja": "ウズベキスタン", "country_kana": "うずべきすたん", "region": "アジア・中央アジア",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "UZS", "curr_ja": "スム", "sym": "so'm",
        "tip": "optional", "tip_badge": "5〜10%（サ料込なら不要）", "tip_detail": "多くのレストランで会計に10〜15%のサービス料が含まれています。タクシーは端数切り上げ程度。",
        "tax": "VAT 12%。",
        "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。",
        "emerg": "警察102 / 救急103 / 消防101",
        "apps": ["Yandex Go（必須の配車アプリ・流しの白タク回避）", "2GIS / Yandex Maps", "ウズベキスタン鉄道アプリ"],
        "embassy": "在ウズベキスタン日本国大使館（タシュケント: +998-78-120-80-60）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_045.html",
        "safety_note": "治安は良好ですが、地下鉄駅構内や空港・軍事施設の撮影には注意し、宿泊施設で発行される滞在登録票（レギストラーツィヤ）は出国審査まで紛失せず保管してください。",
        "special_ui": "standard"
    },
    "KZ": {
        "country_ja": "カザフスタン", "country_kana": "かざふすたん", "region": "アジア・中央アジア",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "KZT", "curr_ja": "テンゲ", "sym": "₸",
        "tip": "optional", "tip_badge": "10%（サ料込が一般的）", "tip_detail": "レストランでは伝票に10%のサービス料が含まれていることが多いです。",
        "tax": "VAT 12%。",
        "water": False, "water_note": "水道水は飲用不可。市販のミネラルウォーターを購入してください。",
        "emerg": "総合緊急112 / 警察102 / 救急103",
        "apps": ["Yandex Go（配車必須）", "2GIS（オフライン地図・乗換案内）"],
        "embassy": "在カザフスタン日本国大使館（アスタナ: +7-7172-977-843）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_046.html",
        "safety_note": "流しの白タクはぼったくりや強盗リスクがあるため使わず、必ずYandex Goアプリで配車してください。",
        "special_ui": "standard"
    },

    "US": {
        "country_ja": "アメリカ", "country_kana": "あめりか べいこく", "region": "北米・ハワイ",
        "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False,
        "curr": "USD", "curr_ja": "米ドル", "sym": "$",
        "tip": "required", "tip_badge": "必須（18〜22%）", "tip_detail": "着席レストランは税前価格の18〜22%が必須マナー。タクシー・Uberは15〜20%、ホテルのベッドメイクは1泊$2〜5。",
        "tax": "州・都市ごとに売上税（約4〜10%・ハワイは4.712%）がレジで加算。観光客向けの免税還付制度はなし。",
        "water": True, "water_note": "水道水は飲用可能ですが、乾燥対策や持ち歩きにはペットボトル水のまとめ買いが便利です。",
        "emerg": "警察・救急・消防 911",
        "apps": ["Uber", "Lyft", "Googleマップ", "MPC（入国審査短縮アプリ）"],
        "embassy": "在アメリカ合衆国日本国大使館（ワシントンDC: +1-202-238-6700）/ NY・LA・SF・ホノルル・シカゴ・ボストン・シアトル・マイアミ各総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_221.html",
        "safety_note": "渡航72時間前までに電子渡航認証「ESTA」の取得が必須です。銃犯罪や車上荒らし、都市部の一部危険エリア（夜間の一人歩き）に注意し、また医療費が世界一高額（盲腸手術で数百万円）なため無制限または高額補償の海外旅行保険が必須です。",
        "special_ui": "us_tip_medical"
    },
    "US_GUM": {
        "country_ja": "グアム・サイパン（米国準州）", "country_kana": "ぐあむ さいぱん", "region": "太平洋・リゾート",
        "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False,
        "curr": "USD", "curr_ja": "米ドル", "sym": "$",
        "tip": "required", "tip_badge": "必須（15〜20%）", "tip_detail": "レストランでは15〜20%が相場ですが、伝票にService Chargeが含まれている場合は追加不要です（二重払いに注意）。",
        "tax": "グアムは消費税（売上税）が0%のフリーポートのため、表示価格のまま買い物できます。",
        "water": False, "water_note": "サンゴ礁由来の石灰分が多い硬水のため、飲料用には市販のミネラルウォーターを購入してください。",
        "emerg": "警察・救急・消防 911",
        "apps": ["Stroll（グアム版Uber）", "赤いシャトルバス（eチケット）"],
        "embassy": "在ハガッニャ（グアム）日本国総領事館（+1-671-646-1290）/ 在サイパン領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_221.html",
        "safety_note": "グアム・北マリアナ諸島用のオンライン電子渡航認証（G-CNMI ETA）またはESTAの事前申請が必要です。ビーチでの置き引きやレンタカーの車上荒らしに注意してください。",
        "special_ui": "us_tip_medical"
    },
    "CA": {
        "country_ja": "カナダ", "country_kana": "かなだ", "region": "北米",
        "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False,
        "curr": "CAD", "curr_ja": "カナダドル", "sym": "C$",
        "tip": "required", "tip_badge": "必須（15〜20%）", "tip_detail": "アメリカ同様チップ社会。レストランやタクシーではカード端末に表示される15%・18%・20%のボタンから選ぶだけで完了します。",
        "tax": "連邦税(GST 5%)＋州税(PST)または統合税(HST)で計5〜15%が加算。旅行者向けの免税還付制度は原則なし。",
        "water": True, "water_note": "水道水は水質基準が非常に高く、そのまま美味しく飲めます。",
        "emerg": "警察・救急・消防 911",
        "apps": ["Uber", "Lyft", "Transit", "ArriveCAN（任意・入国事前申告）"],
        "embassy": "在カナダ日本国大使館（オタワ: +1-613-241-8541）/ バンクーバー・トロント・モントリオール・カルガリー各総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_222.html",
        "safety_note": "空路入国には電子渡航認証「eTA」の事前取得が必須です。治安は良好ですが、バンクーバーのイースト・ヘイスティングス通り周辺など薬物中毒者が集まるエリアには絶対に立ち入らないでください。",
        "special_ui": "us_tip_medical"
    },
    "MX": {
        "country_ja": "メキシコ", "country_kana": "めきしこ", "region": "中南米",
        "plug": "A", "voltage": "127V", "freq": "60Hz", "trans": False,
        "curr": "MXN", "curr_ja": "メキシコペソ", "sym": "Mex$",
        "tip": "required", "tip_badge": "必須（10〜15%）", "tip_detail": "レストランでは会計の10〜15%（カンクン等のリゾート地では15〜20%）。ポーターには20〜50ペソ程度。",
        "tax": "IVA（付加価値税）16%。Tax Free加盟店で一定額以上購入時、空港で還付申請可能。",
        "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。",
        "emerg": "警察・救急・消防 911",
        "apps": ["Uber", "DiDi"],
        "embassy": "在メキシコ日本国大使館（メキシコシティ: +52-55-5211-0028）/ 在レオン総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_264.html",
        "safety_note": "流しのタクシーは強盗被害のリスクがあるため絶対に乗らず、Uberまたはホテル手配の無線タクシー（Sitio）を利用してください。",
        "special_ui": "standard"
    },
    "PE": {
        "country_ja": "ペルー", "country_kana": "ぺるー", "region": "中南米",
        "plug": "A/C", "voltage": "220V", "freq": "60Hz", "trans": False,
        "curr": "PEN", "curr_ja": "ソル（米ドル併用可）", "sym": "S/",
        "tip": "optional", "tip_badge": "5〜10%（中高級店）", "tip_detail": "観光客向けレストランでは会計の5〜10%程度。タクシーはチップ不要（配車アプリ利用推奨）。",
        "tax": "IGV（一般売上税）18%。",
        "water": False, "water_note": "水道水は飲用不可。高山病対策としてもミネラルウォーターをこまめに摂取してください。",
        "emerg": "警察105 / 救急116 / 観光警察(POLTUR) 01-460-1060",
        "apps": ["Uber", "Cabify"],
        "embassy": "在ペルー日本国大使館（リマ: +51-1-219-9500）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_261.html",
        "safety_note": "クスコ（標高3,400m）等の高地では到着初日の飲酒・暴飲暴食を避け、高山病対策薬（ダイアモックス等）やコカ茶で順応してください。",
        "special_ui": "altitude_alert"
    },
    "BO": {
        "country_ja": "ボリビア", "country_kana": "ぼりびあ うゆに", "region": "中南米",
        "plug": "A/C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "BOB", "curr_ja": "ボリビアーノ", "sym": "Bs",
        "tip": "optional", "tip_badge": "5〜10%（ツアーガイド・高級店）", "tip_detail": "ウユニ塩湖の専属ドライバーやガイドには満足度に応じて1日50〜100ボリビアーノ（または10米ドル前後）のチップが喜ばれます。",
        "tax": "IVA 13%（内税）。",
        "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。",
        "emerg": "警察110 / 救急118",
        "apps": ["Yango（ラパス等の配車）", "Maps.me"],
        "embassy": "在ボリビア日本国大使館（ラパス: +591-2-241-9110）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_262.html",
        "safety_note": "ラパスやウユニは標高3,600mを超える超高地です。重い高山病や寒暖差による体調不良に備え、必ず高地治療・搬送対応の海外旅行保険に加入してください。また偽警察官詐欺にも注意。",
        "special_ui": "altitude_alert"
    },
    "CL": {
        "country_ja": "チリ", "country_kana": "ちり", "region": "中南米",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "CLP", "curr_ja": "チリペソ", "sym": "CLP$",
        "tip": "optional", "tip_badge": "10%（レストラン慣例）", "tip_detail": "レストランでは会計時に「10%のチップ（Propina）を含めますか？」と聞かれるため、「Sí（はい）」と答えてカード決済するのが一般的です。ホテル代は外国人旅行者なら米ドルまたは海外クレカ払いで19%のIVA（付加価値税）が免税になります。",
        "tax": "IVA 19%。外国人はパスポートと入国カード(PDI)提示＋外貨/クレカ払いで宿泊税19%が免除されます。",
        "water": True, "water_note": "サンティアゴ市内の水道水は飲用可能ですが、硬水のため旅行者はミネラルウォーター（Sin gas＝炭酸なし）が安心です。",
        "emerg": "警察133 / 救急131 / 消防132",
        "apps": ["Uber", "Cabify"],
        "embassy": "在チリ日本国大使館（サンティアゴ: +56-2-2232-1807）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_252.html",
        "safety_note": "入国審査で発行される「PDI（入国記録票のレシート）」はホテル免税と出国審査に必須のため絶対になくさないでください。またケチャップかけスリやスマホひったくりに注意。",
        "special_ui": "standard"
    },
    "BR": {
        "country_ja": "ブラジル", "country_kana": "ぶらじる", "region": "中南米",
        "plug": "C", "voltage": "127/220V", "freq": "60Hz", "trans": False,
        "curr": "BRL", "curr_ja": "レアル", "sym": "R$",
        "tip": "optional", "tip_badge": "10%（伝票に加算済多数）", "tip_detail": "レストランでは伝票に10%のサービス料（Taxa de Serviço）が含まれていることがほとんどです。",
        "tax": "商品価格に税金が含まれる内税方式。",
        "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーター（Água sem gás＝炭酸なし）を購入してください。",
        "emerg": "警察190 / 救急192 / 消防193",
        "apps": ["Uber（流しのタクシーより圧倒的に安全）", "99"],
        "embassy": "在ブラジル日本国大使館（ブラジリア）/ 在サンパウロ総領事館（+55-11-3254-0100）/ 在リオデジャネイロ総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_259.html",
        "safety_note": "歩きスマホや貴金属の着用は強盗（アラストン）の標的になります。夜間の一人歩きやファヴェーラ（スラム街）への接近は絶対に避け、移動は短距離でもUberを利用してください。",
        "special_ui": "standard"
    },
    "AR": {
        "country_ja": "アルゼンチン", "country_kana": "あるぜんちん", "region": "中南米",
        "plug": "BF/O", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "ARS", "curr_ja": "アルゼンチンペソ", "sym": "ARS$",
        "tip": "optional", "tip_badge": "10%程度（レストラン）", "tip_detail": "レストランでは会計の10%程度をテーブルに置くか上乗せするのが習慣です。",
        "tax": "IVA 21%。外国人旅行者が海外発行のクレジットカード・デビットカードでホテル宿泊費を支払うと21%のIVAが自動免税されます。",
        "water": True, "water_note": "ブエノスアイレス市内の水道水は飲用可能ですが、ミネラルウォーターの購入が一般的です。",
        "emerg": "総合緊急911 / 警察101 / 救急107",
        "apps": ["Uber", "Cabify", "BA Cómo Llego"],
        "embassy": "在アルゼンチン日本国大使館（ブエノスアイレス: +54-11-4318-8200）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_242.html",
        "safety_note": "海外発行のVisa/Mastercardで決済すると「旅行者向け優遇レート（MEPレート）」が自動適用され、現金両替の手間なくお得に決済できます。ボカ地区等の観光地から1本外れた通りには立ち入らないでください。",
        "special_ui": "standard"
    },

    "GB": {
        "country_ja": "イギリス", "country_kana": "いぎりす えいこく ろんどん", "region": "ヨーロッパ",
        "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "GBP", "curr_ja": "ポンド", "sym": "£",
        "tip": "optional", "tip_badge": "10〜12.5%（サ料込なら不要）", "tip_detail": "レストランでは伝票に12.5%のService Chargeが含まれていることが多く、その場合は追加不要。パブのカウンター注文はチップ不要。",
        "tax": "標準VAT 20%（内税表示）。イギリスの観光客向け免税還付制度は廃止済みのため空港還付はありません。",
        "water": True, "water_note": "水道水は飲用可能（Tap waterは無料）。ただし石灰分が多い硬水のため、胃腸が弱い方や紅茶・洗髪ケアには注意。",
        "emerg": "警察・救急・消防 999（または112）",
        "apps": ["Citymapper（乗換神アプリ）", "Uber", "Trainline（GWR等の英国鉄道予約）"],
        "embassy": "在英国日本国大使館（ロンドン: +44-20-7465-6500）/ 在エディンバラ総領事館（+44-131-225-4777）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_154.html",
        "safety_note": "短期滞在でも電子渡航認証「UK ETA」の事前取得が必須です。またロンドン等の都市部では電動自転車に乗った犯人による「歩きスマホのひったくり（Phone snatching）」が多発しているため、路上でスマホを操作する際は周囲に警戒してください。",
        "special_ui": "europe_cashless"
    },
    "FR": {
        "country_ja": "フランス", "country_kana": "ふらんす ぱり", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "気持ち程度（サ料15%込）", "tip_detail": "法律によりサービス料15%が価格に含まれています。良いサービスを受けた際にカフェで小銭（1〜2€）、レストランで5%程度置くのがスマート。",
        "tax": "標準VAT 20%。同一店舗で同日100.01€以上購入すると、空港のPABLO端末で免税手続き（約12%還付）が可能。",
        "water": True, "water_note": "水道水は飲用可能。レストランで「キャラフ・ドー（Carafe d'eau）」と頼めば無料の水道水ピッチャーが出ます。",
        "emerg": "欧州共通112 / 警察17 / 救急15",
        "apps": ["Bonjour RATP（パリ地下鉄・スマホ乗車券）", "Citymapper", "Uber / Bolt"],
        "embassy": "在フランス日本国大使館（パリ: +33-1-4888-6200）/ ストラスブール・マルセイユ各総領事館 / リヨン領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_170.html",
        "safety_note": "地下鉄（メトロ）やRER B線、エッフェル塔・ルーヴル周辺のスリ集団（署名運動詐欺・ミサンガ売り・ドア閉まり際のスマホ奪取）に厳重注意してください。",
        "special_ui": "europe_cashless"
    },
    "IT": {
        "country_ja": "イタリア", "country_kana": "いたりあ ろーま", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "基本不要（席料Coperto有）", "tip_detail": "レストランでは1人1〜4€の席料（Coperto）が加算されるためチップは原則不要。特別なサービスを受けた際のみ端数を置きます。",
        "tax": "標準VAT 22%。同一店舗で70.01€以上購入すると空港で免税還付が可能。",
        "water": True, "water_note": "水道水は飲用可能ですが硬水です。レストランでの水（Acqua naturale＝炭酸なし / frizzante＝炭酸あり）注文は有料のボトル水が出てきます。",
        "emerg": "欧州共通 112",
        "apps": ["FreeNow / itTaxi（公式タクシー配車）", "Trenitalia / Italo（高速鉄道）", "Googleマップ"],
        "embassy": "在イタリア日本国大使館（ローマ: +39-06-487-991）/ 在ミラノ総領事館（+39-02-6241141）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_153.html",
        "safety_note": "ローマ・テルミニ駅やミラノ中央駅、地下鉄車内でのスリ、およびミサンガ押し売り・自動券売機での親切を装ったお釣り盗難に注意してください。",
        "special_ui": "europe_cashless"
    },
    "ES": {
        "country_ja": "スペイン", "country_kana": "すぺいん", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "端数〜5%程度", "tip_detail": "バルやカフェではお釣りの小銭を置く程度、レストランでは会計の5〜10%程度が目安です。",
        "tax": "標準IVA 21%。スペインは免税最低購入金額の制限（0€〜）が撤廃されており、少額の買い物でもTax Free書類を作れます。",
        "water": True, "water_note": "マドリード等は軟水で美味しいですが、バルセロナ等は硬水のためミネラルウォーターが好まれます。",
        "emerg": "欧州共通 112",
        "apps": ["Cabify（スペイン最強の配車アプリ）", "Uber", "FreeNow"],
        "embassy": "在スペイン日本国大使館（マドリード: +34-91-590-7600）/ 在バルセロナ総領事館（+34-93-280-3433）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_161.html",
        "safety_note": "バルセロナやマドリードでは、カフェのテラス席テーブル上に置いたスマホの持ち去りや、液体をかけて注意を逸らすスリが多発しています。",
        "special_ui": "europe_cashless"
    },
    "DE": {
        "country_ja": "ドイツ", "country_kana": "どいつ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%（切り上げ払い）", "tip_detail": "テーブル会計時に「18.50€なら20€で！」とチップ込みのキリの良い金額を店員に伝えて支払うのがドイツ流です。",
        "tax": "標準VAT 19%。同一店舗で50.01€以上購入時に免税手続きが可能。",
        "water": True, "water_note": "水質基準が厳しく水道水は飲用可能ですが、スーパーでは炭酸水（Classic）と水（Still/Naturell）の間違いに注意。",
        "emerg": "欧州共通112 / 警察110",
        "apps": ["DB Navigator（ドイツ鉄道必須アプリ）", "FreeNow", "Uber"],
        "embassy": "在ドイツ日本国大使館（ベルリン: +49-30-210940）/ ミュンヘン・フランクフルト・デュッセルドルフ・ハンブルク各総領事館",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_165.html",
        "safety_note": "フランクフルト中央駅周辺の特定通り（タウヌス通り等）は薬物常習者が多いため夜間は避けてください。日曜日はスーパーや百貨店が法律で全面休業になる点にも注意。",
        "special_ui": "europe_cashless"
    },
    "CH": {
        "country_ja": "スイス", "country_kana": "すいす", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "CHF", "curr_ja": "スイスフラン", "sym": "CHF",
        "tip": "optional", "tip_badge": "端数切り上げ（サ料込）", "tip_detail": "すべてサービス料込みですが、レストラン等で23.50フランなら25フランに切り上げて支払うとスマートです。",
        "tax": "標準VAT 8.1%。1店舗300フラン以上購入で免税対象（EU圏外のため、EU諸国へ抜ける国境駅や空港でスタンプ必須）。",
        "water": True, "water_note": "アルプスの天然水に近く、水道水や街中の水飲み場の水が非常に美味しくそのまま飲めます。",
        "emerg": "欧州共通112 / 警察117 / 救急144",
        "apps": ["SBB Mobile（スイス国鉄・登山鉄道必須）", "Uber"],
        "embassy": "在スイス日本国大使館（ベルン: +41-31-300-2222）/ 在ジュネーブ領事事務所（+41-22-716-9900）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_159.html",
        "safety_note": "治安は極めて良好ですが、空港駅や長距離列車（IC）の荷物置き場でのスーツケース置き引きに注意してください。",
        "special_ui": "europe_cashless"
    },
    "AT": {
        "country_ja": "オーストリア", "country_kana": "おーすとりあ うぃーん", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%（切り上げ払い）", "tip_detail": "ドイツと同様、会計時に5〜10%を上乗せしたキリの良い金額を店員に伝えて精算します。",
        "tax": "標準VAT 20%。75.01€以上の購入で免税対象。",
        "water": True, "water_note": "ウィーンの水道水はアルプスからの湧き水（高地泉水）が引かれており、世界最高峰の美味しさでそのまま飲めます。",
        "emerg": "欧州共通112 / 警察133 / 救急144",
        "apps": ["WienMobil", "ÖBB Scotty", "Bolt / Uber"],
        "embassy": "在オーストリア日本国大使館（ウィーン: +43-1-531920）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_155.html",
        "safety_note": "地下鉄やトラムは改札がない信用乗車方式ですが、私服検札員による抜き打ちチェックが頻繁にあるため、必ず乗車前に打刻（バリデート）またはアプリ購入を行ってください。",
        "special_ui": "europe_cashless"
    },
    "CZ": {
        "country_ja": "チェコ", "country_kana": "ちぇこ ぷらは", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "CZK", "curr_ja": "チェココルナ", "sym": "Kč",
        "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでは会計時に10%程度を上乗せして支払うのが一般的です。テーブルの上に現金を放置せず、会計時に直接伝えます。",
        "tax": "標準VAT 21%。1店舗2,000CZK以上の購入で免税対象。",
        "water": True, "water_note": "水道水は飲用可能です。",
        "emerg": "欧州共通112 / 警察158 / 救急155",
        "apps": ["PID Lítačka（プラハ交通必須）", "Bolt", "Uber"],
        "embassy": "在チェコ日本国大使館（プラハ: +420-257-533-546）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_163.html",
        "safety_note": "街中の一部の悪質両替所（0% Commissionと大きく掲げて極端に悪いレートを適用する店）や、路上で声をかけてくる偽替詐欺（使えないベラルーシ紙幣を渡す手口）に注意。基本はクレカのタッチ決済だけで過ごせます。",
        "special_ui": "europe_cashless"
    },
    "NL": {
        "country_ja": "オランダ", "country_kana": "おらんだ あむすてるだむ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "サービス料込みのため必須ではありませんが、レストランでは5〜10%程度を切り上げて払うことが多いです。完全キャッシュレス社会です。",
        "tax": "標準VAT 21%。50€以上の購入で免税対象。",
        "water": True, "water_note": "水道水は非常に水質が高く、そのまま美味しく飲めます。",
        "emerg": "欧州共通 112",
        "apps": ["9292（オランダ全土の乗換案内）", "NS（オランダ鉄道）", "Uber"],
        "embassy": "在オランダ日本国大使館（ハーグ: +31-70-346-9544）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_156.html",
        "safety_note": "自転車専用レーン（赤い舗装）を歩行者が歩くと高速の自転車と接触して大変危険です。またスキポール空港〜アムステルダム中央駅間の列車内での置き引きに注意してください。",
        "special_ui": "europe_cashless"
    },
    "BE": {
        "country_ja": "ベルギー", "country_kana": "べるぎー", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "基本不要（端数程度）", "tip_detail": "サービス料が含まれているため原則不要。満足した際に端数を切り上げる程度で十分です。",
        "tax": "標準VAT 21%。125.01€以上の購入で免税対象。",
        "water": True, "water_note": "水道水は飲用可能ですが硬水です。",
        "emerg": "欧州共通 112",
        "apps": ["SNCB（ベルギー国鉄）", "STIB-MIVB", "Uber"],
        "embassy": "在ベルギー日本国大使館（ブリュッセル: +32-2-513-2340）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_171.html",
        "safety_note": "ブリュッセル南駅（Midi駅）および北駅周辺はスリ・ひったくりが多発しているため、スーツケースや手荷物から絶対に目を離さないでください。",
        "special_ui": "europe_cashless"
    },
    "PT": {
        "country_ja": "ポルトガル", "country_kana": "ぽるとがる", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%（レストラン）", "tip_detail": "カフェは小銭程度、観光客向けレストランでは5〜10%程度置くと喜ばれます。",
        "tax": "標準IVA 23%。61.50€以上の購入で免税対象。",
        "water": True, "water_note": "水道水は飲用可能です。",
        "emerg": "欧州共通 112",
        "apps": ["Bolt（Uberより安いことが多い）", "Uber", "Navegante"],
        "embassy": "在ポルトガル日本国大使館（リスボン: +351-21-311-0560）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_173.html",
        "safety_note": "リスボンの名物トラム28番線の車内はプロのスリ集団が常駐しているため、貴重品は服の内側にしまう対策が必須です。またレストランで最初に出されるパンやオリーブ（Couvert）は有料なので不要なら断れます。",
        "special_ui": "europe_cashless"
    },
    "GR": {
        "country_ja": "ギリシャ", "country_kana": "ぎりしゃ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "タベルナ（大衆食堂）では端数〜5%、レストランでは5〜10%程度をテーブルに置くのが一般的です。",
        "tax": "標準VAT 24%。50€以上の購入で免税対象。",
        "water": True, "water_note": "アテネ本土は飲用可能ですが、サントリーニ島・ミコノス島などの島嶼部は水道水が飲めないためミネラルウォーター必須です。",
        "emerg": "欧州共通112 / 警察100 / 観光警察1571",
        "apps": ["FreeNow", "Uber（タクシー配車）", "Ferryhopper（島間フェリー予約）"],
        "embassy": "在ギリシャ日本国大使館（アテネ: +30-210-670-9900）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_157.html",
        "safety_note": "アテネの地下鉄（特に空港〜シンタグマ広場・モナスティラキ駅間）での集団スリに注意。また多くの場所でトイレットペーパーを便器に流さず備え付けのゴミ箱に捨てる方式です。",
        "special_ui": "europe_cashless"
    },
    "HR": {
        "country_ja": "クロアチア", "country_kana": "くろあちあ どぶろぶにく", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "2023年から通貨がユーロになりシェンゲン圏に加盟しました。レストランでは会計の5〜10%程度、カフェでは端数を置くのが一般的です。",
        "tax": "標準PDV（VAT）25%。1店舗100€以上の購入で免税対象。",
        "water": True, "water_note": "水道水は飲用可能です。ドブロブニク旧市街のオノフリオの大噴水の水もそのまま飲めます。",
        "emerg": "欧州共通 112",
        "apps": ["Uber（ドブロブニク・ザグレブで大活躍）", "Bolt", "FlixBus"],
        "embassy": "在クロアチア日本国大使館（ザグレブ: +385-1-4870-650）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_185.html",
        "safety_note": "治安は非常に良好ですが、夏季のドブロブニク旧市街など混雑する観光地でのスリと熱中症対策に注意してください。",
        "special_ui": "europe_cashless"
    },
    "MT": {
        "country_ja": "マルタ", "country_kana": "まるた ばれった", "region": "ヨーロッパ",
        "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "レストランでサービス料が含まれていない場合は5〜10%程度。イギリス統治の歴史があるためコンセントはBFタイプ（3つ穴）です。",
        "tax": "標準VAT 18%。100€以上の購入で免税対象。",
        "water": False, "water_note": "海水を淡水化した水で塩分・石灰分を感じるため、飲料用には市販のミネラルウォーターを購入してください。",
        "emerg": "欧州共通 112",
        "apps": ["Bolt（マルタで圧倒的に便利）", "Uber", "Tallinja（マルタ公共バス）"],
        "embassy": "在マルタ日本国大使館（バレッタ近郊スリマ: +356-2133-8601）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_176.html",
        "safety_note": "治安はヨーロッパでもトップクラスに良好ですが、パーチャビル等の夜間の繁華街での置き引きに注意してください。",
        "special_ui": "europe_cashless"
    },
    "IS": {
        "country_ja": "アイスランド", "country_kana": "あいすらんど れいきゃびく", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "ISK", "curr_ja": "アイスランドクローナ", "sym": "kr",
        "tip": "none", "tip_badge": "不要", "tip_detail": "すべてサービス料込みでチップの習慣はありません。公衆トイレからホットドッグ屋台まで100%クレジットカードのタッチ決済で完結するため現金への両替は一切不要です。",
        "tax": "標準VAT 24%。同一店舗で12,000ISK以上の買い物をするとケプラヴィーク国際空港で免税還付が受けられます。",
        "water": True, "water_note": "冷たい水道水は氷河の湧き水そのもので世界一美味しく飲めます（温水は地熱の硫黄臭がするため、必ず冷水になるまで流してから飲んでください）。",
        "emerg": "欧州共通 112",
        "apps": ["Vedur（アイスランド気象庁・オーロラ＆暴風予報必須）", "SafeTravel.is", "Straeto（バス）"],
        "embassy": "在アイスランド日本国大使館（レイキャビク: +354-510-8600）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_151.html",
        "safety_note": "犯罪率が世界一低い安全な国ですが、急激な天候変化・強風（レンタカーのドアが風で壊れる事故が多発）や火山活動情報（SafeTravel.is）の確認が必須です。",
        "special_ui": "europe_cashless"
    },
    "HU": {
        "country_ja": "ハンガリー", "country_kana": "はんがりー ぶだぺすと", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "HUF", "curr_ja": "フォリント", "sym": "Ft",
        "tip": "optional", "tip_badge": "10%（サ料別の場合）", "tip_detail": "伝票にSzervizdíj（サービス料10〜15%）が含まれていれば不要。含まれない場合は会計時に10%程度を上乗せします。",
        "tax": "標準VAT 27%（欧州最高水準のため、免税店でのTax Free手続きのメリットが大きいです）。",
        "water": True, "water_note": "水道水はそのまま飲用可能です。",
        "emerg": "欧州共通 112",
        "apps": ["BudapestGO（交通チケット必須）", "Bolt（ブダペスト公認タクシー配車）"],
        "embassy": "在ハンガリー日本国大使館（ブダペスト: +36-1-398-3100）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_169.html",
        "safety_note": "流しの個人タクシー（「Freelancer」表示）はぼったくりが多いため乗らず、必ずBoltアプリで公認イエロータクシーを配車してください。",
        "special_ui": "europe_cashless"
    },
    "FI": {
        "country_ja": "フィンランド", "country_kana": "ふぃんらんど へるしんき", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "EUR", "curr_ja": "ユーロ", "sym": "€",
        "tip": "none", "tip_badge": "不要", "tip_detail": "北欧はサービス料込みかつ高賃金体系のため、チップの習慣は基本的にありません。",
        "tax": "標準VAT 25.5%。40€以上の購入で免税対象。",
        "water": True, "water_note": "水道水は世界トップクラスの純度で、ペットボトル水以上に美味しくそのまま飲めます。",
        "emerg": "欧州共通 112",
        "apps": ["HSL（ヘルシンキ交通）", "Bolt", "Uber"],
        "embassy": "在フィンランド日本国大使館（ヘルシンキ: +358-9-686-0200）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_169.html",
        "safety_note": "治安は非常に良好で、ほぼ完全なキャッシュレス社会です。冬季は路面凍結による転倒と極寒によるスマホのバッテリー急減に注意してください。",
        "special_ui": "europe_cashless"
    },
    "SE": {
        "country_ja": "スウェーデン", "country_kana": "すうぇーでん すとっくほるむ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "SEK", "curr_ja": "スウェーデンクローナ", "sym": "kr",
        "tip": "none", "tip_badge": "不要（端数程度）", "tip_detail": "基本的に不要。現金お断り（No Cash）の店舗が大半のためタッチ決済対応のカードが必須です。",
        "tax": "標準VAT 25%。200SEK以上の購入で免税対象。",
        "water": True, "water_note": "水道水は非常に綺麗でそのまま飲めます。",
        "emerg": "欧州共通 112",
        "apps": ["SL（ストックホルム交通）", "Uber", "Bolt"],
        "embassy": "在スウェーデン日本国大使館（ストックホルム: +46-8-579-35300）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_160.html",
        "safety_note": "世界最先端のキャッシュレス国のため現金は不要です。ホテルの朝食会場やカフェでの置き引きにだけ注意してください。",
        "special_ui": "europe_cashless"
    },
    "NO": {
        "country_ja": "ノルウェー", "country_kana": "のるうぇー おすろ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "NOK", "curr_ja": "ノルウェークローネ", "sym": "kr",
        "tip": "none", "tip_badge": "不要（端数程度）", "tip_detail": "サービス料が含まれておりチップは原則不要です。カードタッチ決済が100%普及しています。",
        "tax": "標準VAT 25%。315NOK以上の購入で免税対象（EU圏外のためノルウェー出国時に手続き）。",
        "water": True, "water_note": "氷河と山岳由来の水道水は極めて純度が高くそのまま美味しく飲めます。",
        "emerg": "警察112 / 救急113 / 消防110",
        "apps": ["Ruter（オスロ交通）", "Vy（ノルウェー国鉄）", "Uber / Bolt"],
        "embassy": "在ノルウェー日本国大使館（オスロ: +47-2201-2900）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_167.html",
        "safety_note": "治安は非常に良好ですが、オスロ中央駅周辺でのスリには注意してください。",
        "special_ui": "europe_cashless"
    },
    "DK": {
        "country_ja": "デンマーク", "country_kana": "でんまーく こぺんはーげん", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "DKK", "curr_ja": "デンマーククローネ", "sym": "kr",
        "tip": "none", "tip_badge": "不要", "tip_detail": "法律でサービス料込みの表示が義務付けられており、チップは不要です。",
        "tax": "標準VAT 25%。300DKK以上の購入で免税対象。",
        "water": True, "water_note": "水道水はそのまま飲用可能です。",
        "emerg": "欧州共通 112",
        "apps": ["DOT Tickets", "Rejseplanen", "Viggo（配車）"],
        "embassy": "在デンマーク日本国大使館（コペンハーゲン: +45-3311-3344）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_164.html",
        "safety_note": "コペンハーゲン中央駅周辺での置き引きと、自転車専用道への誤進入に注意してください。",
        "special_ui": "europe_cashless"
    },
    "PL": {
        "country_ja": "ポーランド", "country_kana": "ぽーらんど わるしゃわ", "region": "ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "PLN", "curr_ja": "ズウォティ", "sym": "zł",
        "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでは会計の10%程度を上乗せするのが一般的です。",
        "tax": "標準VAT 23%。200PLN以上の購入で免税対象。",
        "water": True, "water_note": "主要都市の水道水は飲用可能ですが、ミネラルウォーターも安価に買えます。",
        "emerg": "欧州共通 112",
        "apps": ["Jakdojade（乗換・電子切符購入必須）", "Uber", "Bolt"],
        "embassy": "在ポーランド日本国大使館（ワルシャワ: +48-22-696-5000）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_174.html",
        "safety_note": "治安はヨーロッパの中でも非常に良好で物価も手頃です。キャッシュレス決済が隅々まで普及しています。",
        "special_ui": "europe_cashless"
    },

    "AU": {
        "country_ja": "オーストラリア", "country_kana": "おーすとらりあ ごうしゅう", "region": "オセアニア",
        "plug": "O", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "AUD", "curr_ja": "豪ドル", "sym": "A$",
        "tip": "none", "tip_badge": "不要", "tip_detail": "最低賃金が高くチップの習慣はありません。高級レストランで特別なサービスを受けた際のみ5〜10%程度。",
        "tax": "GST 10%。同一店舗で300A$以上購入時、空港のTRSカウンター（アプリ事前入力推奨）で免税還付が可能。",
        "water": True, "water_note": "水道水は安全基準が高く、そのまま美味しく飲めます。",
        "emerg": "警察・救急・消防 000",
        "apps": ["Uber", "DiDi", "Googleマップ", "AustralianETA（ビザ申請アプリ）"],
        "embassy": "在オーストラリア日本国大使館（キャンベラ）/ シドニー・メルボルン・ブリスベン・パース各総領事館 / ケアンズ領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_071.html",
        "safety_note": "渡航前に公式アプリ「AustralianETA」から電子渡航許可（ETA）の取得が必須です。また食品・動植物の検疫が世界一厳しいため、機内食やわずかなお菓子・常備薬も必ず入国カードで申告してください（無申告は高額罰金）。",
        "special_ui": "standard"
    },
    "NZ": {
        "country_ja": "ニュージーランド", "country_kana": "にゅーじーらんど", "region": "オセアニア",
        "plug": "O", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "NZD", "curr_ja": "NZドル", "sym": "NZ$",
        "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。どこでも表示価格（税金・サービス料込）の支払いで完結します。",
        "tax": "GST 15%。空港での旅行者向け免税還付制度はありません。",
        "water": True, "water_note": "水道水は非常に綺麗でそのまま飲用可能です。",
        "emerg": "警察・救急・消防 111",
        "apps": ["Uber", "AT Mobile（オークランド交通）", "NZeTA（渡航認証アプリ）"],
        "embassy": "在ニュージーランド日本国大使館（ウェリントン）/ 在オークランド総領事館 / 在クライストチャーチ領事事務所",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_074.html",
        "safety_note": "渡航前に電子渡航認証「NZeTA」および環境保護・観光税（IVL）の支払いが必須です。オーストラリア同様、食品や泥のついた登山靴などの検疫申告が極めて厳格です。",
        "special_ui": "standard"
    },
    "FJ": {
        "country_ja": "フィジー", "country_kana": "ふぃじー", "region": "オセアニア",
        "plug": "O", "voltage": "240V", "freq": "50Hz", "trans": False,
        "curr": "FJD", "curr_ja": "フィジードル", "sym": "FJ$",
        "tip": "none", "tip_badge": "不要", "tip_detail": "フィジーには元々チップの習慣はありません。",
        "tax": "VAT 15%。",
        "water": False, "water_note": "リゾート内を除き、念のため市販のミネラルウォーター（Fiji Water等）の飲用を推奨します。",
        "emerg": "警察917 / 救急911",
        "apps": ["リゾート送迎・ローカルタクシー"],
        "embassy": "在フィジー日本国大使館（スバ: +679-3304633）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_076.html",
        "safety_note": "ナンディタウン等で親しげに日本語で話しかけ、名前を彫った木彫りの民芸品を強引に高額で売りつける手口に注意してください。",
        "special_ui": "standard"
    },
    "NC": {
        "country_ja": "ニューカレドニア", "country_kana": "にゅーかれどにあ", "region": "オセアニア",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "XPF", "curr_ja": "CFPフラン", "sym": "CFPF",
        "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。",
        "tax": "TGC（一般消費税）3〜22%。",
        "water": True, "water_note": "ヌメア市内の水道水は飲用可能ですが、離島ではミネラルウォーターを利用してください。",
        "emerg": "警察17 / 救急15",
        "apps": ["Tanéo（バス）"],
        "embassy": "在ヌメア領事事務所 / 在フランス日本国大使館管轄",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_071.html",
        "safety_note": "渡航前に最新の現地治安情勢（外務省危険情報）を必ず確認してください。",
        "special_ui": "standard"
    },
    "PF": {
        "country_ja": "タヒチ（仏領ポリネシア）", "country_kana": "たひち ぼらぼら", "region": "オセアニア",
        "plug": "C", "voltage": "220V", "freq": "60Hz", "trans": False,
        "curr": "XPF", "curr_ja": "CFPフラン", "sym": "CFPF",
        "tip": "none", "tip_badge": "不要", "tip_detail": "原則としてチップは不要です。",
        "tax": "TVA 5〜16%。",
        "water": False, "water_note": "離島（ボラボラ島等）では市販のミネラルウォーターを飲用してください。",
        "emerg": "警察17 / 救急15",
        "apps": ["リゾート水上ボート・タクシー"],
        "embassy": "在フランス日本国大使館管轄（米国経由時はESTAも必須）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_170.html",
        "safety_note": "治安は非常に良好です。日差しが強烈なためサンゴに優しい日焼け止めとマリンシューズを準備してください。",
        "special_ui": "standard"
    },

    "AE": {
        "country_ja": "アラブ首長国連邦（UAE）", "country_kana": "あらぶしゅちょうこくれんぽう どばい", "region": "中東・アフリカ",
        "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "AED", "curr_ja": "ディルハム", "sym": "AED",
        "tip": "optional", "tip_badge": "10%程度（サ料別の場合）", "tip_detail": "ホテルや高級店はサービス料込みが多いですが、カフェやレストランでは10%程度、ポーターには10〜20AED程度渡すのが一般的。",
        "tax": "VAT 5%。250AED以上の買い物でPlanet社の免税タグを発行してもらえば空港で還付可能。",
        "water": False, "water_note": "海水を淡水化した水のため、飲料用には市販のミネラルウォーターを購入してください。",
        "emerg": "警察999 / 救急998",
        "apps": ["Careem（中東最強の配車・タクシーアプリ）", "Uber", "RTA Dubai"],
        "embassy": "在アラブ首長国連邦日本国大使館（アブダビ: +971-2-4435696）/ 在ドバイ総領事館（+971-4-2938888）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_048.html",
        "safety_note": "治安は世界最高水準ですが、モスク訪問時の服装規定（肌・髪の露出禁止）や、公共の場での過度な愛情表現・無断撮影（特に現地女性や政府施設）は法律で厳しく処罰されます。",
        "special_ui": "standard"
    },
    "TR": {
        "country_ja": "トルコ", "country_kana": "とるこ いすたんぶーる", "region": "中東・ヨーロッパ",
        "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "TRY", "curr_ja": "トルコリラ", "sym": "₺",
        "tip": "optional", "tip_badge": "5〜10%（レストラン・ハマム）", "tip_detail": "レストランでは会計の5〜10%、ハマム（トルコ式風呂）の垢すりスタッフには10〜15%程度のチップが慣例です。",
        "tax": "KDV（付加価値税）10〜20%。Tax Free加盟店で一定額以上購入時、空港で還付可能。",
        "water": False, "water_note": "水道水は硬水で塩素が強いため飲用せず、安価なミネラルウォーターを購入してください。",
        "emerg": "総合緊急 112",
        "apps": ["BiTaksi", "Uber（イスタンブールで公認タクシーを呼べる）", "Googleマップ"],
        "embassy": "在トルコ日本国大使館（アンカラ: +90-312-446-0500）/ 在イスタンブール総領事館（+90-212-317-4600）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_052.html",
        "safety_note": "イスタンブール旧市街やタクシム広場周辺で「日本語が話せる親日家」を装ってバーに誘い込み、数十万円を請求するぼったくりバー被害や、靴磨きブラシ落とし詐欺に厳重注意してください。",
        "special_ui": "standard"
    },
    "QA": {
        "country_ja": "カタール", "country_kana": "かたーる どーは", "region": "中東・アフリカ",
        "plug": "BF", "voltage": "240V", "freq": "50Hz", "trans": False,
        "curr": "QAR", "curr_ja": "カタールリヤル", "sym": "QR",
        "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでサービス料が含まれない場合は10%程度、ポーターには10〜20リヤル程度。",
        "tax": "付加価値税（VAT）は0%のため、買い物はすべて免税相当です。",
        "water": False, "water_note": "市販のミネラルウォーターの飲用を推奨します。",
        "emerg": "警察・救急・消防 999",
        "apps": ["Uber", "Karwa Taxi"],
        "embassy": "在カタール日本国大使館（ドーハ: +974-4440-9000）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_049.html",
        "safety_note": "治安は極めて良好ですが、イスラム教の戒律により国内へのアルコール類や豚肉製品の持ち込みは厳禁です（空港の荷物検査で没収されます）。",
        "special_ui": "standard"
    },
    "EG": {
        "country_ja": "エジプト", "country_kana": "えじぷと かいろ", "region": "中東・アフリカ",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "EGP", "curr_ja": "エジプトポンド（米ドルも重宝）", "sym": "E£",
        "tip": "required", "tip_badge": "必須（バクシーシ文化）", "tip_detail": "あらゆる場面で少額のチップ（バクシーシ：10〜50EGPまたは1米ドル札）が求められます。トイレ利用や荷物運び用に小額紙幣を常備してください。",
        "tax": "VAT 14%。",
        "water": False, "water_note": "水道水は飲用不可。必ずキャップが密閉されたミネラルウォーターを購入してください。",
        "emerg": "観光警察126 / 警察122 / 救急123",
        "apps": ["Uber（料金交渉・ぼったくり回避に絶対必須）", "Careem"],
        "embassy": "在エジプト日本国大使館（カイロ: +20-2-2528-5910）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_094.html",
        "safety_note": "入国時に空港銀行窓口でアライバルビザ（25米ドル現金）の購入が必要です。ピラミッド周辺でのラクダ乗り料金トラブルや偽ガイドの客引きが多いため、はっきり断る姿勢が重要です。",
        "special_ui": "standard"
    },
    "MA": {
        "country_ja": "モロッコ", "country_kana": "もろっこ まらけしゅ", "region": "中東・アフリカ",
        "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False,
        "curr": "MAD", "curr_ja": "ディルハム", "sym": "DH",
        "tip": "optional", "tip_badge": "10%程度（カフェ・ガイド）", "tip_detail": "カフェで1〜2DH、レストランで会計の10%程度、リヤド（宿）のスタッフや荷物運びには10〜20DH程度が相場です。",
        "tax": "TVA 20%。",
        "water": False, "water_note": "水道水は飲用不可。市販のミネラルウォーターを購入してください。",
        "emerg": "警察19 / 救急・消防15",
        "apps": ["InDrive", "Careem", "Maps.me（迷宮メディナ散策に必須のオフライン地図）"],
        "embassy": "在モロッコ日本国大使館（ラバト: +212-537-63-17-82）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_122.html",
        "safety_note": "旧市街（メディナ）で「その道は閉まっている、案内してあげる」と声をかけて路地裏へ誘導し金銭を要求する自称ガイドに注意してください。ドローンの持ち込みは許可なしでは厳禁（空港で没収・拘束対象）です。",
        "special_ui": "standard"
    },
    "ZA": {
        "country_ja": "南アフリカ", "country_kana": "みなみあふりか けーぷたうん", "region": "中東・アフリカ",
        "plug": "B3/C", "voltage": "230V", "freq": "50Hz", "trans": False,
        "curr": "ZAR", "curr_ja": "ランド", "sym": "R",
        "tip": "required", "tip_badge": "必須（10〜15%）", "tip_detail": "レストランやカフェでは会計の10〜15%のチップが必須習慣です。ポーターには1個あたり20〜50ランド程度。",
        "tax": "VAT 15%。合計250ランド以上の買い物をした場合、主要空港のTax Refundカウンターで還付申請が可能。",
        "water": True, "water_note": "都市部の水道水は飲用可能とされていますが、旅行者は市販のミネラルウォーターが安心です。",
        "emerg": "総合緊急112 / 警察10111 / 救急10177",
        "apps": ["Uber（ドアツードア移動に絶対必須）", "Bolt"],
        "embassy": "在南アフリカ共和国日本国大使館（プレトリア: +27-12-452-1500）/ 在ケープタウン領事事務所（+27-21-425-1677）",
        "mofa_url": "https://www.anzen.mofa.go.jp/info/pcinfectionspothazardinfo_121.html",
        "safety_note": "ヨハネスブルグ中心部（CBD）など危険エリアへの徒歩立ち入りは厳禁です。日中であっても移動は徒歩を避け、ホテル玄関から目的地玄関まで必ずUberでドアツードア移動してください。コンセントは特殊形状（M/B3タイプ）のため専用変換プラグがあると便利です。",
        "special_ui": "standard"
    }
}

# ==========================================
# 3. 世界130都市リスト（ひらがな検索対応キーワード付き）
# ==========================================
# (slug, name_ja, kana_keywords, name_en, cc, tz, has_dst, airport, fastest, cheapest)
RAW_CITIES = [
    # 韓国
    ("seoul", "ソウル", "そうる かんこく みょんどん ほんんで", "Seoul", "KR", "Asia/Seoul", False, "仁川国際空港(ICN) / 金浦空港(GMP)", "空港鉄道A'REX直通列車（ソウル駅まで43分 / 11,000₩）", "A'REX一般列車（ソウル駅まで約60分 / 4,450〜5,050₩）"),
    ("busan", "釜山（プサン）", "ぷさん ぶさん かんこく", "Busan", "KR", "Asia/Seoul", False, "金海国際空港(PUS)", "タクシー（西面・南浦洞まで約30分 / 約20,000₩）", "釜山金海軽電鉄＋地下鉄（西面駅まで約30分 / 約2,100₩）"),
    ("jeju", "済州島（チェジュ）", "ちぇじゅ さいしゅうとう かんこく", "Jeju", "KR", "Asia/Seoul", False, "済州国際空港(CJU)", "タクシー（新済州エリアまで約10分 / 約6,000₩）", "市内急行バス（中文リゾートまで約50分 / 3,000₩）"),
    ("incheon", "仁川（インチョン）", "いんちょん にんせん かんこく", "Incheon", "KR", "Asia/Seoul", False, "仁川国際空港(ICN)", "タクシー・無料シャトル（パラダイスシティ・松島まで10〜25分）", "空港鉄道A'REX＋仁川地下鉄1号線（約3,000₩）"),
    ("daegu", "大邱（テグ）", "てぐ たいきゅう かんこく", "Daegu", "KR", "Asia/Seoul", False, "大邱国際空港(TAE)", "タクシー（東大邱駅まで約10分 / 約7,000₩）", "市内バス401・急行1番＋地下鉄（中心部まで約30分 / 1,500₩）"),
    ("gyeongju", "慶州（キョンジュ）", "きょんじゅ けいしゅう かんこく", "Gyeongju", "KR", "Asia/Seoul", False, "金海国際空港(PUS)", "空港リムジンバス（慶州バスターミナルまで約70分 / 11,000₩）", "軽電鉄＋KTX鉄道（新慶州駅まで約60分）"),

    # 台湾
    ("taipei", "台北（タイペイ）", "たいぺい たいほく たいわん", "Taipei", "TW", "Asia/Taipei", False, "桃園国際空港(TPE) / 松山空港(TSA)", "桃園メトロ空港線・直達車（台北駅まで35分 / 160元）", "國光客運リムジンバス1819路（台北駅まで約55分 / 140元）"),
    ("kaohsiung", "高雄（カオシュン）", "たかお かおしゅん たいわん", "Kaohsiung", "TW", "Asia/Taipei", False, "高雄国際空港(KHH)", "高雄MRTレッドライン（美麗島駅まで16分 / 35元）", "高雄MRTレッドライン（高雄駅まで19分 / 35元）"),
    ("taichung", "台中（タイチュン）", "たいちゅう たいちゅん たいわん", "Taichung", "TW", "Asia/Taipei", False, "台中国際空港(RMQ) / 台湾高鉄台中駅", "タクシー（台中駅・逢甲夜市まで約30〜40分 / 約500元）", "市内バス302・A2路（市内まで約50分 / 悠遊カード利用で格安）"),
    ("tainan", "台南（タイナン）", "たいなん たいわん", "Tainan", "TW", "Asia/Taipei", False, "高雄空港(KHH) / 高鉄台南駅", "高雄空港からMRT＋台湾鉄道・自強号（台南駅まで約60分 / 約140元）", "高鉄台南駅から台鉄沙崙線（台南駅まで22分 / 25元）"),

    # タイ・シンガポール
    ("bangkok", "バンコク", "ばんこく たい", "Bangkok", "TH", "Asia/Bangkok", False, "スワンナプーム国際空港(BKK) / ドンムアン(DMK)", "エアポート・レール・リンクARL（パヤタイ駅まで26分 / 45B）", "ARL＋BTS/MRT乗り継ぎ（アソーク・サイアムまで約40分 / 約75B）"),
    ("phuket", "プーケット", "ぷーけっと たい", "Phuket", "TH", "Asia/Bangkok", False, "プーケット国際空港(HKT)", "空港リムジンタクシー・Grab（パトンビーチまで約50分 / 800B〜）", "プーケット・スマートバス（パトン・カロンまで約70分 / 一律100B）"),
    ("chiang-mai", "チェンマイ", "ちぇんまい たい", "Chiang Mai", "TH", "Asia/Bangkok", False, "チェンマイ国際空港(CNX)", "エアポートタクシー・Grab（旧市街・ニマンヘミンまで15分 / 一律150B〜）", "RTCシティバス（旧市街まで約20分 / 30B）"),
    ("pattaya", "パタヤ", "ぱたや たい", "Pattaya", "TH", "Asia/Bangkok", False, "スワンナプーム空港(BKK)", "チャータータクシー・Grab（パタヤ中心部まで約90分 / 約1,200〜1,500B）", "空港1階8番ゲート発・直行バス（パタヤまで約120分 / 143B）"),
    ("chiang-rai", "チェンライ", "ちぇんらい たい", "Chiang Rai", "TH", "Asia/Bangkok", False, "チェンライ国際空港(CEI)", "Grab・空港タクシー（市内中心部まで約15〜20分 / 約150〜200B）", "空港シャトル・ソンテウ（市内バスターミナルまで約20分）"),
    ("singapore", "シンガポール", "しんがぽーる まりーなべい", "Singapore", "SG", "Asia/Singapore", False, "チャンギ国際空港(SIN)", "タクシー・Grab（マリーナベイ・オーチャードまで約20分 / 約25〜35S$）", "MRT地下鉄（市内中心部まで約40分 / 約2.2S$・クレカタッチ乗車可）"),

    # ベトナム・フィリピン・マレーシア・インドネシア
    ("ho-chi-minh", "ホーチミン", "ほーちみん さいごん べとなむ", "Ho Chi Minh City", "VN", "Asia/Ho_Chi_Minh", False, "タンソンニャット国際空港(SGN)", "Grab・Vinasunタクシー（1区ドンコイ通り周辺まで約25分 / 約15万VND）", "空港バス109番・152番（ベンタイン市場まで約40分 / 5,000〜20,000VND）"),
    ("hanoi", "ハノイ", "はのい べとなむ", "Hanoi", "VN", "Asia/Ho_Chi_Minh", False, "ノイバイ国際空港(HAN)", "Grab・タクシー（旧市街・ホアンキエム湖まで約40分 / 約35万VND）", "急行バス86番（ハノイ駅・オペラハウスまで約50分 / 45,000VND）"),
    ("da-nang", "ダナン・ホイアン", "だなん ほいあん べとなむ", "Da Nang", "VN", "Asia/Ho_Chi_Minh", False, "ダナン国際空港(DAD)", "Grab・タクシー（ミーケビーチ・市街地までわずか10〜15分 / 約10万VND）", "シャトルバス（市街地まで約20分・ホイアンまでGrabで約40分）"),
    ("nha-trang", "ニャチャン", "にゃちゃん べとなむ", "Nha Trang", "VN", "Asia/Ho_Chi_Minh", False, "カムラン国際空港(CXR)", "Grab・タクシー（ニャチャン中心部まで約40分 / 約35万VND）", "Dat Moi空港シャトルバス（市内まで約45分 / 65,000VND）"),
    ("phu-quoc", "フーコック島", "ふーこっく ふーこっくとう べとなむ", "Phu Quoc", "VN", "Asia/Ho_Chi_Minh", False, "フーコック国際空港(PQC)", "Grab・ホテル送迎（ユーンドン中心部・ビーチまで約15〜20分 / 約15万VND）", "VinBus無料電動バス（空港からグランドワールド・主要ホテルへ無料運行！）"),
    ("cebu", "セブ島", "せぶ せぶとう ふぃりぴん", "Cebu", "PH", "Asia/Manila", False, "マクタン・セブ国際空港(CEB)", "Grab・ホワイトタクシー（マクタン島リゾートまで20分・セブ市内まで45分 / 300〜500P）", "MyBus空港バス（SMシティセブまで約40分 / 50P）"),
    ("manila", "マニラ", "まにら ふぃりぴん", "Manila", "PH", "Asia/Manila", False, "ニノイ・アキノ国際空港(MNL)", "Grab（マカティ・BGCまでスカイウェイ経由で約25分 / 約350〜500P）", "UBE Express空港バス（市内主要ホテル・モールまで150P）"),
    ("boracay", "ボラカイ島", "ぼらかい ぼらかいとう ふぃりぴん", "Boracay", "PH", "Asia/Manila", False, "カティクラン空港(MPH)", "ホテル送迎パッケージ（バン＋ボート＋eトライシクルでホテルまで約30分）", "ローカルボート＋トライシクル乗り継ぎ（港諸税込みで約400P）"),
    ("kuala-lumpur", "クアラルンプール", "くあらるんぷーる まれーしあ", "Kuala Lumpur", "MY", "Asia/Kuala_Lumpur", False, "クアラルンプール国際空港(KUL)", "KLIAエクスプレス（KLセントラル駅までノンストップ28分 / 55RM）", "空港リムジンバス（KLセントラル駅まで約60分 / 15RM）"),
    ("penang", "ペナン島", "ぺなん ぺなんとう まれーしあ", "Penang", "MY", "Asia/Kuala_Lumpur", False, "ペナン国際空港(PEN)", "Grab（世界遺産ジョージタウンまで約30分 / 約25〜35RM）", "Rapid Penangバス401E（コムタまで約50分 / 2.7RM）"),
    ("kota-kinabalu", "コタキナバル", "こたきなばる ぼるねお まれーしあ", "Kota Kinabalu", "MY", "Asia/Kuching", False, "コタキナバル国際空港(BKI)", "Grab（市内中心部までわずか15分 / 約15RM）", "エアポートバス（市内まで約20分 / 5RM）"),
    ("johor-bahru", "ジョホールバル", "じょほーるばる まれーしあ", "Johor Bahru", "MY", "Asia/Kuala_Lumpur", False, "スナイ国際空港(JHB) / シンガポール・チャンギ空港", "Grab（スナイ空港からJBセントラルまで約30分 / 約35RM）", "Causeway Link AA1シャトルバス（JBセントラルまで約40分 / 8RM）"),
    ("bali", "バリ島（デンパサール・ウブド）", "ばり ばりとう でんぱさーる うぶど ぬさどぅあ いんどねしあ", "Bali", "ID", "Asia/Makassar", False, "ングラ・ライ国際空港(DPS)", "Grab（空港公式ラウンジ発）・空港タクシー（クタ15分・ヌサドゥア25分・ウブド90分 / 15万〜45万Rp）", "トランス・サルバギタ / クラクラバス（主要エリアへ格安移動）"),
    ("jakarta", "ジャカルタ", "じゃかるた いんどねしあ", "Jakarta", "ID", "Asia/Jakarta", False, "スカルノ・ハッタ国際空港(CGK)", "空港鉄道Railink（BNIシティ駅まで約45分 / 70,000Rp）", "DAMRI空港バス（ガンビル駅・ブロックMまで約60分 / 80,000Rp）"),
    ("yogyakarta", "ジョグジャカルタ", "じょぐじゃかるた ぼろぶどぅーる いんどねしあ", "Yogyakarta", "ID", "Asia/Jakarta", False, "ジョグジャカルタ国際空港(YIA)", "空港特急列車YIA Xpress（トゥグ駅まで35分 / 50,000Rp）", "一般空港列車（トゥグ駅まで39分 / 20,000Rp）"),
    ("surabaya", "スラバヤ（ブロモ山拠点）", "すらばや ぶろも いんどねしあ", "Surabaya", "ID", "Asia/Jakarta", False, "ジュアンダ国際空港(SUB)", "Grab・Bluebirdタクシー（市内中心部まで高速経由で約30分 / 約10万〜15万Rp）", "DAMRI空港バス（ブンurasihバスターミナルまで約30分 / 35,000Rp）"),

    # 香港・マカオ・中国本土（VPN必須エリア）
    ("hong-kong", "香港（ホンコン）", "ほんこん きゅうりゅう", "Hong Kong", "HK", "Asia/Hong_Kong", False, "香港国際空港(HKG)", "エアポート・エクスプレス機場快線（香港駅まで24分 / 115HKD）", "城バスCityflyer A11・A21（中環・尖沙咀まで約45〜60分 / 34.6〜41.9HKD）"),
    ("macau", "マカオ", "まかお", "Macau", "MO", "Asia/Macau", False, "マカオ国際空港(MFM) / 港珠澳大橋", "各統合型リゾート(IR)の無料シャトルバス（コタイ地区ホテルまで5〜10分 / 無料）", "マカオLRT軽軌鉄道（コタイ・タイパエリアまで約10分 / 6〜8MOP）"),
    ("shanghai", "上海（シャンハイ）", "しゃんはい ちゅうごく", "Shanghai", "CN", "Asia/Shanghai", False, "上海浦東国際空港(PVG) / 虹橋空港(SHA)", "上海トランスラピッド・リニアモーターカー（龍陽路駅までわずか8分 / 50元）", "地下鉄2号線（人民広場・南京東路まで約65分 / 7元）"),
    ("beijing", "北京（ペキン）", "ぺきん ちゅうごく", "Beijing", "CN", "Asia/Shanghai", False, "北京首都国際空港(PEK) / 大興国際空港(PKX)", "首都空港線エアポートエクスプレス（東直門駅まで約20分 / 25元）", "空港リムジンバス（市内主要エリアまで約60分 / 20〜30元）"),
    ("guangzhou", "広州（コウシュウ）", "こうしゅう ちゅうごく", "Guangzhou", "CN", "Asia/Shanghai", False, "広州白雲国際空港(CAN)", "地下鉄3号線（体育西路・珠江新城まで約45分 / 7〜8元）", "空港快線バス（市内各所へ約50分 / 20元前後）"),
    ("shenzhen", "深セン（シンセン）", "しんせん ちゅうごく", "Shenzhen", "CN", "Asia/Shanghai", False, "深セン宝安国際空港(SZX)", "地下鉄11号線・空港快線（福田駅まで約30分 / 7元）", "地下鉄11号線普通車両（市内まで7元）"),
    ("chengdu", "成都（セイト）", "せいと ちぇんどぅ ぱんだ ちゅうごく", "Chengdu", "CN", "Asia/Shanghai", False, "成都天府国際空港(TFU) / 双流国際空港(CTU)", "地下鉄18号線直達快車（孵化園・南駅まで約35〜40分 / 10元）", "天府空港バス1号線（春熙路・中心部まで約60分 / 15〜25元）"),
    ("xian", "西安（シーアン）", "しーあん せいあん へいばよう ちゅうごく", "Xi'an", "CN", "Asia/Shanghai", False, "西安咸陽国際空港(XIY)", "地下鉄14号線（北客駅経由で鐘楼・中心部まで約50分 / 約9元）", "空港バス（鐘楼・西安駅まで約60分 / 25元）"),
    ("hangzhou", "杭州（コウシュウ）", "こうしゅう はんじょう せいこ ちゅうごく", "Hangzhou", "CN", "Asia/Shanghai", False, "杭州蕭山国際空港(HGH)", "地下鉄19号線・空港快線（杭州東駅・西湖周辺まで約30分 / 7〜8元）", "地下鉄1号線・7号線（市内中心部まで約45分 / 7元）"),
    ("dalian", "大連（ダイレン）", "だいれん ちゅうごく", "Dalian", "CN", "Asia/Shanghai", False, "大連周水子国際空港(DLC)", "タクシー・DiDi（中山広場・大連駅まで約20分 / 約30元）", "地下鉄2号線（青泥窪橋・中山広場まで約25分 / 3〜4元）"),
    ("qingdao", "青島（チンタオ）", "ちんたお あおしま ちゅうごく", "Qingdao", "CN", "Asia/Shanghai", False, "青島膠東国際空港(TAO)", "地下鉄8号線＋3号線（五四広場・青島駅まで約60分 / 7〜8元）", "空港快線バス（市内まで約60分 / 25元）"),
    ("xiamen", "厦門（アモイ）", "あもい しゃめん ちゅうごく", "Xiamen", "CN", "Asia/Shanghai", False, "厦門高崎国際空港(XMN)", "タクシー・DiDi（中山路・フェリーターミナルまで約20分 / 約35元）", "BRT快速バス・空港リムジン（市内中心部まで約30分 / 1〜15元）"),
    ("harbin", "ハルビン（哈爾浜）", "はるびん ちゅうごく", "Harbin", "CN", "Asia/Shanghai", False, "ハルビン太平国際空港(HRB)", "タクシー・DiDi（中央大街まで約40分 / 約100元）", "空港バス1号線・3号線（中央大街・ハルビン駅まで約50分 / 20元）"),

    # 南アジア・中央アジア
    ("siem-reap", "シェムリアップ（アンコールワット）", "しぇむりあっぷ あんこーるわっと かんぼじあ", "Siem Reap", "KH", "Asia/Phnom_Penh", False, "シェムリアップ・アンコール国際空港(SAI)", "公式空港タクシー・Grab（市内中心部まで約50分 / 35USD）", "空港シャトルバス（市内CDF免税店前まで約60分 / 8USD）"),
    ("phnom-penh", "プノンペン", "ぷのんぺん かんぼじあ", "Phnom Penh", "KH", "Asia/Phnom_Penh", False, "プノンペン国際空港(PNH)", "Grab・タクシー（リバーサイド中心部まで約35分 / 約10〜15USD）", "市バス3番（市内中心部まで約50分 / 1,500リエル≒0.38USD）"),
    ("delhi", "デリー（ニューデリー）", "でりー にゅーでりー いんど", "New Delhi", "IN", "Asia/Kolkata", False, "インディラ・ガンディー国際空港(DEL)", "デリーメトロ・エアポートエクスプレス線（ニューデリー駅まで19分 / 60₹）", "エアポートエクスプレス線（渋滞・客引き皆無で最速かつ最安60₹）"),
    ("mumbai", "ムンバイ", "むんばい いんど", "Mumbai", "IN", "Asia/Kolkata", False, "チャトラパティ・シヴァージー国際空港(BOM)", "Uber・プリペイドタクシー（コラバ・南ムンバイまで約45〜60分 / 約600₹）", "ムンバイメトロ3号線（市内主要エリアへ直結）"),
    ("colombo", "コロンボ", "ころんぼ すりらんか", "Colombo", "LK", "Asia/Colombo", False, "バンダラナイケ国際空港(CMB)", "空港高速経由タクシー・PickMe（コロンボ市内まで約40分 / 約4,000Rs）", "高速バス187番（コロンボ・フォート駅まで約45分 / 約350Rs）"),
    ("kathmandu", "カトマンズ", "かとまんず ねぱーる", "Kathmandu", "NP", "Asia/Kathmandu", False, "トリブバン国際空港(KTM)", "空港プリペイドタクシー・Pathao（タメル地区まで約20分 / 約800〜1,000Rs）", "路線バス（空港ゲート外から中心部へ約30Rs）"),
    ("male", "モルディブ（マレ）", "もるでぃぶ まれ", "Male", "MV", "Indian/Maldives", False, "ヴェラナ国際空港(MLE)", "各リゾート専用スピードボートまたは水上飛行機（空港島から直接乗船）", "公共フェリー（マレ本島まで約10分 / 1〜2USD）"),
    ("tashkent", "タシュケント・サマルカンド", "たしゅけんと さまるかんど うずべきすたん", "Tashkent", "UZ", "Asia/Tashkent", False, "タシュケント国際空港(TAS)", "Yandex Go配車タクシー（市内中心部・タシュケント駅までわずか15分 / 約25,000スム≒300円）", "路線バス67・11番（市内まで約25分 / 2,000スム）"),
    ("almaty", "アルマトイ", "あるまとい かざふすたん", "Almaty", "KZ", "Asia/Almaty", False, "アルマトイ国際空港(ALA)", "Yandex Go配車タクシー（市内中心部まで約30分 / 約2,500〜3,500₸）", "市バス92番（市内中心部まで約45分 / 100〜200₸）"),

    # ハワイ・グアム・北米・中南米
    ("honolulu", "ホノルル（ハワイ・オアフ島）", "ほのるる はわい わいきき おあふ あめりか", "Honolulu", "US", "Pacific/Honolulu", False, "ダニエル・K・イノウエ国際空港(HNL)", "Uber・チャーリーズタクシー（ワイキキまで約25分 / 定額$33〜45＋チップ）", "ザ・バス20番 / スカイライン鉄道（ワイキキまで約55分 / $3.00・大きなスーツケース持込不可）"),
    ("kona", "ハワイ島（コナ・ヒロ）", "はわいとう こな ひろ はわい", "Kailua-Kona", "US", "Pacific/Honolulu", False, "エリソン・オニヅカ・コナ国際空港(KOA)", "レンタカー・Uber（カイルア・コナ中心部まで約15分・ワイコロアまで30分）", "ヘレオン・バス（無料〜少額運行・本数少なめ）"),
    ("guam", "グアム", "ぐあむ たもん", "Guam", "US_GUM", "Pacific/Guam", False, "グアム国際空港(GUM)", "ミキタクシー・Stroll配車（タモン地区ホテルまでわずか10〜15分 / 約$25〜30）", "ホテル送迎シャトル（事前予約制）"),
    ("saipan", "サイパン", "さいぱん", "Saipan", "US_GUM", "Pacific/Saipan", False, "サイパン国際空港(SPN)", "タクシー・ホテル送迎（ガラパン地区まで約20分 / 約$25〜30）", "レンタカー（島内観光と兼用に最適）"),
    ("new-york", "ニューヨーク", "にゅーよーく まんはったん あめりか", "New York", "US", "America/New_York", True, "JFK国際空港(JFK) / ニューアーク空港(EWR)", "エアトレイン＋LIRRロングアイランド鉄道（ペン駅・グランドセントラルまで約35分 / 計$13.50〜）", "エアトレイン＋地下鉄E/A線（マンハッタンまで約60分 / 計$11.40・タッチ決済可）"),
    ("los-angeles", "ロサンゼルス", "ろさんぜるす はりうっど さんたもにか あめりか", "Los Angeles", "US", "America/Los_Angeles", True, "ロサンゼルス国際空港(LAX)", "LAX-it発Uber・タクシー（サンタモニカ・ダウンタウンまで約35分 / 約$45〜70）", "FlyAway直行バス（ユニオン駅まで約35分 / $9.75・クレカタッチ決済可）"),
    ("san-francisco", "サンフランシスコ", "さんふらんしすこ しりこんばれー あめりか", "San Francisco", "US", "America/Los_Angeles", True, "サンフランシスコ国際空港(SFO)", "BART高速鉄道（パウエル駅・ユニオンスクエアまで約30分 / $10.55）", "SamTrans路線バス292・ECR（ダウンタウンまで約60分 / $2.25）"),
    ("las-vegas", "ラスベガス", "らすべがす あめりか", "Las Vegas", "US", "America/Los_Angeles", True, "ハリー・リード国際空港(LAS)", "Uber・タクシー（ストリップ地区ホテルまで約10〜15分 / 定額ゾーン制$21〜30）", "RTC公共バスCX・108・109番（ストリップまで約20分 / $2〜6）"),
    ("orlando", "オーランド（ディズニー・WDW）", "おーらんど でぃずにー あめりか", "Orlando", "US", "America/New_York", True, "オーランド国際空港(MCO)", "Uber・Lyft（ディズニーワールド・ユニバーサルまで約25〜30分 / 約$35〜50）", "Mears Connectシャトルバス（ディズニー公式ホテル群へ片道$16）"),
    ("seattle", "シアトル", "しあとる あめりか", "Seattle", "US", "America/Los_Angeles", True, "シアトル・タコマ国際空港(SEA)", "リンク・ライトレール1号線（ウエストレイク駅まで38分 / $3.00）", "リンク・ライトレール（渋滞知らずで最速かつ最安の$3.00）"),
    ("chicago", "シカゴ", "しかご あめりか", "Chicago", "US", "America/Chicago", True, "オヘア国際空港(ORD)", "CTA地下鉄ブルーライン（ダウンタウン・ループまで約45分 / $5.00）", "CTAブルーライン（24時間運行・$5.00で直結）"),
    ("boston", "ボストン", "ぼすとん あめりか", "Boston", "US", "America/New_York", True, "ローガン国際空港(BOS)", "MBTAシルバーラインSL1（サウス駅まで約20分 / 空港発は完全無料！）", "シルバーラインSL1（サウス駅まで無料＋地下鉄レッドラインへ無料乗継）"),
    ("washington-dc", "ワシントンD.C.", "わしんとん あめりか", "Washington D.C.", "US", "America/New_York", True, "ダレス国際空港(IAD) / レーガン空港(DCA)", "メトロ・シルバーライン（ダレス空港から市内中心部まで約50分 / $2.25〜6.00）", "メトロ鉄道（DCAからはわずか15分、IADからも乗り換えなしで直結）"),
    ("san-diego", "サンディエゴ", "さんでぃえご あめりか", "San Diego", "US", "America/Los_Angeles", True, "サンディエゴ国際空港(SAN)", "Uber・タクシー（ダウンタウン・ガスランプまでわずか10分 / 約$15〜20）", "サンディエゴ・フライヤー無料シャトル＋トロリー（オールドタウン駅経由）"),
    ("miami", "マイアミ", "まいあみ あめりか", "Miami", "US", "America/New_York", True, "マイアミ国際空港(MIA)", "Uber・タクシー（サウスビーチ・ダウンタウンまで約20分 / 約$25〜35）", "メトロレール・オレンジラインまたはメトロバス150番（各$2.25）"),
    ("vancouver", "バンクーバー", "ばんくーばー かなだ", "Vancouver", "CA", "America/Vancouver", True, "バンクーバー国際空港(YVR)", "スカイトレイン・カナダライン（ウォーターフロント駅まで26分 / 約9.55C$）", "スカイトレイン・カナダライン（タッチ決済でそのまま乗車可能）"),
    ("toronto", "トロント", "とろんと ないあがら かなだ", "Toronto", "CA", "America/Toronto", True, "トロント・ピアソン国際空港(YYZ)", "UPエクスプレス空港鉄道（ユニオン駅まで25分 / 12.35C$）", "TTC急行バス900番＋地下鉄（市内まで約50分 / 3.35C$）"),
    ("montreal", "モントリオール", "もんとおりおーる かなだ", "Montreal", "CA", "America/Toronto", True, "モントリオール・トルドー国際空港(YUL)", "タクシー・Uber（ダウンタウンまで定額約48.40C$ / 約25分）", "747エアポート急行バス（ライオネル・グルー駅・中心部まで約45分 / 11C$）"),
    ("banff", "バンフ（カナディアンロッキー）", "ばんふ かるがりー かなだ", "Banff", "CA", "America/Edmonton", True, "カルガリー国際空港(YYC)", "Brewster Express / Banff Airporter直行バス（バンフ各ホテルまで約100分 / 約80C$）", "On-It季節運行バス・FlixBus（カルガリー経由で格安移動）"),
    ("cancun", "カンクン", "かんくん めきしこ", "Cancun", "MX", "America/Cancun", False, "カンクン国際空港(CUN)", "事前予約プライベート送迎バン（ホテルゾーンまで約25分 / 1台約$40）", "ADO空港バス（カンクン・セントロまで約35分 / 約130Mex$＋市内バスR1）"),
    ("mexico-city", "メキシコシティ", "めきしこしてぃ めきしこ", "Mexico City", "MX", "America/Mexico_City", False, "メキシコシティ国際空港(MEX)", "Uber・空港公認サイトタクシー（レフォルマ・ポランコまで約25〜40分 / 約200〜300Mex$）", "メトロバス4号線（歴史地区・セントロまで約30分 / 30Mex$）"),
    ("cusco", "クスコ（マチュピチュ玄関口）", "くすこ まちゅぴちゅ ぺるー", "Cusco", "PE", "America/Lima", False, "アレハンドロ・ベラスコ・アステテ国際空港(CUZ)", "Uber・空港内公式タクシー（アルマス広場周辺まで約15分 / 約25〜35ソル）", "コレクティーボ・路線バス（空港外大通りから1〜2ソル）"),
    ("lima", "リマ", "りま ぺるー", "Lima", "PE", "America/Lima", False, "ホルヘ・チャベス国際空港(LIM)", "Airport Express Lima公式バス（ミラフローレス地区まで約50分 / $8または25ソル）", "QuickLlama乗合バン・Uber（ミラフローレスまで約45ソル）"),
    ("uyuni", "ウユニ塩湖（ラパス経由）", "うゆに うゆにえんこ らぱす ぼりびあ", "Uyuni", "BO", "America/La_Paz", False, "ウユニ空港(UYU) / エル・アルト国際空港(LPB)", "ツアー送迎車・空港タクシー（ウユニ市街まで約10分 / 約15〜20Bs）", "ラパスから夜行長距離バスTodo Turismo（ウユニまで約9時間）"),
    ("santiago", "サンティアゴ", "さんてぃあご ちり", "Santiago", "CL", "America/Santiago", True, "アルトゥーロ・メリノ・ベニテス国際空港(SCL)", "Transvip公式空港バン・タクシー（プロビデンシア・中心部まで約30分 / 約25,000CLP）", "Centropuerto / Turbus空港バス（ロス・エロエス駅まで約35分 / 約2,000CLP）"),
    ("rio-de-janeiro", "リオデジャネイロ", "りおでじゃねいろ ぶらじる", "Rio de Janeiro", "BR", "America/Sao_Paulo", False, "アントニオ・カルロス・ジョビン国際空港(GIG)", "Uber・公式タクシー（コパカバーナ・イパネマまで約35分 / 約70〜100R$）", "Frescãoエアコン付き空港バス（コパカバーナまで約50分 / 約20R$）"),
    ("sao-paulo", "サンパウロ", "さんぱうろ ぶらじる", "Sao Paulo", "BR", "America/Sao_Paulo", False, "グアルーリョス国際空港(GRU)", "Uber・公式タクシー（パウリスタ通りまで約45〜60分 / 約100〜150R$）", "Airport Bus Service直行バスまたはCPTM空港鉄道13号線（市内まで約60分）"),
    ("buenos-aires", "ブエノスアイレス", "ぶえのすあいれす あるぜんちん", "Buenos Aires", "AR", "America/Argentina/Buenos_Aires", False, "エセイサ国際空港(EZE) / アエロパルケ空港(AEP)", "Tienda León公式シャトルバス・Uber（市内中心部まで約45分 / 約$12〜25）", "コレクティーボ路線バス8番（SUBEカード利用で市内まで格安移動）"),

    # ヨーロッパ
    ("london", "ロンドン", "ろんどん いぎりす えいこく", "London", "GB", "Europe/London", True, "ヒースロー空港(LHR) / ガトウィック空港(LGW)", "ヒースロー・エクスプレス（パディントン駅まで15分 / £25・早割あり）", "地下鉄ピカデリーライン / エリザベスライン（中心部まで40〜50分 / £5.60〜12.80）"),
    ("edinburgh", "エディンバラ", "えでぃんばら すこっとらんど いぎりす", "Edinburgh", "GB", "Europe/London", True, "エディンバラ空港(EDI)", "Airlink 100急行バス（ウェイバリー駅まで25分 / £5.50・往復£8）", "エディンバラ・トラム（プリンシズ・ストリートまで30分 / £7.50）"),
    ("manchester", "マンチェスター", "まんちぇすたー いぎりす", "Manchester", "GB", "Europe/London", True, "マンチェスター空港(MAN)", "鉄道TransPennine / Northern（ピカデリー駅まで15分 / 約£4〜6）", "メトロリンク・トラムまたはバス（市内まで£4.60）"),
    ("oxford", "オックスフォード", "おっくすふぉーど いぎりす", "Oxford", "GB", "Europe/London", True, "ヒースロー空港(LHR)", "The Airline直行長距離バス（オックスフォード中心部まで約80分 / £25）", "エリザベスライン＋GWR鉄道（レディング駅乗換で約75分）"),
    ("paris", "パリ", "ぱり ふらんす", "Paris", "FR", "Europe/Paris", True, "シャルル・ド・ゴール空港(CDG) / オルリー空港(ORY)", "公定料金タクシー（パリ右岸まで一律56€・左岸まで一律65€ / 約45分）", "RER B線 / ロワシーバス（オペラ座・北駅まで約50分 / 11.80〜16.60€）"),
    ("nice", "ニース（コート・ダジュール）", "にーす もなこ ふらんす", "Nice", "FR", "Europe/Paris", True, "コート・ダジュール空港(NCE)", "トラム2号線（ジャン・メドサン駅・港までわずか25分 / 1.70€）", "トラム2号線（空港ターミナル直結で最速かつ最安）"),
    ("lyon", "リヨン", "りよん ふらんす", "Lyon", "FR", "Europe/Paris", True, "サン・テグジュペリ空港(LYS)", "ローヌエクスプレス・トラム（パール・デュー駅まで29分 / 約16.70€）", "TCL路線バス47番＋トラムT3号線（市内まで約50分 / 2€）"),
    ("mont-saint-michel", "モン・サン・ミッシェル", "もんさんみっしぇる ふらんす", "Mont-Saint-Michel", "FR", "Europe/Paris", True, "パリ・モンパルナス駅（鉄道起点）", "TGV高速鉄道でレンヌ駅（約90分）＋Keolis直行バス（約70分）", "FlixBus / BlaBlaCar直行長距離バス（パリから約4時間半 / 約25€〜）"),
    ("strasbourg", "ストラスブール", "すとらすぶーる ふらんす", "Strasbourg", "FR", "Europe/Paris", True, "ストラスブール国際空港(SXB)", "TER連絡列車（ストラスブール中央駅までわずか9分 / 約5.10€）", "TER列車（1時間に最大4本運行で圧倒的便利）"),
    ("rome", "ローマ", "ろーま いたりあ ばちかん", "Rome", "IT", "Europe/Rome", True, "フィウミチーノ空港(FCO)", "レオナルド・エクスプレス直通列車（テルミニ駅まで32分 / 14€）", "Terravision等の直行シャトルバス（テルミニ駅まで約55分 / 7€）"),
    ("milan", "ミラノ", "みらの いたりあ", "Milan", "IT", "Europe/Rome", True, "マルペンサ空港(MXP) / リナーテ空港(LIN)", "マルペンサ・エクスプレス鉄道（ミラノ中央駅・カドルナ駅まで37〜50分 / 13€）", "空港シャトルバス（ミラノ中央駅まで約55分 / 10€・リナーテからは地下鉄M4で2.2€）"),
    ("venice", "ヴェネツィア（ベネチア）", "べねちあ ゔぇねつぃあ いたりあ", "Venice", "IT", "Europe/Rome", True, "ヴェネツィア・マルコポーロ空港(VCE)", "ATVO急行バス（ローマ広場まで20分 / 10€）", "Alilaguna水上バス（サン・マルコ広場まで海路で約75分 / 15€）"),
    ("florence", "フィレンツェ", "ふぃれんつぇ いたりあ", "Florence", "IT", "Europe/Rome", True, "ペレトラ空港(FLR)", "トラムT2線（サンタ・マリア・ノヴェッラ中央駅まで20分 / 1.70€）", "トラムT2線（空港から中央駅へ直結・1.70€）"),
    ("naples", "ナポリ（アマルフィ・カプリ島）", "なぽり あまるふぃ かぷり いたりあ", "Naples", "IT", "Europe/Rome", True, "ナポリ・カポディキーノ国際空港(NAP)", "Alibus空港シャトルバス（ナポリ中央駅まで15分・港まで30分 / 5€）", "Alibus（クレカタッチ乗車対応・5€）"),
    ("barcelona", "バルセロナ", "ばるせろな すぺいん", "Barcelona", "ES", "Europe/Madrid", True, "バルセロナ・エル・プラット空港(BCN)", "Aerobús空港急行バス（カタルーニャ広場まで35分 / 7.25€）", "国鉄R2 Nord線または市バス46番（パセジ・ダ・グラシア駅まで25分 / 約5€）"),
    ("madrid", "マドリード", "まどりーど すぺいん", "Madrid", "ES", "Europe/Madrid", True, "バラハス国際空港(MAD)", "公定料金タクシー（M-30環状線内の中心部まで一律33€ / 約25分）", "Cercanías国鉄C1/C10線または24時間空港急行バス（アトーチャ駅まで30分 / 2.6〜5€）"),
    ("seville", "セビリア", "せびりあ すぺいん", "Seville", "ES", "Europe/Madrid", True, "セビリア空港(SVQ)", "タクシー（旧市街まで定額約25〜30€ / 約20分）", "EA空港特別バス（サンタ・フスタ駅・アルマス広場まで35分 / 5€）"),
    ("granada", "グラナダ", "ぐらなだ すぺいん", "Granada", "ES", "Europe/Madrid", True, "グラナダ空港(GRX)", "タクシー（アルハンブラ宮殿・中心部まで約25分 / 約30€）", "ALSA空港バス（カテドラル・中心部まで約40分 / 3€）"),
    ("frankfurt", "フランクフルト", "ふらんくふると どいつ", "Frankfurt", "DE", "Europe/Berlin", True, "フランクフルト国際空港(FRA)", "SバーンS8/S9近郊電車（フランクフルト中央駅までわずか11分 / 5.80€）", "SバーンS8/S9（中央駅・ハウプトヴァッヘまで直通）"),
    ("munich", "ミュンヘン", "みゅんへん どいつ", "Munich", "DE", "Europe/Berlin", True, "ミュンヘン国際空港(MUC)", "ルフトハンザ・エクスプレス・バス（ミュンヘン中央駅まで45分 / 約13€）", "SバーンS1/S8近郊電車（マリエン広場・中央駅まで約40分 / 13.60€）"),
    ("berlin", "ベルリン", "べるりん どいつ", "Berlin", "DE", "Europe/Berlin", True, "ベルリン・ブランデンブルク国際空港(BER)", "FEX空港急行列車・RE列車（ベルリン中央駅まで30分 / 4.40€）", "SバーンS9/S45（市内中心部まで4.40€・ABCゾーン切符）"),
    ("zurich", "チューリッヒ", "ちゅーりっひ すいす", "Zurich", "CH", "Europe/Zurich", True, "チューリッヒ国際空港(ZRH)", "スイス国鉄SBB列車（チューリッヒ中央駅までわずか10分 / 6.80CHF）", "SBB列車またはトラム10番（同一ゾーン料金6.80CHF）"),
    ("geneva", "ジュネーブ", "じゅねーぶ すいす", "Geneva", "CH", "Europe/Zurich", True, "ジュネーブ国際空港(GVA)", "スイス国鉄SBB列車（コルナヴァン中央駅までわずか7分 / 3.00CHF）", "SBB列車・UNIRESOバス（10番バスのアプリ等で80分有効チケット購入）"),
    ("interlaken", "インターラーケン（ユングフラウ）", "いんたーらーけん ゆんぐふらう すいす", "Interlaken", "CH", "Europe/Zurich", True, "チューリッヒ空港(ZRH)", "スイス国鉄IC特急（ベルン乗換または直通で約2時間15分 / スイストラベルパス対応）", "SBB早割Supersaverチケット利用（半額以下で乗車可能）"),
    ("zermatt", "ツェルマット（マッターホルン）", "つぇるまっと まったーほるん すいす", "Zermatt", "CH", "Europe/Zurich", True, "チューリッヒ空港(ZRH) / ジュネーブ空港(GVA)", "スイス国鉄IC＋マッターホルン・ゴッタルド鉄道（フィスプ乗換で約3時間半）", "SBB Supersaverチケットまたはスイストラベルパス利用"),
    ("vienna", "ウィーン", "うぃーん おーすとりあ", "Vienna", "AT", "Europe/Vienna", True, "ウィーン国際空港(VIE)", "CATシティ・エアポート・トレイン（ウィーン・ミッテ駅までノンストップ16分 / 14.90€）", "ÖBB国鉄S7近郊列車・Railjet（ミッテ駅・中央駅まで15〜25分 / わずか4.40€）"),
    ("salzburg", "ザルツブルク", "ざるつぶるく おーすとりあ", "Salzburg", "AT", "Europe/Vienna", True, "ザルツブルク空港(SZG)", "タクシー（旧市街・中央駅まで約15分 / 約20€）", "トロリーバス2番・10番（中央駅・旧市街まで約20分 / 2.30€）"),
    ("prague", "プラハ", "ぷらは ちぇこ", "Prague", "CZ", "Europe/Prague", True, "ヴァーツラフ・ハヴェル・プラハ国際空港(PRG)", "Uber Airport公式配車・AEエアポートエクスプレスバス（プラハ本駅まで35分 / 100CZK）", "トロリーバス59番＋地下鉄A線（中心部ムーステク駅まで約30分 / わずか40CZK）"),
    ("amsterdam", "アムステルダム", "あむすてるだむ おらんだ", "Amsterdam", "NL", "Europe/Amsterdam", True, "スキポール国際空港(AMS)", "NSオランダ鉄道（アムステルダム中央駅までわずか14〜17分 / 4.90€）", "NS鉄道（クレカのタッチ決済で改札をそのまま通過可能）"),
    ("brussels", "ブリュッセル", "ぶりゅっせる べるぎー", "Brussels", "BE", "Europe/Brussels", True, "ブリュッセル国際空港(BRU)", "ベルギー国鉄SNCB（ブリュッセル中央駅・南駅まで約17分 / 約10.30€）", "STIB空港バス12番（EU機関エリア・市内まで約30分 / 7.50€）"),
    ("lisbon", "リスボン", "りすぼん ぽるとがる", "Lisbon", "PT", "Europe/Lisbon", True, "ウンベルト・デルガード空港(LIS)", "地下鉄レッドライン（サルダーニャ・中心部まで約20分 / 1.80€）", "地下鉄レッドライン（クレカタッチ乗車対応で1.80€）"),
    ("porto", "ポルト", "ぽると ぽるとがる", "Porto", "PT", "Europe/Lisbon", True, "フランシスコ・サ・カルネイロ空港(OPO)", "メトロE線パープルライン（トリンダーデ駅・中心部まで約27分 / 約2.20€）", "メトロE線（空港ターミナル直結で安価・快適）"),
    ("athens", "アテネ", "あてね ぎりしゃ", "Athens", "GR", "Europe/Athens", True, "アテネ国際空港(ATH)", "地下鉄3号線ブルーライン（シンタグマ広場まで40分 / 9€）", "24時間運行X95急行バス（シンタグマ広場まで約60分 / 5.50€）"),
    ("santorini", "サントリーニ島", "さんとりーに さんとりーにとう ぎりしゃ", "Santorini", "GR", "Europe/Athens", True, "サントリーニ空港(JTR)", "ホテル送迎・タクシー（フィラまで15分・イアまで30分 / 約25〜40€）", "KTEL公共バス（フィラのバスターミナルまで約15分 / 1.60€）"),
    ("dubrovnik", "ドブロブニク", "どぶろぶにく くろあちあ", "Dubrovnik", "HR", "Europe/Zagreb", True, "ドブロブニク空港(DBV)", "Uber・タクシー（旧市街ピレ門まで約25分 / 約30〜35€）", "Platanus公式空港シャトルバス（ピレ門・グルージュ港まで約30分 / 10€）"),
    ("valletta", "マルタ（バレッタ・スリマ）", "まるた ばれった すりま", "Valletta", "MT", "Europe/Malta", True, "マルタ国際空港(MLA)", "Bolt・Uber・空港定額タクシー（バレッタまで約20分・スリマまで25分 / 15〜20€）", "空港急行バスTD2・TD4または路線バスX4（市内まで2〜3€）"),
    ("reykjavik", "レイキャビク（アイスランド）", "れいきゃびく あいすらんど", "Reykjavik", "IS", "Atlantic/Reykjavik", False, "ケプラヴィーク国際空港(KEF)", "Flybus / Airport Direct直行バス（レイキャビク市内・各ホテルまで約45分 / 約3,999ISK）", "公共バスStraeto 55番（市内BSÍバスターミナルまで約70分 / 約2,280ISK）"),
    ("budapest", "ブダペスト", "ぶだぺすと はんがりー", "Budapest", "HU", "Europe/Budapest", True, "リスト・フェレンツ国際空港(BUD)", "100E空港シャトル急行バス（デアーク広場まで35分 / 2,200Ft・タッチ決済可）", "200Eバス＋地下鉄M3線（中心部まで約50分 / 900Ft）"),
    ("helsinki", "ヘルシンキ", "へるしんき ふぃんらんど", "Helsinki", "FI", "Europe/Helsinki", True, "ヘルシンキ・ヴァンター国際空港(HEL)", "VR近郊列車I線・P線（ヘルシンキ中央駅まで約30分 / 4.10€）", "HSLバス600番または列車（どちらもABCゾーン切符4.10€で共通）"),
    ("stockholm", "ストックホルム", "すとっくほるむ すうぇーでん", "Stockholm", "SE", "Europe/Stockholm", True, "アーランダ国際空港(ARN)", "アーランダ・エクスプレス高速列車（中央駅までわずか18分 / 340SEK）", "Flygbussarna / FlixBus空港バス（中央駅まで約45分 / 129SEK〜）"),
    ("oslo", "オスロ", "おすろ のるうぇー", "Oslo", "NO", "Europe/Oslo", True, "オスロ・ガーデモエン空港(OSL)", "Flytoget空港高速列車（オスロ中央駅まで19分 / 240NOK）", "Vy国鉄近郊列車R12/R13/RE10（オスロ中央駅まで23分 / 半額以下の124NOK！）"),
    ("copenhagen", "コペンハーゲン", "こぺんはーげん でんまーく", "Copenhagen", "DK", "Europe/Copenhagen", True, "コペンハーゲン空港(CPH)", "メトロM2線またはDSB国鉄（コンゲンス・ニュートー駅・中央駅まで13〜15分 / 30DKK）", "メトロ・国鉄共通3ゾーン切符（30DKKでわずか15分）"),
    ("warsaw", "ワルシャワ", "わるしゃわ ぽーらんど", "Warsaw", "PL", "Europe/Warsaw", True, "ワルシャワ・ショパン空港(WAW)", "SKM近郊鉄道S2/S3線（ワルシャワ中央駅まで約20分 / 4.40PLN≒約170円）", "市バス175番（旧市街・中央駅まで約25分 / 4.40PLN）"),
    ("krakow", "クラクフ（アウシュヴィッツ拠点）", "くらくふ ぽーらんど", "Krakow", "PL", "Europe/Warsaw", True, "クラクフ・バリツェ空港(KRK)", "Koleje Małopolskie空港列車（クラクフ本駅までわずか17分 / 17PLN）", "市バス209・300番（市内まで約40分 / 6PLN）"),

    # オセアニア
    ("sydney", "シドニー", "しどにー おーすとらりあ", "Sydney", "AU", "Australia/Sydney", True, "シドニー・キングスフォード・スミス国際空港(SYD)", "エアポート・リンク鉄道（セントラル駅・サーキュラーキーまで10〜15分 / 約20.60A$）", "路線バス420番＋電車乗継（空港駅アクセス料を回避して約5A$）"),
    ("melbourne", "メルボルン", "めるぼるん おーすとらりあ", "Melbourne", "AU", "Australia/Melbourne", True, "メルボルン空港(MEL)", "スカイバス・メルボルンシティエクスプレス（サザンクロス駅まで約30分 / 23.90A$）", "路線バス901番＋鉄道ブロードメドウズ駅乗継（mykiカードで約5.30A$）"),
    ("cairns", "ケアンズ", "けあんず おーすとらりあ", "Cairns", "AU", "Australia/Brisbane", False, "ケアンズ国際空港(CNS)", "タクシー・Uber（ケアンズ市内中心部までわずか10分 / 約25〜30A$）", "空港乗合シャトルバス（市内ホテルまで約15分 / 約15A$）"),
    ("gold-coast", "ゴールドコースト", "ごーるどこーすと おーすとらりあ", "Gold Coast", "AU", "Australia/Brisbane", False, "ゴールドコースト空港(OOL)", "Uber・タクシー（サーファーズパラダイスまで約35分 / 約60〜75A$）", "777番バス＋G:linkトラム（サーファーズパラダイスまで約45分 / わずか0.50A$！）"),
    ("brisbane", "ブリスベン", "ぶりすべん おーすとらりあ", "Brisbane", "AU", "Australia/Brisbane", False, "ブリスベン空港(BNE)", "エアトレイン空港鉄道（ブリスベンセントラル駅まで20分 / 21.90A$）", "Uber（2〜3人以上ならエアトレインより割安・約45A$）"),
    ("perth", "パース", "ぱーす おーすとらりあ", "Perth", "AU", "Australia/Perth", False, "パース空港(PER)", "トランスパース鉄道エアポートライン（パース駅までわずか18分 / 5.10A$）", "エアポートライン鉄道（速くて激安の5.10A$）"),
    ("auckland", "オークランド", "おーくらんど にゅーじーらんど", "Auckland", "NZ", "Pacific/Auckland", True, "オークランド国際空港(AKL)", "SkyDrive直行バス（スカイシティ中心部まで約35分 / 20NZ$）", "AirportLinkバス＋鉄道（プヒヌイ駅乗換でブリトマート駅まで約45分 / 約6NZ$）"),
    ("queenstown", "クイーンズタウン", "くいーんずたうん にゅーじーらんど", "Queenstown", "NZ", "Pacific/Auckland", True, "クイーンズタウン空港(ZQN)", "タクシー・Uber（中心部まで約15分 / 約35〜45NZ$）", "Orbus公共バス1番（中心部まで約20分 / Bee Card利用で2NZ$・現金10NZ$）"),
    ("christchurch", "クライストチャーチ", "くらいすとちゃーち にゅーじーらんど", "Christchurch", "NZ", "Pacific/Auckland", True, "クライストチャーチ国際空港(CHC)", "Uber・タクシー（市内中心部まで約20分 / 約40NZ$）", "メトロバス3番・29番（バスインターチェンジまで約30分 / 現金4NZ$・カード2NZ$）"),
    ("nadi", "フィジー（ナンディ）", "ふぃじー なんでぃ", "Nadi", "FJ", "Pacific/Fiji", False, "ナンディ国際空港(NAN)", "空港公認イエロータクシー（デナラウ地区リゾートまで約20分 / 約30〜35FJ$）", "ローカルバス（ナンディタウンまで約15分 / 約2FJ$）"),
    ("noumea", "ニューカレドニア（ヌメア）", "にゅーかれどにあ ぬめあ", "Noumea", "NC", "Pacific/Noumea", False, "ラ・トントゥータ国際空港(NOU)", "エアポートシャトルバス（ヌメア市内ホテルまで約45〜60分 / 約3,000XPF）", "Raï長距離バス（市内まで格安移動・本数限定）"),
    ("tahiti", "タヒチ（パペーテ・ボラボラ）", "たひち ぱぺーて ぼらぼら", "Tahiti", "PF", "Pacific/Tahiti", False, "ファアア国際空港(PPT)", "タクシー（パペーテ中心部まで約15分 / 約2,000〜2,500XPF）", "Terevau高速フェリー（モーレア島へ30分）または国内線（ボラボラ島へ50分）"),

    # 中東・アフリカ
    ("dubai", "ドバイ", "どばい あらぶ", "Dubai", "AE", "Asia/Dubai", False, "ドバイ国際空港(DXB)", "ドバイ・メトロ・レッドライン（ブルジュ・ハリファ駅まで約25分 / 約8AED）", "公営タクシー・Careem（初乗り25AED〜・市内中心部まで約50〜70AEDで激安）"),
    ("abu-dhabi", "アブダビ", "あぶだび あらぶ", "Abu Dhabi", "AE", "Asia/Dubai", False, "ザイード国際空港(AUH)", "タクシー・Careem（市内中心部・シェイクザイードモスクまで約20〜30分 / 約70〜90AED）", "空港急行バスA1・A2（市内中心部まで約45分 / 4AED）"),
    ("istanbul", "イスタンブール", "いすたんぶーる とるこ", "Istanbul", "TR", "Europe/Istanbul", False, "イスタンブール空港(IST) / サビハ・ギョクチェン空港(SAW)", "Havaist空港リムジンバス（スルタンアフメット・タクシム広場まで約60〜80分 / 約200〜250₺）", "地下鉄M11号線＋M2号線乗り継ぎ（市内中心部まで約50分 / 約50₺）"),
    ("cappadocia", "カッパドキア", "かっぱどきあ とるこ", "Cappadocia", "TR", "Europe/Istanbul", False, "ネヴシェヒル空港(NAV) / カイセリ空港(ASR)", "事前予約乗合シャトルバン（ギョレメの洞窟ホテルまで直接送迎・約40〜60分 / 約10〜15€）", "ホテル手配シャトル（公共交通がないため事前予約シャトルが最安かつ確実）"),
    ("ankara", "アンカラ", "あんから とるこ", "Ankara", "TR", "Europe/Istanbul", False, "エセンボーア国際空港(ESB)", "Havaş空港シャトルバス・442番EGOバス（クズライ広場・AŞTİまで約45分 / 約100₺）", "442番EGO市バス（中心部まで24時間運行）"),
    ("izmir", "イズミル（エフェソス拠点）", "いずみいる えふぇそす とるこ", "Izmir", "TR", "Europe/Istanbul", False, "アドナン・メンデレス空港(ADB)", "İZBAN近郊鉄道（アルサンジャック駅まで約30分・セルチュク/エフェソス方面も直結）", "Havaş空港バス（市内中心部まで約40分）"),
    ("doha", "ドーハ", "どーは かたーる", "Doha", "QA", "Asia/Qatar", False, "ハマド国際空港(DOH)", "ドーハ・メトロ・レッドライン（スーク・ワキーフ・ウエストベイまで約15〜20分 / わずか2QR！）", "ドーハ・メトロ（世界最高峰の清潔さと安さ・1日券でも6QR）"),
    ("cairo", "カイロ（ギザのピラミッド）", "かいろ ぴらみっど えじぷと", "Cairo", "EG", "Africa/Cairo", True, "カイロ国際空港(CAI)", "Uber（タハリール広場・ギザのピラミッド周辺まで約40〜60分 / 約250〜400E£）", "エアコン付き空港バス（タハリール広場まで約50分 / 約25E£）"),
    ("marrakech", "マラケシュ", "まらけしゅ もろっこ", "Marrakech", "MA", "Africa/Casablanca", False, "マラケシュ・メナラ空港(RAK)", "空港公認タクシー（フナ広場・新市街まで約15分 / 定額70〜100DH）", "ALSA空港急行バスL19（フナ広場まで約20分 / 30DH・往復50DH）"),
    ("casablanca", "カサブランカ", "かさぶらんか もろっこ", "Casablanca", "MA", "Africa/Casablanca", False, "ムハンマド5世国際空港(CMN)", "ONCF空港連絡列車（カサ・ヴォヤジャー駅・カサ・ポール駅まで約35〜45分 / 50DH）", "ONCF空港列車（1時間に1本運行・渋滞なしで最も安全確実）"),
    ("cape-town", "ケープタウン", "けーぷたうん みなみあふりか", "Cape Town", "ZA", "Africa/Johannesburg", False, "ケープタウン国際空港(CPT)", "Uber・空港公認タクシー（ウォーターフロント・市内中心部まで約20〜25分 / 約200〜300R）", "Uber（安全面から夜間や荷物ありの移動はUber一択）"),
    ("johannesburg", "ヨハネスブルグ", "よはねすぶるぐ みなみあふりか", "Johannesburg", "ZA", "Africa/Johannesburg", False, "O・R・タンボ国際空港(JNB)", "ハウトレイン高速鉄道（サントン駅までわずか15分 / 約220R）", "ハウトレイン＋サントン駅からホテルまでUber（安全性と速さを両立）")
]


def generate_cities_data() -> list:
    cities = []
    for item in RAW_CITIES:
        slug, name_ja, kana_kw, name_en, cc, tz, has_dst, airport, fastest, cheapest = item
        p = COUNTRY_PROFILES[cc]
        dst_note = "あり（春〜秋は時計が1時間進みます。上の時計はサマータイム自動反映済み）" if has_dst else "なし（年間を通じて時差は一定です）"
        trans_note = "スマホ・PC・カメラ等の充電器（100-240V対応表記）は変圧器不要。日本の100V専用ドライヤーやヘアアイロンは変圧器が必要です。" if p["voltage"] not in ("120V", "110V") else "電圧が日本(100V)と近いため、短期旅行ならスマホ充電器や多くの電化製品がそのまま使えます。"

        if p.get("special_ui") == "china_vpn":
            telecom_note = f"{name_ja}（中国本土）では、ネット検閲（グレートファイアウォール）により現地のホテルWi-Fiや一般SIMではLINE・Instagram・Googleマップ・Gmail・YouTube等が一切繋がりません。必ず日本出発前に「壁越え対応のローミングeSIM」または「中国対応VPN」をインストールしてください。"
        else:
            telecom_note = f"{name_ja}（{p['country_ja']}）では空港からの移動・配車アプリ（{p['apps'][0]}等）・キャッシュレス決済に常時通信が必須です。到着前に日本でeSIMを設定しておくと空港に降りた瞬間から繋がります。"

        cities.append({
            "slug": slug,
            "name_ja": name_ja,
            "kana_kw": kana_kw + " " + p.get("country_kana", ""),
            "name_en": name_en,
            "country_ja": p["country_ja"],
            "region": p["region"],
            "timezone": tz,
            "has_dst": has_dst,
            "dst_note": dst_note,
            "plug_type": p["plug"],
            "voltage": p["voltage"],
            "frequency": p["freq"],
            "transformer_needed": p["trans"],
            "transformer_note": trans_note,
            "currency_code": p["curr"],
            "currency_name": p["curr_ja"],
            "currency_symbol": p["sym"],
            "tip_level": p["tip"],
            "tip_badge": p["tip_badge"],
            "tip_detail": p["tip_detail"],
            "tax_note": p["tax"],
            "tap_water_safe": p["water"],
            "tap_water_note": p["water_note"],
            "emergency_numbers": p["emerg"],
            "embassy": p["embassy"],
            "mofa_url": p["mofa_url"],
            "safety_note": p["safety_note"],
            "special_ui": p.get("special_ui", "standard"),
            "airport_access": {
                "airport_name": airport,
                "fastest": fastest,
                "cheapest": cheapest
            },
            "transport_apps": p["apps"],
            "telecom_note": telecom_note
        })
    return cities


def fetch_exchange_rates() -> dict:
    api_url = "https://open.er-api.com/v6/latest/JPY"
    jst = timezone(timedelta(hours=9))
    now_jst = datetime.now(jst).strftime("%Y-%m-%d %H:%M JST")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            if data.get("result") == "success":
                return {"updated_at": now_jst, "base": "JPY", "rates": data["rates"]}
    except Exception:
        pass

    return {
        "updated_at": now_jst,
        "base": "JPY",
        "rates": {
            "USD": 0.0065, "EUR": 0.0061, "GBP": 0.0051, "KRW": 9.1, "TWD": 0.21,
            "THB": 0.22, "SGD": 0.0087, "VND": 165.0, "PHP": 0.38, "MYR": 0.029,
            "IDR": 103.0, "HKD": 0.050, "MOP": 0.052, "CNY": 0.047, "INR": 0.55,
            "LKR": 1.9, "NPR": 0.88, "UZS": 83.0, "KZT": 3.2, "CAD": 0.0091,
            "MXN": 0.13, "PEN": 0.024, "BOB": 0.045, "CLP": 6.3, "BRL": 0.038,
            "ARS": 6.4, "CHF": 0.0057, "CZK": 0.15, "ISK": 0.90, "HUF": 2.45,
            "SEK": 0.070, "NOK": 0.072, "DKK": 0.045, "PLN": 0.026, "AUD": 0.010,
            "NZD": 0.011, "FJD": 0.015, "XPF": 0.73, "AED": 0.024, "TRY": 0.22,
            "QAR": 0.024, "EGP": 0.32, "MAD": 0.065, "ZAR": 0.12
        }
    }


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


def render_gtm_head() -> str:
    return f"""<script async src="https://www.googletagmanager.com/gtm.js?id={GTM_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
  </script>"""


def render_telecom_box(city: dict) -> str:
    if city["special_ui"] == "china_vpn":
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border-2 border-rose-300">
      <div class="flex items-center justify-between">
        <h2 class="text-sm font-extrabold flex items-center gap-1.5 text-rose-800">🛡️ 中国ネット検閲（金盾）対策：VPN・壁越えeSIM必須</h2>
        <span class="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded-full">重要</span>
      </div>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2.5">
        <div class="p-3 rounded-xl bg-blue-50 border border-blue-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-blue-900">📱 壁越え対応！中国ローミングeSIM</p>
            <p class="text-[11px] text-slate-600 mt-0.5">VPN設定不要でそのままLINE・Google・インスタが使える香港/国際ローミング仕様eSIM。</p>
          </div>
          <a href="{AFFILIATE_ESIM_URL}" class="mt-2.5 block bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3 py-2 rounded-lg text-center transition">
            中国対応eSIMを見る →
          </a>
        </div>
        <div class="p-3 rounded-xl bg-rose-50 border border-rose-200 flex flex-col justify-between">
          <div>
            <p class="text-xs font-bold text-rose-900">🔒 ホテルWi-Fi・PC作業にはVPN必須</p>
            <p class="text-[11px] text-slate-600 mt-0.5">現地到着後はVPNサイト自体がブロックされます。必ず日本出発前にアプリを入れておきましょう。</p>
          </div>
          <a href="{AFFILIATE_VPN_URL}" class="mt-2.5 block bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold px-3 py-2 rounded-lg text-center transition">
            中国で繋がるVPNを見る →
          </a>
        </div>
      </div>
    </section>"""
    else:
        return f"""
    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <h2 class="text-sm font-bold flex items-center gap-1.5">📶 現地の通信・ネット環境</h2>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 p-3.5 rounded-xl bg-blue-50 border border-blue-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <p class="text-xs font-bold text-blue-900">📱 搭乗前に5分で開通！{city['country_ja']}対応eSIM</p>
          <p class="text-[11px] text-slate-600 mt-0.5">SIMピン不要・空港に着いた瞬間からマップや配車アプリ（{city['transport_apps'][0]}）が使えます。</p>
        </div>
        <a href="{AFFILIATE_ESIM_URL}" class="shrink-0 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3.5 py-2.5 rounded-lg text-center transition">
          最安eSIMを見る →
        </a>
      </div>
    </section>"""


def render_context_affiliate(city: dict) -> str:
    ui_type = city.get("special_ui", "standard")
    if ui_type == "us_tip_medical":
        return f"""
        <div class="p-4 rounded-xl bg-rose-50 border border-rose-200 mt-3 space-y-2">
          <p class="text-xs font-bold text-rose-900">🏥 {city['name_ja']}は医療費が超高額＆カード決済社会</p>
          <p class="text-xs text-slate-700 leading-relaxed">北米の救急搬送・入院は数百万円単位の請求になるケースが珍しくありません。キャッシュレス診療対応の海外旅行保険と、海外事務手数料が安いタッチ決済カードの2枚持ちが必須です。</p>
          <div class="flex flex-wrap gap-3 pt-1">
            <a href="{AFFILIATE_INSURANCE_URL}" class="text-xs font-bold text-rose-700 underline">→ 高額医療対応の保険・付帯カードを見る</a>
            <a href="{AFFILIATE_CARD_URL}" class="text-xs font-bold text-blue-600 underline">→ 海外手数料が安いカード・Wise比較</a>
          </div>
        </div>"""
    elif ui_type == "europe_cashless":
        return f"""
        <div class="p-4 rounded-xl bg-indigo-50 border border-indigo-200 mt-3">
          <p class="text-xs font-bold text-indigo-900">💳 {city['name_ja']}は地下鉄もカフェもタッチ決済（コンタクトレス）主流</p>
          <p class="text-xs text-slate-700 mt-1">一般的な日本のクレジットカードは海外事務手数料（約2.2〜3.85%）が毎回上乗せされます。リアルレートで決済できるデビット（Wise等）や海外特化カードを準備すると数千円〜数万円節約できます。</p>
          <a href="{AFFILIATE_CARD_URL}" class="inline-block mt-2 text-xs font-bold text-indigo-700 underline">→ ヨーロッパ渡航におすすめの決済カード・Wiseを見る</a>
        </div>"""
    elif ui_type == "altitude_alert":
        return f"""
        <div class="p-4 rounded-xl bg-amber-50 border border-amber-300 mt-3">
          <p class="text-xs font-bold text-amber-900">⛰️ 高地（標高3,000m超）の体調不良・高山病対策</p>
          <p class="text-xs text-slate-700 mt-1">{city['name_ja']}周辺は標高が高く、高山病による酸素吸入や私立クリニック受診が発生しやすい地域です。必ず救援者費用・キャッシュレス診療付きの海外旅行保険を準備して渡航してください。</p>
          <a href="{AFFILIATE_INSURANCE_URL}" class="inline-block mt-2 text-xs font-bold text-amber-900 underline">→ 海外旅行保険・利用付帯カードを確認する</a>
        </div>"""
    elif not city["tap_water_safe"]:
        return f"""
        <div class="p-4 rounded-xl bg-amber-50 border border-amber-200 mt-3">
          <p class="text-xs font-bold text-amber-900">⚠️ {city['name_ja']}は水道水の直接飲用NG</p>
          <p class="text-xs text-slate-700 mt-1">水質や氷の違いによる急な胃腸炎・発熱時、現地の日本語対応私立病院は高額になります。キャッシュレス診療対応の海外旅行保険（または付帯クレカ）を必ず準備しておきましょう。</p>
          <a href="{AFFILIATE_INSURANCE_URL}" class="inline-block mt-2 text-xs font-bold text-blue-600 underline">→ {city['country_ja']}対応の海外旅行保険・付帯カードを見る</a>
        </div>"""
    return ""


def build_city_html(city: dict, rates_data: dict, all_cities: list) -> str:
    code = city["currency_code"]
    jpy_to_local = rates_data["rates"].get(code, 0.01)
    local_to_jpy = round(1 / jpy_to_local, 2) if jpy_to_local >= 0.005 else round(1 / jpy_to_local, 4)
    thousand_jpy_in_local = round(1000 * jpy_to_local, 2)

    related = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:10]
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
                "name": f"{city['name_ja']}でチップは必要ですか？相場は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"{city['tip_badge']}です。{city['tip_detail']}"}
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}の空港から市内へのアクセス方法は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"{city['airport_access']['airport_name']}から市内へは、最速が「{city['airport_access']['fastest']}」、最安が「{city['airport_access']['cheapest']}」です。"}
            },
            {
                "@type": "Question",
                "name": f"{city['name_ja']}の治安・緊急連絡先・日本大使館の情報は？",
                "acceptedAnswer": {"@type": "Answer", "text": f"緊急通報は「{city['emergency_numbers']}」、管轄公館は「{city['embassy']}」です。{city['safety_note']}"}
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_gtm_head()}
  <title>{city['name_ja']}の現地情報まとめ｜時差・コンセント({city['plug_type']})・チップ・治安・為替を1画面で即答</title>
  <meta name="description" content="{city['name_ja']}（{city['country_ja']}）の現在時刻・時差、コンセントのプラグ形状（{city['plug_type']}）・電圧（{city['voltage']}）、チップ相場、最新為替レート、{city['airport_access']['airport_name']}からの移動手段、外務省安全情報・大使館連絡先を1画面で即確認。">
  <link rel="canonical" href="{SITE_URL}/{city['slug']}/">
  <link rel="manifest" href="../manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-12">
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

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-2.5">
      <h2 class="text-sm font-bold flex items-center gap-1.5 text-slate-800">✈️ {city['airport_access']['airport_name']}から市内への移動</h2>
      <div class="text-xs space-y-2 text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
        <p><span class="inline-block bg-blue-100 text-blue-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最速・快適</span>{city['airport_access']['fastest']}</p>
        <p><span class="inline-block bg-emerald-100 text-emerald-800 font-bold px-1.5 py-0.5 rounded text-[10px] mr-1">最安・定番</span>{city['airport_access']['cheapest']}</p>
      </div>
      <div class="text-xs text-slate-700 pt-1">
        <strong class="text-slate-900">必須の移動・配車アプリ：</strong>{', '.join(city['transport_apps'])}
      </div>
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
      {render_context_affiliate(city)}
    </section>

    <section class="bg-white p-4 rounded-2xl shadow-sm border-l-4 border-l-rose-500 border border-slate-200 space-y-3">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-sm font-extrabold text-slate-900 flex items-center gap-1.5">🚨 安全・防犯・外務省＆日本大使館情報</h2>
        <span class="text-[11px] bg-rose-50 text-rose-700 font-bold px-2.5 py-0.5 rounded-full border border-rose-200">緊急通報: {city['emergency_numbers']}</span>
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

    <section class="pt-2">
      <h3 class="text-xs font-bold text-slate-500 mb-2">🗺️ {city['region']}の他の都市をチェック</h3>
      <div class="flex flex-wrap gap-1.5">{related_html}</div>
    </section>

    <footer class="pt-6 pb-4 text-center text-[11px] text-slate-400 space-y-1">
      <p>※本ページはプロモーションが含まれています。渡航前に必ず外務省・各国大使館の最新公式情報をご確認ください。</p>
      <p>© {SITE_NAME} ({SITE_URL})</p>
    </footer>
  </main>

  <script>
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

    const rate = {jpy_to_local};
    const jpyInput = document.getElementById('jpy-input');
    const localOutput = document.getElementById('local-output');
    jpyInput.addEventListener('input', () => {{
      const val = parseFloat(jpyInput.value) || 0;
      localOutput.textContent = `≒ ${{(val * rate).toFixed(2)}} {code}`;
    }});

    if ('serviceWorker' in navigator) {{
      navigator.serviceWorker.register('../sw.js').catch(() => {{}});
    }}
  </script>
</body>
</html>"""


def build_index_html(cities: list, rates_data: dict) -> str:
    unique_regions = ["すべて"] + sorted(list({c["region"] for c in cities}))

    region_buttons = "".join([
        f'<button data-region="{r}" class="region-btn shrink-0 px-3 py-1.5 rounded-full text-xs font-bold border transition '
        f'{"bg-slate-900 text-white border-slate-900" if r == "すべて" else "bg-white text-slate-600 border-slate-200"}">{r}</button>'
        for r in unique_regions
    ])

    cards_html = "\n".join([
        f'<a href="./{c["slug"]}/" data-region="{c["region"]}" '
        f'data-name="{c["name_ja"]}" data-country="{c["country_ja"]}" data-slug="{c["slug"]}" '
        f'data-search="{c["name_ja"]} {c["kana_kw"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}" '
        f'class="city-card block bg-white p-3.5 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition">'
        f'<div class="flex items-center justify-between gap-1">'
        f'<span class="font-extrabold text-sm text-slate-900">{c["name_ja"]}</span>'
        f'<span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium shrink-0">{c["country_ja"]}</span>'
        f'</div>'
        f'<div class="text-[11px] text-slate-500 mt-1.5 flex items-center gap-2 flex-wrap">'
        f'<span>🔌 {c["plug_type"]}</span>'
        f'<span>💱 {c["currency_code"]}</span>'
        f'<span>💵 チップ{c["tip_badge"].split("（")[0]}</span>'
        f'{"<span class=\"text-[10px] text-rose-600 font-bold\">🛡️要VPN/eSIM</span>" if c["special_ui"] == "china_vpn" else ""}'
        f'</div>'
        f'</a>'
        for c in cities
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  {render_gtm_head()}
  <title>{SITE_NAME}｜世界{len(cities)}都市の時差・コンセント・チップ・治安・為替を1画面で即答</title>
  <meta name="description" content="海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・コンセント形状・電圧・チップ相場・最新為替レート・外務省安全情報・空港アクセスをスクロールなしで即解決。">
  <link rel="canonical" href="{SITE_URL}/">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  <main class="max-w-3xl mx-auto px-4 pt-8 space-y-6">
    <div class="text-center space-y-2">
      <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">🌐 {SITE_NAME}</h1>
      <p class="text-xs sm:text-sm text-slate-600">世界{len(cities)}都市の「時差・プラグ・チップ・為替・空港移動・外務省安全情報」を1画面で即答</p>
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

    <footer class="pt-8 text-center text-xs text-slate-400 space-y-2">
      <p>🔗 安全な渡航のために：<a href="https://www.anzen.mofa.go.jp/" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">外務省 海外安全ホームページ</a> / <a href="https://www.ezairyu.mofa.go.jp/tabireg/index.html" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-600">たびレジ</a></p>
      <p>© {SITE_NAME} ({SITE_URL})</p>
    </footer>
  </main>

  <script>
    let currentRegion = 'すべて';
    const searchInput = document.getElementById('search');
    const suggestBox = document.getElementById('suggest-box');
    const cards = Array.from(document.querySelectorAll('.city-card'));
    const regionBtns = document.querySelectorAll('.region-btn');

    // カタカナをひらがなに統一して検索精度を上げる関数
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

      // 予測変換（オートコンプリート）ドロップダウンの描画
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

    // 検索欄の外側をクリックしたら予測候補を閉じる
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


def write_auxiliary_files(dist_dir: Path):
    # GitHub Pagesでカスタムドメイン(tokou-pocket.com)が毎回のデプロイで消えないようCNAMEファイルを自動出力
    (dist_dir / "CNAME").write_text("tokou-pocket.com\n", encoding="utf-8")

    manifest = {
        "name": SITE_NAME,
        "short_name": SITE_NAME,
        "start_url": "./",
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#0f172a"
    }
    (dist_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    sw_js = """const CACHE_NAME = 'pocket-guide-v2';
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      return cached || fetch(event.request).then((response) => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      });
    })
  );
});
"""
    (dist_dir / "sw.js").write_text(sw_js, encoding="utf-8")

    wf_dir = Path(".github/workflows")
    wf_dir.mkdir(parents=True, exist_ok=True)
    workflow_yml = """name: Daily Rate Update & Deploy Pages
on:
  schedule:
    - cron: '0 21 * * *'
  workflow_dispatch:
  push:
    branches: [ main ]

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  build_and_deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Generate all city pages with latest exchange rates
        run: python3 setup_and_build.py
      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
    (wf_dir / "daily_update.yml").write_text(workflow_yml, encoding="utf-8")


def main():
    data_dir = Path("data")
    dist_dir = Path("dist")
    data_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)

    cities = generate_cities_data()
    (data_dir / "cities.json").write_text(json.dumps(cities, ensure_ascii=False, indent=2), encoding="utf-8")

    rates_data = fetch_exchange_rates()
    (data_dir / "rates.json").write_text(json.dumps(rates_data, ensure_ascii=False, indent=2), encoding="utf-8")

    urls = [f"{SITE_URL}/"]
    for city in cities:
        city_dir = dist_dir / city["slug"]
        city_dir.mkdir(parents=True, exist_ok=True)
        html = build_city_html(city, rates_data, cities)
        (city_dir / "index.html").write_text(html, encoding="utf-8")
        urls.append(f"{SITE_URL}/{city['slug']}/")

    index_html = build_index_html(cities, rates_data)
    (dist_dir / "index.html").write_text(index_html, encoding="utf-8")

    sitemap_items = "\n".join([f"  <url><loc>{u}</loc></url>" for u in urls])
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>'
    (dist_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
    (dist_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    write_auxiliary_files(dist_dir)
    print(f"✅ 完了！ 全 {len(cities)} 都市のページとCNAME・サイトマップを生成しました。")


if __name__ == "__main__":
    main()
