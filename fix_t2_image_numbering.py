#!/usr/bin/env python3
"""
Fix Theme 2 answer-image numbering.

The quiz expects answer images as img_1, img_2, img_3, img_4.
The download script saved them as img_2, img_3, img_4, img_5.
This script shifts each answer-image question: img_2→img_1, img_3→img_2, img_4→img_3, img_5→img_4.
The old watermarked img_1 is deleted.

Run from anywhere:
  python3 fix_t2_image_numbering.py
"""
import os, glob, re

DIR = os.path.join(os.path.dirname(__file__), 'images', 'questions')

img2_files = sorted(glob.glob(os.path.join(DIR, 't2_question_*_img_2.png')))

renamed, skipped = 0, []

for f2 in img2_files:
    base = re.sub(r'_img_2\.png$', '', f2)
    f1 = base + '_img_1.png'
    f3 = base + '_img_3.png'
    f4 = base + '_img_4.png'
    f5 = base + '_img_5.png'

    # Only shift if old img_1 already exists (watermarked placeholder to replace)
    if not os.path.exists(f1):
        skipped.append(os.path.basename(base))
        continue

    os.remove(f1)                                        # delete old img_1
    os.rename(f2, f1)                                    # img_2 → img_1
    if os.path.exists(f3): os.rename(f3, f2)            # img_3 → img_2
    if os.path.exists(f4): os.rename(f4, f3)            # img_4 → img_3
    if os.path.exists(f5): os.rename(f5, f4)            # img_5 → img_4

    renamed += 1
    print(f'  ✓  {os.path.basename(base)}')

print(f'\n{renamed} questions fixed.')
if skipped:
    print('Skipped (no old img_1 to replace):', skipped)
