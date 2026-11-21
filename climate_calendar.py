#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
都市別カレンダー データ・判定エンジン (climate_calendar.py)
- 相対基準（月平均比）＋絶対基準を併用し、熱帯の乾季・雨季や季節タグを自然に表示
- 全月に同じタグが張り付くのを防ぎ、「この街のベスト3か月（★）」と月別詳細を算出
- 特集ページ（秋休み・GW・夏休み等）の季節スナップショット＆整合性チェックを提供
- 【v1.3】他都市データの流用（フォールバック）を廃止。データ未整備の都市はカレンダーを出さない
"""

from typing import Dict, List

THRESHOLD_VERSION = "v1.3 (2026-11)"
DATA_SOURCE_NOTE = "WMO平年値(1991-2020)およびOpen-Meteo過去気象集計をもとに算出"

TAG_ADVICE = {
    "猛暑": "観光は早朝と夕方に寄せ、日中は屋内で休憩。こまめな水分補給と帽子が必須です。",
    "暑い": "通気性の良い半袖が基本。日差し対策のサングラスや帽子があると快適です。",
    "蒸し暑い": "速乾素材の服が快適。冷房の効いた屋内や移動車両向けに薄手の羽織りを携帯してください。",
    "寒い": "コートやジャケット、ニットなどしっかりした防寒着が必要です。",
    "厳寒": "ダウンコート・手袋・マフラー・防寒靴など真冬装備が必須です。",
    "雨が多い": "防水の上着や折りたたみ傘を常備。滑りにくい靴だと安心です。",
    "乾季・雨少なめ": "比較的雨が少なく外歩きしやすい時期。日焼け止めや保湿ケアを準備してください。",
    "寒暖差大": "朝晩と日中の気温差が大きいため、脱ぎ着しやすい重ね着が基本です。",
    "日照短い": "日照時間が非常に短いため、屋外観光は日中の明るい時間帯に集中させましょう。",
    "紫外線強い": "紫外線が強くなる時期のため、日焼け止め・サングラス・帽子が役立ちます。",
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
        "has_rail": False,
        "hazards": {6: ["猛暑"], 7: ["猛暑"], 8: ["猛暑"], 9: ["猛暑"]},
        "highlight": "2026年9月20日からUTC+0（GMT）の通年固定になり、日本との時差は-9時間で一年中変わりません（それ以前はUTC+1・ラマダン中のみUTC+0）。7〜8月は猛暑・乾燥、冬は雨や朝晩の冷え込みに注意。",
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
        "has_rail": True,
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
        "has_rail": True,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"]},
        "highlight": "11〜2月が比較的過ごしやすい乾季。4〜5月は暑さのピーク、6〜10月はスコールが多い雨季です。",
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
        "has_rail": False,
        "hazards": {},
        "highlight": "4〜10月が晴れが多く過ごしやすい乾季、11〜3月がスコールが増える雨季です（南半球ですが通年常夏です。鉄道はなく車・バイク移動が中心）。",
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
        "has_rail": True,
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
        "has_rail": True,
        "hazards": {},
        "highlight": "日本と季節が逆になります。12〜2月が夏、6〜8月が冬（東京ほど厳寒ではなく晴天が多い）です。",
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
        "has_rail": False,
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
        "has_rail": True,
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
        "has_rail": True,
        "hazards": {8: ["台風"]},
        "highlight": "4〜6月と9〜10月が爽やかなベストシーズン。7〜8月は雨と蒸し暑さ、12〜2月は氷点下の厳しい寒さになります。",
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
        "has_rail": True,
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
        "has_rail": False,
        "hazards": {},
        "highlight": "12〜1月は日照時間が極端に短く防寒必須。オーロラ観測は9〜4月、白夜と観光は6〜8月が中心です。",
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
        "has_rail": True,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"]},
        "highlight": "10〜11月と3〜4月が過ごしやすい時期。5月後半〜6月は梅雨、7〜9月は暑さと台風接近に注意が必要です。",
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
        "has_rail": True,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"]},
        "highlight": "10〜12月が晴天率が高く爽やかなベストシーズン。5〜9月は高温多湿で雨が多く、台風シーズンとも重なります。",
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
        "has_rail": True,
        "hazards": {},
        "highlight": "5〜6月と9〜10月が街歩きしやすい時期。7〜8月は暑くなる日もあり、10月最終日曜に冬時間へ切り替わります。",
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
        "has_rail": True,
        "hazards": {},
        "highlight": "4〜6月と9〜10月が観光のベストシーズン。7〜8月は雨が少なく日差しが強くなります。",
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
        "has_rail": True,
        "hazards": {},
        "highlight": "4〜6月と9〜10月がベストシーズン。冬はボスポラス海峡からの冷たい風と雨・雪で体感温度が下がります。",
        "months": [
            (9, 3, 105, 14, 77, 2.3, 2), (9, 3, 78, 12, 75, 3.1, 3), (12, 5, 71, 11, 74, 4.3, 4),
            (17, 9, 46, 8, 72, 6.0, 6), (22, 13, 36, 7, 72, 8.1, 8), (27, 17, 34, 6, 69, 9.8, 9),
            (29, 20, 39, 4, 68, 10.4, 9), (29, 20, 48, 5, 70, 9.4, 8), (25, 17, 63, 7, 72, 7.4, 6),
            (20, 13, 101, 10, 76, 5.1, 4), (15, 9, 109, 12, 77, 3.4, 2), (11, 5, 124, 15, 78, 2.2, 1),
        ],
    },
    "hanoi": {
        "zone": "subtropical_monsoon",
        "south": False,
        "has_rail": True,
        "hazards": {7: ["台風"], 8: ["台風"], 9: ["台風"]},
        "highlight": "10〜11月は暑さと雨が落ち着き街歩きしやすい秋シーズン。夏は蒸し暑く、冬は肌寒い日もあります。",
        "months": [
            (20, 14, 19, 8, 80, 2.3, 4), (21, 15, 26, 10, 83, 2.2, 5), (24, 18, 43, 14, 84, 2.5, 7),
            (28, 22, 90, 13, 84, 3.6, 9), (32, 25, 195, 14, 81, 5.8, 10), (34, 27, 240, 15, 80, 6.0, 11),
            (34, 27, 288, 15, 80, 6.3, 11), (33, 27, 343, 16, 82, 5.7, 10), (32, 25, 265, 13, 80, 5.5, 9),
            (29, 22, 131, 9, 77, 5.2, 7), (25, 19, 43, 7, 75, 4.7, 5), (22, 15, 23, 6, 75, 3.9, 4),
        ],
    },
    "kuala-lumpur": {
        "zone": "equatorial_wet",
        "south": False,
        "has_rail": True,
        "hazards": {},
        "highlight": "通年高温多湿。10〜11月や3〜4月はスコールが増える時期なので、雨具と冷房対策があると安心です。",
        "months": [
            (32, 23, 160, 14, 79, 6.5, 10), (33, 23, 148, 12, 78, 6.9, 11), (33, 24, 235, 15, 79, 6.7, 11),
            (33, 24, 260, 16, 80, 6.4, 11), (33, 24, 195, 14, 80, 6.3, 10), (33, 24, 130, 11, 79, 6.2, 10),
            (32, 23, 135, 12, 78, 6.4, 10), (32, 23, 150, 12, 78, 6.2, 10), (32, 23, 185, 14, 79, 5.8, 10),
            (32, 23, 265, 17, 81, 5.6, 9), (32, 23, 290, 18, 82, 5.4, 9), (32, 23, 225, 16, 81, 5.7, 9),
        ],
    },
    "shanghai": {
        "zone": "subtropical_east",
        "south": False,
        "has_rail": True,
        "hazards": {8: ["台風"]},
        "highlight": "9〜11月は暑さが和らぎ散策しやすい秋シーズン（10月初旬の国慶節連休は混雑に注意）。",
        "months": [
            (8, 1, 52, 8, 74, 4.1, 3), (10, 3, 59, 9, 73, 4.3, 4), (14, 6, 94, 11, 73, 4.5, 5),
            (20, 11, 98, 11, 73, 5.4, 7), (25, 16, 112, 11, 75, 6.0, 8), (28, 20, 179, 13, 80, 5.1, 9),
            (32, 24, 165, 12, 81, 6.7, 10), (32, 24, 158, 11, 81, 6.6, 9), (28, 20, 132, 10, 77, 5.5, 7),
            (23, 15, 61, 8, 74, 5.1, 5), (17, 9, 50, 8, 74, 4.5, 3), (11, 3, 41, 7, 74, 4.2, 2),
        ],
    },
    "boston": {
        "zone": "new_england_cool",
        "south": False,
        "has_rail": True,
        "hazards": {},
        "highlight": "秋は紅葉と涼しい空気が心地よく、11月は肌寒くなります。11月第1日曜に冬時間へ切り替わります。",
        "months": [
            (2, -6, 89, 11, 63, 5.3, 2), (4, -4, 86, 10, 62, 6.1, 3), (8, 0, 104, 11, 63, 6.7, 4),
            (14, 5, 95, 11, 63, 7.2, 6), (20, 10, 82, 11, 66, 8.0, 7), (25, 15, 92, 11, 68, 8.6, 8),
            (28, 18, 84, 10, 69, 8.8, 8), (27, 18, 88, 10, 71, 8.3, 7), (23, 14, 87, 9, 72, 7.3, 5),
            (16, 8, 97, 9, 70, 6.2, 3), (11, 3, 98, 10, 70, 4.6, 2), (5, -3, 99, 11, 66, 4.3, 1),
        ],
    },
    "prague": {
        "zone": "central_euro_cool",
        "south": False,
        "has_rail": True,
        "hazards": {},
        "highlight": "9〜10月は穏やかな秋、11月はコートが活躍する肌寒さ。10月最終日曜に冬時間へ切り替わります。",
        "months": [
            (1, -4, 24, 9, 82, 2.0, 1), (3, -3, 22, 8, 79, 2.9, 2), (8, 0, 29, 9, 74, 4.2, 3),
            (14, 4, 38, 9, 67, 5.8, 5), (19, 8, 67, 10, 68, 7.0, 6), (22, 11, 72, 11, 69, 7.3, 7),
            (24, 13, 74, 11, 68, 7.4, 7), (24, 13, 69, 10, 69, 6.9, 6), (19, 9, 45, 9, 74, 5.3, 4),
            (13, 5, 31, 8, 79, 3.7, 2), (6, 0, 32, 9, 84, 1.9, 1), (2, -3, 26, 10, 85, 1.5, 1),
        ],
    },
}


ALTITUDE_SLUGS = ("cusco", "uyuni", "la-paz", "quito", "bogota")


def has_exact_data(city: dict) -> bool:
    """この都市に専用の月別気候データがあるか（他都市の流用は行わない）"""
    return city.get("slug", "") in CITY_MONTHLY_CLIMATE


def evaluate_city_calendar(city: dict) -> dict:
    """都市の12か月カレンダーデータ（スコア・ラベル・理由タグ・服装・自動要約）を生成"""
    slug = city.get("slug", "")
    profile = CITY_MONTHLY_CLIMATE.get(slug)
    if profile is None:
        # 他都市のデータを流用しない。データ未整備の都市はカレンダーを出さない（呼び出し側で非表示/「データ準備中」）
        return None
    months_raw = profile["months"]
    avg_monthly_rain = max(1.0, sum(m[2] for m in months_raw) / 12.0)
    is_altitude = slug in ALTITUDE_SLUGS
    is_south = bool(profile.get("south", False))
    has_rail = bool(profile.get("has_rail", True))
    hazards = profile.get("hazards", {})

    records = []
    for idx, (tmax, tmin, rain_mm, rain_days, hum, sun_h, uvi) in enumerate(months_raw, start=1):
        tags: List[str] = []

        # 1. 気温タグ（全月に一律で付かないよう閾値を調整）
        if tmax >= 37:
            tags.append("猛暑")
        elif tmax >= 33 and hum >= 78:
            tags.append("蒸し暑い")
        elif tmax >= 33:
            tags.append("暑い")
        elif tmin < -10:
            tags.append("厳寒")
        elif tmax < 9:
            tags.append("寒い")

        # 2. 雨・乾季タグ（月平均比の相対基準＋絶対基準を併用）
        is_rainy = (rain_mm >= avg_monthly_rain * 1.35 and rain_days >= 10) or (rain_days >= 16)
        is_dry = (rain_mm < avg_monthly_rain * 0.5) or (rain_mm < 35)
        if is_rainy:
            tags.append("雨が多い")
        elif is_dry:
            tags.append("乾季・雨少なめ")

        # 3. 寒暖差・日照・UVI・災害・標高
        if (tmax - tmin) >= 15:
            tags.append("寒暖差大")
        if sun_h < 2.2:
            tags.append("日照短い")
        if uvi >= 10 and tmax >= 26:
            tags.append("紫外線強い")
        for hz in hazards.get(idx, []):
            tags.append(hz)
        if is_altitude:
            tags.append("高山病・寒暖差")

        # 快適スコア計算（100点減点方式）
        score = 100.0
        if tmax > 27:
            score -= (tmax - 27) * 5.5
        elif tmax < 17:
            score -= (17 - tmax) * 3.5
        score -= min(28.0, rain_days * 1.8)
        if hum > 78:
            score -= min(18.0, (hum - 78) * 1.4)
        if sun_h < 2.2:
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

        cool_note = "屋内や移動中の冷房" if has_rail else "冷房の効いた屋内や移動車両"
        if tmax >= 32:
            outfit = f"通気性の良い半袖・帽子・日焼け止め（{cool_note}対策に薄手の羽織り）"
        elif tmax >= 25:
            outfit = f"半袖・薄手のシャツ中心（{cool_note}や朝晩用にカーディガン）"
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
            "tags": tags[:2],
            "all_tags": tags,
            "outfit": outfit,
            "is_rainy": is_rainy,
            "is_dry": is_dry,
            "city_best": False,
        })

    top3 = sorted(records, key=lambda r: r["score"], reverse=True)[:3]
    for r in top3:
        r["city_best"] = True

    # ベスト月は「スコア上位」から選ぶ（旧版は1月から順に4か月を切り出していたため、1〜4月になりやすかった）
    ranked = sorted(records, key=lambda r: r["score"], reverse=True)
    best_candidates = [r for r in ranked if r["label"] in ("ベスト", "快適") or r["city_best"]]
    if len(best_candidates) > 5:
        best_candidates = best_candidates[:4]
    best_months = sorted(r["month"] for r in best_candidates)
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
        "best_months_str": _fmt_ranges(best_months),
        "caution_months_str": _fmt_ranges(caution_months),
        "summary_note": " ".join(auto_notes),
        "source": DATA_SOURCE_NOTE,
        "version": THRESHOLD_VERSION,
    }


def get_season_snapshot(city: dict, target_months: List[int]) -> dict:
    """特集ページ用に該当月の平均気温・降水日数・服装・ベスト月・評価を返す"""
    cal = evaluate_city_calendar(city)
    if cal is None:
        return None
    subset = [cal["months"][m - 1] for m in target_months]
    avg_max = round(sum(r["tmax"] for r in subset) / len(subset))
    avg_min = round(sum(r["tmin"] for r in subset) / len(subset))
    avg_rain_days = round(sum(r["rain_days"] for r in subset) / len(subset))
    avg_score = round(sum(r["score"] for r in subset) / len(subset))

    best_in_season = max(subset, key=lambda r: r["score"])
    rep = best_in_season if avg_score < 65 else subset[0]

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
        "best_month_str": f"{best_in_season['month']}月が狙い目",
        "tags": tags[:2],
    }


def _fmt_hours(h: float) -> str:
    sign = "+" if h > 0 else ""
    return f"{sign}{int(h)}" if float(h).is_integer() else f"{sign}{h:.1f}"


def season_tz_label(city: dict, months: List[int], ref_year: int = None) -> str:
    """特集の対象月に合わせた日本との時差ラベル。

    ビルド日の時差ではなく、対象月（1日・15日・28日）の時差を tzdata から計算する。
    期間中に夏時間・ラマダン等で時差が変わる場合は範囲で表示する。
    """
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    tz_name = city.get("timezone", "")
    if not tz_name:
        return "現地時刻参照"
    today = datetime.now(timezone.utc)
    diffs = set()
    try:
        jst, local = ZoneInfo("Asia/Tokyo"), ZoneInfo(tz_name)
        for m in months:
            year = ref_year or (today.year if m >= today.month else today.year + 1)
            for day in (1, 15, 28):
                dt = datetime(year, m, day, 12, tzinfo=timezone.utc)
                d = (dt.astimezone(local).utcoffset() - dt.astimezone(jst).utcoffset()).total_seconds() / 3600.0
                diffs.add(d)
    except Exception:
        return "現地時刻参照"
    if len(diffs) == 1:
        d = next(iter(diffs))
        return "時差なし（日本と同じ）" if d == 0 else f"{_fmt_hours(d)}時間"
    lo, hi = min(diffs), max(diffs)
    return f"{_fmt_hours(lo)}〜{_fmt_hours(hi)}時間（期間中に時刻切替あり）"


def run_calendar_qa(cities: List[dict], feature_pages: List[dict]) -> List[str]:
    """公開前チェック。"[ERROR]" が1件でもあればビルドを止める運用を想定。

    ERROR: データ構造の誤り／他都市データのコピー／緯度と矛盾する気温
    WARN : 気候帯が異なる都市で12か月ラベルが一致／特集の都市がデータ未整備／特集の見出しと評価の矛盾
    """
    msgs: List[str] = []
    city_map = {c["slug"]: c for c in cities}

    # tzdata が古いと時差を誤る。モロッコは2026-09-20からUTC+0固定（tzdata 2026c以降が必要）
    try:
        from datetime import datetime, timezone
        from zoneinfo import ZoneInfo
        for slug in ("marrakech", "casablanca", "fes"):
            tz_name = city_map.get(slug, {}).get("timezone")
            if not tz_name:
                continue
            dt = datetime(2026, 11, 15, 12, tzinfo=timezone.utc)
            diff = (dt.astimezone(ZoneInfo(tz_name)).utcoffset() - dt.astimezone(ZoneInfo("Asia/Tokyo")).utcoffset()).total_seconds() / 3600.0
            if diff != -9.0:
                msgs.append(f"[ERROR] {slug}: 2026年11月の日本との時差が{diff:+.0f}時間になっています。tzdata が古い可能性があります（2026c以降に更新してください）")
    except Exception as e:
        msgs.append(f"[WARN] タイムゾーンDBの検証をスキップしました: {e}")

    seen_numeric = {}
    seen_labels = {}
    for slug, prof in CITY_MONTHLY_CLIMATE.items():
        months = prof["months"]
        if len(months) != 12:
            msgs.append(f"[ERROR] {slug}: 月別データが12か月分ありません（{len(months)}件）")
            continue
        for i, (tmax, tmin, rain_mm, rain_days, hum, sun_h, uvi) in enumerate(months, start=1):
            if tmin > tmax:
                msgs.append(f"[ERROR] {slug} {i}月: 最低気温({tmin})が最高気温({tmax})を上回っています")
            if not (0 <= hum <= 100):
                msgs.append(f"[ERROR] {slug} {i}月: 湿度の値が不正です({hum})")
            if not (0 <= rain_days <= 31) or rain_mm < 0:
                msgs.append(f"[ERROR] {slug} {i}月: 降水量/降水日数の値が不正です")

        key = tuple(months)
        if key in seen_numeric:
            msgs.append(f"[ERROR] {slug} と {seen_numeric[key]} の月別データが完全に同一です（コピーの疑い）")
        seen_numeric[key] = slug

        city = city_map.get(slug)
        if city and slug not in ALTITUDE_SLUGS:
            lat = city.get("lat")
            if isinstance(lat, (int, float)) and abs(lat) < 20 and min(m[1] for m in months) < 10:
                msgs.append(f"[ERROR] {slug}（緯度{lat}）: 熱帯の都市なのに最低気温10℃未満の月があります。データを確認してください")

        cal = evaluate_city_calendar({"slug": slug})
        sig = tuple((m["label"], tuple(m["tags"])) for m in cal["months"])
        if sig in seen_labels and seen_labels[sig][1] != prof["zone"]:
            msgs.append(f"[WARN] {slug} と {seen_labels[sig][0]} の12か月ラベルが完全一致しています（気候帯が異なります）")
        seen_labels[sig] = (slug, prof["zone"])

    for feat in feature_pages:
        months = feat.get("target_months")
        slugs = [s for s in feat.get("cities", []) if s in city_map]
        missing = [s for s in slugs if s not in CITY_MONTHLY_CLIMATE]
        if missing:
            msgs.append(f"[WARN] 特集『{feat.get('slug')}』: {len(missing)}都市が気候データ未整備です（表示は「データ準備中」）: {', '.join(missing)}")
        title = feat.get("title", "")
        if ("快適" in title or "ベストシーズン" in title) and months:
            for slug in slugs:
                if slug in missing:
                    continue
                snap = get_season_snapshot(city_map[slug], months)
                if snap and snap["label"] == "注意":
                    msgs.append(f"[WARN] 特集『{feat.get('slug')}』の見出しは「{title}」ですが、{slug} の該当月は「注意（{'・'.join(snap['tags'])}）」です")
    return msgs
