#!/usr/bin/env python3
"""
Apply quality upgrade: move preview images to production.

Run ONLY after visual inspection of quality_preview.html!

This script:
  1. Copies PNG@2x files from images/questions_preview/ → images/questions/
     (overwriting existing PNG files)
  2. Copies SVG files from images/questions_preview/ → images/questions/
     (new files, old PNG remains as backup)
  3. Updates questions.js: changes .png → .svg references for vector nodes
  4. Prints a summary of all changes made

Usage:
  python3 apply_quality_upgrade.py [--dry-run]
"""
import os, sys, json, shutil, re

DRY_RUN = '--dry-run' in sys.argv

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
PREVIEW_DIR = os.path.join(BASE_DIR, 'images', 'questions_preview')
PROD_DIR    = os.path.join(BASE_DIR, 'images', 'questions')
CLS_FILE    = os.path.join(BASE_DIR, 'figma_node_classification.json')
QJS_FILE    = os.path.join(BASE_DIR, 'questions.js')

if DRY_RUN:
    print('DRY RUN MODE — no files will be changed\n')

# ── Load classification ───────────────────────────────────────────────────────

if not os.path.exists(CLS_FILE):
    print(f'ERROR: {CLS_FILE} not found.')
    print('Run download_figma_quality_upgrade.py first.')
    sys.exit(1)

with open(CLS_FILE) as f:
    cls = json.load(f)

vector_basenames = set(cls.get('vector', {}).values())
raster_basenames = set(cls.get('raster', {}).values())

print(f'Classification loaded: {len(vector_basenames)} vector, {len(raster_basenames)} raster\n')

# ── Step 1: copy PNG@2x files ─────────────────────────────────────────────────

png_copied = 0
png_missing = []

print('Step 1: Applying PNG@2x files...')
for basename in sorted(raster_basenames):
    src = os.path.join(PREVIEW_DIR, basename + '.png')
    dst = os.path.join(PROD_DIR, basename + '.png')
    if not os.path.exists(src):
        print(f'  SKIP (missing preview): {basename}.png')
        png_missing.append(basename)
        continue
    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst) if os.path.exists(dst) else 0
    print(f'  {basename}.png  ({dst_size//1024}KB → {src_size//1024}KB)')
    if not DRY_RUN:
        shutil.copy2(src, dst)
    png_copied += 1

print(f'  Copied {png_copied} PNG files.\n')

# ── Step 2: copy SVG files ────────────────────────────────────────────────────

svg_copied = 0
svg_missing = []

print('Step 2: Applying SVG files...')
for basename in sorted(vector_basenames):
    src = os.path.join(PREVIEW_DIR, basename + '.svg')
    dst = os.path.join(PROD_DIR, basename + '.svg')
    if not os.path.exists(src):
        print(f'  SKIP (missing preview): {basename}.svg')
        svg_missing.append(basename)
        continue
    src_size = os.path.getsize(src)
    old_png = os.path.join(PROD_DIR, basename + '.png')
    old_size = os.path.getsize(old_png) if os.path.exists(old_png) else 0
    print(f'  {basename}: PNG {old_size//1024}KB → SVG {src_size//1024}B')
    if not DRY_RUN:
        shutil.copy2(src, dst)
    svg_copied += 1

print(f'  Copied {svg_copied} SVG files.\n')

# ── Step 3: update questions.js ───────────────────────────────────────────────

print('Step 3: Updating questions.js references...')

if not vector_basenames:
    print('  No vector nodes → no changes needed in questions.js\n')
else:
    with open(QJS_FILE, encoding='utf-8') as f:
        content = f.read()

    changes = 0
    new_content = content
    for basename in sorted(vector_basenames):
        old_ref = f'{basename}.png'
        new_ref = f'{basename}.svg'
        if old_ref in new_content:
            if not DRY_RUN:
                new_content = new_content.replace(old_ref, new_ref)
            changes += 1
            print(f'  {old_ref} → {new_ref}')
        else:
            print(f'  NOT FOUND in questions.js: {old_ref}')

    if not DRY_RUN and changes > 0:
        with open(QJS_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'  questions.js updated ({changes} references changed).\n')
    else:
        print(f'  {"Would change" if DRY_RUN else "Changed"} {changes} references.\n')

# ── Summary ───────────────────────────────────────────────────────────────────

print('=' * 60)
print('SUMMARY')
print('=' * 60)
print(f'  PNG@2x applied:  {png_copied}')
print(f'  SVG applied:     {svg_copied}')
if png_missing:
    print(f'  PNG missing:     {len(png_missing)} — {png_missing}')
if svg_missing:
    print(f'  SVG missing:     {len(svg_missing)} — {svg_missing}')

if DRY_RUN:
    print('\nDry run complete. Remove --dry-run to apply changes.')
else:
    print('\nDone! Commit and deploy:')
    print('  git add images/questions/ questions.js')
    print('  git commit -m "Quality upgrade: SVG for vector signs, PNG@2x for raster"')
    print('  git push origin main && npx wrangler deploy')
