#!/usr/bin/env python3
"""
Download Figma images for Bulgarian Driving Trainer — Theme 2.

Images are split into two groups:
  • Question images  (node 4:2910) → t2_question_{page}_{sub}_img_1.png
  • Answer images    (node 4:3417) → t2_question_{page}_{sub}_img_{2-5}.png

Usage:
  1. Get your Figma Personal Access Token:
     Figma → Menu → Account Settings → Personal access tokens → Generate new token
  2. Run:
       FIGMA_TOKEN=your_token python3 download_figma_images_t2.py
     Or edit the TOKEN line below.
"""
import os, sys, json, urllib.request

TOKEN    = os.environ.get('FIGMA_TOKEN', 'paste_your_token_here')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
OUT_DIR  = os.path.join(os.path.dirname(__file__), 'images', 'questions')

# ── Question images (img_1) from node 4:2910 ─────────────────────────────────
NODES_Q = {
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

# ── Answer option images (img_2…img_5) from node 4:3417 ──────────────────────
# Columns: (a)=img_2  (b)=img_3  (c)=img_4  (d)=img_5
NODES_A = {
    # 1-2
    '4:3418': 't2_question_1_2_img_2.png',
    '4:3720': 't2_question_1_2_img_3.png',
    '4:4097': 't2_question_1_2_img_4.png',
    '4:4403': 't2_question_1_2_img_5.png',
    # 2-1
    '4:3427': 't2_question_2_1_img_2.png',
    '4:3696': 't2_question_2_1_img_3.png',
    '4:3727': 't2_question_2_1_img_4.png',
    '4:4064': 't2_question_2_1_img_5.png',
    # 3-1  (3 options)
    '4:3437': 't2_question_3_1_img_2.png',
    '4:3763': 't2_question_3_1_img_3.png',
    '4:4106': 't2_question_3_1_img_4.png',
    # 3-2  (3 options)
    '4:3686': 't2_question_3_2_img_2.png',
    '4:4056': 't2_question_3_2_img_3.png',
    '4:4395': 't2_question_3_2_img_4.png',
    # 7-1
    '4:3445': 't2_question_7_1_img_2.png',
    '4:3842': 't2_question_7_1_img_3.png',
    '4:4169': 't2_question_7_1_img_4.png',
    '4:4588': 't2_question_7_1_img_5.png',
    # 7-2
    '4:3453': 't2_question_7_2_img_2.png',
    '4:3848': 't2_question_7_2_img_3.png',
    '4:4175': 't2_question_7_2_img_4.png',
    '4:4595': 't2_question_7_2_img_5.png',
    # 7-3
    '4:3461': 't2_question_7_3_img_2.png',
    '4:3854': 't2_question_7_3_img_3.png',
    '4:4185': 't2_question_7_3_img_4.png',
    '4:4607': 't2_question_7_3_img_5.png',
    # 7-4
    '4:3468': 't2_question_7_4_img_2.png',
    '4:3861': 't2_question_7_4_img_3.png',
    '4:4218': 't2_question_7_4_img_4.png',
    '4:4617': 't2_question_7_4_img_5.png',
    # 11-2
    '4:3474': 't2_question_11_2_img_2.png',
    '4:3871': 't2_question_11_2_img_3.png',
    '4:4230': 't2_question_11_2_img_4.png',
    '4:4626': 't2_question_11_2_img_5.png',
    # 13-1
    '4:3507': 't2_question_13_1_img_2.png',
    '4:3880': 't2_question_13_1_img_3.png',
    '4:4239': 't2_question_13_1_img_4.png',
    '4:4640': 't2_question_13_1_img_5.png',
    # 13-2
    '4:3516': 't2_question_13_2_img_2.png',
    '4:3894': 't2_question_13_2_img_3.png',
    '4:4283': 't2_question_13_2_img_4.png',
    '4:4673': 't2_question_13_2_img_5.png',
    # 13-3
    '4:3525': 't2_question_13_3_img_2.png',
    '4:3912': 't2_question_13_3_img_3.png',
    '4:4292': 't2_question_13_3_img_4.png',
    '4:4695': 't2_question_13_3_img_5.png',
    # 13-4
    '4:3534': 't2_question_13_4_img_2.png',
    '4:3903': 't2_question_13_4_img_3.png',
    '4:4261': 't2_question_13_4_img_4.png',
    '4:4632': 't2_question_13_4_img_5.png',
    # 13-5
    '4:3543': 't2_question_13_5_img_2.png',
    '4:3945': 't2_question_13_5_img_3.png',
    '4:4306': 't2_question_13_5_img_4.png',
    '4:4719': 't2_question_13_5_img_5.png',
    # 15-1
    '4:3552': 't2_question_15_1_img_2.png',
    '4:3954': 't2_question_15_1_img_3.png',
    '4:4314': 't2_question_15_1_img_4.png',
    '4:4752': 't2_question_15_1_img_5.png',
    # 15-2
    '4:3560': 't2_question_15_2_img_2.png',
    '4:3962': 't2_question_15_2_img_3.png',
    '4:4337': 't2_question_15_2_img_4.png',
    '4:4761': 't2_question_15_2_img_5.png',
    # 16-1
    '4:3568': 't2_question_16_1_img_2.png',
    '4:3988': 't2_question_16_1_img_3.png',
    '4:4344': 't2_question_16_1_img_4.png',
    '4:4770': 't2_question_16_1_img_5.png',
    # 22-1
    '4:3578': 't2_question_22_1_img_2.png',
    '4:3970': 't2_question_22_1_img_3.png',
    '4:4321': 't2_question_22_1_img_4.png',
    '4:4733': 't2_question_22_1_img_5.png',
    # 22-2
    '4:3587': 't2_question_22_2_img_2.png',
    '4:3979': 't2_question_22_2_img_3.png',
    '4:4329': 't2_question_22_2_img_4.png',
    '4:4742': 't2_question_22_2_img_5.png',
    # 24-1
    '4:3596': 't2_question_24_1_img_2.png',
    '4:3994': 't2_question_24_1_img_3.png',
    '4:4350': 't2_question_24_1_img_4.png',
    '4:4802': 't2_question_24_1_img_5.png',
    # 24-2
    '4:3602': 't2_question_24_2_img_2.png',
    '4:4000': 't2_question_24_2_img_3.png',
    '4:4356': 't2_question_24_2_img_4.png',
    '4:4808': 't2_question_24_2_img_5.png',
    # 24-3
    '4:3608': 't2_question_24_3_img_2.png',
    '4:4006': 't2_question_24_3_img_3.png',
    '4:4363': 't2_question_24_3_img_4.png',
    '4:4814': 't2_question_24_3_img_5.png',
    # 25-2
    '4:3614': 't2_question_25_2_img_2.png',
    '4:4012': 't2_question_25_2_img_3.png',
    '4:4369': 't2_question_25_2_img_4.png',
    '4:4830': 't2_question_25_2_img_5.png',
    # 26-2
    '4:3620': 't2_question_26_2_img_2.png',
    '4:4018': 't2_question_26_2_img_3.png',
    '4:4375': 't2_question_26_2_img_4.png',
    '4:4837': 't2_question_26_2_img_5.png',
    # 27-1
    '4:3626': 't2_question_27_1_img_2.png',
    '4:4027': 't2_question_27_1_img_3.png',
    '4:4384': 't2_question_27_1_img_4.png',
    '4:4843': 't2_question_27_1_img_5.png',
    # 27-2
    '4:3632': 't2_question_27_2_img_2.png',
    '4:4033': 't2_question_27_2_img_3.png',
    '4:4427': 't2_question_27_2_img_4.png',
    '4:4859': 't2_question_27_2_img_5.png',
    # 27-3
    '4:3638': 't2_question_27_3_img_2.png',
    '4:4039': 't2_question_27_3_img_3.png',
    '4:4448': 't2_question_27_3_img_4.png',
    '4:4875': 't2_question_27_3_img_5.png',
    # 27-4
    '4:3644': 't2_question_27_4_img_2.png',
    '4:4091': 't2_question_27_4_img_3.png',
    '4:4467': 't2_question_27_4_img_4.png',
    '4:4881': 't2_question_27_4_img_5.png',
    # 33-1
    '4:3650': 't2_question_33_1_img_2.png',
    '4:4045': 't2_question_33_1_img_3.png',
    '4:4436': 't2_question_33_1_img_4.png',
    '4:4849': 't2_question_33_1_img_5.png',
    # 33-2
    '4:3656': 't2_question_33_2_img_2.png',
    '4:4120': 't2_question_33_2_img_3.png',
    '4:4473': 't2_question_33_2_img_4.png',
    '4:4887': 't2_question_33_2_img_5.png',
    # 34-2
    '4:3662': 't2_question_34_2_img_2.png',
    '4:4114': 't2_question_34_2_img_3.png',
    '4:4455': 't2_question_34_2_img_4.png',
    '4:4865': 't2_question_34_2_img_5.png',
    # 35-2
    '4:3673': 't2_question_35_2_img_2.png',
    '4:4132': 't2_question_35_2_img_3.png',
    '4:4483': 't2_question_35_2_img_4.png',
    '4:4899': 't2_question_35_2_img_5.png',
    # 36-2
    '4:3680': 't2_question_36_2_img_2.png',
    '4:4138': 't2_question_36_2_img_3.png',
    '4:4526': 't2_question_36_2_img_4.png',
    '4:4905': 't2_question_36_2_img_5.png',
    # 37-1
    '4:3756': 't2_question_37_1_img_2.png',
    '4:4145': 't2_question_37_1_img_3.png',
    '4:4569': 't2_question_37_1_img_4.png',
    '4:4911': 't2_question_37_1_img_5.png',
    # 38-2
    '4:3773': 't2_question_38_2_img_2.png',
    '4:4151': 't2_question_38_2_img_3.png',
    '4:4575': 't2_question_38_2_img_4.png',
    '4:4917': 't2_question_38_2_img_5.png',
    # 39-2
    '4:3816': 't2_question_39_2_img_2.png',
    '4:4161': 't2_question_39_2_img_3.png',
    '4:4581': 't2_question_39_2_img_4.png',
    '4:4943': 't2_question_39_2_img_5.png',
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


def download_batch(nodes: dict, images: dict, label: str) -> tuple[int, int]:
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
    ok, fail = download_batch(NODES_Q, images, 'Q')
    total_ok += ok; total_fail += fail

    # ── Answer images — download in batches of 50 ─────────────────────────────
    chunks = list(chunked(NODES_A, 50))
    print(f'\n[2/2] Answer images ({len(NODES_A)} nodes, {len(chunks)} batches)…')
    for i, chunk in enumerate(chunks, 1):
        print(f'      Batch {i}/{len(chunks)} — requesting {len(chunk)} URLs…')
        images = fetch_batch(chunk)
        ok, fail = download_batch(chunk, images, f'A{i}')
        total_ok += ok; total_fail += fail

    print(f'\n{"─"*50}')
    print(f'{total_ok} downloaded, {total_fail} failed  →  {OUT_DIR}')


if __name__ == '__main__':
    main()
