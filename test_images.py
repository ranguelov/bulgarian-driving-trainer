#!/usr/bin/env python3
"""
Тесты для SVG-изображений и questions.js.

Проверяет:
  1. Все t2/t3 ссылки в questions.js ведут на существующие файлы
  2. Каждый SVG-файл не пуст и содержит валидный SVG
  3. Нет пустых <clipPath> (иначе знак не отображается)
  4. Нет белого фона в SVG (fill="white" на фоновом пути/rect)
  5. Нет дубликатов контента внутри одного вопроса
  6. Файлы с правильным именованием img_1-4 (не img_2-5) для ответов

Запуск:
  python3 test_images.py
"""

import os, re, sys, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR    = os.path.join(SCRIPT_DIR, 'images', 'questions')
QJS_PATH   = os.path.join(SCRIPT_DIR, 'questions.js')

PASS = '\033[92m✓\033[0m'
FAIL = '\033[91m✗\033[0m'
WARN = '\033[93m⚠\033[0m'

errors   = []
warnings = []
passed   = 0


def ok(msg):
    global passed
    passed += 1
    print(f'  {PASS} {msg}')


def fail(msg):
    errors.append(msg)
    print(f'  {FAIL} {msg}')


def warn(msg):
    warnings.append(msg)
    print(f'  {WARN} {msg}')


# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 1: Все ссылки questions.js существуют')
print('══════════════════════════════════════════════')

with open(QJS_PATH, 'r', encoding='utf-8') as f:
    qjs = f.read()

all_refs = re.findall(r'"(t[23]_question_[^"]+\.(?:svg|png))"', qjs)
missing_files = []
for ref in all_refs:
    path = os.path.join(IMG_DIR, ref)
    if not os.path.exists(path):
        missing_files.append(ref)

if missing_files:
    fail(f'{len(missing_files)} отсутствующих файлов из {len(all_refs)}:')
    for f in missing_files[:20]:
        print(f'    ! {f}')
    if len(missing_files) > 20:
        print(f'    ... и ещё {len(missing_files)-20}')
else:
    ok(f'Все {len(all_refs)} файлов существуют')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 2: SVG-файлы не пусты и содержат <svg>')
print('══════════════════════════════════════════════')

svg_files = glob.glob(os.path.join(IMG_DIR, 't[23]_question_*.svg'))
empty_svgs = []
invalid_svgs = []

for path in svg_files:
    size = os.path.getsize(path)
    if size == 0:
        empty_svgs.append(os.path.basename(path))
        continue
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    if '<svg' not in content.lower():
        invalid_svgs.append(os.path.basename(path))

if empty_svgs:
    fail(f'{len(empty_svgs)} пустых SVG-файлов:')
    for f in empty_svgs[:10]:
        print(f'    ! {f}')
else:
    ok(f'Нет пустых SVG-файлов ({len(svg_files)} проверено)')

if invalid_svgs:
    fail(f'{len(invalid_svgs)} файлов без тега <svg>:')
    for f in invalid_svgs[:10]:
        print(f'    ! {f}')
else:
    ok(f'Все SVG-файлы содержат корректный тег <svg>')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 3: Нет пустых <clipPath>')
print('══════════════════════════════════════════════')

empty_clip = []
for path in svg_files:
    if os.path.getsize(path) == 0:
        continue
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    # Пустой clipPath = <clipPath ...></clipPath> или <clipPath .../>
    if re.search(r'<clipPath\b[^>]*>\s*</clipPath>', content) or \
       re.search(r'<clipPath\b[^>]*/>', content):
        empty_clip.append(os.path.basename(path))

if empty_clip:
    fail(f'{len(empty_clip)} файлов с пустым clipPath (знак невидим!):')
    for f in empty_clip[:10]:
        print(f'    ! {f}')
else:
    ok(f'Нет пустых clipPath')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 4: Нет белого фонового прямоугольника')
print('══════════════════════════════════════════════')

WHITE = r'(?:white|#fff|#ffffff|#FFF|#FFFFFF)'
with_bg = []
for path in svg_files:
    if os.path.getsize(path) == 0:
        continue
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    # Ищем только ДО <defs> — после может быть легальный белый в clipPath
    defs_pos = re.search(r'<defs\b', content, re.IGNORECASE)
    before = content[:defs_pos.start()] if defs_pos else content

    has_white_path = bool(re.search(
        r'<path\b[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\'][^>]*\bd\s*=\s*["\']M0\s+0H',
        before, re.IGNORECASE))
    has_white_path2 = bool(re.search(
        r'<path\b[^>]*\bd\s*=\s*["\']M0\s+0H[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\']',
        before, re.IGNORECASE))
    has_white_rect = bool(re.search(
        r'<rect\b[^>]*\bfill\s*=\s*["\']' + WHITE + r'["\']',
        before, re.IGNORECASE))

    if has_white_path or has_white_path2 or has_white_rect:
        with_bg.append(os.path.basename(path))

