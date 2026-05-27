#!/usr/bin/env python3
"""
Исправляет 13 групп T3 ответов, где Figma хранит растровые фото (не вектор).
Скачивает img_1 как PNG (не SVG), затем обновляет questions.js на .png для
всех img_1-4 этих групп.

Использование:
  export FIGMA_TOKEN=ваш_токен
  python3 fix_raster_answers.py
"""

import os, re, sys, time, requests

FIGMA_TOKEN = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY    = 'hKqLcn15skV1x2VFDUumnd'

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
IMG_DIR     = os.path.join(SCRIPT_DIR, 'images', 'questions')
QJS_PATH    = os.path.join(SCRIPT_DIR, 'questions.js')

# Только img_1 — остальные PNG уже существуют из старой загрузки
IMG1_NODES = {
    # t3_question_5_*
    '4:4956': 't3_question_5_1_img_1.png',
    '4:4959': 't3_question_5_2_img_1.png',
    '4:4963': 't3_question_5_3_img_1.png',
    '4:4967': 't3_question_5_4_img_1.png',
    # t3_question_7_*
    '4:4970': 't3_question_7_2_img_1.png',
    '4:4973': 't3_question_7_3_img_1.png',
    '4:4976': 't3_question_7_4_img_1.png',
    # t3_question_37_*
    '4:5193': 't3_question_37_1_img_1.png',
    '4:5202': 't3_question_37_2_img_1.png',
    '4:5212': 't3_question_37_3_img_1.png',
    # t3_question_38_*
    '4:5214': 't3_question_38_1_img_1.png',
    '4:5231': 't3_question_38_2_img_1.png',
    '4:5226': 't3_question_38_3_img_1.png',
}

# Группы, у которых ВСЕ img_1-4 должны быть PNG
RASTER_GROUPS = [
    't3_question_5_1', 't3_question_5_2', 't3_question_5_3', 't3_question_5_4',
    't3_question_7_2', 't3_question_7_3', 't3_question_7_4',
    't3_question_37_1', 't3_question_37_2', 't3_question_37_3',
    't3_question_38_1', 't3_question_38_2', 't3_question_38_3',
]


def fetch_png_urls(node_ids: list) -> dict:
    ids_str = ','.join(node_ids)
    url = f'https://api.figma.com/v1/images/{FILE_KEY}'
    params = {'ids': ids_str, 'format': 'png', 'scale': '2'}
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


def download_img1_as_png():
    print('=== Скачиваем img_1 как PNG для 13 групп ===')
    node_ids = list(IMG1_NODES.keys())
    urls = fetch_png_urls(node_ids)
    if not urls:
        return False

    downloaded = errors = 0
    for node_id, filename in IMG1_NODES.items():
        url = urls.get(node_id)
        if not url:
            print(f'  [!] Нет URL для {node_id} ({filename})')
            errors += 1
            continue
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            out_path = os.path.join(IMG_DIR, filename)
            with open(out_path, 'wb') as f:
                f.write(resp.content)
            size_kb = len(resp.content) // 1024
            print(f'  ✓ {filename} ({size_kb}KB)')
            downloaded += 1
        except Exception as e:
            print(f'  [!] Ошибка {filename}: {e}')
            errors += 1

    print(f'\n  Скачано: {downloaded}, ошибок: {errors}')
    return errors == 0


def revert_groups_to_png():
    print('\n=== Обновляем questions.js: SVG → PNG для растровых групп ===')
    with open(QJS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = 0
    for group in RASTER_GROUPS:
        for i in range(1, 5):
            old = f'"{group}_img_{i}.svg"'
            new = f'"{group}_img_{i}.png"'
            if old in content:
                content = content.replace(old, new)
                changed += 1

    with open(QJS_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Заменено ссылок: {changed}')


def verify():
    print('\n=== Проверка ===')
    with open(QJS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    ok = errors = 0
    for group in RASTER_GROUPS:
        for i in range(1, 5):
            png_name = f'{group}_img_{i}.png'
            png_path = os.path.join(IMG_DIR, png_name)
            ref = f'"{png_name}"' in content
            exists = os.path.exists(png_path)

            if ref and exists:
                ok += 1
            else:
                if not ref:
                    print(f'  ! Не найдена ссылка в questions.js: {png_name}')
                if not exists:
                    print(f'  ! Файл отсутствует: {png_name}')
                errors += 1

    # Also check no bad SVG refs remain
    for group in RASTER_GROUPS:
        for i in range(1, 5):
            if f'"{group}_img_{i}.svg"' in content:
                print(f'  ! SVG ссылка всё ещё в questions.js: {group}_img_{i}.svg')
                errors += 1

    print(f'  OK: {ok}, Ошибок: {errors}')
    return errors == 0


if __name__ == '__main__':
    if not FIGMA_TOKEN:
        print('ОШИБКА: задайте FIGMA_TOKEN')
        sys.exit(1)

    ok = download_img1_as_png()
    revert_groups_to_png()
    all_ok = verify()

    if all_ok:
        print('\n✓ Готово! Запусти: python3 test_images.py && npx wrangler deploy')
    else:
        print('\n✗ Есть проблемы — проверь вывод выше')
