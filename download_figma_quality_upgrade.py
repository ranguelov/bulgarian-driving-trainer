#!/usr/bin/env python3
"""
Quality upgrade: download high-res images from Figma for themes 1-3.

  Vector nodes (road signs, diagrams) → exported as SVG
  Raster nodes (photos, illustrations) → exported as PNG at 2x scale

SAFE WORKFLOW:
  1. Run this script → files saved to images/questions_preview/
  2. Open quality_preview.html in browser to compare old vs new
  3. If everything looks good → run apply_quality_upgrade.py

Usage:
  FIGMA_TOKEN=your_token python3 download_figma_quality_upgrade.py
"""
import os, sys, json, urllib.request, urllib.parse, time

TOKEN    = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PREVIEW_DIR = os.path.join(BASE_DIR, 'images', 'questions_preview')
CURRENT_DIR = os.path.join(BASE_DIR, 'images', 'questions')

if not TOKEN:
    print('ERROR: Set FIGMA_TOKEN environment variable')
    print('  export FIGMA_TOKEN=your_personal_access_token')
    sys.exit(1)

os.makedirs(PREVIEW_DIR, exist_ok=True)

# ── Node maps: {node_id: base_filename_without_extension} ────────────────────

NODES_T1_Q = {
    '4:2896': 't1_question_39_3_img_1',
    '4:2898': 't1_question_39_2_img_1',
    '4:2900': 't1_question_39_1_img_1',
    '4:2902': 't1_question_44_1_img_1',
    '4:2904': 't1_question_48_1_img_1',
    '4:2906': 't1_question_45_1_img_1',
    '4:2908': 't1_question_51_1_img_1',
}

NODES_T2_Q = {
    '4:2911': 't2_question_1_1_img_1',
    '4:2920': 't2_question_4_1_img_1',
    '4:2950': 't2_question_4_2_img_1',
    '4:2952': 't2_question_4_3_img_1',
    '4:3010': 't2_question_4_4_img_1',
    '4:3043': 't2_question_4_5_img_1',
    '4:3055': 't2_question_4_6_img_1',
    '4:3062': 't2_question_4_8_img_1',
    '4:3068': 't2_question_4_7_img_1',
    '4:3076': 't2_question_5_1_img_1',
    '4:3083': 't2_question_5_2_img_1',
    '4:3091': 't2_question_6_1_img_1',
    '4:3097': 't2_question_6_2_img_1',
    '4:3104': 't2_question_11_1_img_1',
    '4:3136': 't2_question_12_1_img_1',
    '4:3145': 't2_question_12_2_img_1',
    '4:3154': 't2_question_12_3_img_1',
    '4:3163': 't2_question_14_1_img_1',
    '4:3169': 't2_question_17_1_img_1',
    '4:3179': 't2_question_17_2_img_1',
    '4:3189': 't2_question_17_3_img_1',
    '4:3191': 't2_question_23_2_img_1',
    '4:3197': 't2_question_35_1_img_1',
    '4:3204': 't2_question_23_3_img_1',
    '4:3210': 't2_question_18_1_img_1',
    '4:3216': 't2_question_36_1_img_1',
    '4:3222': 't2_question_25_1_img_1',
    '4:3228': 't2_question_26_1_img_1',
    '4:3234': 't2_question_38_1_img_1',
    '4:3277': 't2_question_18_2_img_1',
    '4:3279': 't2_question_29_1_img_1',
    '4:3281': 't2_question_39_1_img_1',
    '4:3307': 't2_question_30_1_img_1',
    '4:3309': 't2_question_19_1_img_1',
    '4:3317': 't2_question_40_1_img_1',
    '4:3319': 't2_question_32_1_img_1',
    '4:3325': 't2_question_40_2_img_1',
    '4:3327': 't2_question_40_3_img_1',
    '4:3329': 't2_question_34_1_img_1',
    '4:3340': 't2_question_19_2_img_1',
    '4:3348': 't2_question_20_1_img_1',
    '4:3356': 't2_question_21_1_img_1',
    '4:3362': 't2_question_23_1_img_1',
}

