#!/usr/bin/env python3
"""Save lossless rectangular crops of original scan figures, with provenance."""
from pathlib import Path
from PIL import Image
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
ITEMS = [('2.1',28,(0.59,0.09,0.92,0.307)),
         ('2.2',29,(0.59,0.28,0.93,0.486)),
         ('2.3',29,(0.235,0.698,0.753,0.881)),
         ('2.4',30,(0.113,0.575,0.91,0.778))]

def main():
    out=ROOT/'figures'/'source'
    out.mkdir(parents=True,exist_ok=True)
    (ROOT/'quality').mkdir(exist_ok=True)
    records=[]
    for name,page,box in ITEMS:
        src=ROOT/'source-images'/f'pdf-{page:03d}.jpeg'
        im=Image.open(src)
        px=tuple(round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box))
        dest=out/f'figure-{name}.png'
        im.crop(px).save(dest)
        records.append({'figure':name,'pdf_page':page,'image':str(dest.relative_to(ROOT)),
                        'source_image':str(src.relative_to(ROOT)),'crop_xyxy_pixels':px,
                        'original_dimensions':im.size,
                        'crop_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    (ROOT/'quality'/'source-figures.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    main()
