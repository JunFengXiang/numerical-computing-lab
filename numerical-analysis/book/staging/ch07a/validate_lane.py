from pathlib import Path
import re,json,hashlib,sys,subprocess
ROOT=Path(__file__).resolve().parents[2]
LANE=ROOT/'staging/ch07a'
# Normalize the printed dotted augmentation rule to a standard LaTeX array rule.
for p in [LANE/'pages/pdf-178.md',LANE/'batch02.py']:
 t=p.read_text();p.write_text(t.replace('{rrr:r}','{rrr|r}'))
rp=LANE/'review.json';r=json.loads(rp.read_text())
for q in r['pages']:
 q['sha256']=hashlib.sha256((ROOT/q['path']).read_bytes()).hexdigest()
r['validation_notes']=['逐一打开PDF177–195全部19张原图，转录完整正文、全部公式矩阵、表7.1、例题与算法步骤；发现的6项疑似原书错另注且保留原文。','所有写入限定staging/ch07a；未运行额外OCR，未改原PDF或source-images。']
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
sys.path.insert(0,str(ROOT/'tools'))
from audit_staging import audit_lane,read_page
from export_lanes import rewrite_local_links
manifest=json.loads((ROOT/'source-manifest.json').read_text())
lane=next(q for q in json.loads((ROOT/'workflow/lanes.json').read_text()) if q['lane']=='ch07a')
audit=audit_lane(lane,manifest,require_complete=True)
(LANE/'structural-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k not in ['checked_pages','expected_pages']},ensure_ascii=False))
assert audit['primary_review_complete']
qa=LANE/'qa';qa.mkdir(exist_ok=True)
body=['---\ntitle: ch07a逐页转录排版检查\ndate: ""\n---\n']
for q in r['pages']:
 p=ROOT/q['path'];meta,b,raw=read_page(p)
 body.append('\n\n\\clearpage\n\n'+f'原书 PDF {q["pdf_page"]}；书页 {q["printed_page"]}。\n\n'+rewrite_local_links(b,p,qa/'content.md'))
(qa/'content.md').write_text(''.join(body))
(qa/'header.tex').write_text('\\usepackage{amsmath,amssymb,mathtools}\n\\xeCJKDeclareCharClass{CJK}{"2160->"216B,"2460->"2473}\n\\setcounter{secnumdepth}{0}\n\\setlength{\\emergencystretch}{2em}\n\\allowdisplaybreaks\n')
subprocess.run(['pandoc','--from=markdown-implicit_figures+tex_math_dollars','--to=latex','--standalone','--wrap=none','-V','documentclass=ctexart','-V','classoption=fontset=fandol','-V','fontsize=10pt','-V','geometry:margin=13mm','--include-in-header',str(qa/'header.tex'),str(qa/'content.md'),'-o',str(qa/'content.tex')],check=True,cwd=qa)
with (qa/'compile.stdout').open('w') as f:
 p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','content.tex'],cwd=qa,stdout=f,stderr=subprocess.STDOUT)
log=(qa/'content.log').read_text(errors='replace')
result={'exit_code':p.returncode,'warnings':[s for s in log.splitlines() if any(q in s for q in ['Overfull','Missing character','LaTeX Error','! '])], 'note':'语法/排版检查不替代原图核验。'}
if p.returncode:result['error_context']=log[-4000:]
(qa/'compile-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
