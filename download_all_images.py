#!/usr/bin/env python3
"""
Обновить все изображения из Figma (Тема 2 + Тема 3).

Скачивает 292 изображения (185 для T2 + 107 для T3) в images/questions/.

Использование:
  FIGMA_TOKEN=ваш_токен python3 download_all_images.py

Получить токен:
  Figma → верхнее меню → Account Settings → Personal access tokens → Generate new token
"""
import os, sys, json, urllib.request, time

TOKEN    = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
OUT_DIR  = os.path.join(os.path.dirname(__file__), 'images', 'questions')

# ─────────────────────────────────────────────────────────────
# Тема 3 (T3)
# ─────────────────────────────────────────────────────────────

T3_NODES_Q = {
    '4:5236': 't3_question_1_1_img_1.png',
    '4:5239': 't3_question_2_1_img_1.png',
    '4:5242': 't3_question_3_1_img_1.png',
    '4:5244': 't3_question_4_1_img_1.png',
    '4:5246': 't3_question_4_2_img_1.png',
    '4:5248': 't3_question_4_3_img_1.png',
    '4:5250': 't3_question_6_1_img_1.png',
    '4:5252': 't3_question_6_2_img_1.png',
    '4:5254': 't3_question_6_3_img_1.png',
    '4:5256': 't3_question_9_1_img_1.png',
    '4:5266': 't3_question_10_1_img_1.png',
    '4:5273': 't3_question_11_1_img_1.png',
    '4:5285': 't3_question_13_1_img_1.png',
    '4:5287': 't3_question_13_2_img_1.png',
    '4:5289': 't3_question_13_3_img_1.png',
    '4:5291': 't3_question_13_4_img_1.png',
    '4:5293': 't3_question_14_1_img_1.png',
    '4:5296': 't3_question_14_2_img_1.png',
    '4:5298': 't3_question_14_3_img_1.png',
    '4:5300': 't3_question_17_1_img_1.png',
    '4:5302': 't3_question_17_2_img_1.png',
    '4:5304': 't3_question_20_1_img_1.png',
    '4:5306': 't3_question_21_1_img_1.png',
    '4:5309': 't3_question_21_2_img_1.png',
    '4:5312': 't3_question_21_3_img_1.png',
    '4:5314': 't3_question_22_1_img_1.png',
    '4:5316': 't3_question_23_1_img_1.png',
    '4:5318': 't3_question_23_2_img_1.png',
    '4:5320': 't3_question_24_1_img_1.png',
    '4:5322': 't3_question_25_1_img_1.png',
    '4:5324': 't3_question_26_1_img_1.png',
    '4:5326': 't3_question_27_1_img_1.png',
    '4:5328': 't3_question_28_1_img_1.png',
    '4:5330': 't3_question_29_1_img_1.png',
    '4:5332': 't3_question_30_1_img_1.png',
    '4:5338': 't3_question_32_1_img_1.png',
    '4:5340': 't3_question_54_1_img_1.png',
    '4:5357': 't3_question_58_1_img_1.png',
    '4:5360': 't3_question_59_1_img_1.png',
    '4:5363': 't3_question_60_1_img_1.png',
    '4:5366': 't3_question_61_1_img_1.png',
    '4:5369': 't3_question_62_1_img_1.png',
    '4:5372': 't3_question_63_1_img_1.png',
    '4:5375': 't3_question_64_1_img_1.png',
    '4:5378': 't3_question_65_1_img_1.png',
}

