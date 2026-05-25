#!/usr/bin/env python3
"""
Download Figma images for Bulgarian Driving Trainer — Theme 3.

Images are split into two groups:
  • Question images  (node 4:5235) → t3_question_{page}_{sub}_img_1.png
  • Answer images    (node 4:4952) → t3_question_{page}_{sub}_img_{2-5}.png

Usage:
  1. Get your Figma Personal Access Token:
     Figma → Menu → Account Settings → Personal access tokens → Generate new token
  2. Run:
       FIGMA_TOKEN=your_token python3 download_figma_images_t3.py
     Or edit the TOKEN line below.
"""
import os, sys, json, urllib.request

TOKEN    = os.environ.get('FIGMA_TOKEN', 'paste_your_token_here')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
OUT_DIR  = os.path.join(os.path.dirname(__file__), 'images', 'questions')

# ── Question images (img_1) from node 4:5235 ─────────────────────────────────
NODES_Q = {
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

# ── Answer option images (img_2…img_5) from node 4:4952 ──────────────────────
# Columns: (a)=img_2  (b)=img_3  (c)=img_4  (d)=img_5
NODES_A = {
    # 1_2
    '4:4953': 't3_question_1_2_img_2.png',
    '4:5005': 't3_question_1_2_img_3.png',
    '4:5147': 't3_question_1_2_img_4.png',
    '4:5181': 't3_question_1_2_img_5.png',
    # 5_1
    '4:4956': 't3_question_5_1_img_2.png',
    '4:5002': 't3_question_5_1_img_3.png',
    '4:5050': 't3_question_5_1_img_4.png',
    '4:5059': 't3_question_5_1_img_5.png',
    # 5_2
    '4:4959': 't3_question_5_2_img_2.png',
    '4:5011': 't3_question_5_2_img_3.png',
    '4:5056': 't3_question_5_2_img_4.png',
    '4:5065': 't3_question_5_2_img_5.png',
    # 5_3
    '4:4963': 't3_question_5_3_img_2.png',
    '4:5016': 't3_question_5_3_img_3.png',
    '4:5062': 't3_question_5_3_img_4.png',
    '4:5071': 't3_question_5_3_img_5.png',
    # 5_4
    '4:4967': 't3_question_5_4_img_2.png',
    '4:5019': 't3_question_5_4_img_3.png',
    '4:5068': 't3_question_5_4_img_4.png',
    '4:5079': 't3_question_5_4_img_5.png',
    # 7_2
    '4:4970': 't3_question_7_2_img_2.png',
    '4:5024': 't3_question_7_2_img_3.png',
    '4:5074': 't3_question_7_2_img_4.png',
    '4:5085': 't3_question_7_2_img_5.png',
    # 7_3
    '4:4973': 't3_question_7_3_img_2.png',
    '4:5027': 't3_question_7_3_img_3.png',
    '4:5082': 't3_question_7_3_img_4.png',
    '4:5093': 't3_question_7_3_img_5.png',
    # 7_4
    '4:4976': 't3_question_7_4_img_2.png',
    '4:5030': 't3_question_7_4_img_3.png',
    '4:5089': 't3_question_7_4_img_4.png',
    '4:5108': 't3_question_7_4_img_5.png',
    # 9_2
    '4:4979': 't3_question_9_2_img_2.png',
    '4:5033': 't3_question_9_2_img_3.png',
    '4:5097': 't3_question_9_2_img_4.png',
    '4:5123': 't3_question_9_2_img_5.png',
    # 10_2
    '4:4989': 't3_question_10_2_img_2.png',
    '4:5040': 't3_question_10_2_img_3.png',
    '4:5111': 't3_question_10_2_img_4.png',
    '4:5135': 't3_question_10_2_img_5.png',
    # 30_2
    '4:4996': 't3_question_30_2_img_2.png',
    '4:5053': 't3_question_30_2_img_3.png',
    '4:5164': 't3_question_30_2_img_4.png',
    '4:5187': 't3_question_30_2_img_5.png',
    # 37_1  (3 options)
    '4:5193': 't3_question_37_1_img_2.png',
    '4:5199': 't3_question_37_1_img_3.png',
    '4:5208': 't3_question_37_1_img_4.png',
    # 37_2  (3 options)
    '4:5202': 't3_question_37_2_img_2.png',
    '4:5210': 't3_question_37_2_img_3.png',
    '4:5195': 't3_question_37_2_img_4.png',
    # 37_3  (3 options)
    '4:5212': 't3_question_37_3_img_2.png',
    '4:5205': 't3_question_37_3_img_3.png',
    '4:5197': 't3_question_37_3_img_4.png',
    # 38_1  (3 options)
    '4:5214': 't3_question_38_1_img_2.png',
    '4:5220': 't3_question_38_1_img_3.png',
    '4:5229': 't3_question_38_1_img_4.png',
    # 38_2  (3 options)
    '4:5231': 't3_question_38_2_img_2.png',
    '4:5223': 't3_question_38_2_img_3.png',
    '4:5216': 't3_question_38_2_img_4.png',
    # 38_3  (3 options)
    '4:5226': 't3_question_38_3_img_2.png',
    '4:5218': 't3_question_38_3_img_3.png',
    '4:5233': 't3_question_38_3_img_4.png',
}


def fetch_batch(nodes: dict) -> dict:
    """Request render URLs from Figma API for a dict of {node_id: filename}."""
    ids = ','.join(k.replace(':', '-') for k in nodes)
    url = (f'https://api.figma.com/v1/images/{FILE_KEY}'
           f'?ids={ids}&format=png&scale=1')
    req = urllib.request.Request(url, headers={'X-Figma-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    if resp.get('err'):
        raise RuntimeError(f'Figma error: {resp["err"]}')
    return resp.get('images', {})


def download_batch(nodes: dict, images: dict) -> tuple[int, int]:
    ok, fail = 0, 0
    for node_id, filename in nodes.items():
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
    return ok, fail


def chunked(d: dict, size: int):
    items = list(d.items())
    for i in range(0, len(items), size):
        yield dict(items[i:i + size])


def main():
    if TOKEN == 'paste_your_token_here':
        print('ERROR: set FIGMA_TOKEN env var or edit TOKEN in this script')
        sys.exit(1)
    try:
        TOKEN.encode('latin-1')
    except (UnicodeEncodeError, UnicodeDecodeError):
        print('ERROR: FIGMA_TOKEN contains non-ASCII characters.')
        print('       Make sure you are passing your real Figma token, not a placeholder.')
        print('       Get it at: Figma → Account Settings → Personal access tokens')
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    total_ok = total_fail = 0

    # ── Question images ───────────────────────────────────────────────────────
    print(f'\n[1/2] Question images ({len(NODES_Q)} nodes)…')
    images = fetch_batch(NODES_Q)
    print(f'      Got {len(images)} render URL(s)')
    ok, fail = download_batch(NODES_Q, images)
    total_ok += ok; total_fail += fail

    # ── Answer images — download in batches of 50 ─────────────────────────────
    chunks = list(chunked(NODES_A, 50))
    print(f'\n[2/2] Answer images ({len(NODES_A)} nodes, {len(chunks)} batch(es))…')
    for i, chunk in enumerate(chunks, 1):
        print(f'      Batch {i}/{len(chunks)} — requesting {len(chunk)} URLs…')
        images = fetch_batch(chunk)
        ok, fail = download_batch(chunk, images)
        total_ok += ok; total_fail += fail

    print(f'\n{"─"*50}')
    print(f'{total_ok} downloaded, {total_fail} failed  →  {OUT_DIR}')


if __name__ == '__main__':
    main()
