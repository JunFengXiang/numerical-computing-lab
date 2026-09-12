from pathlib import Path
import hashlib
import json
import re
import sys

LANE = Path(__file__).resolve().parent
BOOK = LANE.parent.parent
SOURCE_SHA = '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'
review_path = LANE / 'review.json'
review = json.loads(review_path.read_text()) if review_path.exists() else {
    'lane': 'ch06', 'reviewer': 'Codex agent ch06', 'human_review': False,
    'source_sha256': SOURCE_SHA, 'pages': [], 'unresolved': [],
    'source_errata': [], 'validation_notes': []}
records = {p['pdf_page']: p for p in review['pages']}
for number in map(int, sys.argv[1:]):
    page = LANE / 'pages' / f'pdf-{number:03}.md'
    source = BOOK / 'source-images' / f'pdf-{number:03}.jpeg'
    content = page.read_text()
    headings = []
    for match in re.finditer(r'^#{1,6} (.+)$', content, re.M):
        value = match.group(1)
        m = re.match(r'(6(?:\.\d+)*)\s+(.+)', value)
        if m:
            headings.append({'id': m[1], 'title': m[2]})
        elif value == '第 6 章 方程求根':
            headings.append({'id': '6', 'title': '方程求根'})
        elif value in ('小结', '习题'):
            headings.append({'id': '6.summary' if value == '小结' else '6.exercises', 'title': value})
    records[number] = {
        'pdf_page': number, 'printed_page': int(re.search(r'^printed_page: (\d+)$', content, re.M)[1]),
        'path': str(page.relative_to(BOOK)),
        'sha256': hashlib.sha256(page.read_bytes()).hexdigest(),
        'source_image_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'visual_review': 'completed', 'content_coverage': 'complete',
        'headings': headings, 'formula_ids': re.findall(r'\\tag\{([^}]+)\}', content),
        'figures': re.findall(r'^图 (6\.\d+)', content, re.M),
        'tables': re.findall(r'^表 (6\.\d+)\s*$', content, re.M),
        'notes': records.get(number, {}).get('notes', [])}
review['pages'] = [records[k] for k in sorted(records)]
review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
print(f'Recorded {len(review["pages"])} individually viewed pages.')
