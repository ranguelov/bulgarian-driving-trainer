#!/usr/bin/env python3
"""
Download all t4 images from Figma for Bulgarian Driving Trainer.

Usage:
  FIGMA_TOKEN=your_token python3 download_figma_t4.py

Get your token: Figma → Menu → Account Settings → Personal access tokens → Generate new token
"""
import os, sys, json, urllib.request, urllib.parse, time

TOKEN    = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
# Group 1: illustration images (PNG, node 230:7497)
# Group 2: answer images (PNG, node 230:7698)
# Group 1: sign images → SVG (no background)
# Group 2: answer images → PNG
GROUPS = [
    ('230:7497', 'svg'),
    ('230:7698', 'png'),
]
OUT_DIR = os.path.join(os.path.dirname(__file__), 'images', 'questions')

if not TOKEN or TOKEN == 'paste_your_token_here':
    print("ERROR: Set FIGMA_TOKEN environment variable")
    print("  export FIGMA_TOKEN=your_personal_access_token")
    sys.exit(1)

def figma_get(path):
    url = f'https://api.figma.com/v1{path}'
    req = urllib.request.Request(url)
    req.add_unredirected_header('X-Figma-Token', TOKEN.encode('ascii'))
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get_children_ids(parent_node_id):
    """Get all direct children node IDs and names from a parent node."""
    encoded = urllib.parse.quote(parent_node_id, safe='')
    data = figma_get(f'/files/{FILE_KEY}/nodes?ids={encoded}')
    nodes = data.get('nodes', {})
    node_data = nodes.get(parent_node_id, {})
    document = node_data.get('document', {})
    children = document.get('children', [])
    return [(child['id'], child['name']) for child in children]

def export_nodes(node_ids, fmt='png', scale=2):
    """Export a batch of nodes, returns {nodeId: url}."""
    ids_param = ','.join(node_ids)
    encoded_ids = urllib.parse.quote(ids_param, safe=',')
    params = f'format={fmt}'
    if fmt == 'png':
        params += f'&scale={scale}'
    data = figma_get(f'/images/{FILE_KEY}?ids={encoded_ids}&{params}')
    return data.get('images', {})

def download_file(url, dest_path):
    req = urllib.request.Request(url, headers={'X-Figma-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        with open(dest_path, 'wb') as f:
            f.write(r.read())

os.makedirs(OUT_DIR, exist_ok=True)

all_nodes = []  # [(node_id, filename, fmt)]
svg_names = set()  # track which base names are SVG (to update questions.js)

for parent_id, fmt in GROUPS:
    print(f'Getting children of {parent_id} (format={fmt})...')
    children = get_children_ids(parent_id)
    print(f'  Found {len(children)} children')
    for node_id, name in children:
        base = name.rsplit('.', 1)[0] if '.' in name else name
        filename = base + '.' + fmt
        all_nodes.append((node_id, filename, fmt))
        if fmt == 'svg':
            svg_names.add(base)

print(f'\nTotal images to download: {len(all_nodes)}')

# Export in batches of 50 (Figma API limit)
BATCH = 50
downloaded = 0
failed = []

for i in range(0, len(all_nodes), BATCH):
    batch = all_nodes[i:i+BATCH]
    node_ids = [n[0] for n in batch]
    id_to_filename = {n[0]: n[1] for n in batch}
    fmt = batch[0][2]  # all items in batch have same fmt (groups are processed sequentially)

    print(f'Exporting batch {i//BATCH + 1}/{(len(all_nodes)+BATCH-1)//BATCH} ({fmt})...', end=' ', flush=True)
    try:
        urls = export_nodes(node_ids, fmt=fmt)
        for node_id, url in urls.items():
            filename = id_to_filename.get(node_id)
            if not filename or not url:
                continue
            dest = os.path.join(OUT_DIR, filename)
            try:
                urllib.request.urlretrieve(url, dest)
                downloaded += 1
            except Exception as e:
                failed.append((filename, str(e)))
        print(f'OK ({len(urls)} images)')
        time.sleep(0.5)  # rate limit
    except Exception as e:
        print(f'FAILED: {e}')
        failed.extend([(id_to_filename[n], 'batch failed') for n in node_ids])

print(f'\nDone: {downloaded} downloaded, {len(failed)} failed')
if failed:
    print('Failed:')
    for f, e in failed:
        print(f'  {f}: {e}')

# Update questions.js: replace .png → .svg for SVG images
if svg_names:
    qs_path = os.path.join(os.path.dirname(__file__), 'questions.js')
    with open(qs_path) as f:
        content = f.read()
    updated = 0
    for base in svg_names:
        old = f'{base}.png'
        new = f'{base}.svg'
        if old in content:
            content = content.replace(old, new)
            updated += 1
    with open(qs_path, 'w') as f:
        f.write(content)
    print(f'\nUpdated questions.js: {updated} image references changed .png → .svg')