if with_bg:
    fail(f'{len(with_bg)} файлов с белым фоном:')
    for f in with_bg[:10]:
        print(f'    ! {f}')
else:
    ok(f'Нет файлов с белым фоном')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 5: Нет дубликатов в ответах одного вопроса')
print('══════════════════════════════════════════════')

# Группируем файлы по вопросу (всё кроме _img_N)
from collections import defaultdict
by_question = defaultdict(dict)
for path in svg_files:
    name = os.path.basename(path)
    m = re.match(r'(t[23]_question_\d+_\d+)_img_(\d+)\.svg$', name)
    if m:
        q_key = m.group(1)
        img_num = int(m.group(2))
        by_question[q_key][img_num] = path

dup_questions = []
for q_key, files in by_question.items():
    contents = {}
    has_dup = False
    for num, path in sorted(files.items()):
        if os.path.getsize(path) == 0:
            continue
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read().strip()
        if content in contents.values():
            has_dup = True
            break
        contents[num] = content
    if has_dup:
        dup_questions.append(q_key)

if dup_questions:
    fail(f'{len(dup_questions)} вопросов с дублирующимися картинками ответов:')
    for q in dup_questions[:10]:
        print(f'    ! {q}')
else:
    ok(f'Нет дублирующихся ответов')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 6: Нет img_5 файлов (нумерация img_1-4)')
print('══════════════════════════════════════════════')

img5_files = glob.glob(os.path.join(IMG_DIR, 't[23]_question_*_img_5.svg'))
if img5_files:
    fail(f'{len(img5_files)} файлов с неправильным именем _img_5 (должно быть _img_4 макс.):')
    for f in img5_files[:10]:
        print(f'    ! {os.path.basename(f)}')
else:
    ok('Нет файлов с _img_5 — нумерация корректна')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 7: questions.js — корректное смешение PNG/SVG')
print('══════════════════════════════════════════════')

# Illustration images (single img, text answers) should be PNG
# Answer images (multiple imgs, choose-sign) should be SVG
# A problem: SVG answer file that is very large = likely embedded raster (wrong Figma node)
large_svgs = []
for path in svg_files:
    size = os.path.getsize(path)
    if size > 150_000:  # >150KB for an answer SVG sign is suspicious
        name = os.path.basename(path)
        # Only flag answer-type SVGs (those referenced as SVG in questions.js)
        if f'"{name}"' in qjs:
            large_svgs.append((name, size))

if large_svgs:
    fail(f'{len(large_svgs)} SVG-файлов ответов подозрительно велики (встроенный растр?):')
    for n, s in sorted(large_svgs, key=lambda x: -x[1])[:10]:
        print(f'    ! {n} ({s//1024} KB)')
else:
    ok('Все SVG-файлы ответов имеют разумный размер (нет встроенного растра)')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ТЕСТ 8: SVG ответов не содержат <pattern>/<image> (встроенный растр)')
print('══════════════════════════════════════════════')

raster_svgs = []
for path in svg_files:
    if os.path.getsize(path) == 0:
        continue
    name = os.path.basename(path)
    if f'"{name}"' not in qjs:
        continue  # not referenced
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    if re.search(r'<pattern\b|<image\b', content, re.IGNORECASE):
        raster_svgs.append(name)

if raster_svgs:
    fail(f'{len(raster_svgs)} SVG-файлов содержат встроенное растровое изображение:')
    for n in raster_svgs[:10]:
        print(f'    ! {n}')
else:
    ok('Все SVG-файлы ответов содержат только векторную графику')

# ─────────────────────────────────────────────────────────────────────────────
print('\n══════════════════════════════════════════════')
print(' ИТОГИ')
print('══════════════════════════════════════════════')
total_checks = passed + len(errors)
print(f'  Пройдено: {passed}/{total_checks}')
if warnings:
    print(f'  Предупреждений: {len(warnings)}')
if errors:
    print(f'  Ошибок: {len(errors)}')
    print('\n  Деплой не рекомендован — исправьте ошибки выше.')
    sys.exit(1)
else:
    print('\n  ✓ Все тесты пройдены — можно запускать: npx wrangler deploy')
