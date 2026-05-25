#!/usr/bin/env python3
"""
Fix answer-image numbering for Themes 2 and 3.

The quiz expects answer images as img_1, img_2, img_3, img_4.
The t2/t3 download scripts saved them as img_2, img_3, img_4, img_5.
This script shifts each affected question: img_2→img_1, img_3→img_2, img_4→img_3, img_5→img_4.
The old watermarked img_1 is deleted.

Theme 1 is NOT touched — its download script already named files correctly (img_1 = first answer).

Run from anywhere:
  python3 fix_image_numbering.py
"""
import os, glob, re

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'questions')

if not os.path.isdir(DIR):
    print(f'ERROR: directory not found: {DIR}')
    exit(1)

total_renamed = 0
total_skipped = []

for prefix in ('t2', 't3'):
    img2_files = sorted(glob.glob(os.path.join(DIR, f'{prefix}_question_*_img_2.png')))
    renamed = 0
    print(f'\n── Theme {prefix[-1]} ({len(img2_files)} candidates) ──')

    for f2 in img2_files:
        base = re.sub(r'_img_2\.png$', '', f2)
        f1 = base + '_img_1.png'
        f3 = base + '_img_3.png'
        f4 = base + '_img_4.png'
        f5 = base + '_img_5.png'

        # Only shift if the old img_1 exists (watermarked placeholder to replace)
        if not os.path.exists(f1):
            total_skipped.append(os.path.basename(base))
            continue

        os.remove(f1)                                    # delete old img_1
        os.rename(f2, f1)                                # img_2 → img_1
        if os.path.exists(f3): os.rename(f3, f2)        # img_3 → img_2
        if os.path.exists(f4): os.rename(f4, f3)        # img_4 → img_3
        if os.path.exists(f5): os.rename(f5, f4)        # img_5 → img_4

        renamed += 1
        print(f'  ✓  {os.path.basename(base)}')

    print(f'  {renamed} questions fixed.')
    total_renamed += renamed

print(f'\n{"─"*50}')
print(f'Total: {total_renamed} questions fixed across t2 + t3.')
if total_skipped:
    print('Skipped (no old img_1):', total_skipped)
