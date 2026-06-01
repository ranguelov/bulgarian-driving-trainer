#!/usr/bin/env python3
"""
Download hero illustration (node 242:9450) from Figma.
Usage: FIGMA_TOKEN=your_token python3 download_hero_image.py
"""
import os, json, urllib.request

TOKEN    = os.environ.get('FIGMA_TOKEN', '')
FILE_KEY = 'hKqLcn15skV1x2VFDUumnd'
NODE_ID  = '242:9450'
OUT_PATH = os.path.join(os.path.dirname(__file__), 'images', 'hero.png')

if not TOKEN:
    print("ERROR: Set FIGMA_TOKEN environment variable")
    raise SystemExit(1)

def figma_get(path):
    url = f'https://api.figma.com/v1{path}'
    req = urllib.request.Request(url)
    req.add_unredirected_header('X-Figma-Token', TOKEN.encode('ascii'))
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

print(f'Exporting node {NODE_ID} as PNG (scale=3)...')
encoded_id = NODE_ID.replace(':', '%3A')
data = figma_get(f'/images/{FILE_KEY}?ids={encoded_id}&format=png&scale=3')
url = data['images'].get(NODE_ID)
if not url:
    print('ERROR: no image URL returned', data)
    raise SystemExit(1)

print(f'Downloading...')
urllib.request.urlretrieve(url, OUT_PATH)
print(f'Saved to {OUT_PATH}')
