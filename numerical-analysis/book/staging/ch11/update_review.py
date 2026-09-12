from pathlib import Path
import hashlib
import json
import re

base = Path(__file__).resolve().parent
book = base.parent.parent
manifest = base / 'review.json'
data = json.loads(manifest.read_text()) if manifest.exists() else {
    'lane': 'ch11', 'reviewer': 'Codex agent ch11', 'human_review': False,
    'source_sha256': '0e6f90896fb560e91f0dbf6855a166673aa908162f999b6c248b2fe6afacf4c2',
    'pages': [], 'unresolved': [], 'source_errata': [], 'validation_notes': []}
prior = {p['pdf_page']: p for p in data['pages']}
pages = []
for path in sorted((base / 'pages').glob('pdf-*.md')):
    text = path.read_text()
    n = int(re.search(r'^pdf_page: (\d+)$', text, re.M).group(1))
    printed = int(re.search(r'^printed_page: (\d+)$', text, re.M).group(1))
    headings = []
    for line in text.splitlines():
        m = re.match(r'^#{1,6} (11(?:\.\d+)*)[\s　]+(.+)$', line)
        if m: headings.append({'id':m.group(1), 'title':m.group(2)})
        m = re.match(r'^# \\\*第 11 章[\s　]+(.+)$', line)
        if m: headings.append({'id':'11', 'title':m.group(1), 'source_prefix_star':True})
        if line == '## 小结': headings.append({'id':'11.summary','title':'小结'})
        if line == '## 习题': headings.append({'id':'11.exercises','title':'习题'})
    item = {
        'pdf_page':n, 'printed_page':printed,
        'path':str(path.relative_to(book)),
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'source_image_sha256':hashlib.sha256((book / f'source-images/pdf-{n}.jpeg').read_bytes()).hexdigest(),
        'visual_review':'completed', 'content_coverage':'complete', 'headings':headings,
        'formula_ids':re.findall(r'\\tag\{([^}]+)\}',text),
        'figures':list(dict.fromkeys(re.findall(r'!\[图\s*(11\.\d+)',text))),
        'tables':list(dict.fromkeys(re.findall(r'表\s*(11\.\d+)',text))),
        'notes':prior.get(n,{}).get('notes',[])}
    pages.append(item)
data['pages'] = pages
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Saved {len(pages)} reviewed pages')
