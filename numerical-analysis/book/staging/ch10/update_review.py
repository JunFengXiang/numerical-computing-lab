"""Refresh hashes only for pages explicitly reviewed in this lane."""
import hashlib
import json
import re
from pathlib import Path

LANE = Path(__file__).resolve().parent
BOOK = LANE.parent.parent
SOURCE_SHA = '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def update(reviewed, notes=None, errata=None, validation=None):
    ann_path = LANE / 'annotations.json'
    annotations = json.loads(ann_path.read_text()) if ann_path.exists() else {}
    notes = notes or {int(k): v for k, v in annotations.get('page_notes', {}).items()}
    errata = annotations.get('source_errata', []) if errata is None else errata
    validation = annotations.get('validation_notes', []) if validation is None else validation
    entries = []
    for n in reviewed:
        path = LANE / 'pages' / f'pdf-{n}.md'
        text = path.read_text()
        headings = []
        for line in text.splitlines():
            match = re.match(r'^#{1,6}\s+(10(?:\.\d+)*)(?:\s|　)+(.*)$', line)
            if match:
                headings.append({'id': match[1], 'title': match[2]})
            elif line.startswith('# \\*第 10 章'):
                headings.append({'id': '10', 'title': '快速算法设计：快速 Walsh 变换', 'source_prefix_star': True})
            elif line.startswith('# 下篇'):
                headings.append({'id': '下篇', 'title': '高效算法设计', 'kind': 'part'})
            elif line.startswith('## 小结'):
                headings.append({'id': '10.summary', 'title': '小结'})
        entries.append({
            'pdf_page': n, 'printed_page': n - 13,
            'path': str(path.relative_to(BOOK)), 'sha256': sha(path),
            'source_image_sha256': sha(BOOK / f'source-images/pdf-{n}.jpeg'),
            'visual_review': 'completed', 'content_coverage': 'complete',
            'headings': headings,
            'formula_ids': re.findall(r'\\tag\{([^}]+)\}', text),
            'figures': re.findall(r'^图 (10\.\d+)$', text, re.M),
            'tables': re.findall(r'^表 (10\.\d+)$', text, re.M), 'notes': notes.get(n, [])})
    result = {'lane':'ch10', 'reviewer':'Codex agent ch10', 'human_review':False,
              'source_sha256':SOURCE_SHA, 'pages':entries, 'unresolved':[],
              'source_errata':errata or [], 'validation_notes':validation or []}
    (LANE / 'review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')

if __name__ == '__main__':
    import sys
    # Callers provide only pages actually opened and compared in this session.
    update([int(x) for x in sys.argv[1:]])
