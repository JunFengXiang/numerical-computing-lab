#!/usr/bin/env python3
"""Publish only complete, independently cross-reviewed lanes and assemble reader artifacts."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import re
import shutil
import os
import yaml
from audit_staging import ROOT, audit_lane, read_page, normalize_layout


def rewrite_links(body, original, destination, lane):
    def replace(match):
        label, target = match.groups()
        clean = target.strip().strip('<>')
        if clean.startswith(('http:', 'https:', '#', 'mailto:')):
            return match[0]
        src = (original.parent/clean.split('#', 1)[0]).resolve()
        if not src.exists():
            return match[0]
        src.relative_to(ROOT)
        staging_assets = ROOT/'staging'/lane/'assets'
        try:
            tail = src.relative_to(staging_assets)
            dest = ROOT/'verified/assets'/lane/tail
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
        except ValueError:
            dest = src
        rel = Path(os.path.relpath(dest, destination.parent)).as_posix()
        return label+'('+rel+')'
    return re.sub(r'(!?\[[^\n]*?\])\(([^\n]+?)\)', replace, body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    lanes = json.loads((ROOT/'workflow/lanes.json').read_text())
    reports = [audit_lane(lane, manifest, True) for lane in lanes]
    accepted = [(lane, audit) for lane, audit in zip(lanes, reports) if audit['cross_review_complete']]
    if args.require_complete and len(accepted) != len(lanes):
        missing = [audit['lane'] for audit in reports if not audit['cross_review_complete']]
        raise SystemExit(f'Cross-reviewed lanes still missing: {missing}')
    if not accepted:
        raise SystemExit('No complete cross-reviewed lane; nothing promoted.')
    target = ROOT/'verified/pages'
    target.mkdir(exist_ok=True)
    published, errata, reader = [], [], []
    is_complete = len(accepted) == len(lanes)
    reader_path = ROOT/'textbook.md'
    reader.append('# 数值分析（第5版）\n\n')
    reader.append('李庆扬、王能超、易大义。教材正文按原扫描页顺序转录；数学公式为 LaTeX。\n\n')
    reader.append(('全书页码已完整覆盖。' if is_complete else '当前仅含完成独立交叉复核的页，尚未全书完成。')+
                  '原书疑误保留原式并紧邻校注；原页链接用于回查。\n\n')
    reader.append('[章节索引](index/INDEX.md) · [公式索引](index/formulas.json) · [疑误与纠错](quality/ERRATA.md) · [状态](STATUS.json)\n\n')
    for lane, audit in accepted:
        name = lane['lane']
        primary = json.loads((ROOT/'staging'/name/'review.json').read_text())
        for item in primary.get('source_errata', []):
            errata.append({'lane': name, **item} if isinstance(item, dict) else {'lane': name, 'description': item})
        for page in sorted(audit['checked_pages'], key=lambda p: p['pdf_page']):
            src = ROOT/page['path']
            meta, body, raw = read_page(src)
            n = page['pdf_page']
            dest = target/src.name
            normalized = normalize_layout(rewrite_links(body, src, dest, name))
            # Links may change; mathematical source must remain byte-identical.
            math_pattern = r'(?<!\\)\$\$.*?(?<!\\)\$\$|(?<!\\)\$[^$]*?(?<!\\)\$'
            if re.findall(math_pattern, body, re.S) != re.findall(math_pattern, normalized, re.S):
                raise ValueError(f'Link normalization altered math on page {n}')
            meta.update(status='independently_agent_verified_transcription',
                        review_record='../../quality/pages-review.json',
                        primary_transcription=page['path'])
            dest.write_text('---\n'+yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)+'---\n'+normalized)
            item = {**page, 'canonical_path': str(dest.relative_to(ROOT)),
                    'canonical_sha256': sha256(dest.read_bytes()).hexdigest(),
                    'lane': name, 'primary_review': f'staging/{name}/review.json',
                    'cross_review': f'staging/{name}/cross-review.json'}
            published.append(item)
            root_body = normalize_layout(rewrite_links(body, src, reader_path, name))
            reader.append(f'\n\n<a id="pdf-{n:03}"></a>\n\n')
            printed = '印刷页码 '+str(page['printed_page']) if page['printed_page'] is not None else '无印刷页码'
            reader.append(f'> 来源：原书 PDF 页 {n}；{printed}。\n\n')
            reader.append(root_body+'\n\n')
    reader_path.write_text(''.join(reader))
    receipt = {'updated_utc': datetime.now(timezone.utc).isoformat(), 'human_review': False,
               'source_sha256': manifest['source_sha256'], 'pages': published,
               'complete_source_page_coverage': is_complete,
               'scope': 'Two agents visually compared each listed page; structural checks do not prove mathematical correctness.',
               'textbook_markdown': 'textbook.md', 'textbook_sha256': sha256(reader_path.read_bytes()).hexdigest(),
               'normalizations': ['YAML status/review pointers', 'relative local links', 'blank line before Markdown headings', 'PDF 320 answer 9 paragraph breaks between printed parameter groups; math unchanged'],
               'math_preservation_check': 'byte-identical LaTeX before/after link normalization'}
    (ROOT/'quality/pages-review.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    (ROOT/'quality/source-errata.json').write_text(json.dumps({'source_sha256': manifest['source_sha256'],
                         'source_errata': errata}, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'published_pages': len(published), 'complete_coverage': is_complete,
                      'source_errata': len(errata), 'reader': str(reader_path)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
