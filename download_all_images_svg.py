#!/usr/bin/env python3
"""
Скачивает SVG-изображения из Figma для вопросов типа 2 и 3.
Фоновый белый прямоугольник вырезается перед сохранением.

Использование:
  export FIGMA_TOKEN=ваш_токен
  python3 download_all_images_svg.py
"""

import os, re, sys, time, requests

FIGMA_TOKEN = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY    = 'hKqLcn15skV1x2VFDUumnd'

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
IMG_DIR     = os.path.join(SCRIPT_DIR, 'images', 'questions')
QJS_PATH    = os.path.join(SCRIPT_DIR, 'questions.js')

os.makedirs(IMG_DIR, exist_ok=True)

# ── Вопросы-картинки T2 (img_1) ───────────────────────────────────────────────
T2_NODES_Q = {
    '4:3405': 't2_question_1_1_img_1.svg',
    '4:3410': 't2_question_2_2_img_1.svg',
    '4:3415': 't2_question_3_3_img_1.svg',
    '4:3420': 't2_question_7_5_img_1.svg',
    '4:3423': 't2_question_11_1_img_1.svg',
    '4:3425': 't2_question_11_3_img_1.svg',
    '4:3430': 't2_question_13_6_img_1.svg',
    '4:3432': 't2_question_13_7_img_1.svg',
    '4:3434': 't2_question_13_8_img_1.svg',
    '4:3436': 't2_question_15_3_img_1.svg',
    '4:3439': 't2_question_16_2_img_1.svg',
    '4:3441': 't2_question_16_3_img_1.svg',
    '4:3443': 't2_question_22_3_img_1.svg',
    '4:3446': 't2_question_24_4_img_1.svg',
    '4:3448': 't2_question_24_5_img_1.svg',
    '4:3450': 't2_question_25_1_img_1.svg',
    '4:3452': 't2_question_25_3_img_1.svg',
    '4:3454': 't2_question_26_1_img_1.svg',
    '4:3456': 't2_question_26_3_img_1.svg',
    '4:3458': 't2_question_27_5_img_1.svg',
    '4:3460': 't2_question_33_3_img_1.svg',
    '4:3462': 't2_question_34_1_img_1.svg',
    '4:3464': 't2_question_34_3_img_1.svg',
    '4:3466': 't2_question_35_1_img_1.svg',
    '4:3468': 't2_question_35_3_img_1.svg',
    '4:3470': 't2_question_36_1_img_1.svg',
    '4:3472': 't2_question_36_3_img_1.svg',
    '4:3474': 't2_question_37_2_img_1.svg',
    '4:3476': 't2_question_37_3_img_1.svg',
    '4:3478': 't2_question_38_1_img_1.svg',
    '4:3480': 't2_question_38_3_img_1.svg',
    '4:3482': 't2_question_39_1_img_1.svg',
    '4:3484': 't2_question_39_3_img_1.svg',
}