NODES_T3_Q = {
    '4:5236': 't3_question_1_1_img_1',
    '4:5239': 't3_question_2_1_img_1',
    '4:5242': 't3_question_3_1_img_1',
    '4:5244': 't3_question_4_1_img_1',
    '4:5246': 't3_question_4_2_img_1',
    '4:5248': 't3_question_4_3_img_1',
    '4:5250': 't3_question_6_1_img_1',
    '4:5252': 't3_question_6_2_img_1',
    '4:5254': 't3_question_6_3_img_1',
    '4:5256': 't3_question_9_1_img_1',
    '4:5266': 't3_question_10_1_img_1',
    '4:5273': 't3_question_11_1_img_1',
    '4:5285': 't3_question_13_1_img_1',
    '4:5287': 't3_question_13_2_img_1',
    '4:5289': 't3_question_13_3_img_1',
    '4:5291': 't3_question_13_4_img_1',
    '4:5293': 't3_question_14_1_img_1',
    '4:5296': 't3_question_14_2_img_1',
    '4:5298': 't3_question_14_3_img_1',
    '4:5300': 't3_question_17_1_img_1',
    '4:5302': 't3_question_17_2_img_1',
    '4:5304': 't3_question_20_1_img_1',
    '4:5306': 't3_question_21_1_img_1',
    '4:5309': 't3_question_21_2_img_1',
    '4:5312': 't3_question_21_3_img_1',
    '4:5314': 't3_question_22_1_img_1',
    '4:5316': 't3_question_23_1_img_1',
    '4:5318': 't3_question_23_2_img_1',
    '4:5320': 't3_question_24_1_img_1',
    '4:5322': 't3_question_25_1_img_1',
    '4:5324': 't3_question_26_1_img_1',
    '4:5326': 't3_question_27_1_img_1',
    '4:5328': 't3_question_28_1_img_1',
    '4:5330': 't3_question_29_1_img_1',
    '4:5332': 't3_question_30_1_img_1',
    '4:5338': 't3_question_32_1_img_1',
    '4:5340': 't3_question_54_1_img_1',
    '4:5357': 't3_question_58_1_img_1',
    '4:5360': 't3_question_59_1_img_1',
    '4:5363': 't3_question_60_1_img_1',
    '4:5366': 't3_question_61_1_img_1',
    '4:5369': 't3_question_62_1_img_1',
    '4:5372': 't3_question_63_1_img_1',
    '4:5375': 't3_question_64_1_img_1',
    '4:5378': 't3_question_65_1_img_1',
}

ALL_NODES = {}
ALL_NODES.update(NODES_T1_Q)
ALL_NODES.update(NODES_T2_Q)
ALL_NODES.update(NODES_T3_Q)

# ── Figma API helpers ─────────────────────────────────────────────────────────