T3_NODES_A = {
    '4:4953': 't3_question_1_2_img_2.png',
    '4:5005': 't3_question_1_2_img_3.png',
    '4:5147': 't3_question_1_2_img_4.png',
    '4:5181': 't3_question_1_2_img_5.png',
    '4:4956': 't3_question_5_1_img_2.png',
    '4:5002': 't3_question_5_1_img_3.png',
    '4:5050': 't3_question_5_1_img_4.png',
    '4:5059': 't3_question_5_1_img_5.png',
    '4:4959': 't3_question_5_2_img_2.png',
    '4:5011': 't3_question_5_2_img_3.png',
    '4:5056': 't3_question_5_2_img_4.png',
    '4:5065': 't3_question_5_2_img_5.png',
    '4:4963': 't3_question_5_3_img_2.png',
    '4:5016': 't3_question_5_3_img_3.png',
    '4:5062': 't3_question_5_3_img_4.png',
    '4:5071': 't3_question_5_3_img_5.png',
    '4:4967': 't3_question_5_4_img_2.png',
    '4:5019': 't3_question_5_4_img_3.png',
    '4:5068': 't3_question_5_4_img_4.png',
    '4:5079': 't3_question_5_4_img_5.png',
    '4:4970': 't3_question_7_2_img_2.png',
    '4:5024': 't3_question_7_2_img_3.png',
    '4:5074': 't3_question_7_2_img_4.png',
    '4:5085': 't3_question_7_2_img_5.png',
    '4:4973': 't3_question_7_3_img_2.png',
    '4:5027': 't3_question_7_3_img_3.png',
    '4:5082': 't3_question_7_3_img_4.png',
    '4:5093': 't3_question_7_3_img_5.png',
    '4:4976': 't3_question_7_4_img_2.png',
    '4:5030': 't3_question_7_4_img_3.png',
    '4:5089': 't3_question_7_4_img_4.png',
    '4:5108': 't3_question_7_4_img_5.png',
    '4:4979': 't3_question_9_2_img_2.png',
    '4:5033': 't3_question_9_2_img_3.png',
    '4:5097': 't3_question_9_2_img_4.png',
    '4:5123': 't3_question_9_2_img_5.png',
    '4:4989': 't3_question_10_2_img_2.png',
    '4:5040': 't3_question_10_2_img_3.png',
    '4:5111': 't3_question_10_2_img_4.png',
    '4:5135': 't3_question_10_2_img_5.png',
    '4:4996': 't3_question_30_2_img_2.png',
    '4:5053': 't3_question_30_2_img_3.png',
    '4:5164': 't3_question_30_2_img_4.png',
    '4:5187': 't3_question_30_2_img_5.png',
    '4:5193': 't3_question_37_1_img_2.png',
    '4:5199': 't3_question_37_1_img_3.png',
    '4:5208': 't3_question_37_1_img_4.png',
    '4:5202': 't3_question_37_2_img_2.png',
    '4:5210': 't3_question_37_2_img_3.png',
    '4:5195': 't3_question_37_2_img_4.png',
    '4:5212': 't3_question_37_3_img_2.png',
    '4:5205': 't3_question_37_3_img_3.png',
    '4:5197': 't3_question_37_3_img_4.png',
    '4:5214': 't3_question_38_1_img_2.png',
    '4:5220': 't3_question_38_1_img_3.png',
    '4:5229': 't3_question_38_1_img_4.png',
    '4:5231': 't3_question_38_2_img_2.png',
    '4:5223': 't3_question_38_2_img_3.png',
    '4:5216': 't3_question_38_2_img_4.png',
    '4:5226': 't3_question_38_3_img_2.png',
    '4:5218': 't3_question_38_3_img_3.png',
    '4:5233': 't3_question_38_3_img_4.png',
}

# ─────────────────────────────────────────────────────────────
# Тема 2 (T2)
# ─────────────────────────────────────────────────────────────

T2_NODES_Q = {
    '4:2911': 't2_question_1_1_img_1.png',
    '4:2920': 't2_question_4_1_img_1.png',
    '4:2950': 't2_question_4_2_img_1.png',
    '4:2952': 't2_question_4_3_img_1.png',
    '4:3010': 't2_question_4_4_img_1.png',
    '4:3043': 't2_question_4_5_img_1.png',
    '4:3055': 't2_question_4_6_img_1.png',
    '4:3062': 't2_question_4_8_img_1.png',
    '4:3068': 't2_question_4_7_img_1.png',
    '4:3076': 't2_question_5_1_img_1.png',
    '4:3083': 't2_question_5_2_img_1.png',
    '4:3091': 't2_question_6_1_img_1.png',
    '4:3097': 't2_question_6_2_img_1.png',
    '4:3104': 't2_question_11_1_img_1.png',
    '4:3136': 't2_question_12_1_img_1.png',
    '4:3145': 't2_question_12_2_img_1.png',
    '4:3154': 't2_question_12_3_img_1.png',
    '4:3163': 't2_question_14_1_img_1.png',
    '4:3169': 't2_question_17_1_img_1.png',
    '4:3179': 't2_question_17_2_img_1.png',
    '4:3189': 't2_question_17_3_img_1.png',
    '4:3191': 't2_question_23_2_img_1.png',
    '4:3197': 't2_question_35_1_img_1.png',
    '4:3204': 't2_question_23_3_img_1.png',
    '4:3210': 't2_question_18_1_img_1.png',
    '4:3216': 't2_question_36_1_img_1.png',
    '4:3222': 't2_question_25_1_img_1.png',
    '4:3228': 't2_question_26_1_img_1.png',
    '4:3234': 't2_question_38_1_img_1.png',
    '4:3277': 't2_question_18_2_img_1.png',
    '4:3279': 't2_question_29_1_img_1.png',
    '4:3281': 't2_question_39_1_img_1.png',
    '4:3307': 't2_question_30_1_img_1.png',
    '4:3309': 't2_question_19_1_img_1.png',
    '4:3317': 't2_question_40_1_img_1.png',
    '4:3319': 't2_question_32_1_img_1.png',
    '4:3325': 't2_question_40_2_img_1.png',
    '4:3327': 't2_question_40_3_img_1.png',
    '4:3329': 't2_question_34_1_img_1.png',
    '4:3340': 't2_question_19_2_img_1.png',
    '4:3348': 't2_question_20_1_img_1.png',
    '4:3356': 't2_question_21_1_img_1.png',
    '4:3362': 't2_question_23_1_img_1.png',
}