# ── Вопросы типа «выбери знак» T2: ответы img_1-4 ────────────────────────────
T2_NODES_A = {
    '4:3418': 't2_question_1_2_img_1.svg',
    '4:3720': 't2_question_1_2_img_2.svg',
    '4:4097': 't2_question_1_2_img_3.svg',
    '4:4403': 't2_question_1_2_img_4.svg',
    '4:3427': 't2_question_2_1_img_1.svg',
    '4:3696': 't2_question_2_1_img_2.svg',
    '4:3727': 't2_question_2_1_img_3.svg',
    '4:4064': 't2_question_2_1_img_4.svg',
    '4:3437': 't2_question_3_1_img_1.svg',
    '4:3763': 't2_question_3_1_img_2.svg',
    '4:4106': 't2_question_3_1_img_3.svg',
    '4:3686': 't2_question_3_2_img_1.svg',
    '4:4056': 't2_question_3_2_img_2.svg',
    '4:4395': 't2_question_3_2_img_3.svg',
    '4:3445': 't2_question_7_1_img_1.svg',
    '4:3842': 't2_question_7_1_img_2.svg',
    '4:4169': 't2_question_7_1_img_3.svg',
    '4:4588': 't2_question_7_1_img_4.svg',
    '4:3453': 't2_question_7_2_img_1.svg',
    '4:3848': 't2_question_7_2_img_2.svg',
    '4:4175': 't2_question_7_2_img_3.svg',
    '4:4595': 't2_question_7_2_img_4.svg',
    '4:3461': 't2_question_7_3_img_1.svg',
    '4:3854': 't2_question_7_3_img_2.svg',
    '4:4185': 't2_question_7_3_img_3.svg',
    '4:4607': 't2_question_7_3_img_4.svg',
    '4:3468': 't2_question_7_4_img_1.svg',
    '4:3861': 't2_question_7_4_img_2.svg',
    '4:4218': 't2_question_7_4_img_3.svg',
    '4:4617': 't2_question_7_4_img_4.svg',
    '4:3474': 't2_question_11_2_img_1.svg',
    '4:3871': 't2_question_11_2_img_2.svg',
    '4:4230': 't2_question_11_2_img_3.svg',
    '4:4626': 't2_question_11_2_img_4.svg',
    '4:3507': 't2_question_13_1_img_1.svg',
    '4:3880': 't2_question_13_1_img_2.svg',
    '4:4239': 't2_question_13_1_img_3.svg',
    '4:4640': 't2_question_13_1_img_4.svg',
    '4:3516': 't2_question_13_2_img_1.svg',
    '4:3894': 't2_question_13_2_img_2.svg',
    '4:4283': 't2_question_13_2_img_3.svg',
    '4:4673': 't2_question_13_2_img_4.svg',
    '4:3525': 't2_question_13_3_img_1.svg',
    '4:3912': 't2_question_13_3_img_2.svg',
    '4:4292': 't2_question_13_3_img_3.svg',
    '4:4695': 't2_question_13_3_img_4.svg',
    '4:3534': 't2_question_13_4_img_1.svg',
    '4:3903': 't2_question_13_4_img_2.svg',
    '4:4261': 't2_question_13_4_img_3.svg',
    '4:4632': 't2_question_13_4_img_4.svg',
    '4:3543': 't2_question_13_5_img_1.svg',
    '4:3945': 't2_question_13_5_img_2.svg',
    '4:4306': 't2_question_13_5_img_3.svg',
    '4:4719': 't2_question_13_5_img_4.svg',
    '4:3552': 't2_question_15_1_img_1.svg',
    '4:3954': 't2_question_15_1_img_2.svg',
    '4:4314': 't2_question_15_1_img_3.svg',
    '4:4752': 't2_question_15_1_img_4.svg',
    '4:3560': 't2_question_15_2_img_1.svg',
    '4:3962': 't2_question_15_2_img_2.svg',
    '4:4337': 't2_question_15_2_img_3.svg',
    '4:4761': 't2_question_15_2_img_4.svg',
    '4:3568': 't2_question_16_1_img_1.svg',
    '4:3988': 't2_question_16_1_img_2.svg',
    '4:4344': 't2_question_16_1_img_3.svg',
    '4:4770': 't2_question_16_1_img_4.svg',
    '4:3578': 't2_question_22_1_img_1.svg',
    '4:3970': 't2_question_22_1_img_2.svg',
    '4:4321': 't2_question_22_1_img_3.svg',
    '4:4733': 't2_question_22_1_img_4.svg',
    '4:3587': 't2_question_22_2_img_1.svg',
    '4:3979': 't2_question_22_2_img_2.svg',
    '4:4329': 't2_question_22_2_img_3.svg',
    '4:4742': 't2_question_22_2_img_4.svg',
    '4:3596': 't2_question_24_1_img_1.svg',
    '4:3994': 't2_question_24_1_img_2.svg',
    '4:4350': 't2_question_24_1_img_3.svg',
    '4:4802': 't2_question_24_1_img_4.svg',
    '4:3602': 't2_question_24_2_img_1.svg',
    '4:4000': 't2_question_24_2_img_2.svg',
    '4:4356': 't2_question_24_2_img_3.svg',
    '4:4808': 't2_question_24_2_img_4.svg',
    '4:3608': 't2_question_24_3_img_1.svg',
    '4:4006': 't2_question_24_3_img_2.svg',
    '4:4363': 't2_question_24_3_img_3.svg',
    '4:4814': 't2_question_24_3_img_4.svg',
    '4:3614': 't2_question_25_2_img_1.svg',
    '4:4012': 't2_question_25_2_img_2.svg',
    '4:4369': 't2_question_25_2_img_3.svg',
    '4:4830': 't2_question_25_2_img_4.svg',
    '4:3620': 't2_question_26_2_img_1.svg',
    '4:4018': 't2_question_26_2_img_2.svg',
    '4:4375': 't2_question_26_2_img_3.svg',
    '4:4837': 't2_question_26_2_img_4.svg',
    '4:3626': 't2_question_27_1_img_1.svg',
    '4:4027': 't2_question_27_1_img_2.svg',
    '4:4384': 't2_question_27_1_img_3.svg',
    '4:4843': 't2_question_27_1_img_4.svg',
    '4:3632': 't2_question_27_2_img_1.svg',
    '4:4033': 't2_question_27_2_img_2.svg',
    '4:4427': 't2_question_27_2_img_3.svg',
    '4:4859': 't2_question_27_2_img_4.svg',
    '4:3638': 't2_question_27_3_img_1.svg',
    '4:4039': 't2_question_27_3_img_2.svg',
    '4:4448': 't2_question_27_3_img_3.svg',
    '4:4875': 't2_question_27_3_img_4.svg',
    '4:3644': 't2_question_27_4_img_1.svg',
    '4:4091': 't2_question_27_4_img_2.svg',
    '4:4467': 't2_question_27_4_img_3.svg',
    '4:4881': 't2_question_27_4_img_4.svg',
    '4:3650': 't2_question_33_1_img_1.svg',
    '4:4045': 't2_question_33_1_img_2.svg',
    '4:4436': 't2_question_33_1_img_3.svg',
    '4:4849': 't2_question_33_1_img_4.svg',
    '4:3656': 't2_question_33_2_img_1.svg',
    '4:4120': 't2_question_33_2_img_2.svg',
    '4:4473': 't2_question_33_2_img_3.svg',
    '4:4887': 't2_question_33_2_img_4.svg',
    '4:3662': 't2_question_34_2_img_1.svg',
    '4:4114': 't2_question_34_2_img_2.svg',
    '4:4455': 't2_question_34_2_img_3.svg',
    '4:4865': 't2_question_34_2_img_4.svg',
    '4:3673': 't2_question_35_2_img_1.svg',
    '4:4132': 't2_question_35_2_img_2.svg',
    '4:4483': 't2_question_35_2_img_3.svg',
    '4:4899': 't2_question_35_2_img_4.svg',
    '4:3680': 't2_question_36_2_img_1.svg',
    '4:4138': 't2_question_36_2_img_2.svg',
    '4:4526': 't2_question_36_2_img_3.svg',
    '4:4905': 't2_question_36_2_img_4.svg',
    '4:3756': 't2_question_37_1_img_1.svg',
    '4:4145': 't2_question_37_1_img_2.svg',
    '4:4569': 't2_question_37_1_img_3.svg',
    '4:4911': 't2_question_37_1_img_4.svg',
    '4:3773': 't2_question_38_2_img_1.svg',
    '4:4151': 't2_question_38_2_img_2.svg',
    '4:4575': 't2_question_38_2_img_3.svg',
    '4:4917': 't2_question_38_2_img_4.svg',
    '4:3816': 't2_question_39_2_img_1.svg',
    '4:4161': 't2_question_39_2_img_2.svg',
    '4:4581': 't2_question_39_2_img_3.svg',
    '4:4943': 't2_question_39_2_img_4.svg',
}