def figma_get(path):
    url = f'https://api.figma.com/v1{path}'
    req = urllib.request.Request(url, headers={'X-Figma-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def figma_download(url, dest_path):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as r:
        with open(dest_path, 'wb') as f:
            f.write(r.read())


def has_image_fill(node_data):
    """Return True if the node or any of its children has an IMAGE fill (raster)."""
    fills = node_data.get('fills', [])
    for fill in fills:
        if fill.get('type') == 'IMAGE':
            return True
    for child in node_data.get('children', []):
        if has_image_fill(child):
            return True
    return False


def check_raster_batch(node_ids):
    """
    Returns dict: {node_id: True/False} where True = raster (has IMAGE fill).
    Calls Figma nodes API in batches of 50.
    """
    result = {}
    batch_size = 50
    ids_list = list(node_ids)
    for i in range(0, len(ids_list), batch_size):
        batch = ids_list[i:i + batch_size]
        ids_param = ','.join(batch)
        print(f'  Checking fills for {len(batch)} nodes...')
        data = figma_get(f'/files/{FILE_KEY}/nodes?ids={urllib.parse.quote(ids_param)}&depth=3')
        for nid in batch:
            node_info = data.get('nodes', {}).get(nid)
            if node_info and node_info.get('document'):
                result[nid] = has_image_fill(node_info['document'])
            else:
                # If node not found, assume raster (safe fallback)
                result[nid] = True
                print(f'    WARNING: node {nid} not found in API response, assuming raster')
        time.sleep(0.3)  # be polite to API
    return result


def get_image_urls_batch(node_ids, fmt, scale=None):
    """
    Returns dict: {node_id: url} for the given format ('svg' or 'png').
    Calls Figma images API in batches of 50.
    """
    result = {}
    batch_size = 50
    ids_list = list(node_ids)
    for i in range(0, len(ids_list), batch_size):
        batch = ids_list[i:i + batch_size]
        ids_param = ','.join(batch)
        params = f'ids={urllib.parse.quote(ids_param)}&format={fmt}'
        if scale:
            params += f'&scale={scale}'
        print(f'  Getting {fmt.upper()} URLs for {len(batch)} nodes...')
        data = figma_get(f'/images/{FILE_KEY}?{params}')
        if data.get('err'):
            print(f'  ERROR from Figma: {data["err"]}')
            continue
        result.update(data.get('images', {}))
        time.sleep(0.3)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'Total nodes to process: {len(ALL_NODES)}')
    print(f'Preview dir: {PREVIEW_DIR}\n')

    # Step 1: detect raster vs vector
    print('Step 1: Detecting raster vs vector...')
    raster_map = check_raster_batch(list(ALL_NODES.keys()))

    vector_nodes = {nid: name for nid, name in ALL_NODES.items() if not raster_map.get(nid, True)}
    raster_nodes = {nid: name for nid, name in ALL_NODES.items() if raster_map.get(nid, True)}

    print(f'  Vector (SVG): {len(vector_nodes)}')
    print(f'  Raster (PNG@2x): {len(raster_nodes)}\n')

    # Save classification for apply script
    classification = {
        'vector': {nid: name for nid, name in vector_nodes.items()},
        'raster': {nid: name for nid, name in raster_nodes.items()},
    }
    cls_path = os.path.join(BASE_DIR, 'figma_node_classification.json')
    with open(cls_path, 'w') as f:
        json.dump(classification, f, indent=2)
    print(f'Classification saved to figma_node_classification.json\n')

    # Step 2: download SVGs
    downloaded = {}  # basename -> (new_path, old_path, is_svg)

    if vector_nodes:
        print('Step 2a: Downloading SVG (vector nodes)...')
        svg_urls = get_image_urls_batch(list(vector_nodes.keys()), 'svg')
        for nid, url in svg_urls.items():
            if not url:
                print(f'  SKIP {nid}: no URL returned')
                continue
            basename = vector_nodes[nid]
            dest = os.path.join(PREVIEW_DIR, basename + '.svg')
            old_png = os.path.join(CURRENT_DIR, basename + '.png')
            print(f'  → {basename}.svg')
            try:
                figma_download(url, dest)
                downloaded[basename] = (dest, old_png, True)
            except Exception as e:
                print(f'    ERROR: {e}')
        print()

    # Step 3: download PNGs @2x
    if raster_nodes:
        print('Step 2b: Downloading PNG@2x (raster nodes)...')
        png_urls = get_image_urls_batch(list(raster_nodes.keys()), 'png', scale=2)
        for nid, url in png_urls.items():
            if not url:
                print(f'  SKIP {nid}: no URL returned')
                continue
            basename = raster_nodes[nid]
            dest = os.path.join(PREVIEW_DIR, basename + '.png')
            old_png = os.path.join(CURRENT_DIR, basename + '.png')
            print(f'  → {basename}.png (2x)')
            try:
                figma_download(url, dest)
                downloaded[basename] = (dest, old_png, False)
            except Exception as e:
                print(f'    ERROR: {e}')
        print()

    print(f'Downloaded {len(downloaded)} files to {PREVIEW_DIR}\n')

    # Step 4: generate quality_preview.html
    print('Step 3: Generating quality_preview.html...')
    generate_preview_html(downloaded)
    print(f'  → {os.path.join(BASE_DIR, "quality_preview.html")}')
    print('\nDone! Open quality_preview.html in your browser to compare images.')
    print('Then run apply_quality_upgrade.py to apply the changes.\n')


def generate_preview_html(downloaded):
    """Build a side-by-side comparison page."""
    rows = []
    for basename in sorted(downloaded.keys()):
        new_path, old_path, is_svg = downloaded[basename]
        new_ext = '.svg' if is_svg else '.png'
        new_rel = f'images/questions_preview/{basename}{new_ext}'
        old_rel = f'images/questions/{basename}.png'
        kind = 'SVG (vector)' if is_svg else 'PNG @2x'
        old_exists = os.path.exists(old_path)
        old_cell = f'<img src="{old_rel}" style="max-height:200px;max-width:300px">' if old_exists else '<em>no current file</em>'
        rows.append(f'''
    <tr>
      <td style="padding:8px;border-bottom:1px solid #333;color:#aaa;font-size:12px">{basename}<br><span style="color:#6cf">{kind}</span></td>
      <td style="padding:8px;border-bottom:1px solid #333;text-align:center">{old_cell}</td>
      <td style="padding:8px;border-bottom:1px solid #333;text-align:center">
        <img src="{new_rel}" style="max-height:200px;max-width:300px">
      </td>
    </tr>''')

    html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Quality Preview — Bulgarian Driving Trainer</title>
<style>
  body {{ background:#1a1a2e; color:#eee; font-family:sans-serif; margin:0; padding:20px }}
  h1 {{ color:#6cf; margin-bottom:4px }}
  p {{ color:#aaa; margin-top:0 }}
  table {{ border-collapse:collapse; width:100% }}
  th {{ background:#16213e; padding:10px; text-align:left; color:#6cf; border-bottom:2px solid #444 }}
  tr:hover td {{ background:rgba(255,255,255,0.03) }}
</style>
</head>
<body>
<h1>Quality Preview</h1>
<p>{len(downloaded)} images — compare old (current) vs new (high-res) before applying.</p>
<table>
  <thead>
    <tr>
      <th style="width:260px">File</th>
      <th style="width:320px">Current (production)</th>
      <th style="width:320px">New (high-res preview)</th>
    </tr>
  </thead>
  <tbody>
{''.join(rows)}
  </tbody>
</table>
</body>
</html>'''

    preview_path = os.path.join(BASE_DIR, 'quality_preview.html')
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    main()