T2_NODES_A = {
    '4:3418': 't2_question_1_2_img_2.png',
    '4:3720': 't2_question_1_2_img_3.png',
    '4:4097': 't2_question_1_2_img_4.png',
    '4:4403': 't2_question_1_2_img_5.png',
    '4:3427': 't2_question_2_1_img_2.png',
    '4:3696': 't2_question_2_1_img_3.png',
    '4:3727': 't2_question_2_1_img_4.png',
    '4:4064': 't2_question_2_1_img_5.png',
    '4:3437': 't2_question_3_1_img_2.png',
    '4:3763': 't2_question_3_1_img_3.png',
    '4:4106': 't2_question_3_1_img_4.png',
    '4:3686': 't2_question_3_2_img_2.png',
    '4:4056': 't2_question_3_2_img_3.png',
    '4:4395': 't2_question_3_2_img_4.png',
    '4:3445': 't2_question_7_1_img_2.png',
    '4:3842': 't2_question_7_1_img_3.png',
    '4:4169': 't2_question_7_1_img_4.png',
    '4:4588': 't2_question_7_1_img_5.png',
    '4:3453': 't2_question_7_2_img_2.png',
    '4:3848': 't2_question_7_2_img_3.png',
    '4:4175': 't2_question_7_2_img_4.png',
    '4:4595': 't2_question_7_2_img_5.png',
    '4:3461': 't2_question_7_3_img_2.png',
    '4:3854': 't2_question_7_3_img_3.png',
    '4:4185': 't2_question_7_3_img_4.png',
    '4:4607': 't2_question_7_3_img_5.png',
    '4:3468': 't2_question_7_4_img_2.png',
    '4:3861': 't2_question_7_4_img_3.png',
    '4:4218': 't2_question_7_4_img_4.png',
    '4:4617': 't2_question_7_4_img_5.png',
    '4:3474': 't2_question_11_2_img_2.png',
    '4:3871': 't2_question_11_2_img_3.png',
    '4:4230': 't2_question_11_2_img_4.png',
    '4:4626': 't2_question_11_2_img_5.png',
    '4:3507': 't2_question_13_1_img_2.png',
    '4:3880': 't2_question_13_1_img_3.png',
    '4:4239': 't2_question_13_1_img_4.png',
    '4:4640': 't2_question_13_1_img_5.png',
    '4:3516': 't2_question_13_2_img_2.png',
    '4:3894': 't2_question_13_2_img_3.png',
    '4:4283': 't2_question_13_2_img_4.png',
    '4:4673': 't2_question_13_2_img_5.png',
    '4:3525': 't2_question_13_3_img_2.png',
    '4:3912': 't2_question_13_3_img_3.png',
    '4:4292': 't2_question_13_3_img_4.png',
    '4:4695': 't2_question_13_3_img_5.png',
    '4:3534': 't2_question_13_4_img_2.png',
    '4:3903': 't2_question_13_4_img_3.png',
    '4:4261': 't2_question_13_4_img_4.png',
    '4:4632': 't2_question_13_4_img_5.png',
    '4:3543': 't2_question_13_5_img_2.png',
    '4:3945': 't2_question_13_5_img_3.png',
    '4:4306': 't2_question_13_5_img_4.png',
    '4:4719': 't2_question_13_5_img_5.png',
    '4:3552': 't2_question_15_1_img_2.png',
    '4:3954': 't2_question_15_1_img_3.png',
    '4:4314': 't2_question_15_1_img_4.png',
    '4:4752': 't2_question_15_1_img_5.png',
    '4:3560': 't2_question_15_2_img_2.png',
    '4:3962': 't2_question_15_2_img_3.png',
    '4:4337': 't2_question_15_2_img_4.png',
    '4:4761': 't2_question_15_2_img_5.png',
    '4:3568': 't2_question_16_1_img_2.png',
    '4:3988': 't2_question_16_1_img_3.png',
    '4:4344': 't2_question_16_1_img_4.png',
    '4:4770': 't2_question_16_1_img_5.png',
    '4:3578': 't2_question_22_1_img_2.png',
    '4:3970': 't2_question_22_1_img_3.png',
    '4:4321': 't2_question_22_1_img_4.png',
    '4:4733': 't2_question_22_1_img_5.png',
    '4:3587': 't2_question_22_2_img_2.png',
    '4:3979': 't2_question_22_2_img_3.png',
    '4:4329': 't2_question_22_2_img_4.png',
    '4:4742': 't2_question_22_2_img_5.png',
    '4:3596': 't2_question_24_1_img_2.png',
    '4:3994': 't2_question_24_1_img_3.png',
    '4:4350': 't2_question_24_1_img_4.png',
    '4:4802': 't2_question_24_1_img_5.png',
    '4:3602': 't2_question_24_2_img_2.png',
    '4:4000': 't2_question_24_2_img_3.png',
    '4:4356': 't2_question_24_2_img_4.png',
    '4:4808': 't2_question_24_2_img_5.png',
    '4:3608': 't2_question_24_3_img_2.png',
    '4:4006': 't2_question_24_3_img_3.png',
    '4:4363': 't2_question_24_3_img_4.png',
    '4:4814': 't2_question_24_3_img_5.png',
    '4:3614': 't2_question_25_2_img_2.png',
    '4:4012': 't2_question_25_2_img_3.png',
    '4:4369': 't2_question_25_2_img_4.png',
    '4:4830': 't2_question_25_2_img_5.png',
    '4:3620': 't2_question_26_2_img_2.png',
    '4:4018': 't2_question_26_2_img_3.png',
    '4:4375': 't2_question_26_2_img_4.png',
    '4:4837': 't2_question_26_2_img_5.png',
    '4:3626': 't2_question_27_1_img_2.png',
    '4:4027': 't2_question_27_1_img_3.png',
    '4:4384': 't2_question_27_1_img_4.png',
    '4:4843': 't2_question_27_1_img_5.png',
    '4:3632': 't2_question_27_2_img_2.png',
    '4:4033': 't2_question_27_2_img_3.png',
    '4:4427': 't2_question_27_2_img_4.png',
    '4:4859': 't2_question_27_2_img_5.png',
    '4:3638': 't2_question_27_3_img_2.png',
    '4:4039': 't2_question_27_3_img_3.png',
    '4:4448': 't2_question_27_3_img_4.png',
    '4:4875': 't2_question_27_3_img_5.png',
    '4:3644': 't2_question_27_4_img_2.png',
    '4:4091': 't2_question_27_4_img_3.png',
    '4:4467': 't2_question_27_4_img_4.png',
    '4:4881': 't2_question_27_4_img_5.png',
    '4:3650': 't2_question_33_1_img_2.png',
    '4:4045': 't2_question_33_1_img_3.png',
    '4:4436': 't2_question_33_1_img_4.png',
    '4:4849': 't2_question_33_1_img_5.png',
    '4:3656': 't2_question_33_2_img_2.png',
    '4:4120': 't2_question_33_2_img_3.png',
    '4:4473': 't2_question_33_2_img_4.png',
    '4:4887': 't2_question_33_2_img_5.png',
    '4:3662': 't2_question_34_2_img_2.png',
    '4:4114': 't2_question_34_2_img_3.png',
    '4:4455': 't2_question_34_2_img_4.png',
    '4:4865': 't2_question_34_2_img_5.png',
    '4:3673': 't2_question_35_2_img_2.png',
    '4:4132': 't2_question_35_2_img_3.png',
    '4:4483': 't2_question_35_2_img_4.png',
    '4:4899': 't2_question_35_2_img_5.png',
    '4:3680': 't2_question_36_2_img_2.png',
    '4:4138': 't2_question_36_2_img_3.png',
    '4:4526': 't2_question_36_2_img_4.png',
    '4:4905': 't2_question_36_2_img_5.png',
    '4:3756': 't2_question_37_1_img_2.png',
    '4:4145': 't2_question_37_1_img_3.png',
    '4:4569': 't2_question_37_1_img_4.png',
    '4:4911': 't2_question_37_1_img_5.png',
    '4:3773': 't2_question_38_2_img_2.png',
    '4:4151': 't2_question_38_2_img_3.png',
    '4:4575': 't2_question_38_2_img_4.png',
    '4:4917': 't2_question_38_2_img_5.png',
    '4:3816': 't2_question_39_2_img_2.png',
    '4:4161': 't2_question_39_2_img_3.png',
    '4:4581': 't2_question_39_2_img_4.png',
    '4:4943': 't2_question_39_2_img_5.png',
}

