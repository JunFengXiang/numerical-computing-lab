#!/usr/bin/env python3
"""Check source-bound transcription receipts; structural checks are not visual review."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read_page(path):
    raw = path.read_text()
    match = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
    if not match:
        raise ValueError('missing YAML front matter')
    return yaml.safe_load(match[1]), raw[match.end():], raw


def math_blocks(body):
    return re.findall(r'(?<!\\)\$\$(.*?)(?<!\\)\$\$', body, re.S)


def normalize_layout(body):
    """Add blank space before ATX headings without changing text or mathematics."""
    if re.search(r'source-page:\s*320\b', body):
        body = re.sub(r'(达到精度要求[， ]*)(?=\$\\boldsymbol)', r'\1\n\n', body)
        body = body.replace('，$\\omega=', '，\n\n$\\omega=')
    lines, fence, math = [], False, False
    for line in body.splitlines(keepends=True):
        if line.lstrip().startswith(('```', '~~~')):
            fence = not fence
        if not fence and not math and re.match(r'^#{1,6}\s', line) and lines and lines[-1].strip():
            lines.append('\n')
        lines.append(line)
        if not fence:
            math = bool(math ^ (len(re.findall(r'(?<!\\)\$\$', line)) % 2))
    return ''.join(lines)


def audit_lane(lane, manifest, require_complete=False):
    name = lane['lane']
    directory = ROOT/'staging'/name
    receipt_path = directory/'review.json'
    errors, warnings, checked = [], [], []
    expected = set(range(lane['start'], lane['end']+1))
    result = {'lane': name, 'expected_pages': sorted(expected), 'checked_pages': checked,
              'errors': errors, 'warnings': warnings, 'structural_pass': False,
              'primary_review_complete': False, 'cross_review_complete': False}
    if not receipt_path.exists():
        warnings.append('primary receipt not yet written')
        return result
    try:
        receipt = json.loads(receipt_path.read_text())
    except Exception as exc:
        errors.append(f'cannot read receipt: {exc}')
        return result
    if receipt.get('source_sha256') != manifest['source_sha256']:
        errors.append('source PDF hash does not match')
    if receipt.get('human_review') is not False:
        errors.append('human_review must explicitly be false')
    seen = set()
    for page in receipt.get('pages', []):
        n = page.get('pdf_page')
        local_errors = []
        if n not in expected or n in seen:
            errors.append(f'invalid/duplicate/out-of-scope page: {n}')
            continue
        seen.add(n)
        expected_file = directory/'pages'/f'pdf-{n:03}.md'
        path = ROOT/page.get('path', '')
        if path != expected_file or not path.is_file():
            errors.append(f'page {n}: missing or wrong file path')
            continue
        checksum = digest(path)
        if checksum != page.get('sha256'):
            local_errors.append('receipt hash stale')
        source = manifest['pages'][n-1]
        if page.get('source_image_sha256') != source['image_sha256']:
            local_errors.append('source image receipt hash mismatch')
        if digest(ROOT/source['image']) != source['image_sha256']:
            local_errors.append('source image bytes changed')
        if page.get('visual_review') != 'completed':
            local_errors.append('visual review not completed')
        if page.get('content_coverage') != 'complete':
            local_errors.append('page content not complete')
        try:
            meta, body, raw = read_page(path)
            if meta.get('pdf_page') != n:
                local_errors.append('metadata PDF page mismatch')
            if meta.get('printed_page') != page.get('printed_page'):
                local_errors.append('printed-page metadata/receipt mismatch')
            if meta.get('source_sha256') != manifest['source_sha256']:
                local_errors.append('metadata source hash mismatch')
            if meta.get('source_image') != source['image']:
                local_errors.append('metadata source image mismatch')
            if not re.search(r'<!--\s*source-page:\s*'+str(n)+r'\s*-->', body):
                local_errors.append('source page marker absent')
            if re.search(r'\[待核[:：]|TODO|TBD|待转录|未转录|待辨认', body):
                local_errors.append('unresolved placeholder in page')
            # Even delimiters are necessary; full LaTeX compilation follows separately.
            display_count = len(re.findall(r'(?<!\\)\$\$', body))
            if display_count % 2:
                local_errors.append('unpaired display math delimiters')
            inline = re.sub(r'(?<!\\)\$\$.*?(?<!\\)\$\$', '', body, flags=re.S)
            if len(re.findall(r'(?<!\\)\$', inline)) % 2:
                local_errors.append('unpaired inline math delimiters')
            actual_tags = re.findall(r'\\tag\{([^}]+)\}', body)
            recorded_tags = [str(tag) for tag in page.get('formula_ids', [])]
            if sorted(actual_tags) != sorted(recorded_tags):
                local_errors.append(f'formula IDs mismatch: actual={actual_tags}, receipt={recorded_tags}')
            for block in math_blocks(body):
                opens = re.findall(r'\\begin\{([^}]+)\}', block)
                closes = re.findall(r'\\end\{([^}]+)\}', block)
                if sorted(opens) != sorted(closes):
                    local_errors.append('unbalanced math environments')
            link_text = re.sub(r'(?<!\\)\$\$.*?(?<!\\)\$\$', '', body, flags=re.S)
            link_text = re.sub(r'(?<!\\)\$[^$]*?(?<!\\)\$', '', link_text)
            for link in re.findall(r'!?\[[^\n]*?\]\(([^\n]+?)\)', link_text):
                link = link.strip().split(' "', 1)[0].strip('<>')
                if link.startswith(('http:', 'https:', '#', 'mailto:')):
                    continue
                target = (path.parent/link.split('#', 1)[0]).resolve()
                if not target.exists():
                    local_errors.append(f'broken local link: {link}')
            checked.append({'pdf_page': n, 'path': str(path.relative_to(ROOT)),
                            'sha256': checksum, 'printed_page': page.get('printed_page'),
                            'headings': page.get('headings', []), 'formula_ids': actual_tags,
                            'figures': page.get('figures', []), 'tables': page.get('tables', []),
                            'pass': not local_errors})
        except Exception as exc:
            local_errors.append(f'page parse failed: {exc}')
        errors.extend(f'page {n}: {e}' for e in local_errors)
    missing = sorted(expected-seen)
    result['missing_pages'] = missing
    if missing:
        (errors if require_complete else warnings).append(f'pages not yet covered: {missing}')
    unresolved = receipt.get('unresolved', [])
    if unresolved:
        errors.append(f'unresolved recognition issues: {unresolved}')
    result['primary_receipt_sha256'] = digest(receipt_path)
    result['source_errata_count'] = len(receipt.get('source_errata', []))
    result['primary_review_complete'] = not missing and not errors
    result['structural_pass'] = not errors
    cross_path = directory/'cross-review.json'
    if cross_path.exists():
        cross = json.loads(cross_path.read_text())
        cross_pages = {p['pdf_page']: p for p in cross.get('pages', [])}
        expected_reviewer = receipt.get('reviewer', '')
        independent = bool(cross.get('reviewer')) and cross.get('reviewer') != expected_reviewer
        passed = independent and cross.get('status') == 'pass' and not cross.get('unresolved')
        if not independent:
            warnings.append('cross review is not explicitly independent')
        for p in checked:
            cp = cross_pages.get(p['pdf_page'], {})
            passed = passed and cp.get('sha256') == p['sha256'] and cp.get('source_visual_review') == 'completed'
        result['cross_review_complete'] = bool(passed and set(cross_pages) == expected and result['primary_review_complete'])
        result['cross_review_status'] = cross.get('status')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lane')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    lanes = json.loads((ROOT/'workflow/lanes.json').read_text())
    if args.lane:
        lanes = [lane for lane in lanes if lane['lane'] == args.lane]
        if not lanes:
            raise SystemExit('Unknown lane')
    reports = [audit_lane(lane, manifest, args.require_complete) for lane in lanes]
    output = {'updated_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'structural integrity; visual judgments supplied by named agents',
              'lanes': reports,
              'primary_pages': sum(len(l['checked_pages']) for l in reports),
              'passing_primary_pages': sum(sum(p['pass'] for p in l['checked_pages']) for l in reports),
              'primary_complete_lanes': [l['lane'] for l in reports if l['primary_review_complete']],
              'cross_review_complete_lanes': [l['lane'] for l in reports if l['cross_review_complete']]}
    path = ROOT/'quality'/('staging-audit-'+args.lane+'.json' if args.lane else 'staging-audit.json')
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'lanes'}, ensure_ascii=False))
    for lane in reports:
        if lane['errors']:
            print(json.dumps({'lane': lane['lane'], 'errors': lane['errors']}, ensure_ascii=False))
    if args.require_complete and any(not l['primary_review_complete'] for l in reports):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
