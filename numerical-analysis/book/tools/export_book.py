#!/usr/bin/env python3
"""Build a portable master from visually reviewed lane TeX, checking every math span."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import re
import subprocess
import fitz

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def math_nodes(value):
    result = []
    if isinstance(value, dict):
        if value.get('t') == 'Math':
            result.append(value['c'][1])
        else:
            for v in value.values():
                result.extend(math_nodes(v))
    elif isinstance(value, list):
        for v in value:
            result.extend(math_nodes(v))
    return result


def math_key(value):
    return re.sub(r'\s+', '', value.replace(r'\allowbreak', ''))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--compile', action='store_true')
    args = p.parse_args()
    work = ROOT/'.work/full-latex'
    work.mkdir(parents=True, exist_ok=True)
    target = ROOT/'verified/latex-lanes'
    target.mkdir(exist_ok=True)
    lanes = json.loads((ROOT/'workflow/lanes.json').read_text())
    review = json.loads((ROOT/'quality/pages-review.json').read_text())
    if not review['complete_source_page_coverage']:
        raise SystemExit('322 cross-reviewed pages required')
    # Pandoc collects the union of packages needed by the entire Markdown book.
    subprocess.run(['pandoc', '--from=markdown-implicit_figures+tex_math_dollars', '--to=latex',
                    '--standalone', '--wrap=none', '-V', 'documentclass=ctexart',
                    '-V', 'classoption=fontset=fandol', '-V', 'fontsize=10pt',
                    '-V', 'colorlinks=true', '-V', 'geometry:margin=16mm',
                    '-M', 'title=数值分析（第5版）：Markdown 与 LaTeX 核对版',
                    '--include-in-header', str(ROOT/'tools/latex-header.tex'),
                    str(ROOT/'textbook.md'), '-o', str(work/'package-template.tex')],
                   cwd=ROOT, check=True)
    preamble = (work/'package-template.tex').read_text().split(r'\begin{document}', 1)[0]
    parts, receipts = [], []
    for lane in lanes:
        name = lane['lane']
        q = json.loads((ROOT/f'quality/latex-lanes/{name}.json').read_text())
        v = json.loads((ROOT/f'quality/latex-lanes/{name}-visual.json').read_text())
        if q['status'] != 'compiled' or v['status'] != 'pass' or q['pdf_sha256'] != v['pdf_sha256']:
            raise SystemExit(f'{name}: current visual pass required')
        tex = ROOT/q['standalone_tex']
        if digest(tex) != q['tex_sha256'] or digest(ROOT/q['pdf']) != q['pdf_sha256']:
            raise SystemExit(f'{name}: lane artifact changed since review')
        for src in q['sources']:
            if digest(ROOT/src['markdown']) != src['sha256']:
                raise SystemExit(f'{name}: source changed')
        body = tex.read_text().split(r'\begin{document}', 1)[1].rsplit(r'\end{document}', 1)[0]
        body = r'\clearpage'+body.split(r'\clearpage', 1)[1]
        # Canonical image assets are byte copies of the reviewed staging images.
        for other in lanes:
            old = f'{ROOT}/staging/{other["lane"]}/assets/'
            body = body.replace(old, f'verified/assets/{other["lane"]}/')
        body = body.replace(str(ROOT)+'/', '')
        body = re.sub(r'\\label\{([^}]+)\}', lambda m:r'\label{'+name+'-'+m[1]+'}', body)
        body = re.sub(r'\\hyperlink\{([^}]+)\}', lambda m:r'\hyperlink{'+name+'-'+m[1]+'}', body)
        out = target/(name+'.tex')
        out.write_text('% Generated from reviewed lane; compile via book/textbook.tex.\n'+body)
        parts.append(body)
        receipts.append({'lane':name, 'tex':str(out.relative_to(ROOT)), 'tex_sha256':digest(out),
                         'reviewed_pdf':q['pdf'], 'reviewed_pdf_sha256':q['pdf_sha256'],
                         'reviewed_pages':q['rendered_pages']})
    # Assert exact mathematical contents and order, not just counts or compilation.
    ast = json.loads(subprocess.check_output(['pandoc', '--from=markdown-implicit_figures+tex_math_dollars',
                                             '--to=json', str(ROOT/'textbook.md')]))
    expected = [math_key(x) for x in math_nodes(ast['blocks'])]
    actual = [math_key(a or b) for a,b in re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', ''.join(parts), re.S)]
    if expected != actual:
        mismatch = next((i for i,(a,b) in enumerate(zip(expected,actual)) if a != b), min(len(expected),len(actual)))
        (work/'math-mismatch.json').write_text(json.dumps({'expected_count':len(expected), 'actual_count':len(actual),
              'first_mismatch':mismatch, 'expected':expected[max(0,mismatch-1):mismatch+2],
              'actual':actual[max(0,mismatch-1):mismatch+2]},ensure_ascii=False,indent=2))
        raise SystemExit(f'Math mismatch at {mismatch}; see .work/full-latex/math-mismatch.json')
    body = (r'\begin{document}'+'\n'+r'\maketitle'+'\n\n'
            '李庆扬、王能超、易大义。原扫描 322 页完整转录，经逐页 agent 核验和独立交叉复核。'
            '原书疑误保留，并附明确校注；来源页码指原 PDF，排版页码另计。\n\n'
            +r'\href{index/INDEX.md}{章节索引}；\href{quality/ERRATA.md}{疑误与条件校注}。'+'\n\n'
            +'\n'.join(r'\input{verified/latex-lanes/'+l['lane']+'.tex}' for l in lanes)
            +'\n'+r'\end{document}'+'\n')
    master = ROOT/'textbook.tex'
    master.write_text('% Generated; edit verified Markdown and rebuild, never formulas in this file.\n'+preamble+body)
    report = {'created_utc':datetime.now(timezone.utc).isoformat(), 'status':'exported',
              'master_tex':'textbook.tex', 'master_tex_sha256':digest(master),
              'source_markdown':'textbook.md', 'source_markdown_sha256':digest(ROOT/'textbook.md'),
              'math_spans_checked':len(expected), 'math_sequence_preserved':True,
              'normalizations':['relative canonical image links', 'unique lane-prefixed labels',
                                'lane cover sheets replaced with one book cover; source pages unchanged',
                                'line-breaking commands excluded from math token comparison'],
              'lanes':receipts, 'human_review':False}
    if args.compile:
        for run in range(2):
            with (work/f'compile-{run+1}.stdout').open('w') as out:
                proc = subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
                                       '-output-directory='+str(work), str(master)],
                                      cwd=ROOT, stdout=out, stderr=subprocess.STDOUT)
            if proc.returncode:
                break
        log = (work/'textbook.log').read_text(errors='replace')
        report.update(status='compiled' if proc.returncode == 0 else 'compile_failed',
                      warnings=[l for l in log.splitlines() if any(t in l for t in ['Overfull', 'Missing character', '! '])])
        if proc.returncode:
            report['error_context']=log[-6000:]
        else:
            pdf_path = ROOT/'textbook.pdf'
            pdf_path.write_bytes((work/'textbook.pdf').read_bytes())
            pdf = fitz.open(pdf_path)
            report.update(pdf='textbook.pdf', pdf_sha256=digest(pdf_path), rendered_pages=len(pdf))
            # Every source-content page should render like its reviewed lane. ctexart
            # puts the running page number above y=30pt; source content begins at 45pt.
            pos, changes, checks = 1, [], []
            for r in receipts:
                original = fitz.open(ROOT/r['reviewed_pdf'])
                for i in range(1,len(original)):
                    if pos >= len(pdf):
                        raise ValueError('Full book ended before reviewed content')
                    clip=fitz.Rect(0,30,original[i].rect.width,original[i].rect.height)
                    a=original[i].get_pixmap(matrix=fitz.Matrix(1,1),clip=clip,colorspace=fitz.csGRAY)
                    b=pdf[pos].get_pixmap(matrix=fitz.Matrix(1,1),clip=clip,colorspace=fitz.csGRAY)
                    same=a.width==b.width and a.height==b.height and a.samples==b.samples
                    item={'lane':r['lane'], 'lane_pdf_page':i+1, 'full_pdf_page':pos+1,
                          'body_pixels_identical':same}
                    if not same:
                        changes.append(item)
                        d=work/'changed-pages';d.mkdir(exist_ok=True)
                        pdf[pos].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(d/f'full-{pos+1:03}.png'))
                        original[i].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(str(d/f'{r["lane"]}-{i+1:03}.png'))
                    checks.append(item)
                    pos+=1
            report.update(page_count_matches=(pos==len(pdf)), page_render_checks=checks,
                          comparison_clip_rule='Entire page below y=30pt; only running page number header excluded. Body starts at y=45.35pt.',
                          changed_content_pages=changes,
                          visual_review_status='pass_by_reviewed_page_pixel_identity' if not changes and pos==len(pdf) else 'pending_changed_pages')
            pdf[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(work/'cover.png'))
    (ROOT/'quality/book-latex.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['lanes','page_render_checks','changed_content_pages']},ensure_ascii=False))
    if report['status']=='compile_failed':
        raise SystemExit(1)


if __name__=='__main__':
    main()
