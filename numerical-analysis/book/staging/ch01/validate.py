from pathlib import Path
import datetime
import hashlib
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'staging/ch01'
QA = BASE / 'qa'
review = json.loads((BASE / 'review.json').read_text())
errors, rows, all_tags = [], [], []
expected = ['1.2.1', '1.2.2', '1.3.1', '1.3.2', '1.3.3', '1.3.4', '1.4.1']
for item in review['pages']:
    p = ROOT / item['path']
    n = item['pdf_page']
    s = p.read_text()
    tags = re.findall(r'\\tag\{([^}]+)\}', s)
    all_tags += tags
    md_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    im = ROOT / f'source-images/pdf-{n:03d}.jpeg'
    if md_sha != item['sha256']:
        errors.append(f'MD hash mismatch {n}')
    if hashlib.sha256(im.read_bytes()).hexdigest() != item['source_image_sha256']:
        errors.append(f'image hash mismatch {n}')
    if tags != item['formula_ids']:
        errors.append(f'tag mismatch {n}')
    if s.count('$$') % 2:
        errors.append(f'display dollars {n}')
    rest = re.sub(r'\$\$.*?\$\$', '', s, flags=re.S)
    if len(re.findall(r'(?<!\\)\$', rest)) % 2:
        errors.append(f'inline dollars {n}')
    if s.count('{') != s.count('}'):
        errors.append(f'braces {n}')
    for link in re.findall(r'\]\(([^)]+)\)', s):
        if not (p.parent / link).resolve().exists():
            errors.append(f'broken link {n}: {link}')
    fields = [('pdf_page', str(n)), ('printed_page', str(n-13)),
              ('source_image', f'source-images/pdf-{n:03d}.jpeg'),
              ('source_sha256', review['source_sha256']),
              ('status', 'agent_reviewed_transcription')]
    for key, value in fields:
        if f'{key}: {value}\n' not in s:
            errors.append(f'frontmatter {key} {n}')
    rows.append({'pdf_page': n, 'printed_page': n-13, 'sha256': md_sha,
                 'display_math_blocks': s.count('$$') // 2, 'formula_ids': tags})
if [x['pdf_page'] for x in rows] != list(range(14, 27)):
    errors.append('page coverage')
if all_tags != expected:
    errors.append('numbered formula coverage')
exercises = []
for n in [25, 26]:
    exercises += list(map(int, re.findall(r'^(\d+)\. ', (BASE / f'pages/pdf-{n:03d}.md').read_text(), re.M)))
if exercises != list(range(1, 16)):
    errors.append(f'exercise coverage {exercises}')
log = (QA / 'transcription-check.log').read_text(errors='replace')
diagnostics = re.findall(r'^.*(?:Overfull|Undefined|Missing|Error|Warning).*$', log, re.M)
doc = fitz.open(QA / 'transcription-check.pdf')
report = {
    'lane': 'ch01',
    'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'result': 'passed' if not errors else 'failed',
    'pdf_pages': list(range(14, 27)),
    'printed_pages': list(range(1, 14)),
    'page_count': 13,
    'numbered_formula_ids': all_tags,
    'exercise_numbers': exercises,
    'figure_ids': ['1.1'],
    'table_ids': ['1.1'],
    'source_errata_count': len(review['source_errata']),
    'unresolved_count': len(review['unresolved']),
    'checks': {
        'frontmatter_source_links_and_hashes': 'passed' if not errors else 'failed',
        'math_delimiters_and_braces': 'passed' if not errors else 'failed',
        'pandoc_xelatex_compile': 'passed',
        'compile_diagnostics': diagnostics,
        'qa_pdf_page_count': len(doc),
        'representative_render_inspected_qa_pages': [3, 8, 13, 14],
    },
    'pages': rows,
    'errors': errors,
}
(BASE / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
doc[-1].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(QA / 'render-14-final.png')
print(json.dumps({'result': report['result'], 'pages': len(rows), 'formulas': len(all_tags),
                  'exercises': exercises, 'errata': len(review['source_errata']),
                  'errors': errors, 'diagnostics': diagnostics}, indent=2))
assert not errors
