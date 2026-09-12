#!/usr/bin/env python3
"""Extract original embedded scan bytes; never rasterize or alter the source PDF."""
from pathlib import Path
from hashlib import sha256
import json
import fitz

ROOT = Path(__file__).resolve().parents[1]


def main():
    sources = list(ROOT.glob('*.pdf'))
    if len(sources) != 1:
        raise SystemExit('Expected exactly one original PDF in book/.')
    src = sources[0]
    source_digest = sha256(src.read_bytes()).hexdigest()
    old_path = ROOT / 'source-manifest.json'
    old = json.loads(old_path.read_text()) if old_path.exists() else {}
    if old and old.get('source_sha256') != source_digest:
        raise ValueError('Original PDF changed; do not carry old review records across source changes.')
    old_pages = {p['pdf_page']: p for p in old.get('pages', [])}
    out = ROOT / 'source-images'
    out.mkdir(exist_ok=True)
    doc = fitz.open(src)
    pages = []
    for number, page in enumerate(doc, 1):
        imgs = page.get_images(full=True)
        if len(imgs) != 1:
            raise ValueError(f'PDF page {number}: expected one scan image, got {len(imgs)}')
        obj = doc.extract_image(imgs[0][0])
        raw = obj['image']
        target = out / f'pdf-{number:03d}.{obj["ext"]}'
        if not target.exists() or sha256(target.read_bytes()).digest() != sha256(raw).digest():
            target.write_bytes(raw)
        pages.append({
            'pdf_page': number, 'printed_page': None,
            'printed_page_status': 'pending_visual_verification',
            'image': str(target.relative_to(ROOT)),
            'image_sha256': sha256(raw).hexdigest(),
            'width': obj['width'], 'height': obj['height'],
            'pdf_rect': list(page.rect), 'native_text_characters': len(page.get_text()),
            'content_review_status': 'pending',
        })
        prior = old_pages.get(number, {})
        if prior.get('image_sha256') == pages[-1]['image_sha256']:
            for key in ['printed_page','printed_page_status','content_review_status']:
                if key in prior:
                    pages[-1][key] = prior[key]
    manifest = {
        'source_file': src.name, 'source_bytes': src.stat().st_size,
        'source_sha256': source_digest,
        'source_pdf_pages': len(doc), 'extraction': 'unmodified embedded image bytes via PyMuPDF',
        'pages': pages,
    }
    (ROOT / 'source-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    status = json.loads((ROOT / 'STATUS.json').read_text())
    status['source_images_extracted'] = len(pages)
    (ROOT / 'STATUS.json').write_text(json.dumps(status, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k != 'pages'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
