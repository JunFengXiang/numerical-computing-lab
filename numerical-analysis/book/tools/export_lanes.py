#!/usr/bin/env python3
"""Build source-page QA LaTeX from complete primary-reviewed lanes, without promoting them."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import re
import subprocess
from audit_staging import ROOT, audit_lane, read_page, normalize_layout


def rewrite_local_links(body, original, destination):
    def replace(match):
        label, target = match.groups()
        clean = target.strip().strip('<>')
        if clean.startswith(('http:', 'https:', '#', 'mailto:')):
            return match[0]
        path = (original.parent/clean.split('#', 1)[0]).resolve()
        if not path.exists():
            return match[0]  # Not a link, e.g. adjacent mathematical brackets.
        return label+'('+path.as_posix()+')'
    # Existing local links only. Math tokens are unchanged unless they name a real file.
    return re.sub(r'(!?\[[^\n]*?\])\(([^\n]+?)\)', replace, body)


def export(lane, compile_pdf=False):
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    audit = audit_lane(lane, manifest, require_complete=True)
    if not audit['primary_review_complete']:
        raise ValueError(f'{lane["lane"]} not ready: {audit["errors"]}')
    work = ROOT/'.work/lane-latex'/lane['lane']
    work.mkdir(parents=True, exist_ok=True)
    assembled = ['---\ntitle: "数值分析第5版：'+lane['title']+'校对稿"\ndate: ""\n---\n\n',
                 '> 从逐页 Markdown 自动导出；校对中版本。来源页码指原扫描，排版页码另计。\n\n']
    sources = []
    for page in audit['checked_pages']:
        path = ROOT/page['path']
        meta, body, raw = read_page(path)
        body = normalize_layout(rewrite_local_links(body, path, work/'content.md'))
        n = page['pdf_page']
        assembled.append('\n\n\\clearpage\n\n')
        printed = str(page['printed_page']) if page['printed_page'] is not None else '无印刷页码'
        assembled.append(f'原书 PDF 页 {n}；{("印刷页码 "+printed) if page["printed_page"] is not None else printed}。\n\n')
        assembled.append(body+'\n\n')
        sources.append({'pdf_page': n, 'markdown': page['path'], 'sha256': page['sha256']})
    md = work/'content.md'
    md.write_text(''.join(assembled))
    header = work/'header.tex'
    header.write_text((ROOT/'tools/latex-header.tex').read_text())
    lua = work/'images.lua'
    lua.write_text((ROOT/'tools/latex-layout.lua').read_text())
    tex = work/'content.tex'
    subprocess.run(['pandoc', '--from=markdown-implicit_figures+tex_math_dollars', '--to=latex',
                    '--standalone', '--wrap=none', '-V', 'documentclass=ctexart',
                    '-V', 'classoption=fontset=fandol', '-V', 'fontsize=10pt',
                    '-V', 'colorlinks=true', '-V', 'geometry:margin=16mm',
                    '--include-in-header', str(header), '--lua-filter', str(lua),
                    str(md), '-o', str(tex)], check=True, cwd=work)
    record = {'lane': lane['lane'], 'updated_utc': datetime.now(timezone.utc).isoformat(),
              'sources': sources, 'standalone_tex': str(tex.relative_to(ROOT)),
              'tex_sha256': sha256(tex.read_bytes()).hexdigest(),
              'status': 'exported', 'render_visual_review': 'pending',
              'mathematical_correctness': 'not established by compilation'}
    if compile_pdf:
        for attempt in range(2):
            with (work/f'compile-{attempt+1}.stdout').open('w') as stream:
                proc = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                                       'content.tex'], cwd=work, stdout=stream, stderr=subprocess.STDOUT)
            if proc.returncode:
                break
        log = (work/'content.log').read_text(errors='replace')
        record.update(status='compiled' if proc.returncode == 0 else 'compile_failed',
                      warnings=[line for line in log.splitlines()
                                if any(s in line for s in ['Overfull', 'Missing character', 'LaTeX Error', '! '])])
        if proc.returncode:
            record['error_context'] = log[-5000:]
        else:
            import fitz
            pdf = work/'content.pdf'
            document = fitz.open(pdf)
            record.update(pdf=str(pdf.relative_to(ROOT)), pdf_sha256=sha256(pdf.read_bytes()).hexdigest(),
                          rendered_pages=len(document))
            render = work/'render'
            render.mkdir(exist_ok=True)
            for i, page in enumerate(document):
                page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(str(render/f'page-{i+1:03}.png'))
            # Contact sheets are navigation aids. Review dense math/tables at full size.
            from PIL import Image, ImageDraw
            for offset in range(0, len(document), 12):
                count = min(12, len(document)-offset)
                sheet = Image.new('RGB', (1280, 450*((count+3)//4)), '#dddddd')
                draw = ImageDraw.Draw(sheet)
                for j in range(count):
                    im = Image.open(render/f'page-{offset+j+1:03}.png').convert('RGB')
                    im.thumbnail((300, 420))
                    x, y = (j%4)*320, (j//4)*450
                    sheet.paste(im, (x+(320-im.width)//2, y+25))
                    draw.text((x+10, y+5), str(offset+j+1), fill='black')
                sheet.save(render/f'contact-{offset//12+1:02}.png')
    target = ROOT/'quality/latex-lanes'
    target.mkdir(exist_ok=True)
    (target/f'{lane["lane"]}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    return record


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--lane', required=True)
    p.add_argument('--compile', action='store_true')
    args = p.parse_args()
    lanes = json.loads((ROOT/'workflow/lanes.json').read_text())
    lane = next(l for l in lanes if l['lane'] == args.lane)
    record = export(lane, args.compile)
    print(json.dumps({k: v for k, v in record.items() if k != 'sources'}, ensure_ascii=False))
    if record['status'] == 'compile_failed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
