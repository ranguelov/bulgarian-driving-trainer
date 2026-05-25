#!/usr/bin/env python3
"""
Download updated Figma images for Bulgarian Driving Trainer.

Usage:
  1. Get your Figma Personal Access Token:
     Figma → Menu → Account Settings → Personal access tokens → Generate new token
  2. Run:
       FIGMA_TOKEN=your_token python3 download_figma_images.py
     Or edit the TOKEN line below.
"""
import os, sys, json, urllib.request

TOKEN   = os.environ.get('FIGMA_TOKEN', 'paste_your_token_here')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
OUT_DIR  = os.path.join(os.path.dirname(__file__), 'images', 'questions')

# Figma node-id → destination filename
NODES = {
    '4:2896': 't1_question_39_3_img_1.png',
    '4:2898': 't1_question_39_2_img_1.png',
    '4:2900': 't1_question_39_1_img_1.png',
    '4:2902': 't1_question_44_1_img_1.png',
    '4:2904': 't1_question_48_1_img_1.png',
    '4:2906': 't1_question_45_1_img_1.png',
    '4:2908': 't1_question_51_1_img_1.png',
    '4:3369': 't1_question_22_1_img_1.png',
    '4:3371': 't1_question_20_1_img_1.png',
    '4:3373': 't1_question_21_3_img_1.png',
    '4:3375': 't1_question_21_2_img_1.png',
    '4:3377': 't1_question_21_1_img_1.png',
    '4:3379': 't1_question_22_2_img_1.png',
    '4:3381': 't1_question_22_1_img_2.png',
    '4:3383': 't1_question_20_1_img_2.png',
    '4:3387': 't1_question_21_3_img_2.png',
    '4:3385': 't1_question_21_2_img_2.png',
    '4:3389': 't1_question_21_1_img_2.png',
    '4:3391': 't1_question_22_2_img_2.png',
    '4:3393': 't1_question_22_1_img_3.png',
    '4:3397': 't1_question_20_1_img_3.png',
    '4:3399': 't1_question_21_3_img_3.png',
    '4:3395': 't1_question_21_2_img_3.png',
    '4:3401': 't1_question_21_1_img_3.png',
    '4:3403': 't1_question_22_2_img_3.png',
    '4:3407': 't1_question_22_1_img_4.png',
    '4:3409': 't1_question_20_1_img_4.png',
    '4:3411': 't1_question_21_3_img_4.png',
    '4:3405': 't1_question_21_2_img_4.png',
    '4:3413': 't1_question_21_1_img_4.png',
    '4:3415': 't1_question_22_2_img_4.png',
}

def main():
    if TOKEN == 'paste_your_token_here':
        print("ERROR: set FIGMA_TOKEN env var or edit TOKEN in this script")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    # Ask Figma to render all nodes as PNG
    ids = ','.join(k.replace(':', '-') for k in NODES)
    api_url = (f'https://api.figma.com/v1/images/{FILE_KEY}'
               f'?ids={ids}&format=png&scale=1')
    req = urllib.request.Request(api_url,
                                 headers={'X-Figma-Token': TOKEN})
    print('Requesting export URLs from Figma API…')
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())

    if resp.get('err'):
        print(f"Figma error: {resp['err']}")
        sys.exit(1)

    images = resp.get('images', {})
    print(f'Got {len(images)} render URL(s)\n')

    ok, fail = 0, 0
    for node_id, filename in NODES.items():
        figma_id = node_id.replace(':', '-')
        img_url  = images.get(figma_id) or images.get(node_id)
        if not img_url:
            print(f'  ✗  {filename}  — no URL returned')
            fail += 1
            continue
        dst = os.path.join(OUT_DIR, filename)
        urllib.request.urlretrieve(img_url, dst)
        kb = os.path.getsize(dst) // 1024
        print(f'  ✓  {filename}  ({kb} KB)')
        ok += 1

    print(f'\n{ok} downloaded, {fail} failed  →  {OUT_DIR}')

if __name__ == '__main__':
    main()