# ─────────────────────────────────────────────────────────────
# Утилиты
# ─────────────────────────────────────────────────────────────

def fetch_render_urls(nodes: dict) -> dict:
    """Запросить render URL-ы у Figma API для пачки нод."""
    ids = ','.join(k.replace(':', '-') for k in nodes)
    url = (f'https://api.figma.com/v1/images/{FILE_KEY}'
           f'?ids={ids}&format=png&scale=2')
    req = urllib.request.Request(url, headers={'X-Figma-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    if resp.get('err'):
        raise RuntimeError(f'Figma error: {resp["err"]}')
    return resp.get('images', {})


def download_batch(nodes: dict, images: dict) -> tuple:
    ok = fail = 0
    for node_id, filename in nodes.items():
        figma_id = node_id.replace(':', '-')
        img_url  = images.get(figma_id) or images.get(node_id)
        if not img_url:
            print(f'  ✗  {filename}  — нет URL')
            fail += 1
            continue
        dst = os.path.join(OUT_DIR, filename)
        urllib.request.urlretrieve(img_url, dst)
        kb = os.path.getsize(dst) // 1024
        print(f'  ✓  {filename}  ({kb} KB)')
        ok += 1
    return ok, fail


def chunked(d: dict, size: int):
    items = list(d.items())
    for i in range(0, len(items), size):
        yield dict(items[i:i + size])


def process_group(label: str, nodes: dict):
    total_ok = total_fail = 0
    chunks = list(chunked(nodes, 50))
    print(f'\n{label} — {len(nodes)} нод, {len(chunks)} запрос(ов)…')
    for i, chunk in enumerate(chunks, 1):
        print(f'  Батч {i}/{len(chunks)} — {len(chunk)} нод…')
        try:
            images = fetch_render_urls(chunk)
            ok, fail = download_batch(chunk, images)
            total_ok += ok; total_fail += fail
        except Exception as e:
            print(f'  ОШИБКА: {e}')
            total_fail += len(chunk)
        if i < len(chunks):
            time.sleep(0.5)  # небольшая пауза между запросами
    return total_ok, total_fail


# ─────────────────────────────────────────────────────────────
# Основной скрипт
# ─────────────────────────────────────────────────────────────

def main():
    if not TOKEN or TOKEN == '':
        print('ОШИБКА: Не задан FIGMA_TOKEN')
        print('')
        print('Получить токен:')
        print('  Figma → верхнее меню (☰) → Account Settings')
        print('  → Personal access tokens → Generate new token')
        print('')
        print('Запустить скрипт:')
        print('  FIGMA_TOKEN=ваш_токен python3 download_all_images.py')
        sys.exit(1)

    try:
        TOKEN.encode('latin-1')
    except (UnicodeEncodeError, UnicodeDecodeError):
        print('ОШИБКА: Токен содержит не-ASCII символы. Проверьте токен.')
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    total_ok = total_fail = 0

    ok, fail = process_group('T3 вопросы (img_1)', T3_NODES_Q)
    total_ok += ok; total_fail += fail

    ok, fail = process_group('T3 ответы (img_2-5)', T3_NODES_A)
    total_ok += ok; total_fail += fail

    ok, fail = process_group('T2 вопросы (img_1)', T2_NODES_Q)
    total_ok += ok; total_fail += fail

    ok, fail = process_group('T2 ответы (img_2-5)', T2_NODES_A)
    total_ok += ok; total_fail += fail

    print(f'\n{"─"*50}')
    print(f'Результат: {total_ok} скачано, {total_fail} ошибок')
    print(f'Папка: {OUT_DIR}')

if __name__ == '__main__':
    main()
