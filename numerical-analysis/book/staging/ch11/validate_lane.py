from pathlib import Path
import hashlib
import json
import re

lane = Path(__file__).resolve().parent
book = lane.parent.parent
review = json.loads((lane / 'review.json').read_text())
expected_pages = list(range(276, 294))
errors = []
seen = []
formula_ids = []
algorithms = []
figure_assets = []
for row in review['pages']:
    n = row['pdf_page']
    seen.append(n)
    path = book / row['path']
    raw = path.read_bytes()
    text = raw.decode()
    if hashlib.sha256(raw).hexdigest() != row['sha256']:
        errors.append(f'{n}: Markdown SHA256 mismatch')
    image_path = book / f'source-images/pdf-{n}.jpeg'
    if hashlib.sha256(image_path.read_bytes()).hexdigest() != row['source_image_sha256']:
        errors.append(f'{n}: source-image SHA256 mismatch')
    required = [f'pdf_page: {n}', f'printed_page: {n-13}',
                f'source_image: source-images/pdf-{n}.jpeg',
                f'source_sha256: {review["source_sha256"]}',
                'status: agent_reviewed_transcription', f'<!-- source-page: {n} -->']
    for value in required:
        if value not in text:
            errors.append(f'{n}: missing {value}')
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if not (path.parent / target).resolve().is_file():
            errors.append(f'{n}: missing link {target}')
    for target in re.findall(r'!\[[^\]]+\]\(([^)]+)\)', text):
        figure_assets.append(str((path.parent / target).resolve().relative_to(book)))
    if len(re.findall(r'^\$\$$', text, re.M)) % 2:
        errors.append(f'{n}: unmatched display-math fence')
    body_no_display_fences = re.sub(r'^\$\$$', '', text, flags=re.M)
    if len(re.findall(r'(?<!\\)\$', body_no_display_fences)) % 2:
        errors.append(f'{n}: unmatched inline-math delimiter')
    stack = []
    for action, environment in re.findall(r'\\(begin|end)\{([^}]+)\}', text):
        if action == 'begin':
            stack.append(environment)
        elif not stack or stack.pop() != environment:
            errors.append(f'{n}: mismatched math environment {environment}')
    if stack:
        errors.append(f'{n}: unclosed environments {stack}')
    depth = 0
    for char in re.findall(r'(?<!\\)[{}]', text):
        depth += 1 if char == '{' else -1
        if depth < 0:
            errors.append(f'{n}: prematurely closed LaTeX brace')
            break
    if depth:
        errors.append(f'{n}: unbalanced LaTeX braces ({depth})')
    formula_ids.extend(re.findall(r'\\tag\{([^}]+)\}', text))
    algorithms.extend(re.findall(r'^\*\*算法 ([\d.]+)\*\*', text, re.M))
    if '[待核:' in text:
        errors.append(f'{n}: unresolved glyph marker present')
if seen != expected_pages:
    errors.append(f'Page coverage mismatch: {seen}')
expected_formulas = ([f'11.2.{i}' for i in range(1, 6)] +
                     [f'11.3.{i}' for i in range(1, 12)] +
                     [f'11.4.{i}' for i in range(1, 4)])
if formula_ids != expected_formulas:
    errors.append('Numbered formula sequence differs from observed source sequence')
if algorithms != ['11.1','11.2','11.3','11.4','10.5']:
    errors.append(f'Algorithm source titles mismatch: {algorithms}')
if len(figure_assets) != 5:
    errors.append(f'Expected 5 source figure crops, found {len(figure_assets)}')
if not re.search(r'^# \\\*第 11 章', (lane/'pages/pdf-276.md').read_text(), re.M):
    errors.append('Source chapter star missing')
result = {
    'lane': 'ch11', 'scope': 'PDF276-293 / printed263-280',
    'status': 'passed' if not errors else 'failed',
    'checks': ['18 assigned pages present in order', 'printed-page metadata',
               'Markdown and source-image SHA256', 'local image and source links',
               'display and inline math delimiters', 'LaTeX environment and brace balance',
               '19 source formula identifiers', '5 source algorithm titles including original 10.5',
               '5 original figure crops', 'chapter prefix star', 'no unresolved glyph markers'],
    'numbered_formula_count': len(formula_ids),
    'source_algorithm_titles': algorithms, 'figure_assets': figure_assets,
    'source_errata_groups': len(review['source_errata']),
    'errors': errors,
    'limits': 'Structural checks do not establish mathematical correctness. All 18 pages were separately viewed against the original images; suspected source errors remain as printed and are annotated.'}
(lane/'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)