# ── Вопросы-картинки T3 (img_1) ───────────────────────────────────────────────
T3_NODES_Q = {
    '4:4950': 't3_question_1_1_img_1.svg',
    '4:4982': 't3_question_5_5_img_1.svg',
    '4:4985': 't3_question_7_1_img_1.svg',
    '4:4986': 't3_question_7_5_img_1.svg',
    '4:4987': 't3_question_9_1_img_1.svg',
    '4:4988': 't3_question_9_3_img_1.svg',
    '4:4990': 't3_question_10_1_img_1.svg',
    '4:4991': 't3_question_10_3_img_1.svg',
    '4:4992': 't3_question_30_1_img_1.svg',
    '4:4993': 't3_question_30_3_img_1.svg',
}

# ── Вопросы типа «выбери знак» T3: ответы img_1-4 ────────────────────────────
T3_NODES_A = {
    '4:4953': 't3_question_1_2_img_1.svg',
    '4:5005': 't3_question_1_2_img_2.svg',
    '4:5147': 't3_question_1_2_img_3.svg',
    '4:5181': 't3_question_1_2_img_4.svg',
    '4:4956': 't3_question_5_1_img_1.svg',
    '4:5002': 't3_question_5_1_img_2.svg',
    '4:5050': 't3_question_5_1_img_3.svg',
    '4:5059': 't3_question_5_1_img_4.svg',
    '4:4959': 't3_question_5_2_img_1.svg',
    '4:5011': 't3_question_5_2_img_2.svg',
    '4:5056': 't3_question_5_2_img_3.svg',
    '4:5065': 't3_question_5_2_img_4.svg',
    '4:4963': 't3_question_5_3_img_1.svg',
    '4:5016': 't3_question_5_3_img_2.svg',
    '4:5062': 't3_question_5_3_img_3.svg',
    '4:5071': 't3_question_5_3_img_4.svg',
    '4:4967': 't3_question_5_4_img_1.svg',
    '4:5019': 't3_question_5_4_img_2.svg',
    '4:5068': 't3_question_5_4_img_3.svg',
    '4:5079': 't3_question_5_4_img_4.svg',
    '4:4970': 't3_question_7_2_img_1.svg',
    '4:5024': 't3_question_7_2_img_2.svg',
    '4:5074': 't3_question_7_2_img_3.svg',
    '4:5085': 't3_question_7_2_img_4.svg',
    '4:4973': 't3_question_7_3_img_1.svg',
    '4:5027': 't3_question_7_3_img_2.svg',
    '4:5082': 't3_question_7_3_img_3.svg',
    '4:5093': 't3_question_7_3_img_4.svg',
    '4:4976': 't3_question_7_4_img_1.svg',
    '4:5030': 't3_question_7_4_img_2.svg',
    '4:5089': 't3_question_7_4_img_3.svg',
    '4:5108': 't3_question_7_4_img_4.svg',
    '4:4979': 't3_question_9_2_img_1.svg',
    '4:5033': 't3_question_9_2_img_2.svg',
    '4:5097': 't3_question_9_2_img_3.svg',
    '4:5123': 't3_question_9_2_img_4.svg',
    '4:4989': 't3_question_10_2_img_1.svg',
    '4:5040': 't3_question_10_2_img_2.svg',
    '4:5111': 't3_question_10_2_img_3.svg',
    '4:5135': 't3_question_10_2_img_4.svg',
    '4:4996': 't3_question_30_2_img_1.svg',
    '4:5053': 't3_question_30_2_img_2.svg',
    '4:5164': 't3_question_30_2_img_3.svg',
    '4:5187': 't3_question_30_2_img_4.svg',
    '4:5193': 't3_question_37_1_img_1.svg',
    '4:5199': 't3_question_37_1_img_2.svg',
    '4:5208': 't3_question_37_1_img_3.svg',
    '4:5202': 't3_question_37_2_img_1.svg',
    '4:5210': 't3_question_37_2_img_2.svg',
    '4:5195': 't3_question_37_2_img_3.svg',
    '4:5212': 't3_question_37_3_img_1.svg',
    '4:5205': 't3_question_37_3_img_2.svg',
    '4:5197': 't3_question_37_3_img_3.svg',
    '4:5214': 't3_question_38_1_img_1.svg',
    '4:5220': 't3_question_38_1_img_2.svg',
    '4:5229': 't3_question_38_1_img_3.svg',
    '4:5231': 't3_question_38_2_img_1.svg',
    '4:5223': 't3_question_38_2_img_2.svg',
    '4:5216': 't3_question_38_2_img_3.svg',
    '4:5226': 't3_question_38_3_img_1.svg',
    '4:5218': 't3_question_38_3_img_2.svg',
    '4:5233': 't3_question_38_3_img_3.svg',
}


