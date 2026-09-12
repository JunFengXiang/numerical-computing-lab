#!/usr/bin/env python3
"""Locate original headings and equations in page transcriptions; publish only reviewed full coverage."""
from pathlib import Path
from bisect import bisect_right
from hashlib import sha256
import argparse
import json
import re
import yaml
from audit_staging import ROOT, read_page
from assemble_book import rewrite_links


def page_annotations(body):
    """Copy complete marked agent notes, retaining their original mathematical text."""
    lines = body.splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        heading = re.match(r'^(#{1,6})\s+.*(?:校注|原书疑误)', line)
        if heading:
            j = i + 1
            while j < len(lines) and not re.match(r'^#{1,6}\s+', lines[j]):
                j += 1
            result.append(''.join(lines[i:j]).strip())
            i = j
        elif line.startswith('>'):
            j = i + 1
            while j < len(lines) and lines[j].startswith('>'):
                j += 1
            block = ''.join(lines[i:j]).strip()
            if '校注' in block or '原书疑误' in block:
                result.append(block)
            i = j
        else:
            i += 1
    return result


def locate(pages, entries):
    combined, boundaries, occurrences = [], [], []
    offset = 0
    current_chapter = None
    valid = {e['id'] for e in entries}
    for page in pages:
        path = ROOT/page['path']
        _, body, _ = read_page(path)
        boundaries.append({'pdf_page': page['pdf_page'], 'start': offset, 'path': page['path']})
        cursor = offset
        for line in body.splitlines(keepends=True):
            h = re.match(r'^#{1,6}\s+(.+?)\s*\n?$', line)
            if h:
                title = h[1].strip()
                clean = title.lstrip('\\* ').strip()
                if clean.endswith(('（续）', '(续)', '（续前页）')):
                    cursor += len(line)
                    continue
                ch = re.match(r'^第\s*(\d+)\s*章\s*(.*)', clean)
                sec = re.match(r'^(\d+(?:\.\d+){1,2})\s+(.+)', clean)
                sid = None
                if ch and page['pdf_page'] < 318:
                    sid = current_chapter = ch[1]
                elif sec:
                    sid = sec[1]
                    current_chapter = sid.split('.')[0]
                elif clean == '小结' and current_chapter:
                    sid = current_chapter+'.summary'
                elif clean in ['习题', '习题与思考题'] and current_chapter:
                    sid = current_chapter+'.exercises'
                elif clean == '部分习题答案':
                    sid = 'answers'
                elif clean == '参考文献':
                    sid = 'references'
                if sid in valid:
                    occurrences.append({'id': sid, 'heading': clean, 'raw_heading': title,
                                        'pdf_page': page['pdf_page'], 'offset': cursor,
                                        'source_prefix_star': bool(re.match(r'^\\?\*', title.lstrip()))})
            cursor += len(line)
        combined.append(body+'\n\n')
        offset += len(body)+2
    return ''.join(combined), boundaries, occurrences


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--diagnose-staging', action='store_true')
    args = parser.parse_args()
    old = json.loads((ROOT/'index/sections.json').read_text())
    entries = old['entries']
    pages = []
    if args.diagnose_staging:
        for file in (ROOT/'staging').glob('*/review.json'):
            for p in json.loads(file.read_text()).get('pages', []):
                if 14 <= p['pdf_page'] <= 321:
                    pages.append(p)
    else:
        review = json.loads((ROOT/'quality/pages-review.json').read_text())
        if not review['complete_source_page_coverage']:
            raise SystemExit('Full source-page cross-review required before replacing section index.')
        for p in review['pages']:
            if 14 <= p['pdf_page'] <= 321:
                pages.append({**p, 'path': p['canonical_path']})
    pages.sort(key=lambda p:p['pdf_page'])
    text, boundaries, headings = locate(pages, entries)
    grouped = {}
    for h in headings:
        grouped.setdefault(h['id'], []).append(h)
    missing = [e['id'] for e in entries if e['id'] not in grouped]
    duplicate = {sid:[h['pdf_page'] for h in hs] for sid,hs in grouped.items() if len(hs)>1}
    report = {'scope': 'staging diagnosis' if args.diagnose_staging else 'verified full book',
              'source_pages_available': len(pages), 'headings_located':len(headings),
              'missing_headings': missing, 'duplicate_headings':duplicate,
              'headings':headings}
    (ROOT/'quality/headings-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='headings'},ensure_ascii=False))
    if args.diagnose_staging:
        return
    if missing or duplicate:
        raise SystemExit('Heading coverage must be resolved before index publication.')
    destination = ROOT/'verified/sections'
    destination.mkdir(exist_ok=True)
    position_map = {p['pdf_page']:p for p in pages}
    source_errata = json.loads((ROOT/'quality/source-errata.json').read_text())['source_errata']
    starts = [b['start'] for b in boundaries]
    enriched, formulas, context_audit = [], [], []
    page_lookup = {b['pdf_page']:b for b in boundaries}
    # Formula locations come from actual page math, independent of section ID namespace.
    for page in pages:
        _, body, _ = read_page(ROOT/page['path'])
        for match in re.finditer(r'\$\$(.*?)\$\$',body,re.S):
            block=match[1]
            tags=re.findall(r'\\tag\{([^}]+)\}',block)
            absolute_offset=page_lookup[page['pdf_page']]['start']+match.start()
            prior=[h for h in headings if h['offset']<=absolute_offset]
            owner=prior[-1]['id'] if prior else None
            nearby=[e for e in source_errata if e.get('pdf_page')==page['pdf_page']]
            for tag in tags:
                formulas.append({'id':tag,'kind':'formula','latex':block.strip(),
                                 'section_id':owner,'adjacent_source_errata':nearby,
                                 'source_pdf_pages':[page['pdf_page']],
                                 'markdown':page['path'],'verification_status':'independently_agent_verified_transcription'})
    for entry in entries:
        h=grouped[entry['id']][0]
        end=len(text)
        for nxt in headings:
            if nxt['offset']<=h['offset']:
                continue
            if not nxt['id'].startswith(entry['id']+'.'):
                end=nxt['offset']
                # A new source page has a source-image link and HTML marker before
                # its first heading; that empty prefix is not part of the prior section.
                boundary = boundaries[bisect_right(starts, end)-1]
                prefix = text[boundary['start']:end]
                prefix = re.sub(r'<!--.*?-->', '', prefix, flags=re.S)
                prefix = re.sub(r'^\s*\[[^\n]*\]\([^\n]*source-images/[^\n]*\)\s*$', '', prefix, flags=re.M)
                if not prefix.strip():
                    end=boundary['start']
                break
        selected=[b for b in boundaries if b['start']<end and
                  (b is boundaries[-1] or boundaries[boundaries.index(b)+1]['start']>h['offset'])]
        page_ids=[b['pdf_page'] for b in selected]
        body_parts=[]
        for b in selected:
            source=ROOT/b['path']
            _, body, _ = read_page(source)
            lo=max(0,h['offset']-b['start']);hi=min(len(body),end-b['start'])
            fragment=body[lo:hi]
            dest=destination/(entry['id']+'.md')
            fragment=rewrite_links(fragment,source,dest,'')
            body_parts.append(f'\n\n<!-- source-page: {b["pdf_page"]} -->\n\n'+fragment)
        nearby=[e for e in source_errata if e.get('pdf_page') in page_ids or
                bool(set(e.get('pdf_pages',[])) & set(page_ids))]
        # Page-end corrections may follow the next section heading on the same page.
        # A section-only cut must carry those notes too, explicitly as page context.
        main_body = ''.join(body_parts)
        missing_notes = []
        for b in selected:
            source = ROOT/b['path']
            _, full_body, _ = read_page(source)
            notes = page_annotations(full_body)
            page_records = [e for e in nearby if e.get('pdf_page') == b['pdf_page'] or
                            b['pdf_page'] in e.get('pdf_pages', [])]
            if page_records and not notes:
                raise ValueError(f'Page {b["pdf_page"]}: errata records without extractable complete notes')
            copied = []
            for note in notes:
                normalized = rewrite_links(note, source, dest, '')
                if normalized not in main_body:
                    copied.append(normalized)
            if copied:
                ids = ', '.join(e['id'] for e in page_records if e.get('id'))
                missing_notes.append(f'\n\n### 原书 PDF 页 {b["pdf_page"]} 的校注\n\n'
                    f'[完整原页转录](../pages/pdf-{b["pdf_page"]:03}.md) · '
                    f'[原页图像](../../source-images/pdf-{b["pdf_page"]:03}.jpeg)\n\n'
                    +(f'校注记录：{ids}。\n\n' if ids else '')+'\n\n'.join(copied))
            context_audit.append({'section_id':entry['id'], 'pdf_page':b['pdf_page'],
                                  'page_note_blocks':len(notes), 'appended_note_blocks':len(copied),
                                  'all_notes_present':all(rewrite_links(n,source,dest,'') in
                                    main_body+'\n'.join(copied) for n in notes)})
        if missing_notes:
            body_parts.append('\n\n---\n\n## 相关原页校注（agent 补充）\n\n'
                '以下校注来自本节覆盖的原页，可能也涉及同页相邻小节；原文照录与校正说明分开保留。'
                +'\n'.join(missing_notes)+'\n')
        if nearby:
            body_parts.append('\n\n## 本节覆盖原页的校注记录\n\n'
                '下列记录按原页关联，含同页相邻小节的校注；计算时同时读取上文校注和完整原页。\n\n'
                +'\n'.join(f'- `{e["id"]}`：原书 PDF 页 '
                            +', '.join(map(str,e.get('pdf_pages',[e.get('pdf_page')])))
                    for e in nearby if e.get('id'))+'\n')
        meta={'section_id':entry['id'],'title':entry['title'],
              'status':'independently_agent_verified_transcription','pdf_pages':page_ids,
              'printed_pages':[position_map[n].get('printed_page') for n in page_ids],
              'source_sha256':review['source_sha256'],'review_record':'../../quality/pages-review.json',
              'source_errata':[e.get('id') for e in nearby if e.get('id')]}
        dest.write_text('---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False)+'---\n'+''.join(body_parts))
        record={**entry,'body_status':'independently_agent_verified_transcription',
                'verified_markdown':str(dest.relative_to(ROOT)),
                'verified_latex':str(dest.with_suffix('.tex').relative_to(ROOT)),
                'pdf_pages':page_ids,'printed_pages':meta['printed_pages'],
                'pdf_page_start_hint':h['pdf_page'],'locator_status':'body_start_visually_verified',
                'body_heading':h['heading'],'body_prefix_star':h['source_prefix_star'],
                'source_errata':meta['source_errata'],'adjacent_source_errata':nearby,
                'markdown_sha256':sha256(dest.read_bytes()).hexdigest(),
                'use_rule':'Read adjacent agent errata annotations before mathematical use.'}
        enriched.append(record)
    # Use deepest section that contains each equation's source position.
    for formula in formulas:
        n=formula['source_pdf_pages'][0]
        candidates=[e for e in enriched if n in e['pdf_pages'] and e['kind']=='section']
        formula['page_overlapping_sections']=[e['id'] for e in candidates]
        formula['use_rule']='Original printed formulas can have source errors; read all adjacent errata before use.'
    old.update(entries=enriched,note='所有正文按原页逐页转录并经独立 agent 交叉复核。章节与公式编号分属不同命名空间；原书疑误保留并紧邻校注。')
    (ROOT/'index/sections.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'index/formulas.json').write_text(json.dumps({'scope':'independently reviewed full book','formulas':formulas},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'quality/section-context-checks.json').write_text(json.dumps({
        'status':'pass' if all(x['all_notes_present'] for x in context_audit) else 'fail',
        'checks':context_audit,
        'rule':'Every marked agent note on every overlapping original page is included; extra page notes are explicitly separated.'
    },ensure_ascii=False,indent=2)+'\n')
    rows=['# 章节索引\n\n全书正文经逐页转录及独立 agent 交叉复核；使用数学结论前读取相邻校注。\n\n',
          '| 编号 | 标题 | 原书页 | PDF页 |\n|---|---|---|---|\n']
    for e in enriched:
        rows.append(f'| {e["id"]} | [{e["title"]}](../{e["verified_markdown"]}) | {e["printed_pages"][0]} | {e["pdf_pages"][0]} |\n')
    (ROOT/'index/INDEX.md').write_text(''.join(rows))
    print(json.dumps({'section_files':len(enriched),'formula_records':len(formulas)},ensure_ascii=False))


if __name__=='__main__':
    main()
