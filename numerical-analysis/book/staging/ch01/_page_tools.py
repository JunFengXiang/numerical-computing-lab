from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / 'staging/ch01'
SOURCE_SHA = '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'

def ocr_body(n):
    s = (ROOT / f'ocr/glm-fullpage/pdf-{n:03d}.md').read_text()
    s = s.split(f'[查看原页](../../source-images/pdf-{n:03d}.jpeg)\n\n', 1)[1]
    return re.sub(r'\n[·•]\s*\d+\s*[·•]\s*$', '', s).strip()

def save_page(n, text, headings=(), formulas=(), figures=(), tables=(), notes=()):
    p = LANE / f'pages/pdf-{n:03d}.md'
    p.write_text(f'---\npdf_page: {n}\nprinted_page: {n-13}\nsource_image: source-images/pdf-{n:03d}.jpeg\nsource_sha256: {SOURCE_SHA}\nstatus: agent_reviewed_transcription\n---\n\n[查看原页](../../../source-images/pdf-{n:03d}.jpeg)\n\n<!-- source-page: {n} -->\n\n' + text.strip() + '\n')
    review = json.loads((LANE / 'review.json').read_text())
    item = {'pdf_page': n, 'printed_page': n-13, 'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'source_image_sha256': hashlib.sha256((ROOT / f'source-images/pdf-{n:03d}.jpeg').read_bytes()).hexdigest(), 'visual_review': 'completed', 'content_coverage': 'complete', 'headings': [{'id': a, 'title': b} for a, b in headings], 'formula_ids': list(formulas), 'figures': list(figures), 'tables': list(tables), 'notes': list(notes)}
    review['pages'] = sorted([x for x in review['pages'] if x['pdf_page'] != n] + [item], key=lambda x:x['pdf_page'])
    (LANE / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

def save_erratum(item):
    review = json.loads((LANE / 'review.json').read_text())
    review['source_errata'] = [x for x in review['source_errata'] if x.get('id') != item['id']] + [item]
    (LANE / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