def strip_background(svg: str) -> str:
    """Удаляет белый фоновый прямоугольник/путь НЕ затрагивая defs/clipPath."""
    WHITE = r'(?:white|#fff|#ffffff|#FFF|#FFFFFF)'
    # Разбиваем SVG на часть до <defs> и часть с <defs> и далее
    defs_pos = re.search(r'<defs\b', svg, re.IGNORECASE)
    if defs_pos:
        before = svg[:defs_pos.start()]
        after  = svg[defs_pos.start():]
    else:
        before = svg
        after  = ''

    # Удаляем белый <path d="M0 0H..."> (fill сначала, потом d)
    before = re.sub(
        r'<path\b(?=[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\'])(?=[^>]*\bd\s*=\s*["\']M0\s+0H)[^>]*/?>',
        '', before, count=1, flags=re.IGNORECASE)
    # Удаляем белый <path d="M0 0H..."> (d сначала, потом fill)
    before = re.sub(
        r'<path\b(?=[^>]*\bd\s*=\s*["\']M0\s+0H)(?=[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\'])[^>]*/?>',
        '', before, count=1, flags=re.IGNORECASE)
    # Удаляем белый <rect fill="white">
    before = re.sub(
        r'<rect\b[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\'][^>]*/?>',
        '', before, count=1, flags=re.IGNORECASE)

    return before + after


