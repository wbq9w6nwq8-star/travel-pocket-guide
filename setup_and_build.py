#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渡航ポケット辞典（世界108都市プログラムSEOサイト）オールインワン生成スクリプト
"""

import json
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ==========================================
# 1. 基本設定
# ==========================================
SITE_URL = "https://wbq9w6nwq8-star.github.io/travel-pocket-guide"
SITE_NAME = "渡航ポケット辞典"

AFFILIATE_ESIM_URL = "#YOUR_ESIM_AFFILIATE_LINK"
AFFILIATE_CARD_URL = "#YOUR_CARD_AFFILIATE_LINK"
AFFILIATE_INSURANCE_URL = "#YOUR_INSURANCE_AFFILIATE_LINK"

# ==========================================
# 2. 国・地域別ベースプロファイル
# ==========================================
COUNTRY_PROFILES = {
    "KR": {"country_ja": "韓国", "region": "アジア", "plug": "C/SE", "voltage": "220V", "freq": "60Hz", "trans": False, "curr": "KRW", "curr_ja": "ウォン", "sym": "₩", "tip": "none", "tip_badge": "不要", "tip_detail": "韓国にチップの習慣はありません。高級ホテルやレストランではサービス料10%が加算される場合があります。", "tax": "付加価値税(VAT)10%。免税店やTax Free加盟店で15,000ウォン以上購入時、空港や市内キオスクで即時または事後還付可能。", "water": False, "water_note": "水道水はそのまま飲まず、市販のミネラルウォーター推奨。飲食店の無料の水は浄水器のものです。", "emerg": "警察112 / 救急・消防119", "apps": ["Kakao T（タクシー）", "NAVERマップ（必須・Googleマップ非対応）", "Subway Korea"]},
    "TW": {"country_ja": "台湾", "region": "アジア", "plug": "A", "voltage": "110V", "freq": "60Hz", "trans": False, "curr": "TWD", "curr_ja": "ニュー台湾ドル", "sym": "NT$", "tip": "none", "tip_badge": "不要", "tip_detail": "基本的に不要。レストランでは会計に10%のサービス料が含まれることが多いです。", "tax": "営業税5%。特定マークのある店舗で同日2,000台湾ドル以上購入すると空港等で還付申請が可能。", "water": False, "water_note": "水道水の直接飲用は不可。必ずミネラルウォーターを購入するか煮沸してください。", "emerg": "警察110 / 救急消防119", "apps": ["Uber", "Googleマップ", "台湾公車通"]},
    "TH": {"country_ja": "タイ", "region": "アジア", "plug": "A/B3/C", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "THB", "curr_ja": "バーツ", "sym": "฿", "tip": "optional", "tip_badge": "気持ち程度（20〜100B）", "tip_detail": "屋台や食堂は不要。マッサージは50〜100バーツ、ホテルのポーターやベッドメイクは20〜50バーツ程度がスマート。", "tax": "VAT 7%。VAT Refund加盟店で同日2,000バーツ以上購入すると空港で還付手続き可能。", "water": False, "water_note": "水道水は飲用不可。氷も衛生的な店舗以外は注意が必要です。", "emerg": "観光警察1155 / 警察191 / 救急1669", "apps": ["Grab（配車・デリバリー必須）", "Bolt", "Googleマップ"]},
    "SG": {"country_ja": "シンガポール", "region": "アジア", "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "SGD", "curr_ja": "シンガポールドル", "sym": "S$", "tip": "none", "tip_badge": "不要（サービス料込）", "tip_detail": "原則不要。ほとんどのレストランやホテルで10%のサービス料が自動で加算されます。", "tax": "GST 9%。加盟店で100S$以上購入時、チャンギ空港の電子キオスク(eTRS)で簡単に免税還付が可能。", "water": True, "water_note": "水道水はWHO基準を満たしておりそのまま飲用可能ですが、気になる場合は市販水を推奨。", "emerg": "警察999 / 救急・消防995", "apps": ["Grab", "Gojek", "Citymapper"]},
    "VN": {"country_ja": "ベトナム", "region": "アジア", "plug": "A/C", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "VND", "curr_ja": "ドン", "sym": "₫", "tip": "optional", "tip_badge": "気持ち程度（スパ・高級店）", "tip_detail": "ローカル店は不要。スパやマッサージでは50,000〜100,000ドン程度渡すのが一般的。", "tax": "VAT 8〜10%。対象店舗で200万ドン以上購入時、国際空港で85%相当のVAT還付が可能。", "water": False, "water_note": "水道水は飲用不可。歯磨きもミネラルウォーターを使う方が安心です。", "emerg": "警察113 / 消防114 / 救急115", "apps": ["Grab（ぼったくり防止に必須）", "Be", "Googleマップ"]},
    "PH": {"country_ja": "フィリピン", "region": "アジア", "plug": "A/B/C", "voltage": "220V", "freq": "60Hz", "trans": False, "curr": "PHP", "curr_ja": "ペソ", "sym": "₱", "tip": "optional", "tip_badge": "10%程度（サ料なしの場合）", "tip_detail": "レシートにService Charge(SC)が含まれていなければ会計の10%程度。マッサージやポーターは20〜50ペソ。", "tax": "VAT 12%。観光客向けの免税還付制度は限定的。", "water": False, "water_note": "水道水は飲用不可。市販のペットボトル水を必ず購入してください。", "emerg": "緊急通報911（警察・救急・消防共通）", "apps": ["Grab（安全移動に必須）", "JoyRide", "Googleマップ"]},
    "MY": {"country_ja": "マレーシア", "region": "アジア", "plug": "BF", "voltage": "240V", "freq": "50Hz", "trans": False, "curr": "MYR", "curr_ja": "リンギット", "sym": "RM", "tip": "none", "tip_badge": "不要", "tip_detail": "基本的に不要。レストランやホテルでは10%のサービス料が含まれています。", "tax": "SST（売上・サービス税）6〜8%。原則として旅行者向けの免税還付制度はなし。", "water": False, "water_note": "水道水は配管が古い場合があるため、そのまま飲まずミネラルウォーターまたは煮沸を推奨。", "emerg": "警察・救急999 / 消防994", "apps": ["Grab（圧倒的シェア）", "AirAsia Ride", "Googleマップ"]},
    "ID": {"country_ja": "インドネシア", "region": "アジア", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "IDR", "curr_ja": "ルピア", "sym": "Rp", "tip": "optional", "tip_badge": "気持ち程度（5〜10%）", "tip_detail": "サービス料込のレストランは不要。スパやドライバー、ポーターには10,000〜50,000ルピア程度渡すと喜ばれます。", "tax": "VAT 11%。「VAT Refund for Tourists」加盟店で一定額以上購入すると主要空港で還付可能。", "water": False, "water_note": "水道水は絶対に飲用不可（バリ腹の原因になります）。うがいや歯磨きもペットボトル水を推奨。", "emerg": "総合緊急112 / 警察110 / 救急118", "apps": ["Grab", "Gojek（バイク・車・配達すべて対応）", "Bluebird（タクシー）"]},
    "HK": {"country_ja": "香港", "region": "アジア", "plug": "BF", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "HKD", "curr_ja": "香港ドル", "sym": "HK$", "tip": "optional", "tip_badge": "端数〜10%（サ料別の場合）", "tip_detail": "多くの飲食店で10%のサービス料（加一服務費）が加算されます。タクシーは端数切り上げ、ホテルのポーターは10〜20HKD。", "tax": "香港は消費税・付加価値税がないフリーポートのため、街中すべての買い物が最初から免税価格です。", "water": False, "water_note": "水道水は基準を満たしていますが、配管の都合上、煮沸するかミネラルウォーターの購入が一般的です。", "emerg": "警察・救急・消防 999", "apps": ["MTR Mobile", "Uber", "HK Taxi"]},
    "MO": {"country_ja": "マカオ", "region": "アジア", "plug": "BF", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "MOP", "curr_ja": "パタカ（香港ドルも流通）", "sym": "MOP$", "tip": "optional", "tip_badge": "端数〜10%", "tip_detail": "香港と同様、10%のサービス料が含まれる店舗が多数。香港ドルがほぼ1:1でそのまま使えます。", "tax": "消費税はなく、全域で免税価格での買い物が可能です。", "water": False, "water_note": "水道水の直接飲用は避け、ホテルの無料ボトル水や市販水を利用してください。", "emerg": "警察・救急・消防 999", "apps": ["マカオ電召（タクシー）", "バス移動アプリ（巴士報站）"]},
    "CN": {"country_ja": "中国", "region": "アジア", "plug": "A/O", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "CNY", "curr_ja": "人民元", "sym": "元", "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。現金よりもAlipayやWeChat Payの事前登録（日本のクレカ紐付け）が必須です。", "tax": "増値税13%。Tax Free指定店で500元以上購入時、空港で還付手続きが可能。", "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。", "emerg": "警察110 / 救急120 / 消防119", "apps": ["Alipay（決済・配車・地下鉄すべて完結）", "WeChat", "高徳地図 / 百度地図"]},
    "IN": {"country_ja": "インド", "region": "アジア", "plug": "C/BF/B3", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "INR", "curr_ja": "インドルピー", "sym": "₹", "tip": "optional", "tip_badge": "5〜10%（高級店・ドライバー）", "tip_detail": "中級〜高級レストランでサービス料が含まれない場合は会計の5〜10%。ポーターや専属ドライバーには50〜200ルピー程度。", "tax": "GST 5〜28%（品目により異なる）。", "water": False, "water_note": "水道水は厳禁。ペットボトル購入時もキャップが未開封（密閉されているか）必ず確認してください。", "emerg": "総合緊急112 / 警察100 / 救急102", "apps": ["Uber（オートリキシャも呼べて交渉不要）", "Ola", "Googleマップ"]},
    "KH": {"country_ja": "カンボジア", "region": "アジア", "plug": "A/C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "USD", "curr_ja": "米ドル（現地通貨リエル併用）", "sym": "$", "tip": "optional", "tip_badge": "1〜2ドル程度", "tip_detail": "ホテルのポーターやマッサージ、遺跡ガイドには1〜5米ドル程度。街中では米ドル紙幣がメインで流通しています（お釣りの小銭のみリエル）。", "tax": "VAT 10%。", "water": False, "water_note": "水道水は飲用不可。ミネラルウォーターを常備してください。", "emerg": "警察117 / 消防118 / 救急119", "apps": ["Grab（トゥクトゥクも定額で呼べる）", "PassApp"]},
    "LK": {"country_ja": "スリランカ", "region": "アジア", "plug": "BF/B3/C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "LKR", "curr_ja": "スリランカルピー", "sym": "Rs", "tip": "optional", "tip_badge": "10%程度", "tip_detail": "ポーターやドライバー、ベッドメイクには100〜500ルピー程度渡す習慣があります。", "tax": "VAT 18%。", "water": False, "water_note": "水道水は飲用不可。市販のボトル水を利用してください。", "emerg": "警察119 / 救急1990", "apps": ["PickMe（スリランカ版Grab）", "Uber"]},
    "NP": {"country_ja": "ネパール", "region": "アジア", "plug": "C/B3", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "NPR", "curr_ja": "ネパールルピー", "sym": "Rs", "tip": "optional", "tip_badge": "10%程度（ガイド・高級店）", "tip_detail": "トレッキングのガイドやポーター、観光客向けレストランでは10%程度のチップが一般的です。", "tax": "VAT 13%。", "water": False, "water_note": "水道水は飲用不可。必ず密閉されたミネラルウォーターを購入してください。", "emerg": "警察100 / 救急102", "apps": ["Pathao", "InDrive"]},
    "MV": {"country_ja": "モルディブ", "region": "アジア", "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "USD", "curr_ja": "米ドル（現地通貨ルフィヤ）", "sym": "$", "tip": "optional", "tip_badge": "1〜5ドル（リゾート内）", "tip_detail": "リゾートホテルでは10%のサービス料が加算されますが、バトラーやハウスキーピングに1日2〜5米ドル程度渡すのが一般的。", "tax": "TGST（観光財サービス税）16%。", "water": False, "water_note": "リゾート内では毎日無料のミネラルウォーターが補充されます。", "emerg": "警察119 / 救急102", "apps": ["リゾート専用アプリ", "RTL Travel"]},

    "US": {"country_ja": "アメリカ", "region": "北米・ハワイ", "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False, "curr": "USD", "curr_ja": "米ドル", "sym": "$", "tip": "required", "tip_badge": "必須（18〜22%）", "tip_detail": "着席レストランは税前価格の18〜22%が必須マナー。タクシー・Uberは15〜20%、ホテルのベッドメイクは1泊$2〜5。", "tax": "州・都市ごとに売上税（約4〜10%・ハワイは4.712%）がレジで加算。観光客向けの免税還付制度はなし。", "water": True, "water_note": "水道水は飲用可能ですが、乾燥対策や持ち歩きにはペットボトル水のまとめ買いが便利です。", "emerg": "警察・救急・消防 911", "apps": ["Uber", "Lyft", "Googleマップ"]},
    "US_GUM": {"country_ja": "グアム・サイパン（米国準州）", "region": "太平洋・リゾート", "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False, "curr": "USD", "curr_ja": "米ドル", "sym": "$", "tip": "required", "tip_badge": "必須（15〜20%）", "tip_detail": "レストランでは15〜20%が相場ですが、伝票にService Chargeが含まれている場合は追加不要です（二重払いに注意）。", "tax": "グアムは消費税（売上税）が0%のフリーポートのため、表示価格のまま買い物できます。", "water": False, "water_note": "石灰分が多い硬水のため、飲料用には市販のミネラルウォーターを購入してください。", "emerg": "警察・救急・消防 911", "apps": ["Stroll（グアム版Uber）", "赤いシャトルバス（eチケット）"]},
    "CA": {"country_ja": "カナダ", "region": "北米", "plug": "A", "voltage": "120V", "freq": "60Hz", "trans": False, "curr": "CAD", "curr_ja": "カナダドル", "sym": "C$", "tip": "required", "tip_badge": "必須（15〜20%）", "tip_detail": "アメリカ同様チップ社会。レストランやタクシーではカード端末に表示される15%・18%・20%のボタンから選ぶだけで完了します。", "tax": "連邦税(GST 5%)＋州税(PST)または統合税(HST)で計5〜15%が加算。旅行者向けの免税還付制度は原則なし。", "water": True, "water_note": "水道水は水質基準が非常に高く、そのまま美味しく飲めます。", "emerg": "警察・救急・消防 911", "apps": ["Uber", "Lyft", "Transit"]},
    "MX": {"country_ja": "メキシコ", "region": "中南米", "plug": "A", "voltage": "127V", "freq": "60Hz", "trans": False, "curr": "MXN", "curr_ja": "メキシコペソ", "sym": "Mex$", "tip": "required", "tip_badge": "必須（10〜15%）", "tip_detail": "レストランでは会計の10〜15%（カンクン等のリゾート地では15〜20%）。ポーターには20〜50ペソ程度。", "tax": "IVA（付加価値税）16%。Tax Free加盟店で一定額以上購入時、空港で還付申請可能。", "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーターを購入してください。", "emerg": "警察・救急・消防 911", "apps": ["Uber", "DiDi"]},
    "PE": {"country_ja": "ペルー", "region": "中南米", "plug": "A/C", "voltage": "220V", "freq": "60Hz", "trans": False, "curr": "PEN", "curr_ja": "ソル（米ドル併用可）", "sym": "S/", "tip": "optional", "tip_badge": "5〜10%（中高級店）", "tip_detail": "観光客向けレストランでは会計の5〜10%程度。タクシーはチップ不要（乗車前の料金交渉または配車アプリ利用）。", "tax": "IGV（一般売上税）18%。", "water": False, "water_note": "水道水は飲用不可。高山病対策としてもミネラルウォーターをこまめに摂取してください。", "emerg": "警察105 / 救急116", "apps": ["Uber", "Cabify"]},
    "BR": {"country_ja": "ブラジル", "region": "中南米", "plug": "C", "voltage": "127/220V", "freq": "60Hz", "trans": False, "curr": "BRL", "curr_ja": "レアル", "sym": "R$", "tip": "optional", "tip_badge": "10%（会計に加算済多数）", "tip_detail": "レストランでは伝票に10%のサービス料（Taxa de Serviço）が含まれていることがほとんどです。", "tax": "商品価格に税金が含まれる内税方式。", "water": False, "water_note": "水道水は飲用不可。必ず市販のミネラルウォーター（Água sem gás＝炭酸なし）を購入してください。", "emerg": "警察190 / 救急192 / 消防193", "apps": ["Uber（流しのタクシーより安全）", "99"]},

    "GB": {"country_ja": "イギリス", "region": "ヨーロッパ", "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "GBP", "curr_ja": "ポンド", "sym": "£", "tip": "optional", "tip_badge": "10〜12.5%（サ料込なら不要）", "tip_detail": "レストランでは伝票に12.5%のService Chargeが含まれていることが多く、その場合は追加不要。パブのカウンター注文はチップ不要。", "tax": "標準VAT 20%（内税表示）。イギリスの観光客向け免税還付制度は廃止済みのため空港還付はありません。", "water": True, "water_note": "水道水は飲用可能（Tap waterは無料）。ただし石灰分が多い硬水のため、胃腸が弱い方は市販水を推奨。", "emerg": "警察・救急・消防 999（または112）", "apps": ["Citymapper（乗り換え神アプリ）", "Uber", "Trainline"]},
    "FR": {"country_ja": "フランス", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "気持ち程度（サ料込）", "tip_detail": "法律によりサービス料15%が価格に含まれています。良いサービスを受けた際にカフェで小銭（1〜2€）、レストランで5%程度置くのがスマート。", "tax": "標準VAT 20%。同一店舗で同日100.01€以上購入すると、空港のPABLO端末で免税手続き（約12%還付）が可能。", "water": True, "water_note": "水道水は飲用可能。レストランで「キャラフ・ドー（Carafe d'eau）」と頼めば無料の水道水ピッチャーが出ます。", "emerg": "欧州共通112 / 警察17 / 救急15", "apps": ["Bonjour RATP", "Citymapper", "Uber / Bolt"]},
    "IT": {"country_ja": "イタリア", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "基本不要（席料Copertoあり）", "tip_detail": "レストランでは1人1〜4€の席料（Coperto）が加算されるためチップは原則不要。特別なサービスを受けた際のみ端数を置きます。", "tax": "標準VAT 22%。同一店舗で70.01€以上購入すると空港で免税還付が可能。", "water": True, "water_note": "水道水は飲用可能ですが硬水です。レストランでの水（Acqua）注文は有料のボトル水が出てきます。", "emerg": "欧州共通 112", "apps": ["FreeNow（タクシー）", "Trenitalia（鉄道）", "Googleマップ"]},
    "ES": {"country_ja": "スペイン", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "端数〜5%程度", "tip_detail": "バルやカフェではお釣りの小銭を置く程度、レストランでは会計の5〜10%程度が目安です。", "tax": "標準IVA 21%。スペインは免税最低購入金額の制限（0€〜）が撤廃されており、少額の買い物でもTax Free書類を作れます。", "water": True, "water_note": "マドリード等は軟水で美味しいですが、バルセロナ等は硬水のためミネラルウォーターが好まれます。", "emerg": "欧州共通 112", "apps": ["Cabify（スペインで強い配車アプリ）", "Uber", "FreeNow"]},
    "DE": {"country_ja": "ドイツ", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "5〜10%（切り上げ払い）", "tip_detail": "テーブル会計時に「18.50€なら20€で！」とチップ込みのキリの良い金額を店員に伝えて支払うのがドイツ流です。", "tax": "標準VAT 19%。同一店舗で50.01€以上購入時に免税手続きが可能。", "water": True, "water_note": "水質基準が厳しく水道水は飲用可能ですが、スーパーでは炭酸水（Classic）と水（Still/Naturell）の間違いに注意。", "emerg": "欧州共通112 / 警察110", "apps": ["DB Navigator（ドイツ鉄道必須）", "FreeNow", "Uber"]},
    "CH": {"country_ja": "スイス", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "CHF", "curr_ja": "スイスフラン", "sym": "CHF", "tip": "optional", "tip_badge": "端数切り上げ（サ料込）", "tip_detail": "すべてサービス料込みですが、レストラン等で23.50フランなら25フランに切り上げて支払うとスマートです。", "tax": "標準VAT 8.1%。1店舗300フラン以上購入で免税対象（EU圏外のため、EU諸国へ抜ける国境駅や空港でスタンプ必須）。", "water": True, "water_note": "アルプスの天然水に近く、水道水や街中の水飲み場（飲用不可マークがない限り）の水が非常に美味しいです。", "emerg": "欧州共通112 / 警察117 / 救急144", "apps": ["SBB Mobile（スイス国鉄・登山鉄道必須）", "Uber"]},
    "AT": {"country_ja": "オーストリア", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "5〜10%（切り上げ払い）", "tip_detail": "ドイツと同様、会計時に5〜10%を上乗せしたキリの良い金額を店員に伝えて精算します。", "tax": "標準VAT 20%。75.01€以上の購入で免税対象。", "water": True, "water_note": "ウィーンの水道水はアルプスからの湧き水（高地泉水）が引かれており、世界最高峰の美味しさでそのまま飲めます。", "emerg": "欧州共通112 / 警察133 / 救急144", "apps": ["WienMobil", "ÖBB Scotty", "Bolt / Uber"]},
    "CZ": {"country_ja": "チェコ", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "CZK", "curr_ja": "チェココルナ", "sym": "Kč", "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでは会計時に10%程度を上乗せして支払うのが一般的です。テーブルの上に現金を置いたままにせず、会計時に直接伝えます。", "tax": "標準VAT 21%。1店舗2,000CZK以上の購入で免税対象。", "water": True, "water_note": "水道水は飲用可能です。", "emerg": "欧州共通112 / 警察158 / 救急155", "apps": ["PID Lítačka（プラハ交通必須）", "Bolt", "Uber"]},
    "NL": {"country_ja": "オランダ", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "サービス料込みのため必須ではありませんが、レストランでは5〜10%程度を切り上げて払うことが多いです。完全キャッシュレス社会です。", "tax": "標準VAT 21%。50€以上の購入で免税対象。", "water": True, "water_note": "水道水は非常に水質が高く、そのまま美味しく飲めます。", "emerg": "欧州共通 112", "apps": ["9292（オランダ全土の乗換案内）", "NS（オランダ鉄道）", "Uber"]},
    "BE": {"country_ja": "ベルギー", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "基本不要（端数程度）", "tip_detail": "サービス料が含まれているため原則不要。満足した際に端数を切り上げる程度で十分です。", "tax": "標準VAT 21%。125.01€以上の購入で免税対象。", "water": True, "water_note": "水道水は飲用可能ですが硬水です。", "emerg": "欧州共通 112", "apps": ["SNCB（ベルギー国鉄）", "STIB-MIVB", "Uber"]},
    "PT": {"country_ja": "ポルトガル", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "5〜10%（レストラン）", "tip_detail": "カフェは小銭程度、観光客向けレストランでは5〜10%程度置くと喜ばれます。", "tax": "標準IVA 23%。61.50€以上の購入で免税対象。", "water": True, "water_note": "水道水は飲用可能です。", "emerg": "欧州共通 112", "apps": ["Bolt（Uberより安いことが多い）", "Uber", "Navegante"]},
    "GR": {"country_ja": "ギリシャ", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "optional", "tip_badge": "5〜10%程度", "tip_detail": "タベルナ（大衆食堂）では端数〜5%、レストランでは5〜10%程度をテーブルに置くのが一般的です。", "tax": "標準VAT 24%。50€以上の購入で免税対象。", "water": True, "water_note": "アテネ本土は飲用可能ですが、サントリーニ島などの島嶼部は水道水が飲めないためミネラルウォーター必須です。", "emerg": "欧州共通112 / 警察100", "apps": ["FreeNow", "Uber（タクシー配車）"]},
    "HU": {"country_ja": "ハンガリー", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "HUF", "curr_ja": "フォリント", "sym": "Ft", "tip": "optional", "tip_badge": "10%（サ料別の場合）", "tip_detail": "伝票にSzervizdíj（サービス料10〜15%）が含まれていれば不要。含まれない場合は会計時に10%程度を上乗せします。", "tax": "標準VAT 27%（欧州最高水準のため、免税店でのTax Free手続きのメリットが大きいです）。", "water": True, "water_note": "水道水はそのまま飲用可能です。", "emerg": "欧州共通 112", "apps": ["BudapestGO（交通チケット必須）", "Bolt（ブダペスト公認タクシー配車）"]},
    "FI": {"country_ja": "フィンランド", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "EUR", "curr_ja": "ユーロ", "sym": "€", "tip": "none", "tip_badge": "不要", "tip_detail": "北欧はサービス料込みかつ高賃金体系のため、チップの習慣は基本的にありません。", "tax": "標準VAT 25.5%。40€以上の購入で免税対象。", "water": True, "water_note": "水道水は世界トップクラスの純度で、ペットボトル水以上に美味しくそのまま飲めます。", "emerg": "欧州共通 112", "apps": ["HSL（ヘルシンキ交通）", "Bolt", "Uber"]},
    "SE": {"country_ja": "スウェーデン", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "SEK", "curr_ja": "スウェーデンクローナ", "sym": "kr", "tip": "none", "tip_badge": "不要（端数程度）", "tip_detail": "基本的に不要。ディナーで良いサービスを受けた際に端数を切り上げる程度。現金お断りの店が多いためタッチ決済カード必須。", "tax": "標準VAT 25%。200SEK以上の購入で免税対象。", "water": True, "water_note": "水道水は非常に綺麗でそのまま飲めます。", "emerg": "欧州共通 112", "apps": ["SL（ストックホルム交通）", "Uber", "Bolt"]},
    "DK": {"country_ja": "デンマーク", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "DKK", "curr_ja": "デンマーククローネ", "sym": "kr", "tip": "none", "tip_badge": "不要", "tip_detail": "法律でサービス料込みの表示が義務付けられており、チップは不要です。", "tax": "標準VAT 25%。300DKK以上の購入で免税対象。", "water": True, "water_note": "水道水はそのまま飲用可能です。", "emerg": "欧州共通 112", "apps": ["DOT Tickets", "Rejseplanen", "Viggo（配車）"]},
    "PL": {"country_ja": "ポーランド", "region": "ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "PLN", "curr_ja": "ズウォティ", "sym": "zł", "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでは会計の10%程度を上乗せするのが一般的です。", "tax": "標準VAT 23%。200PLN以上の購入で免税対象。", "water": True, "water_note": "主要都市の水道水は飲用可能ですが、ミネラルウォーターも安価に買えます。", "emerg": "欧州共通 112", "apps": ["Jakdojade（乗換・切符購入）", "Uber", "Bolt"]},

    "AU": {"country_ja": "オーストラリア", "region": "オセアニア", "plug": "O", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "AUD", "curr_ja": "豪ドル", "sym": "A$", "tip": "none", "tip_badge": "不要", "tip_detail": "最低賃金が高くチップの習慣はありません。高級レストランで特別なサービスを受けた際のみ5〜10%程度。", "tax": "GST 10%。同一店舗で300A$以上購入時、空港のTRSカウンター（アプリ事前入力推奨）で免税還付が可能。", "water": True, "water_note": "水道水は安全基準が高く、そのまま美味しく飲めます。", "emerg": "警察・救急・消防 000", "apps": ["Uber", "DiDi", "Googleマップ"]},
    "NZ": {"country_ja": "ニュージーランド", "region": "オセアニア", "plug": "O", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "NZD", "curr_ja": "NZドル", "sym": "NZ$", "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。どこでも表示価格（税金・サービス料込）の支払いで完結します。", "tax": "GST 15%。空港での旅行者向け免税還付制度はありません。", "water": True, "water_note": "水道水は非常に綺麗でそのまま飲用可能です。", "emerg": "警察・救急・消防 111", "apps": ["Uber", "AT Mobile（オークランド交通）"]},
    "FJ": {"country_ja": "フィジー", "region": "オセアニア", "plug": "O", "voltage": "240V", "freq": "50Hz", "trans": False, "curr": "FJD", "curr_ja": "フィジードル", "sym": "FJ$", "tip": "none", "tip_badge": "不要", "tip_detail": "フィジーには元々チップの習慣はありません。", "tax": "VAT 15%。", "water": False, "water_note": "リゾート内を除き、念のため市販のミネラルウォーター（Fiji Water等）の飲用を推奨します。", "emerg": "警察917 / 救急911", "apps": ["リゾート送迎・ローカルタクシー"]},
    "NC": {"country_ja": "ニューカレドニア", "region": "オセアニア", "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "XPF", "curr_ja": "CFPフラン", "sym": "CFPF", "tip": "none", "tip_badge": "不要", "tip_detail": "チップの習慣はありません。", "tax": "TGC（一般消費税）3〜22%。", "water": True, "water_note": "ヌメア市内の水道水は飲用可能ですが、離島ではミネラルウォーターを利用してください。", "emerg": "警察17 / 救急15", "apps": ["Tanéo（バス）"]},
    "PF": {"country_ja": "タヒチ（仏領ポリネシア）", "region": "オセアニア", "plug": "C", "voltage": "220V", "freq": "60Hz", "trans": False, "curr": "XPF", "curr_ja": "CFPフラン", "sym": "CFPF", "tip": "none", "tip_badge": "不要", "tip_detail": "原則としてチップは不要です。", "tax": "TVA 5〜16%。", "water": False, "water_note": "離島（ボラボラ島等）では市販のミネラルウォーターを飲用してください。", "emerg": "警察17 / 救急15", "apps": ["リゾート水上ボート・タクシー"]},

    "AE": {"country_ja": "アラブ首長国連邦（UAE）", "region": "中東", "plug": "BF", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "AED", "curr_ja": "ディルハム", "sym": "AED", "tip": "optional", "tip_badge": "10%程度（サ料別の場合）", "tip_detail": "ホテルや高級店はサービス料込みが多いですが、カフェやレストランでは10%程度、ポーターには10〜20AED程度渡すのが一般的。", "tax": "VAT 5%。250AED以上の買い物でPlanet社の免税タグを発行してもらえば空港で還付可能。", "water": False, "water_note": "海水を淡水化した水のため、飲料用には市販のミネラルウォーターを購入してください。", "emerg": "警察999 / 救急998", "apps": ["Careem（中東最強の配車・タクシーアプリ）", "Uber", "RTA Dubai"]},
    "TR": {"country_ja": "トルコ", "region": "中東・ヨーロッパ", "plug": "C", "voltage": "230V", "freq": "50Hz", "trans": False, "curr": "TRY", "curr_ja": "トルコリラ", "sym": "₺", "tip": "optional", "tip_badge": "5〜10%（レストラン・ハマム）", "tip_detail": "レストランでは会計の5〜10%、ハマム（トルコ式風呂）の垢すりスタッフには10〜15%程度のチップが慣例です。", "tax": "KDV（付加価値税）10〜20%。Tax Free加盟店で一定額以上購入時、空港で還付可能。", "water": False, "water_note": "水道水は硬水で塩素が強いため飲用せず、安価なミネラルウォーターを購入してください。", "emerg": "総合緊急 112", "apps": ["BiTaksi", "Uber（イスタンブールでタクシーを呼べる）", "Googleマップ"]},
    "QA": {"country_ja": "カタール", "region": "中東", "plug": "BF", "voltage": "240V", "freq": "50Hz", "trans": False, "curr": "QAR", "curr_ja": "カタールリヤル", "sym": "QR", "tip": "optional", "tip_badge": "10%程度", "tip_detail": "レストランでサービス料が含まれない場合は10%程度、ポーターには10〜20リヤル程度。", "tax": "付加価値税（VAT）は0%のため、買い物はすべて免税相当です。", "water": False, "water_note": "市販のミネラルウォーターの飲用を推奨します。", "emerg": "警察・救急・消防 999", "apps": ["Uber", "Karwa Taxi"]},
    "EG": {"country_ja": "エジプト", "region": "中東・アフリカ", "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "EGP", "curr_ja": "エジプトポンド（米ドルも重宝）", "sym": "E£", "tip": "required", "tip_badge": "必須（バクシーシ文化）", "tip_detail": "あらゆる場面で少額のチップ（バクシーシ：10〜50EGPまたは1米ドル札）が求められます。トイレ利用や荷物運び用に小額紙幣を常備してください。", "tax": "VAT 14%。", "water": False, "water_note": "水道水は飲用不可。必ずキャップが密閉されたミネラルウォーターを購入してください。", "emerg": "観光警察126 / 警察122 / 救急123", "apps": ["Uber（料金交渉・ぼったくり回避に絶対必須）", "Careem"]},
    "MA": {"country_ja": "モロッコ", "region": "アフリカ", "plug": "C", "voltage": "220V", "freq": "50Hz", "trans": False, "curr": "MAD", "curr_ja": "ディルハム", "sym": "DH", "tip": "optional", "tip_badge": "10%程度（カフェ・ガイド）", "tip_detail": "カフェで1〜2DH、レストランで会計の10%程度、リヤド（宿）のスタッフや荷物運びには10〜20DH程度が相場です。", "tax": "TVA 20%。", "water": False, "water_note": "水道水は飲用不可。市販のミネラルウォーターを購入してください。", "emerg": "警察19 / 救急・消防15", "apps": ["InDrive", "Careem", "Maps.me（迷宮メディナ散策に必須）"]}
}

# ==========================================
# 3. 世界108都市リスト
# ==========================================
RAW_CITIES = [
    ("seoul", "ソウル", "Seoul", "KR", "Asia/Seoul", False, "仁川国際空港(ICN)", "空港鉄道A'REX直通列車（ソウル駅まで43分 / 11,000₩）", "A'REX一般列車（ソウル駅まで約60分 / 4,450〜5,050₩）"),
    ("busan", "釜山（プサン）", "Busan", "KR", "Asia/Seoul", False, "金海国際空港(PUS)", "タクシー（西面・南浦洞まで約30分 / 約20,000₩）", "釜山金海軽電鉄＋地下鉄（西面駅まで約30分 / 約2,100₩）"),
    ("jeju", "済州島（チェジュ）", "Jeju", "KR", "Asia/Seoul", False, "済州国際空港(CJU)", "タクシー（新済州エリアまで約10分 / 約6,000₩）", "市内急行バス（中文リゾートまで約50分 / 3,000₩）"),
    ("incheon", "仁川（インチョン）", "Incheon", "KR", "Asia/Seoul", False, "仁川国際空港(ICN)", "タクシー・無料シャトル（パラダイスシティ・松島まで10〜25分）", "空港鉄道A'REX＋仁川地下鉄1号線（約3,000₩）"),
    ("daegu", "大邱（テグ）", "Daegu", "KR", "Asia/Seoul", False, "大邱国際空港(TAE)", "タクシー（東大邱駅まで約10分 / 約7,000₩）", "市内バス401・急行1番＋地下鉄（中心部まで約30分 / 1,500₩）"),
    ("gyeongju", "慶州（キョンジュ）", "Gyeongju", "KR", "Asia/Seoul", False, "金海国際空港(PUS)", "空港リムジンバス（慶州バスターミナルまで約70分 / 11,000₩）", "軽電鉄＋KTX鉄道（新慶州駅まで約60分）"),
    ("taipei", "台北", "Taipei", "TW", "Asia/Taipei", False, "桃園国際空港(TPE) / 松山空港(TSA)", "桃園メトロ空港線・直達車（台北駅まで35分 / 160元）", "國光客運リムジンバス1819路（台北駅まで約55分 / 140元）"),
    ("kaohsiung", "高雄", "Kaohsiung", "TW", "Asia/Taipei", False, "高雄国際空港(KHH)", "高雄MRTレッドライン（美麗島駅まで16分 / 35元）", "高雄MRTレッドライン（高雄駅まで19分 / 35元）"),
    ("taichung", "台中", "Taichung", "TW", "Asia/Taipei", False, "台中国際空港(RMQ) / 台湾高鉄台中駅", "タクシー（台中駅・逢甲夜市まで約30〜40分 / 約500元）", "市内バス302・A2路（市内まで約50分 / 悠遊カード利用で格安）"),
    ("tainan", "台南", "Tainan", "TW", "Asia/Taipei", False, "高雄空港(KHH) / 高鉄台南駅", "高雄空港からMRT＋台湾鉄道・自強号（台南駅まで約60分 / 約140元）", "高鉄台南駅から台鉄沙崙線（台南駅まで22分 / 25元）"),
    ("bangkok", "バンコク", "Bangkok", "TH", "Asia/Bangkok", False, "スワンナプーム国際空港(BKK)", "エアポート・レール・リンクARL（パヤタイ駅まで26分 / 45B）", "ARL＋BTS/MRT乗り継ぎ（アソーク・サイアムまで約40分 / 約75B）"),
    ("phuket", "プーケット", "Phuket", "TH", "Asia/Bangkok", False, "プーケット国際空港(HKT)", "空港リムジンタクシー・Grab（パトンビーチまで約50分 / 800B〜）", "プーケット・スマートバス（パトン・カロンまで約70分 / 一律100B）"),
    ("chiang-mai", "チェンマイ", "Chiang Mai", "TH", "Asia/Bangkok", False, "チェンマイ国際空港(CNX)", "エアポートタクシー・Grab（旧市街・ニマンヘミンまで15分 / 一律150B〜）", "RTCシティバス（旧市街まで約20分 / 30B）"),
    ("pattaya", "パタヤ", "Pattaya", "TH", "Asia/Bangkok", False, "スワンナプーム空港(BKK)", "チャータータクシー・Grab（パタヤ中心部まで約90分 / 約1,200〜1,500B）", "空港1階8番ゲート発・直行バス（パタヤまで約120分 / 143B）"),
    ("singapore", "シンガポール", "Singapore", "SG", "Asia/Singapore", False, "チャンギ国際空港(SIN)", "タクシー・Grab（マリーナベイ・オーチャードまで約20分 / 約25〜35S$）", "MRT地下鉄（市内中心部まで約40分 / 約2.2S$・クレカタッチ乗車可）"),
    ("ho-chi-minh", "ホーチミン", "Ho Chi Minh City", "VN", "Asia/Ho_Chi_Minh", False, "タンソンニャット国際空港(SGN)", "Grab・Vinasunタクシー（1区ドンコイ通り周辺まで約25分 / 約15万VND）", "空港バス109番・152番（ベンタイン市場まで約40分 / 5,000〜20,000VND）"),
    ("hanoi", "ハノイ", "Hanoi", "VN", "Asia/Ho_Chi_Minh", False, "ノイバイ国際空港(HAN)", "Grab・タクシー（旧市街・ホアンキエム湖まで約40分 / 約35万VND）", "急行バス86番（ハノイ駅・オペラハウスまで約50分 / 45,000VND）"),
    ("da-nang", "ダナン", "Da Nang", "VN", "Asia/Ho_Chi_Minh", False, "ダナン国際空港(DAD)", "Grab・タクシー（ミーケビーチ・市街地までわずか10〜15分 / 約10万VND）", "シャトルバス（市街地まで約20分）"),
    ("nha-trang", "ニャチャン", "Nha Trang", "VN", "Asia/Ho_Chi_Minh", False, "カムラン国際空港(CXR)", "Grab・タクシー（ニャチャン中心部まで約40分 / 約35万VND）", "Dat Moi空港シャトルバス（市内まで約45分 / 65,000VND）"),
    ("cebu", "セブ島", "Cebu", "PH", "Asia/Manila", False, "マクタン・セブ国際空港(CEB)", "Grab・ホワイトタクシー（マクタン島リゾートまで20分・セブ市内まで45分 / 300〜500P）", "MyBus空港バス（SMシティセブまで約40分 / 50P）"),
    ("manila", "マニラ", "Manila", "PH", "Asia/Manila", False, "ニノイ・アキノ国際空港(MNL)", "Grab（マカティ・BGCまでスカイウェイ経由で約25分 / 約350〜500P）", "UBE Express空港バス（市内主要ホテル・モールまで150P）"),
    ("boracay", "ボラカイ島", "Boracay", "PH", "Asia/Manila", False, "カティクラン空港(MPH)", "ホテル送迎パッケージ（バン＋ボート＋eトライシクルでホテルまで約30分）", "ローカルボート＋トライシクル乗り継ぎ（港諸税込みで約400P）"),
    ("kuala-lumpur", "クアラルンプール", "Kuala Lumpur", "MY", "Asia/Kuala_Lumpur", False, "クアラルンプール国際空港(KUL)", "KLIAエクスプレス（KLセントラル駅までノンストップ28分 / 55RM）", "空港リムジンバス（KLセントラル駅まで約60分 / 15RM）"),
    ("penang", "ペナン島", "Penang", "MY", "Asia/Kuala_Lumpur", False, "ペナン国際空港(PEN)", "Grab（世界遺産ジョージタウンまで約30分 / 約25〜35RM）", "Rapid Penangバス401E（コムタまで約50分 / 2.7RM）"),
    ("kota-kinabalu", "コタキナバル", "Kota Kinabalu", "MY", "Asia/Kuching", False, "コタキナバル国際空港(BKI)", "Grab（市内中心部までわずか15分 / 約15RM）", "エアポートバス（市内まで約20分 / 5RM）"),
    ("bali", "バリ島（デンパサール）", "Bali", "ID", "Asia/Makassar", False, "ングラ・ライ国際空港(DPS)", "Grab（空港公式ラウンジ発）・空港タクシー（クタ15分・ウブド90分 / 15万〜45万Rp）", "トランス・サルバギタ / クラクラバス（主要エリアへ格安移動）"),
    ("jakarta", "ジャカルタ", "Jakarta", "ID", "Asia/Jakarta", False, "スカルノ・ハッタ国際空港(CGK)", "空港鉄道Railink（BNIシティ駅まで約45分 / 70,000Rp）", "DAMRI空港バス（ガンビル駅・ブロックMまで約60分 / 80,000Rp）"),
    ("yogyakarta", "ジョグジャカルタ", "Yogyakarta", "ID", "Asia/Jakarta", False, "ジョグジャカルタ国際空港(YIA)", "空港特急列車YIA Xpress（トゥグ駅まで35分 / 50,000Rp）", "一般空港列車（トゥグ駅まで39分 / 20,000Rp）"),
    ("hong-kong", "香港", "Hong Kong", "HK", "Asia/Hong_Kong", False, "香港国際空港(HKG)", "エアポート・エクスプレス機場快線（香港駅まで24分 / 115HKD）", "城バスCityflyer A11・A21（中環・尖沙咀まで約45〜60分 / 34.6〜41.9HKD）"),
    ("macau", "マカオ", "Macau", "MO", "Asia/Macau", False, "マカオ国際空港(MFM) / 港珠澳大橋", "各統合型リゾート(IR)の無料シャトルバス（コタイ地区ホテルまで5〜10分 / 無料）", "マカオLRT軽軌鉄道（コタイ・タイパエリアまで約10分 / 6〜8MOP）"),
    ("shanghai", "上海", "Shanghai", "CN", "Asia/Shanghai", False, "上海浦東国際空港(PVG)", "上海トランスラピッド・リニアモーターカー（龍陽路駅までわずか8分 / 50元）", "地下鉄2号線（人民広場・南京東路まで約65分 / 7元）"),
    ("beijing", "北京", "Beijing", "CN", "Asia/Shanghai", False, "北京首都国際空港(PEK)", "首都空港線エアポートエクスプレス（東直門駅まで約20分 / 25元）", "空港リムジンバス（市内主要エリアまで約60分 / 20〜30元）"),
    ("guangzhou", "広州", "Guangzhou", "CN", "Asia/Shanghai", False, "広州白雲国際空港(CAN)", "地下鉄3号線（体育西路・珠江新城まで約45分 / 7〜8元）", "空港快線バス（市内各所へ約50分 / 20元前後）"),
    ("shenzhen", "深セン", "Shenzhen", "CN", "Asia/Shanghai", False, "深セン宝安国際空港(SZX)", "地下鉄11号線・空港快線（福田駅まで約30分 / 7元）", "地下鉄11号線普通車両（市内まで7元）"),
    ("siem-reap", "シェムリアップ", "Siem Reap", "KH", "Asia/Phnom_Penh", False, "シェムリアップ・アンコール国際空港(SAI)", "公式空港タクシー・Grab（市内中心部まで約50分 / 35USD）", "空港シャトルバス（市内CDF免税店前まで約60分 / 8USD）"),
    ("phnom-penh", "プノンペン", "Phnom Penh", "KH", "Asia/Phnom_Penh", False, "プノンペン国際空港(PNH)", "Grab・タクシー（リバーサイド中心部まで約35分 / 約10〜15USD）", "市バス3番（市内中心部まで約50分 / 1,500リエル≒0.38USD）"),
    ("delhi", "デリー", "New Delhi", "IN", "Asia/Kolkata", False, "インディラ・ガンディー国際空港(DEL)", "デリーメトロ・エアポートエクスプレス線（ニューデリー駅まで19分 / 60₹）", "エアポートエクスプレス線（渋滞・客引き皆無で最速かつ最安60₹）"),
    ("mumbai", "ムンバイ", "Mumbai", "IN", "Asia/Kolkata", False, "チャトラパティ・シヴァージー国際空港(BOM)", "Uber・プリペイドタクシー（コラバ・南ムンバイまで約45〜60分 / 約600₹）", "ムンバイメトロ3号線（市内主要エリアへ直結）"),
    ("colombo", "コロンボ", "Colombo", "LK", "Asia/Colombo", False, "バンダラナイケ国際空港(CMB)", "空港高速経由タクシー・PickMe（コロンボ市内まで約40分 / 約4,000Rs）", "高速バス187番（コロンボ・フォート駅まで約45分 / 約350Rs）"),
    ("kathmandu", "カトマンズ", "Kathmandu", "NP", "Asia/Kathmandu", False, "トリブバン国際空港(KTM)", "空港プリペイドタクシー・Pathao（タメル地区まで約20分 / 約800〜1,000Rs）", "路線バス（空港ゲート外から中心部へ約30Rs）"),
    ("male", "モルディブ（マレ）", "Male", "MV", "Indian/Maldives", False, "ヴェラナ国際空港(MLE)", "各リゾート専用スピードボートまたは水上飛行機（空港島から直接乗船）", "公共フェリー（マレ本島まで約10分 / 1〜2USD）"),
    ("honolulu", "ホノルル（ハワイ）", "Honolulu", "US", "Pacific/Honolulu", False, "ダニエル・K・イノウエ国際空港(HNL)", "Uber・チャーリーズタクシー（ワイキキまで約25分 / 定額$33〜45＋チップ）", "ザ・バス20番（ワイキキまで約55分 / $3.00・大きなスーツケース持込不可）"),
    ("kona", "ハワイ島（コナ）", "Kailua-Kona", "US", "Pacific/Honolulu", False, "エリソン・オニヅカ・コナ国際空港(KOA)", "レンタカー・Uber（カイルア・コナ中心部まで約15分・ワイコロアまで30分）", "ヘレオン・バス（無料〜少額運行・本数少なめ）"),
    ("guam", "グアム", "Guam", "US_GUM", "Pacific/Guam", False, "グアム国際空港(GUM)", "ミキタクシー・Stroll配車（タモン地区ホテルまでわずか10〜15分 / 約$25〜30）", "ホテル送迎シャトル（事前予約制）"),
    ("saipan", "サイパン", "Saipan", "US_GUM", "Pacific/Saipan", False, "サイパン国際空港(SPN)", "タクシー・ホテル送迎（ガラパン地区まで約20分 / 約$25〜30）", "レンタカー（島内観光と兼用に最適）"),
    ("new-york", "ニューヨーク", "New York", "US", "America/New_York", True, "JFK国際空港(JFK)", "エアトレイン＋LIRRロングアイランド鉄道（ペン駅まで約35分 / 計$13.50〜）", "エアトレイン＋地下鉄E/A線（マンハッタンまで約60分 / 計$11.40・タッチ決済可）"),
    ("los-angeles", "ロサンゼルス", "Los Angeles", "US", "America/Los_Angeles", True, "ロサンゼルス国際空港(LAX)", "LAX-it発Uber・タクシー（サンタモニカ・ダウンタウンまで約35分 / 約$45〜70）", "FlyAway直行バス（ユニオン駅まで約35分 / $9.75・クレカタッチ決済可）"),
    ("san-francisco", "サンフランシスコ", "San Francisco", "US", "America/Los_Angeles", True, "サンフランシスコ国際空港(SFO)", "BART高速鉄道（パウエル駅・ユニオンスクエアまで約30分 / $10.55）", "SamTrans路線バス292・ECR（ダウンタウンまで約60分 / $2.25）"),
    ("las-vegas", "ラスベガス", "Las Vegas", "US", "America/Los_Angeles", True, "ハリー・リード国際空港(LAS)", "Uber・タクシー（ストリップ地区ホテルまで約10〜15分 / 定額ゾーン制$21〜30）", "RTC公共バスCX・108・109番（ストリップまで約20分 / $2〜6）"),
    ("orlando", "オーランド", "Orlando", "US", "America/New_York", True, "オーランド国際空港(MCO)", "Uber・Lyft（ディズニーワールド・ユニバーサルまで約25〜30分 / 約$35〜50）", "Mears Connectシャトルバス（ディズニー公式ホテル群へ片道$16）"),
    ("seattle", "シアトル", "Seattle", "US", "America/Los_Angeles", True, "シアトル・タコマ国際空港(SEA)", "リンク・ライトレール1号線（ウエストレイク駅まで38分 / $3.00）", "リンク・ライトレール（渋滞知らずで最速かつ最安の$3.00）"),
    ("chicago", "シカゴ", "Chicago", "US", "America/Chicago", True, "オヘア国際空港(ORD)", "CTA地下鉄ブルーライン（ダウンタウン・ループまで約45分 / $5.00）", "CTAブルーライン（24時間運行・$5.00で直結）"),
    ("boston", "ボストン", "Boston", "US", "America/New_York", True, "ローガン国際空港(BOS)", "MBTAシルバーラインSL1（サウス駅まで約20分 / 空港発は完全無料！）", "シルバーラインSL1（サウス駅まで無料＋地下鉄レッドラインへ無料乗継）"),
    ("washington-dc", "ワシントンD.C.", "Washington D.C.", "US", "America/New_York", True, "ダレス国際空港(IAD) / レーガン空港(DCA)", "メトロ・シルバーライン（ダレス空港から市内中心部まで約50分 / $2.25〜6.00）", "メトロ鉄道（DCAからはわずか15分、IADからも乗り換えなしで直結）"),
    ("san-diego", "サンディエゴ", "San Diego", "US", "America/Los_Angeles", True, "サンディエゴ国際空港(SAN)", "Uber・タクシー（ダウンタウン・ガスランプまでわずか10分 / 約$15〜20）", "サンディエゴ・フライヤー無料シャトル＋トロリー（オールドタウン駅経由）"),
    ("miami", "マイアミ", "Miami", "US", "America/New_York", True, "マイアミ国際空港(MIA)", "Uber・タクシー（サウスビーチ・ダウンタウンまで約20分 / 約$25〜35）", "メトロレール・オレンジラインまたはメトロバス150番（各$2.25）"),
    ("vancouver", "バンクーバー", "Vancouver", "CA", "America/Vancouver", True, "バンクーバー国際空港(YVR)", "スカイトレイン・カナダライン（ウォーターフロント駅まで26分 / 約9.55C$）", "スカイトレイン・カナダライン（タッチ決済でそのまま乗車可能）"),
    ("toronto", "トロント", "Toronto", "CA", "America/Toronto", True, "トロント・ピアソン国際空港(YYZ)", "UPエクスプレス空港鉄道（ユニオン駅まで25分 / 12.35C$）", "TTC急行バス900番＋地下鉄（市内まで約50分 / 3.35C$）"),
    ("montreal", "モントリオール", "Montreal", "CA", "America/Toronto", True, "モントリオール・トルドー国際空港(YUL)", "タクシー・Uber（ダウンタウンまで定額約48.40C$ / 約25分）", "747エアポート急行バス（ライオネル・グルー駅・中心部まで約45分 / 11C$）"),
    ("banff", "バンフ（カナディアンロッキー）", "Banff", "CA", "America/Edmonton", True, "カルガリー国際空港(YYC)", "Brewster Express / Banff Airporter直行バス（バンフ各ホテルまで約100分 / 約80C$）", "On-It季節運行バス・FlixBus（カルガリー経由で格安移動）"),
    ("cancun", "カンクン", "Cancun", "MX", "America/Cancun", False, "カンクン国際空港(CUN)", "事前予約プライベート送迎バン（ホテルゾーンまで約25分 / 1台約$40）", "ADO空港バス（カンクン・セントロまで約35分 / 約130Mex$＋市内バスR1）"),
    ("mexico-city", "メキシコシティ", "Mexico City", "MX", "America/Mexico_City", False, "メキシコシティ国際空港(MEX)", "Uber・空港公認サイトタクシー（レフォルマ・ポランコまで約25〜40分 / 約200〜300Mex$）", "メトロバス4号線（歴史地区・セントロまで約30分 / 30Mex$）"),
    ("cusco", "クスコ（マチュピチュ玄関口）", "Cusco", "PE", "America/Lima", False, "アレハンドロ・ベラスコ・アステテ国際空港(CUZ)", "Uber・空港内公式タクシー（アルマス広場周辺まで約15分 / 約25〜35ソル）", "コレクティーボ・路線バス（空港外大通りから1〜2ソル）"),
    ("lima", "リマ", "Lima", "PE", "America/Lima", False, "ホルヘ・チャベス国際空港(LIM)", "Airport Express Lima公式バス（ミラフローレス地区まで約50分 / $8または25ソル）", "QuickLlama乗合バン・Uber（ミラフローレスまで約45ソル）"),
    ("rio-de-janeiro", "リオデジャネイロ", "Rio de Janeiro", "BR", "America/Sao_Paulo", False, "アントニオ・カルロス・ジョビン国際空港(GIG)", "Uber・公式タクシー（コパカバーナ・イパネマまで約35分 / 約70〜100R$）", "Frescãoエアコン付き空港バス（コパカバーナまで約50分 / 約20R$）"),
    ("london", "ロンドン", "London", "GB", "Europe/London", True, "ヒースロー空港(LHR)", "ヒースロー・エクスプレス（パディントン駅まで15分 / £25・早割あり）", "地下鉄ピカデリーライン / エリザベスライン（中心部まで40〜50分 / £5.60〜12.80）"),
    ("edinburgh", "エディンバラ", "Edinburgh", "GB", "Europe/London", True, "エディンバラ空港(EDI)", "Airlink 100急行バス（ウェイバリー駅まで25分 / £5.50・往復£8）", "エディンバラ・トラム（プリンシズ・ストリートまで30分 / £7.50）"),
    ("manchester", "マンチェスター", "Manchester", "GB", "Europe/London", True, "マンチェスター空港(MAN)", "鉄道TransPennine / Northern（ピカデリー駅まで15分 / 約£4〜6）", "メトロリンク・トラムまたはバス（市内まで£4.60）"),
    ("oxford", "オックスフォード", "Oxford", "GB", "Europe/London", True, "ヒースロー空港(LHR)", "The Airline直行長距離バス（オックスフォード中心部まで約80分 / £25）", "エリザベスライン＋GWR鉄道（レディング駅乗換で約75分）"),
    ("paris", "パリ", "Paris", "FR", "Europe/Paris", True, "シャルル・ド・ゴール空港(CDG)", "公定料金タクシー（パリ右岸まで一律56€・左岸まで一律65€ / 約45分）", "RER B線 / ロワシーバス（オペラ座・北駅まで約50分 / 11.80〜16.60€）"),
    ("nice", "ニース", "Nice", "FR", "Europe/Paris", True, "コート・ダジュール空港(NCE)", "トラム2号線（ジャン・メドサン駅・港までわずか25分 / 1.70€）", "トラム2号線（空港ターミナル直結で最速かつ最安）"),
    ("lyon", "リヨン", "Lyon", "FR", "Europe/Paris", True, "サン・テグジュペリ空港(LYS)", "ローヌエクスプレス・トラム（パール・デュー駅まで29分 / 約16.70€）", "TCL路線バス47番＋トラムT3号線（市内まで約50分 / 2€）"),
    ("mont-saint-michel", "モン・サン・ミッシェル", "Mont-Saint-Michel", "FR", "Europe/Paris", True, "パリ・モンパルナス駅（鉄道起点）", "TGV高速鉄道でレンヌ駅（約90分）＋Keolis直行バス（約70分）", "FlixBus / BlaBlaCar直行長距離バス（パリから約4時間半 / 約25€〜）"),
    ("strasbourg", "ストラスブール", "Strasbourg", "FR", "Europe/Paris", True, "ストラスブール国際空港(SXB)", "TER連絡列車（ストラスブール中央駅までわずか9分 / 約5.10€）", "TER列車（1時間に最大4本運行で圧倒的便利）"),
    ("rome", "ローマ", "Rome", "IT", "Europe/Rome", True, "フィウミチーノ空港(FCO)", "レオナルド・エクスプレス直通列車（テルミニ駅まで32分 / 14€）", "Terravision等の直行シャトルバス（テルミニ駅まで約55分 / 7€）"),
    ("milan", "ミラノ", "Milan", "IT", "Europe/Rome", True, "マルペンサ空港(MXP) / リナーテ空港(LIN)", "マルペンサ・エクスプレス鉄道（ミラノ中央駅・カドルナ駅まで37〜50分 / 13€）", "空港シャトルバス（ミラノ中央駅まで約55分 / 10€・リナーテからは地下鉄M4で2.2€）"),
    ("venice", "ヴェネツィア", "Venice", "IT", "Europe/Rome", True, "ヴェネツィア・マルコポーロ空港(VCE)", "ATVO急行バス（ローマ広場まで20分 / 10€）", "Alilaguna水上バス（サン・マルコ広場まで海路で約75分 / 15€）"),
    ("florence", "フィレンツェ", "Florence", "IT", "Europe/Rome", True, "ペレトラ空港(FLR)", "トラムT2線（サンタ・マリア・ノヴェッラ中央駅まで20分 / 1.70€）", "トラムT2線（空港から中央駅へ直結・1.70€）"),
    ("naples", "ナポリ", "Naples", "IT", "Europe/Rome", True, "ナポリ・カポディキーノ国際空港(NAP)", "Alibus空港シャトルバス（ナポリ中央駅まで15分・港まで30分 / 5€）", "Alibus（クレカタッチ乗車対応・5€）"),
    ("barcelona", "バルセロナ", "Barcelona", "ES", "Europe/Madrid", True, "バルセロナ・エル・プラット空港(BCN)", "Aerobús空港急行バス（カタルーニャ広場まで35分 / 7.25€）", "国鉄R2 Nord線または市バス46番（パセジ・ダ・グラシア駅まで25分 / 約5€）"),
    ("madrid", "マドリード", "Madrid", "ES", "Europe/Madrid", True, "バラハス国際空港(MAD)", "公定料金タクシー（M-30環状線内の中心部まで一律33€ / 約25分）", "Cercanías国鉄C1/C10線または24時間空港急行バス（アトーチャ駅まで30分 / 2.6〜5€）"),
    ("seville", "セビリア", "Seville", "ES", "Europe/Madrid", True, "セビリア空港(SVQ)", "タクシー（旧市街まで定額約25〜30€ / 約20分）", "EA空港特別バス（サンタ・フスタ駅・アルマス広場まで35分 / 5€）"),
    ("granada", "グラナダ", "Granada", "ES", "Europe/Madrid", True, "グラナダ空港(GRX)", "タクシー（アルハンブラ宮殿・中心部まで約25分 / 約30€）", "ALSA空港バス（カテドラル・中心部まで約40分 / 3€）"),
    ("frankfurt", "フランクフルト", "Frankfurt", "DE", "Europe/Berlin", True, "フランクフルト国際空港(FRA)", "SバーンS8/S9近郊電車（フランクフルト中央駅までわずか11分 / 5.80€）", "SバーンS8/S9（中央駅・ハウプトヴァッヘまで直通）"),
    ("munich", "ミュンヘン", "Munich", "DE", "Europe/Berlin", True, "ミュンヘン国際空港(MUC)", "ルフトハンザ・エクスプレス・バス（ミュンヘン中央駅まで45分 / 約13€）", "SバーンS1/S8近郊電車（マリエン広場・中央駅まで約40分 / 13.60€）"),
    ("berlin", "ベルリン", "Berlin", "DE", "Europe/Berlin", True, "ベルリン・ブランデンブルク国際空港(BER)", "FEX空港急行列車・RE列車（ベルリン中央駅まで30分 / 4.40€）", "SバーンS9/S45（市内中心部まで4.40€・ABCゾーン切符）"),
    ("zurich", "チューリッヒ", "Zurich", "CH", "Europe/Zurich", True, "チューリッヒ国際空港(ZRH)", "スイス国鉄SBB列車（チューリッヒ中央駅までわずか10分 / 6.80CHF）", "SBB列車またはトラム10番（同一ゾーン料金6.80CHF）"),
    ("geneva", "ジュネーブ", "Geneva", "CH", "Europe/Zurich", True, "ジュネーブ国際空港(GVA)", "スイス国鉄SBB列車（コルナヴァン中央駅までわずか7分 / 3.00CHF）", "SBB列車・UNIRESOバス（10番バスのアプリ等で80分有効チケット購入）"),
    ("interlaken", "インターラーケン（ユングフラウ）", "Interlaken", "CH", "Europe/Zurich", True, "チューリッヒ空港(ZRH)", "スイス国鉄IC特急（ベルン乗換または直通で約2時間15分 / スイストラベルパス対応）", "SBB早割Supersaverチケット利用（半額以下で乗車可能）"),
    ("zermatt", "ツェルマット（マッターホルン）", "Zermatt", "CH", "Europe/Zurich", True, "チューリッヒ空港(ZRH) / ジュネーブ空港(GVA)", "スイス国鉄IC＋マッターホルン・ゴッタルド鉄道（フィスプ乗換で約3時間半）", "SBB Supersaverチケットまたはスイストラベルパス利用"),
    ("vienna", "ウィーン", "Vienna", "AT", "Europe/Vienna", True, "ウィーン国際空港(VIE)", "CATシティ・エアポート・トレイン（ウィーン・ミッテ駅までノンストップ16分 / 14.90€）", "ÖBB国鉄S7近郊列車・Railjet（ミッテ駅・中央駅まで15〜25分 / わずか4.40€）"),
    ("salzburg", "ザルツブルク", "Salzburg", "AT", "Europe/Vienna", True, "ザルツブルク空港(SZG)", "タクシー（旧市街・中央駅まで約15分 / 約20€）", "トロリーバス2番・10番（中央駅・旧市街まで約20分 / 2.30€）"),
    ("prague", "プラハ", "Prague", "CZ", "Europe/Prague", True, "ヴァーツラフ・ハヴェル・プラハ国際空港(PRG)", "Uber Airport公式配車・AEエアポートエクスプレスバス（プラハ本駅まで35分 / 100CZK）", "トロリーバス59番＋地下鉄A線（中心部ムーステク駅まで約30分 / わずか40CZK）"),
    ("amsterdam", "アムステルダム", "Amsterdam", "NL", "Europe/Amsterdam", True, "スキポール国際空港(AMS)", "NSオランダ鉄道（アムステルダム中央駅までわずか14〜17分 / 4.90€）", "NS鉄道（クレカのタッチ決済で改札をそのまま通過可能）"),
    ("brussels", "ブリュッセル", "Brussels", "BE", "Europe/Brussels", True, "ブリュッセル国際空港(BRU)", "ベルギー国鉄SNCB（ブリュッセル中央駅・南駅まで約17分 / 約10.30€）", "STIB空港バス12番（EU機関エリア・市内まで約30分 / 7.50€）"),
    ("lisbon", "リスボン", "Lisbon", "PT", "Europe/Lisbon", True, "ウンベルト・デルガード空港(LIS)", "地下鉄レッドライン（サルダーニャ・中心部まで約20分 / 1.80€）", "地下鉄レッドライン（クレカタッチ乗車対応で1.80€）"),
    ("athens", "アテネ", "Athens", "GR", "Europe/Athens", True, "アテネ国際空港(ATH)", "地下鉄3号線ブルーライン（シンタグマ広場まで40分 / 9€）", "24時間運行X95急行バス（シンタグマ広場まで約60分 / 5.50€）"),
    ("santorini", "サントリーニ島", "Santorini", "GR", "Europe/Athens", True, "サントリーニ空港(JTR)", "ホテル送迎・タクシー（フィラまで15分・イアまで30分 / 約25〜40€）", "KTEL公共バス（フィラのバスターミナルまで約15分 / 1.60€）"),
    ("budapest", "ブダペスト", "Budapest", "HU", "Europe/Budapest", True, "リスト・フェレンツ国際空港(BUD)", "100E空港シャトル急行バス（デアーク広場まで35分 / 2,200Ft・タッチ決済可）", "200Eバス＋地下鉄M3線（中心部まで約50分 / 900Ft）"),
    ("helsinki", "ヘルシンキ", "Helsinki", "FI", "Europe/Helsinki", True, "ヘルシンキ・ヴァンター国際空港(HEL)", "VR近郊列車I線・P線（ヘルシンキ中央駅まで約30分 / 4.10€）", "HSLバス600番または列車（どちらもABCゾーン切符4.10€で共通）"),
    ("stockholm", "ストックホルム", "Stockholm", "SE", "Europe/Stockholm", True, "アーランダ国際空港(ARN)", "アーランダ・エクスプレス高速列車（中央駅までわずか18分 / 340SEK）", "Flygbussarna / FlixBus空港バス（中央駅まで約45分 / 129SEK〜）"),
    ("copenhagen", "コペンハーゲン", "Copenhagen", "DK", "Europe/Copenhagen", True, "コペンハーゲン空港(CPH)", "メトロM2線またはDSB国鉄（コンゲンス・ニュートー駅・中央駅まで13〜15分 / 30DKK）", "メトロ・国鉄共通3ゾーン切符（30DKKでわずか15分）"),
    ("warsaw", "ワルシャワ", "Warsaw", "PL", "Europe/Warsaw", True, "ワルシャワ・ショパン空港(WAW)", "SKM近郊鉄道S2/S3線（ワルシャワ中央駅まで約20分 / 4.40PLN≒約170円）", "市バス175番（旧市街・中央駅まで約25分 / 4.40PLN）"),
    ("sydney", "シドニー", "Sydney", "AU", "Australia/Sydney", True, "シドニー・キングスフォード・スミス国際空港(SYD)", "エアポート・リンク鉄道（セントラル駅・サーキュラーキーまで10〜15分 / 約20.60A$）", "路線バス420番＋電車乗継（空港駅アクセス料を回避して約5A$）"),
    ("melbourne", "メルボルン", "Melbourne", "AU", "Australia/Melbourne", True, "メルボルン空港(MEL)", "スカイバス・メルボルンシティエクスプレス（サザンクロス駅まで約30分 / 23.90A$）", "路線バス901番＋鉄道ブロードメドウズ駅乗継（mykiカードで約5.30A$）"),
    ("cairns", "ケアンズ", "Cairns", "AU", "Australia/Brisbane", False, "ケアンズ国際空港(CNS)", "タクシー・Uber（ケアンズ市内中心部までわずか10分 / 約25〜30A$）", "空港乗合シャトルバス（市内ホテルまで約15分 / 約15A$）"),
    ("gold-coast", "ゴールドコースト", "Gold Coast", "AU", "Australia/Brisbane", False, "ゴールドコースト空港(OOL)", "Uber・タクシー（サーファーズパラダイスまで約35分 / 約60〜75A$）", "777番バス＋G:linkトラム（サーファーズパラダイスまで約45分 / わずか0.50A$！）"),
    ("brisbane", "ブリスベン", "Brisbane", "AU", "Australia/Brisbane", False, "ブリスベン空港(BNE)", "エアトレイン空港鉄道（ブリスベンセントラル駅まで20分 / 21.90A$）", "Uber（2〜3人以上ならエアトレインより割安・約45A$）"),
    ("perth", "パース", "Perth", "AU", "Australia/Perth", False, "パース空港(PER)", "トランスパース鉄道エアポートライン（パース駅までわずか18分 / 5.10A$）", "エアポートライン鉄道（速くて激安の5.10A$）"),
    ("auckland", "オークランド", "Auckland", "NZ", "Pacific/Auckland", True, "オークランド国際空港(AKL)", "SkyDrive直行バス（スカイシティ中心部まで約35分 / 20NZ$）", "AirportLinkバス＋鉄道（プヒヌイ駅乗換でブリトマート駅まで約45分 / 約6NZ$）"),
    ("queenstown", "クイーンズタウン", "Queenstown", "NZ", "Pacific/Auckland", True, "クイーンズタウン空港(ZQN)", "タクシー・Uber（中心部まで約15分 / 約35〜45NZ$）", "Orbus公共バス1番（中心部まで約20分 / Bee Card利用で2NZ$・現金10NZ$）"),
    ("christchurch", "クライストチャーチ", "Christchurch", "NZ", "Pacific/Auckland", True, "クライストチャーチ国際空港(CHC)", "Uber・タクシー（市内中心部まで約20分 / 約40NZ$）", "メトロバス3番・29番（バスインターチェンジまで約30分 / 現金4NZ$・カード2NZ$）"),
    ("nadi", "フィジー（ナンディ）", "Nadi", "FJ", "Pacific/Fiji", False, "ナンディ国際空港(NAN)", "空港公認イエロータクシー（デナラウ地区リゾートまで約20分 / 約30〜35FJ$）", "ローカルバス（ナンディタウンまで約15分 / 約2FJ$）"),
    ("noumea", "ニューカレドニア（ヌメア）", "Noumea", "NC", "Pacific/Noumea", False, "ラ・トントゥータ国際空港(NOU)", "エアポートシャトルバス（ヌメア市内ホテルまで約45〜60分 / 約3,000XPF）", "Raï長距離バス（市内まで格安移動・本数限定）"),
    ("tahiti", "タヒチ（パペーテ・ボラボラ）", "Tahiti", "PF", "Pacific/Tahiti", False, "ファアア国際空港(PPT)", "タクシー（パペーテ中心部まで約15分 / 約2,000〜2,500XPF）", "Terevau高速フェリー（モーレア島へ30分）または国内線（ボラボラ島へ50分）"),
    ("dubai", "ドバイ", "Dubai", "AE", "Asia/Dubai", False, "ドバイ国際空港(DXB)", "ドバイ・メトロ・レッドライン（ブルジュ・ハリファ駅まで約25分 / 約8AED）", "公営タクシー・Careem（初乗り25AED〜・市内中心部まで約50〜70AEDで激安）"),
    ("abu-dhabi", "アブダビ", "Abu Dhabi", "AE", "Asia/Dubai", False, "ザイード国際空港(AUH)", "タクシー・Careem（市内中心部・シェイクザイードモスクまで約20〜30分 / 約70〜90AED）", "空港急行バスA1・A2（市内中心部まで約45分 / 4AED）"),
    ("istanbul", "イスタンブール", "Istanbul", "TR", "Europe/Istanbul", False, "イスタンブール空港(IST)", "Havaist空港リムジンバス（スルタンアフメット・タクシム広場まで約60〜80分 / 約200〜250₺）", "地下鉄M11号線＋M2号線乗り継ぎ（市内中心部まで約50分 / 約50₺）"),
    ("cappadocia", "カッパドキア", "Cappadocia", "TR", "Europe/Istanbul", False, "ネヴシェヒル空港(NAV) / カイセリ空港(ASR)", "事前予約乗合シャトルバン（ギョレメの洞窟ホテルまで直接送迎・約40〜60分 / 約10〜15€）", "ホテル手配シャトル（公共交通がないため事前予約シャトルが最安かつ確実）"),
    ("doha", "ドーハ", "Doha", "QA", "Asia/Qatar", False, "ハマド国際空港(DOH)", "ドーハ・メトロ・レッドライン（スーク・ワキーフ・ウエストベイまで約15〜20分 / わずか2QR！）", "ドーハ・メトロ（世界最高峰の清潔さと安さ・1日券でも6QR）"),
    ("cairo", "カイロ", "Cairo", "EG", "Africa/Cairo", True, "カイロ国際空港(CAI)", "Uber（タハリール広場・ギザのピラミッド周辺まで約40〜60分 / 約250〜400E£）", "エアコン付き空港バス（タハリール広場まで約50分 / 約25E£）"),
    ("marrakech", "マラケシュ", "Marrakech", "MA", "Africa/Casablanca", False, "マラケシュ・メナラ空港(RAK)", "空港公認タクシー（フナ広場・新市街まで約15分 / 定額70〜100DH）", "ALSA空港急行バスL19（フナ広場まで約20分 / 30DH・往復50DH）")
]


def generate_cities_data() -> list:
    cities = []
    for item in RAW_CITIES:
        slug, name_ja, name_en, cc, tz, has_dst, airport, fastest, cheapest = item
        p = COUNTRY_PROFILES[cc]
        dst_note = "あり（春〜秋は時計が1時間進みます。上の時計はサマータイム自動反映済み）" if has_dst else "なし（年間を通じて時差は一定です）"
        trans_note = "スマホ・PC・カメラ等の充電器（100-240V対応表記）は変圧器不要。日本の100V専用ドライヤーやヘアアイロンは変圧器が必要です。" if p["voltage"] not in ("120V", "110V") else "電圧が日本(100V)と近いため、短期旅行ならスマホ充電器や多くの電化製品がそのまま使えます。"

        cities.append({
            "slug": slug,
            "name_ja": name_ja,
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
            "airport_access": {
                "airport_name": airport,
                "fastest": fastest,
                "cheapest": cheapest
            },
            "transport_apps": p["apps"],
            "telecom_note": f"{name_ja}（{p['country_ja']}）では空港からの移動・配車アプリ（{p['apps'][0]}等）・キャッシュレス決済に常時通信が必須です。到着前に日本でeSIMを設定しておくと空港に降りた瞬間から繋がります。"
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
            "LKR": 1.9, "NPR": 0.88, "CAD": 0.0091, "MXN": 0.13, "PEN": 0.024,
            "BRL": 0.038, "CHF": 0.0057, "CZK": 0.15, "HUF": 2.45, "SEK": 0.070,
            "DKK": 0.045, "PLN": 0.026, "AUD": 0.010, "NZD": 0.011, "FJD": 0.015,
            "XPF": 0.73, "AED": 0.024, "TRY": 0.22, "QAR": 0.024, "EGP": 0.32, "MAD": 0.065
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


def build_city_html(city: dict, rates_data: dict, all_cities: list) -> str:
    code = city["currency_code"]
    jpy_to_local = rates_data["rates"].get(code, 0.01)
    local_to_jpy = round(1 / jpy_to_local, 2) if jpy_to_local >= 0.005 else round(1 / jpy_to_local, 4)
    thousand_jpy_in_local = round(1000 * jpy_to_local, 2)

    related = [c for c in all_cities if c["region"] == city["region"] and c["slug"] != city["slug"]][:8]
    related_html = "".join([
        f'<a href="../{c["slug"]}/" class="text-xs bg-white border border-slate-200 px-3 py-1.5 rounded-lg hover:border-blue-500 transition">{c["name_ja"]}</a>'
        for c in related
    ])

    context_affiliate = ""
    if not city["tap_water_safe"]:
        context_affiliate = f"""
        <div class="p-4 rounded-xl bg-amber-50 border border-amber-200 mt-3">
          <p class="text-xs font-bold text-amber-900">⚠️ {city['name_ja']}は水道水の直接飲用NG</p>
          <p class="text-xs text-slate-700 mt-1">万が一の体調不良時、現地の私立病院は高額になります。キャッシュレス診療対応の海外旅行保険（または利用付帯クレカ）を必ず準備しておきましょう。</p>
          <a href="{AFFILIATE_INSURANCE_URL}" class="inline-block mt-2 text-xs font-bold text-blue-600 underline">→ {city['country_ja']}対応の海外旅行保険・付帯カードを見る</a>
        </div>"""
    elif city["tip_level"] == "required":
        context_affiliate = f"""
        <div class="p-4 rounded-xl bg-rose-50 border border-rose-200 mt-3">
          <p class="text-xs font-bold text-rose-900">💳 {city['name_ja']}はカードタッチ決済＆チップ必須</p>
          <p class="text-xs text-slate-700 mt-1">一般的な日本のクレカは海外事務手数料（約2.2〜3.85%）が毎回上乗せされます。海外手数料が安いカードやデビットを使うだけで数千円節約できます。</p>
          <a href="{AFFILIATE_CARD_URL}" class="inline-block mt-2 text-xs font-bold text-blue-600 underline">→ 海外決済に強いおすすめカード比較</a>
        </div>"""

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
                "name": f"{city['name_ja']}の水道水は飲めますか？",
                "acceptedAnswer": {"@type": "Answer", "text": city["tap_water_note"]}
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{city['name_ja']}の現地情報まとめ｜時差・コンセント({city['plug_type']})・チップ・為替を1画面で即答</title>
  <meta name="description" content="{city['name_ja']}（{city['country_ja']}）の現在時刻・時差、コンセントのプラグ形状（{city['plug_type']}）・電圧（{city['voltage']}）、チップ相場、最新為替レート、{city['airport_access']['airport_name']}からの移動手段をスクロールなしで即確認。">
  <link rel="canonical" href="{SITE_URL}/{city['slug']}/">
  <link rel="manifest" href="../manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-12">
  <header class="bg-white border-b border-slate-200 sticky top-0 z-10">
    <div class="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../" class="font-bold text-slate-800 text-sm flex items-center gap-1">🌐 {SITE_NAME}</a>
      <span class="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full font-medium">{city['region']} / {city['country_ja']}</span>
    </div>
  </header>

  <main class="max-w-2xl mx-auto px-4 pt-4 space-y-4">
    <div class="flex items-baseline justify-between">
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

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
      <h2 class="text-sm font-bold flex items-center gap-1.5">📶 現地の通信・ネット環境</h2>
      <p class="text-xs text-slate-700 mt-1.5 leading-relaxed">{city['telecom_note']}</p>
      <div class="mt-3 p-3.5 rounded-xl bg-blue-50 border border-blue-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <p class="text-xs font-bold text-blue-900">📱 搭乗前に5分で開通！{city['country_ja']}対応eSIM</p>
          <p class="text-[11px] text-slate-600 mt-0.5">SIMピン不要・空港に着いた瞬間からGoogleマップや配車アプリが使えます。</p>
        </div>
        <a href="{AFFILIATE_ESIM_URL}" class="shrink-0 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold px-3.5 py-2.5 rounded-lg text-center transition">
          最安eSIMを見る →
        </a>
      </div>
    </section>

    <section class="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 space-y-3">
      <h2 class="text-sm font-bold">📌 お金・マナー・生活ルール詳細</h2>
      <div class="text-xs space-y-2.5 text-slate-700 leading-relaxed">
        <p><strong class="text-slate-900">💵 チップの詳細：</strong>{city['tip_detail']}</p>
        <p><strong class="text-slate-900">🛍️ 税金・免税（Tax Free）：</strong>{city['tax_note']}</p>
        <p><strong class="text-slate-900">🔌 変圧器・周波数（{city['frequency']}）：</strong>{city['transformer_note']}</p>
        <p><strong class="text-slate-900">💧 水道水・氷：</strong>{city['tap_water_note']}</p>
        <p><strong class="text-slate-900">☀️ サマータイム：</strong>{city['dst_note']}</p>
        <p class="text-rose-700 font-bold pt-1">🚨 緊急連絡先（警察・救急・消防）：{city['emergency_numbers']}</p>
      </div>
      {context_affiliate}
    </section>

    <section class="pt-2">
      <h3 class="text-xs font-bold text-slate-500 mb-2">🗺️ {city['region']}の他の都市をチェック</h3>
      <div class="flex flex-wrap gap-1.5">{related_html}</div>
    </section>
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
        f'<a href="./{c["slug"]}/" data-region="{c["region"]}" data-search="{c["name_ja"]} {c["name_en"].lower()} {c["country_ja"]} {c["currency_code"].lower()}" '
        f'class="city-card block bg-white p-3.5 rounded-2xl border border-slate-200 hover:border-blue-500 shadow-sm transition">'
        f'<div class="flex items-center justify-between">'
        f'<span class="font-extrabold text-sm text-slate-900">{c["name_ja"]}</span>'
        f'<span class="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">{c["country_ja"]}</span>'
        f'</div>'
        f'<div class="text-[11px] text-slate-500 mt-1.5 flex items-center gap-2">'
        f'<span>🔌 {c["plug_type"]}</span>'
        f'<span>💱 {c["currency_code"]}</span>'
        f'<span>💵 チップ{c["tip_badge"].split("（")[0]}</span>'
        f'</div>'
        f'</a>'
        for c in cities
    ])

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME}｜世界{len(cities)}都市の時差・コンセント・チップ・為替を1画面で即答</title>
  <meta name="description" content="海外旅行や留学・出張の渡航前や空港ですぐに知りたい世界{len(cities)}都市の現在時刻・時差・コンセント形状・電圧・チップ相場・最新為替レート・空港アクセスをスクロールなしで即解決。">
  <link rel="canonical" href="{SITE_URL}/">
  <link rel="manifest" href="./manifest.json">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased pb-16">
  <main class="max-w-3xl mx-auto px-4 pt-8 space-y-6">
    <div class="text-center space-y-2">
      <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">🌐 {SITE_NAME}</h1>
      <p class="text-xs sm:text-sm text-slate-600">世界{len(cities)}都市の「時差・プラグ・チップ・為替・空港移動」をスクロールなしで即答</p>
    </div>

    <div class="sticky top-2 z-10 bg-slate-50/90 backdrop-blur py-2 space-y-2.5">
      <input id="search" type="text" placeholder="🔍 都市名・国名・英語名で即検索（例：ロンドン、ソウル、ハワイ、タイ）"
        class="w-full p-3.5 rounded-2xl border border-slate-300 bg-white shadow-sm text-sm focus:outline-none focus:border-blue-500">
      <div class="flex gap-1.5 overflow-x-auto pb-1 no-scrollbar">{region_buttons}</div>
    </div>

    <div id="grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">{cards_html}</div>
  </main>

  <script>
    let currentRegion = 'すべて';
    const searchInput = document.getElementById('search');
    const cards = document.querySelectorAll('.city-card');
    const regionBtns = document.querySelectorAll('.region-btn');

    function filterCards() {{
      const q = searchInput.value.toLowerCase().trim();
      cards.forEach(card => {{
        const matchSearch = card.dataset.search.includes(q);
        const matchRegion = (currentRegion === 'すべて' || card.dataset.region === currentRegion);
        card.style.display = (matchSearch && matchRegion) ? 'block' : 'none';
      }});
    }}

    searchInput.addEventListener('input', filterCards);

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
    manifest = {
        "name": SITE_NAME,
        "short_name": SITE_NAME,
        "start_url": "./",
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#0f172a"
    }
    (dist_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    sw_js = """const CACHE_NAME = 'pocket-guide-v1';
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
    print(f"✅ 完了！ 全 {len(cities)} 都市のページを更新しました。")


if __name__ == "__main__":
    main()
