#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
都市別カレンダー データ・判定エンジン (climate_calendar.py)
- 月別の気候平年値（最高/最低気温・降水量・降水日数・湿度・日照・UVI・例外フラグ）から
  快適スコア(0-100)、ラベル、理由タグ、服装、月別アドバイスを自動生成
- 特集ページ（GW・夏休み等）の比較表・選定整合チェックにも再利用
"""

from typing import Dict, List, Tuple

THRESHOLD_VERSION = "v1.0 (2026-11)"
DATA_SOURCE_NOTE = "WMO平年値(1991-2020)およびOpen-Meteo過去気象集計をもとに算出"

# 各タグに対応する対策文
TAG_ADVICE = {
    "猛暑": "観光は早朝と夕方に寄せ、日中は屋内で休憩。こまめな水分補給と帽子が必須です。",
    "暑い": "通気性の良い半袖が基本。日差し対策のサングラスや帽子があると快適です。",
    "蒸し暑い": "速乾素材の服が快適。屋内や電車は冷房が強いので薄手の羽織りを携帯してください。",
    "寒い": "コートやジャケット、ニットなどしっかりした防寒着が必要です。",
    "厳寒": "ダウンコート・手袋・マフラー・防寒靴など真冬装備が必須です。",
    "雨が多い": "防水の上着や折りたたみ傘を常備。滑りにくい靴だと安心です。",
    "乾燥・雨が少ない": "リップクリームや保湿ケア、日中の日差し対策を準備してください。",
    "寒暖差大": "朝晩と日中の気温差が大きいため、脱ぎ着しやすい重ね着が基本です。",
    "日照短い": "日照時間が非常に短いため、屋外観光は日中の明るい時間帯に集中させましょう。",
    "紫外線強い": "紫外線が非常に強いため、日焼け止め・サングラス・帽子が必須です。",
    "台風": "台風接近時はフライト遅延・欠航のリスクあり。運航状況と海外旅行保険を確認してください。",
    "ハリケーン": "ハリケーンシーズンにあたるため、気象警報と変更可能な予約条件の確認が安心です。",
    "サイクロン": "サイクロン発生時期のため、離島移動やマリンアクティビティは天候判断を優先してください。",
    "高山病・寒暖差": "標高が高いため到着初日は無理をせず水分補給を多めに。朝晩の冷え込みにも備えてください。",
}

# 都市ごとの月別気候データ
# 各リストは1月〜12月の12要素:
# (平均最高℃, 平均最低℃, 降水量mm, 降水日数, 湿度%, 日照h/日, UVI)
CITY_MONTHLY_CLIMATE: Dict[str, dict] = {
    "marrakech": {
        "zone": "steppe_desert",
        "south": False,
        "hazards": {6: ["猛暑・砂塵"], 7: ["猛暑・砂塵"], 8: ["猛暑・砂塵"], 9: ["猛暑・砂塵"]},
        "highlight": "ラマダン期間中は飲食店の日中休業や営業時間変更、さらにモロッコ標準時が一時的に1時間戻る（UTC+0）運用があるため事前確認が必要です。",
        "months": [
            (18, 6, 32, 6, 65, 7.1, 4), (20, 8, 38, 6, 63, 7.6, 5), (23, 10, 38, 6, 59, 8.2, 7),
            (25, 12, 34, 5, 56, 8.7, 8), (28, 15, 22, 4, 52, 9.5, 9), (33, 18, 5, 1, 46, 10.6, 10),
            (38, 21, 1, 1, 39, 10.8, 11), (38, 21, 3, 1, 41, 10.2, 10), (33, 19, 6, 2, 49, 8.9, 8),
            (28, 15, 24, 4, 56, 7.9, 6), (22, 10, 41, 6, 63, 7.2, 4), (19, 7, 31, 6, 66, 6.9, 3),
        ],
    },
    "lisbon": {
        "zone": "mediterranean",
        "south": False,
        "hazards": {},
        "highlight": "夏はほとんど雨が降らず乾燥して日差しが強い一方、11〜2月は雨季にあたり石畳が滑りやすくなります。",
        "months": [
            (15, 8, 100, 12, 80, 4.7, 2), (16, 9, 85, 10, 77, 5.5, 3), (19, 11, 55, 8, 72, 6.8, 5),
            (20, 12, 65, 9, 71, 7.9, 7), (22, 14, 50, 7, 70, 9.1, 8), (25, 16, 15, 3, 67, 10.1, 9),
            (28, 18, 4, 1, 64, 11.4, 9), (28, 18, 6, 1, 64, 10.8, 8), (26, 17, 30, 5, 68, 8.8, 6),
            (22, 15, 100, 10, 75, 6.9, 4), (18, 12, 125, 12, 79, 5.2, 2), (15, 9, 120, 13, 81, 4.6, 2),
        ],
    },
    "bangkok": {
        "zone": "tropical_savanna",
        "south": False,
        "hazards": {6: ["モンスーン"], 7: ["モンスーン"], 8: ["モンスーン"], 9: ["モンスーン"], 10: ["モンスーン"]},
        "highlight": "11〜2月が比較的過ごしやすい乾季。4〜5月は年間で最も暑い暑季（4月中旬は水かけ祭りソンクラーン）、6〜10月はスコールが多い雨季です。",
        "months": [
            (32, 22, 13, 2, 68, 8.8, 9), (33, 24, 20, 3, 72, 8.5, 10), (34, 25, 42, 4, 74, 8.4, 11),
            (35, 26, 90, 7, 75, 8.5, 11), (34, 26, 220, 15, 78, 7.5, 11), (33, 26, 155, 15, 78, 6.5, 10),
            (33, 25, 165, 16, 78, 6.0, 10), (33, 25, 205, 18, 79, 5.8, 10), (32, 25, 330, 21, 82, 5.5, 10),
            (32, 24, 280, 17, 81, 6.4, 9), (32, 23, 55, 6, 74, 8.1, 9), (31, 21, 10, 2, 68, 8.6, 8),
        ],
    },
    "bali": {
        "zone": "tropical_monsoon_south",
        "south": True,
        "hazards": {},
        "highlight": "4〜10月が晴れが多く過ごしやすい乾季、11〜3月がスコールが増える雨季です（南半球ですが通年常夏です）。",
        "months": [
            (31, 25, 340, 21, 84, 5.5, 11), (31, 25, 280, 18, 84, 6.0, 11), (31, 25, 210, 15, 82, 6.8, 11),
            (31, 25, 100, 9, 78, 8.0, 10), (31, 24, 80, 7, 77, 8.3, 9), (30, 24, 70, 6, 76, 8.1, 8),
            (29, 23, 55, 5, 75, 8.2, 8), (29, 23, 30, 4, 74, 8.6, 9), (30, 24, 45, 5, 75, 8.5, 10),
            (31, 24, 95, 8, 77, 8.2, 11), (31, 25, 180, 14, 80, 7.2, 11), (31, 25, 290, 19, 83, 5.8, 11),
        ],
    },
    "singapore": {
        "zone": "equatorial",
        "south": False,
        "hazards": {},
        "highlight": "赤道直下で1年を通して高温多湿。月ごとの気温差は小さいですが、11〜1月は北東モンスーンで降水量が増えます。",
        "months": [
            (30, 24, 240, 14, 84, 5.6, 10), (31, 24, 115, 9, 81, 6.5, 11), (32, 25, 170, 13, 82, 6.2, 11),
            (32, 25, 175, 15, 83, 5.8, 11), (32, 25, 170, 14, 83, 5.8, 10), (31, 25, 160, 13, 82, 5.9, 10),
            (31, 25, 160, 13, 82, 6.1, 10), (31, 25, 175, 14, 82, 5.9, 10), (31, 25, 170, 14, 82, 5.4, 11),
            (31, 25, 190, 15, 83, 5.2, 11), (31, 24, 250, 19, 85, 4.4, 10), (30, 24, 290, 19, 86, 4.3, 10),
        ],
    },
    "sydney": {
        "zone": "temperate_south",
        "south": True,
        "hazards": {},
        "highlight": "日本と季節が逆になります。12〜2月が夏（強い紫外線に注意）、6〜8月が冬（東京ほど厳寒ではなく晴天が多い）です。",
        "months": [
            (26, 19, 100, 11, 65, 7.4, 11), (26, 19, 120, 11, 67, 6.9, 10), (25, 18, 130, 12, 66, 6.4, 8),
            (23, 15, 125, 11, 65, 6.4, 5), (20, 12, 120, 10, 64, 6.1, 3), (17, 9, 130, 11, 63, 5.8, 2),
            (17, 8, 95, 9, 60, 6.5, 3), (18, 9, 80, 8, 56, 7.6, 4), (21, 11, 68, 8, 55, 7.8, 6),
            (22, 14, 77, 10, 58, 7.5, 8), (24, 16, 84, 11, 61, 7.4, 10), (25, 18, 78, 10, 63, 7.7, 11),
        ],
    },
    "honolulu": {
        "zone": "tropical_tradewind",
        "south": False,
        "hazards": {},
        "highlight": "年間を通して貿易風が吹き快適。5〜10月が乾季で晴天率が高く、11〜4月はシャワー（通り雨）がやや増えます。",
        "months": [
            (27, 19, 58, 9, 71, 6.9, 7), (27, 19, 50, 8, 70, 7.5, 8), (27, 20, 51, 9, 69, 7.9, 10),
            (28, 21, 20, 7, 67, 8.3, 11), (29, 22, 16, 6, 66, 9.0, 11), (30, 23, 7, 5, 65, 9.5, 11),
            (31, 24, 13, 7, 66, 9.7, 11), (31, 24, 14, 6, 66, 9.6, 11), (31, 23, 19, 7, 66, 9.1, 10),
            (30, 23, 47, 8, 68, 7.9, 8), (29, 22, 60, 9, 70, 6.9, 7), (27, 20, 82, 10, 71, 6.6, 6),
        ],
    },
    "london": {
        "zone": "oceanic",
        "south": False,
        "hazards": {},
        "highlight": "1年を通じて小雨がぱらつきやすく、1日の中で天気が変わりやすいのが特徴。5〜9月は日が長く観光に最適です。",
        "months": [
            (8, 3, 55, 11, 82, 1.9, 1), (9, 3, 41, 9, 78, 2.7, 1), (12, 5, 42, 10, 74, 3.8, 3),
            (15, 7, 44, 10, 69, 5.4, 4), (18, 10, 49, 9, 68, 6.4, 6), (21, 13, 45, 9, 67, 6.7, 7),
            (24, 15, 45, 8, 66, 6.9, 7), (23, 15, 50, 9, 68, 6.5, 5), (20, 13, 49, 9, 72, 5.0, 4),
            (16, 10, 69, 11, 78, 3.6, 2), (11, 6, 59, 11, 81, 2.3, 1), (9, 4, 55, 11, 83, 1.7, 1),
        ],
    },
    "seoul": {
        "zone": "continental_monsoon",
        "south": False,
        "hazards": {7: ["モンスーン"], 8: ["台風"]},
        "highlight": "4〜5月と9〜10月が爽やかなベストシーズン。7〜8月は梅雨・豪雨と蒸し暑さ、12〜2月は氷点下の厳しい寒さになります。",
        "months": [
            (2, -6, 21, 6, 58, 5.5, 2), (5, -3, 25, 6, 57, 6.0, 3), (11, 2, 46, 7, 58, 6.5, 5),
            (18, 8, 77, 8, 58, 7.0, 7), (23, 13, 102, 9, 63, 7.3, 8), (27, 18, 133, 10, 69, 6.3, 9),
            (29, 22, 395, 16, 78, 4.2, 9), (30, 22, 364, 15, 76, 5.0, 9), (26, 17, 169, 9, 68, 6.0, 7),
            (20, 10, 52, 6, 63, 6.5, 5), (12, 3, 52, 8, 62, 5.2, 3), (4, -3, 22, 7, 59, 5.0, 2),
        ],
    },
    "new-york": {
        "zone": "humid_subtropical",
        "south": False,
        "hazards": {},
        "highlight": "4〜6月と9〜10月が街歩きに最適。7〜8月は蒸し暑く、12〜2月は氷点下まで冷え込みます。",
        "months": [
            (4, -3, 92, 10, 62, 5.2, 2), (6, -2, 78, 9, 60, 6.0, 3), (10, 2, 110, 11, 59, 6.9, 5),
            (17, 7, 114, 11, 57, 7.5, 7), (22, 13, 106, 11, 62, 8.2, 8), (27, 18, 112, 11, 65, 8.6, 9),
            (30, 21, 117, 11, 65, 8.6, 9), (29, 20, 113, 10, 67, 8.2, 8), (25, 16, 109, 9, 67, 7.3, 6),
            (18, 10, 111, 9, 65, 6.5, 4), (12, 5, 102, 9, 64, 5.0, 2), (7, 0, 101, 11, 63, 4.5, 2),
        ],
    },
    "reykjavik": {
        "zone": "subpolar",
        "south": False,
        "hazards": {},
        "highlight": "12〜1月は日照時間が1日3〜4時間程度と極端に短く防寒必須。オーロラ観測は9〜4月、白夜と観光は6〜8月が中心です。",
        "months": [
            (2, -3, 76, 13, 78, 0.8, 0), (3, -2, 72, 13, 76, 1.9, 1), (4, -2, 82, 14, 75, 3.6, 1),
            (6, 1, 58, 12, 74, 4.9, 2), (9, 4, 44, 10, 74, 6.2, 3), (12, 7, 50, 10, 77, 5.4, 3),
            (14, 9, 52, 10, 79, 5.5, 3), (13, 8, 62, 12, 79, 5.0, 2), (10, 5, 67, 12, 78, 4.1, 1),
            (7, 2, 86, 14, 79, 2.7, 1), (4, -1, 73, 13, 79, 1.3, 0), (2, -3, 79, 14, 79, 0.4, 0),
        ],
    },
    "taipei": {
        "zone": "subtropical_typhoon",
        "south": False,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"], 10: ["台風"]},
        "highlight": "10〜11月と3〜4月が過ごしやすい時期。5月後半〜6月は梅雨、7〜9月は猛暑・高湿度に加えて台風接近に注意が必要です。",
        "months": [
            (19, 14, 83, 14, 79, 2.6, 4), (20, 14, 170, 14, 80, 2.7, 5), (22, 16, 180, 15, 79, 3.0, 7),
            (26, 19, 178, 15, 78, 3.3, 9), (29, 22, 235, 16, 79, 3.7, 10), (32, 25, 326, 16, 78, 4.5, 11),
            (34, 26, 245, 14, 74, 6.2, 11), (34, 26, 322, 15, 75, 6.1, 11), (31, 24, 360, 15, 76, 5.1, 9),
            (27, 22, 149, 14, 76, 4.0, 7), (24, 19, 83, 14, 76, 3.2, 5), (21, 16, 73, 13, 77, 2.9, 4),
        ],
    },
    "hong-kong": {
        "zone": "subtropical_typhoon",
        "south": False,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"], 10: ["台風"]},
        "highlight": "10〜12月が晴天率が高く爽やかなベストシーズン。5〜9月は高温多湿で雨が非常に多く、台風シーズンとも重なります。",
        "months": [
            (19, 15, 25, 5, 74, 4.6, 5), (19, 15, 54, 9, 80, 3.5, 6), (21, 17, 82, 11, 82, 3.0, 8),
            (25, 21, 175, 12, 83, 3.5, 9), (28, 24, 305, 16, 83, 4.5, 10), (30, 26, 456, 20, 82, 4.9, 11),
            (31, 27, 377, 18, 81, 6.8, 11), (31, 27, 432, 17, 81, 6.1, 11), (30, 26, 328, 15, 78, 5.7, 9),
            (28, 24, 101, 8, 73, 6.2, 7), (24, 20, 38, 6, 71, 6.0, 6), (20, 16, 27, 4, 69, 5.5, 5),
        ],
    },
    "paris": {
        "zone": "oceanic",
        "south": False,
        "hazards": {},
        "highlight": "5〜6月と9月が日照も長く快適。7〜8月は熱波で35℃超えの日もあり、冷房がない宿もあるため注意が必要です。",
        "months": [
            (7, 3, 51, 10, 83, 2.0, 1), (8, 3, 41, 9, 78, 2.8, 2), (12, 6, 48, 10, 73, 4.1, 3),
            (16, 8, 52, 9, 69, 5.5, 5), (20, 11, 63, 10, 70, 6.5, 6), (23, 14, 50, 8, 69, 6.8, 7),
            (25, 16, 62, 8, 68, 7.2, 7), (25, 16, 53, 8, 71, 6.9, 6), (21, 13, 48, 8, 76, 5.5, 4),
            (16, 10, 62, 10, 81, 3.8, 2), (11, 6, 51, 10, 84, 2.3, 1), (8, 4, 58, 11, 84, 1.7, 1),
        ],
    },
    "rome": {
        "zone": "mediterranean",
        "south": False,
        "hazards": {},
        "highlight": "4〜6月と9〜10月が観光のベストシーズン。7〜8月は雨が少なく日差しが強烈な猛暑になります。",
        "months": [
            (12, 3, 67, 8, 75, 3.9, 2), (13, 4, 73, 8, 74, 4.7, 3), (16, 6, 58, 7, 73, 5.4, 4),
            (19, 9, 81, 8, 74, 6.7, 6), (24, 13, 53, 6, 73, 8.5, 8), (28, 17, 34, 4, 71, 9.5, 9),
            (31, 19, 19, 2, 70, 10.7, 9), (31, 19, 22, 3, 70, 9.6, 8), (27, 16, 73, 6, 73, 7.9, 6),
            (22, 12, 113, 8, 76, 6.3, 4), (17, 7, 115, 10, 78, 4.3, 2), (13, 4, 81, 9, 77, 3.6, 2),
        ],
    },
    "istanbul": {
        "zone": "mediterranean_cool",
        "south": False,
        "hazards": {},
        "highlight": "4〜6月と9〜10月がベストシーズン。冬はボスポラス海峡からの冷たい風と雨・雪で体感温度が下がります。",
        "months": [
            (9, 3, 105, 14, 77, 2.3, 2), (9, 3, 78, 12, 75, 3.1, 3), (12, 5, 71, 11, 74, 4.3, 4),
            (17, 9, 46, 8, 72, 6.0, 6), (22, 13, 36, 7, 72, 8.1, 8), (27, 17, 34, 6, 69, 9.8, 9),
            (29, 20, 39, 4, 68, 10.4, 9), (29, 20, 48, 5, 70, 9.4, 8), (25, 17, 63, 7, 72, 7.4, 6),
            (20, 13, 101, 10, 76, 5.1, 4), (15, 9, 109, 12, 77, 3.4, 2), (11, 5, 124, 15, 78, 2.2, 1),
        ],
    },
}


def _fallback_profile_for_city(city: dict) -> dict:
    """未登録都市でも全都市共通テンプレにならないよう、地域・国・緯度傾向から気候プロファイルを割り当てる"""
    slug = city.get("slug", "")
    country = city.get("country_ja", "")
    region = city.get("region", "")

    if country in ("オーストラリア", "ニュージーランド", "チリ", "アルゼンチン", "南アフリカ"):
        return {**CITY_MONTHLY_CLIMATE["sydney"], "zone": f"south_{region}"}
    if country in ("インドネシア", "フィジー", "タヒチ（フランス領ポリネシア）"):
        return {**CITY_MONTHLY_CLIMATE["bali"], "zone": f"trop_south_{region}"}
    if country in ("タイ", "ベトナム", "カンボジア", "フィリピン", "インド", "スリランカ", "マレーシア", "シンガポール"):
        return {**CITY_MONTHLY_CLIMATE["bangkok"], "zone": f"trop_asia_{region}"}
    if country in ("アラブ首長国連邦（UAE）", "カタール", "エジプト", "モロッコ", "ヨルダン", "サウジアラビア"):
        return {**CITY_MONTHLY_CLIMATE["marrakech"], "zone": f"arid_{region}"}
    if country in ("ポルトガル", "スペイン", "イタリア", "ギリシャ", "マルタ", "クロアチア", "トルコ"):
        return {**CITY_MONTHLY_CLIMATE["rome"], "zone": f"med_{region}"}
    if country in ("アイスランド", "ノルウェー", "スウェーデン", "フィンランド"):
        return {**CITY_MONTHLY_CLIMATE["reykjavik"], "zone": f"nordic_{region}"}
    if country in ("台湾", "香港", "マカオ"):
        return {**CITY_MONTHLY_CLIMATE["taipei"], "zone": f"subtrop_ea_{region}"}
    if region == "ヨーロッパ":
        return {**CITY_MONTHLY_CLIMATE["paris"], "zone": f"euro_{region}"}
    if region == "北米":
        if slug in ("honolulu", "maui", "guam", "saipan"):
            return {**CITY_MONTHLY_CLIMATE["honolulu"], "zone": "pacific_island"}
        return {**CITY_MONTHLY_CLIMATE["new-york"], "zone": f"na_{region}"}
    return {**CITY_MONTHLY_CLIMATE["seoul"], "zone": f"east_asia_{region}"}


def evaluate_city_calendar(city: dict) -> dict:
    """都市の12か月カレンダーデータ（スコア・ラベル・理由タグ・服装・自動要約）を生成"""
    slug = city.get("slug", "")
    profile = CITY_MONTHLY_CLIMATE.get(slug) or _fallback_profile_for_city(city)
    months_raw = profile["months"]
    avg_monthly_rain = sum(m[2] for m in months_raw) / 12.0
    is_altitude = slug in ("cusco", "uyuni", "la-paz", "quito", "bogota")
    is_south = profile.get("south", False)
    hazards = profile.get("hazards", {})

    records = []
    for idx, (tmax, tmin, rain_mm, rain_days, hum, sun_h, uvi) in enumerate(months_raw, start=1):
        tags: List[str] = []
        # 1. 気温タグ（強い方を優先）
        if tmax >= 38:
            tags.append("猛暑")
        elif tmax >= 30 and hum >= 75:
            tags.append("蒸し暑い")
        elif tmax >= 32:
            tags.append("暑い")
        elif tmin < -10:
            tags.append("厳寒")
        elif tmax < 10:
            tags.append("寒い")

        # 2. 雨・乾燥タグ
        is_rainy = (rain_mm >= avg_monthly_rain * 1.5 and rain_days >= 10) or rain_days >= 16
        is_dry = rain_mm < 40
        if is_rainy:
            tags.append("雨が多い")
        elif is_dry:
            tags.append("乾燥・雨が少ない")

        # 3. 寒暖差・日照・UVI・災害・標高
        if (tmax - tmin) >= 15:
            tags.append("寒暖差大")
        if sun_h < 3.0:
            tags.append("日照短い")
        if uvi >= 8:
            tags.append("紫外線強い")
        for hz in hazards.get(idx, []):
            tags.append(hz)
        if is_altitude:
            tags.append("高山病・寒暖差")

        # 快適スコア計算（100点減点方式）
        score = 100.0
        if tmax > 27:
            score -= (tmax - 27) * 6.0
        elif tmax < 18:
            score -= (18 - tmax) * 4.0
        score -= min(30.0, rain_days * 2.0)
        if hum > 75:
            score -= min(20.0, (hum - 75) * 1.5)
        if sun_h < 3.0:
            score -= 5.0
        if any(h in ("台風", "ハリケーン", "サイクロン") for h in hazards.get(idx, [])):
            score -= 15.0

        score = max(0, min(100, int(round(score))))
        if score >= 80:
            label = "ベスト"
        elif score >= 65:
            label = "快適"
        elif score >= 45:
            label = "標準"
        else:
            label = "注意"

        # 服装の自動生成（月ごとの実データベース）
        if tmax >= 32:
            outfit = "通気性の良い半袖・帽子・日焼け止め（冷房対策に薄手の羽織り）"
        elif tmax >= 25:
            outfit = "半袖・薄手のシャツ中心（屋内冷房や朝晩用にカーディガン）"
        elif tmax >= 18:
            outfit = "長袖シャツや薄手ニット＋軽めのジャケットで重ね着"
        elif tmax >= 10:
            outfit = "ジャケット・トレンチコート・ニットなど羽織りもの必須"
        else:
            outfit = "冬物コート・ダウン・マフラーなど防寒装備"

        if "雨が多い" in tags:
            outfit += "＋折りたたみ傘・防水の上着"
        elif "寒暖差大" in tags and "重ね着" not in outfit:
            outfit += "（朝晩の冷え対策に重ね着）"

        records.append({
            "month": idx,
            "tmax": tmax,
            "tmin": tmin,
            "rain_mm": rain_mm,
            "rain_days": rain_days,
            "humidity": hum,
            "sun_h": sun_h,
            "uvi": uvi,
            "score": score,
            "label": label,
            "tags": tags[:3],  # 表示は重要度上位3つ
            "all_tags": tags,
            "outfit": outfit,
            "is_rainy": is_rainy,
            "is_dry": is_dry,
            "city_best": False,
        })

    # 熱帯など全体スコアが低めになりやすい都市向けに「この街のベスト上位3か月」フラグ付与
    top3 = sorted(records, key=lambda r: r["score"], reverse=True)[:3]
    for r in top3:
        r["city_best"] = True

    # 連続する月の自動要約生成
    best_months = [r["month"] for r in records if r["label"] in ("ベスト", "快適") or r["city_best"]]
    caution_months = [r["month"] for r in records if r["label"] == "注意"]

    def _fmt_ranges(ms: List[int]) -> str:
        if not ms:
            return "特になし"
        ms = sorted(set(ms))
        ranges = []
        start = prev = ms[0]
        for m in ms[1:]:
            if m == prev + 1:
                prev = m
            else:
                ranges.append(f"{start}月" if start == prev else f"{start}〜{prev}月")
                start = prev = m
        ranges.append(f"{start}月" if start == prev else f"{start}〜{prev}月")
        return "・".join(ranges)

    # 季節別アドバイス（自動生成）
    auto_notes = []
    if is_south:
        auto_notes.append("日本と季節が逆になります。")
    if caution_months:
        sample_tags = []
        for m in caution_months:
            for t in records[m - 1]["tags"]:
                if t in TAG_ADVICE and t not in sample_tags:
                    sample_tags.append(t)
        tag_str = "・".join(sample_tags[:2]) if sample_tags else "気象条件の変化"
        advice_str = TAG_ADVICE.get(sample_tags[0], "") if sample_tags else ""
        auto_notes.append(f"{_fmt_ranges(caution_months)}は「{tag_str}」に注意。{advice_str}")
    if profile.get("highlight"):
        auto_notes.append(profile["highlight"])

    return {
        "zone": profile["zone"],
        "is_exact_data": slug in CITY_MONTHLY_CLIMATE,
        "months": records,
        "best_months_str": _fmt_ranges(best_months[:4] if len(best_months) > 5 else best_months),
        "caution_months_str": _fmt_ranges(caution_months),
        "summary_note": " ".join(auto_notes),
        "source": DATA_SOURCE_NOTE,
        "version": THRESHOLD_VERSION,
    }


def get_season_snapshot(city: dict, target_months: List[int]) -> dict:
    """特集ページ（GW=4〜5月、夏休み=7〜8月など）用に該当月の平均気温・降水日数・服装・評価を返す"""
    cal = evaluate_city_calendar(city)
    subset = [cal["months"][m - 1] for m in target_months]
    avg_max = round(sum(r["tmax"] for r in subset) / len(subset))
    avg_min = round(sum(r["tmin"] for r in subset) / len(subset))
    avg_rain_days = round(sum(r["rain_days"] for r in subset) / len(subset))
    avg_score = round(sum(r["score"] for r in subset) / len(subset))
    rep = subset[0]
    tags = []
    for r in subset:
        for t in r["tags"]:
            if t not in tags:
                tags.append(t)
    return {
        "temp_str": f"{avg_min}〜{avg_max}℃",
        "rain_days_str": f"月{avg_rain_days}日",
        "outfit": rep["outfit"],
        "score": avg_score,
        "label": "ベスト" if avg_score >= 80 else ("快適" if avg_score >= 65 else ("標準" if avg_score >= 45 else "注意")),
        "tags": tags[:2],
    }


def run_calendar_qa(cities: List[dict], feature_pages: List[dict]) -> List[str]:
    """公開前チェック：異気候帯のラベル重複・特集ページとの矛盾を検出"""
    warnings = []
    exact_patterns = {}
    for c in cities:
        cal = evaluate_city_calendar(c)
        if not cal["is_exact_data"]:
            continue
        sig = tuple((m["label"], tuple(m["tags"])) for m in cal["months"])
        if sig in exact_patterns and exact_patterns[sig][1] != cal["zone"]:
            warnings.append(f"[重複警告] {c['slug']} と {exact_patterns[sig][0]} の12か月ラベルが完全一致しています")
        exact_patterns[sig] = (c["slug"], cal["zone"])

    city_map = {c["slug"]: c for c in cities}
    for feat in feature_pages:
        if "ベストシーズン" in feat.get("title", "") and feat.get("target_months"):
            for slug in feat.get("cities", []):
                if slug in city_map:
                    snap = get_season_snapshot(city_map[slug], feat["target_months"])
                    if snap["label"] == "注意":
                        warnings.append(
                            f"[矛盾警告] 特集『{feat['slug']}』で「ベストシーズン」表記ですが、{slug} の該当月は「注意（{'・'.join(snap['tags'])}）」です"
                        )
    return warnings