def fetch_svg_urls(node_ids: list) -> dict:
    """Получает URL для скачивания SVG из Figma API."""
    ids_str = ','.join(node_ids)
    url = f'https://api.figma.com/v1/images/{FILE_KEY}'
    params = {'ids': ids_str, 'format': 'svg', 'svg_include_id': 'false',
              'svg_simplify_stroke': 'true'}
    headers = {'X-Figma-Token': FIGMA_TOKEN}
    r = requests.get(url, params=params, headers=headers, timeout=60)
    if r.status_code != 200:
        print(f'  [ОШИБКА] Figma API {r.status_code}: {r.text[:200]}')
        return {}
    data = r.json()
    if data.get('err'):
        print(f'  [ОШИБКА] Figma: {data["err"]}')
        return {}
    return data.get('images', {})


def download_nodes(nodes: dict, label: str):
    """Скачивает узлы батчами и сохраняет SVG-файлы."""
    node_ids = list(nodes.keys())
    total = len(node_ids)
    downloaded = errors = 0
    BATCH = 50

    for i in range(0, total, BATCH):
        batch_ids = node_ids[i:i+BATCH]
        print(f'  Батч {i//BATCH + 1}: запрашиваем {len(batch_ids)} узлов...')
        urls = fetch_svg_urls(batch_ids)
        if not urls:
            errors += len(batch_ids)
            continue

        for node_id in batch_ids:
            filename = nodes[node_id]
            url = urls.get(node_id)
            if not url:
                print(f'  [!] Нет URL для {node_id} ({filename})')
                errors += 1
                continue
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                svg = resp.text
                svg = strip_background(svg)
                out_path = os.path.join(IMG_DIR, filename)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(svg)
                downloaded += 1
            except Exception as e:
                print(f'  [!] Ошибка {filename}: {e}')
                errors += 1

        if i + BATCH < total:
            time.sleep(0.3)  # вежливая пауза

    print(f'  {label}: {downloaded} скачано, {errors} ошибок')
    return downloaded, errors


def update_questions_js():
    """Заменяет t2/t3 ссылки .png → .svg в questions.js."""
    with open(QJS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    original_svg_count = content.count('.svg')
    content = re.sub(r'(t[23]_question_[^"\']+)\.png', r'\1.svg', content)
    changed = content.count('.svg') - original_svg_count
    with open(QJS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Обновлено ссылок .png → .svg: {changed}')


def verify_references():
    """Проверяет что все SVG-файлы из questions.js существуют."""
    with open(QJS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    refs = re.findall(r'"(t[23]_question_[^"]+\.(?:svg|png))"', content)
    missing = [r for r in refs if not os.path.exists(os.path.join(IMG_DIR, r))]
    print(f'  Всего ссылок: {len(refs)}, отсутствует: {len(missing)}')
    if missing:
        for r in missing[:20]:
            print(f'    ! {r}')
    return len(missing) == 0


if __name__ == '__main__':
    if not FIGMA_TOKEN:
        print('ОШИБКА: задайте переменную FIGMA_TOKEN')
        sys.exit(1)

    print('=== Скачиваем T2 вопросы (картинки) ===')
    download_nodes(T2_NODES_Q, 'T2 вопросы')

    print('\n=== Скачиваем T2 ответы (знаки) ===')
    download_nodes(T2_NODES_A, 'T2 ответы')

    print('\n=== Скачиваем T3 вопросы (картинки) ===')
    download_nodes(T3_NODES_Q, 'T3 вопросы')

    print('\n=== Скачиваем T3 ответы (знаки) ===')
    download_nodes(T3_NODES_A, 'T3 ответы')

    print('\n=== Обновляем questions.js ===')
    update_questions_js()

    print('\n=== Проверка ссылок ===')
    ok = verify_references()

    if ok:
        print('\n✓ Всё готово! Запусти: npx wrangler deploy')
    else:
        print('\n✗ Есть отсутствующие файлы — проверь ошибки выше')
