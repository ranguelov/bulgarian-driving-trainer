#!/usr/bin/env python3
"""
Сдвигает нумерацию SVG-файлов ответов для вопросов типа «выбери знак»:
  img_2.svg → img_1.svg
  img_3.svg → img_2.svg
  img_4.svg → img_3.svg
  img_5.svg → img_4.svg

Затем удаляет старые img_1.png-заглушки и обновляет questions.js.

Запуск:
  python3 fix_image_numbering_svg.py
"""
import os, re, glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR    = os.path.join(SCRIPT_DIR, 'images', 'questions')
QJS_PATH   = os.path.join(SCRIPT_DIR, 'questions.js')

# ── Найти вопросы где есть img_1.png И img_2.svg (нужен сдвиг) ───────────────
img1_pngs = sorted(glob.glob(os.path.join(IMG_DIR, 't*_question_*_img_1.png')))

fixed = skipped = 0
for f1_png in img1_pngs:
    base  = re.sub(r'_img_1\.png$', '', f1_png)
    f2svg = base + '_img_2.svg'

    if not os.path.exists(f2svg):
        skipped += 1
        continue                      # вопрос с реальным фото-вопросом — не трогаем

    f3svg  = base + '_img_3.svg'
    f4svg  = base + '_img_4.svg'
    f5svg  = base + '_img_5.svg'
    f1svg  = base + '_img_1.svg'
    f2new  = base + '_img_2.svg'
    f3new  = base + '_img_3.svg'
    f4new  = base + '_img_4.svg'

    # Сдвиг (порядок важен — сначала последний файл)
    if os.path.exists(f5svg): os.rename(f5svg, f4new)
    if os.path.exists(f4svg): os.rename(f4svg, f3new)
    if os.path.exists(f3svg): os.rename(f3svg, f2new)
    os.rename(f2svg, f1svg)          # img_2.svg → img_1.svg

    # Удалить старую PNG-заглушку
    os.remove(f1_png)

    fixed += 1
    print(f'  ✓  {os.path.basename(base)}')

print(f'\nФайлы: {fixed} сдвинуто, {skipped} пропущено')

# ── Обновить questions.js: img_1.png → img_1.svg для исправленных ────────────
content = open(QJS_PATH, 'r', encoding='utf-8').read()
changed = 0

def replace_png_to_svg(m):
    global changed
    ref     = m.group(1)
    svg_ref = ref[:-4] + '.svg'
    if os.path.exists(os.path.join(IMG_DIR, svg_ref)):
        changed += 1
        return f'"{svg_ref}"'
    return m.group(0)

content = re.sub(
    r'"([^"]*t[23]_question[^"]*_img_1\.png)"',
    replace_png_to_svg,
    content
)
open(QJS_PATH, 'w', encoding='utf-8').write(content)
print(f'questions.js: {changed} ссылок img_1.png → img_1.svg')

# ── Проверка ──────────────────────────────────────────────────────────────────
all_refs = re.findall(r'"([^"]*t[23]_question[^"]*\.(svg|png))"', content)
missing  = [(r, e) for r, e in all_refs if not os.path.exists(os.path.join(IMG_DIR, r))]
print(f'Отсутствующих файлов: {len(missing)}')
if missing:
    for r, _ in missing[:10]:
        print(f'  ! {r}')

print('\n✓ Готово! Запусти: npx wrangler deploy')
