from pathlib import Path
import hashlib,json,re,subprocess
from build_lane import LANE,ROOT,SOURCE,review
# Typography corrections after second comparison; formulas and source values remain unchanged.
p=LANE/'pages/pdf-064.md';s=p.read_text().replace("f'(x_2) ， \\tag{3.2.7}","f'(x_2), \\tag{3.2.7}");p.write_text(s)
p=LANE/'pages/pdf-075.md';s=p.read_text().replace('这里规定 $T_0 = 1/2, n=1 \\sim 8$ 的结果如表 3.2 所示.','这里规定 $T_0 = 1/2$. $n=1 \\sim 8$ 的结果如表 3.2 所示.');p.write_text(s)
review()
d=json.loads((LANE/'review.json').read_text())
assert [p['pdf_page'] for p in d['pages']]==list(range(58,76))
expected=[f'3.{sec}.{i}' for sec,count in [(1,10),(2,9),(3,17),(4,10)] for i in range(1,count+1)]
actual=[f for p in d['pages'] for f in p['formula_ids']]
assert actual==expected,(actual,expected)
assert len([f for p in d['pages'] for f in p['figures']])==5
assert len([t for p in d['pages'] for t in p['tables']])==2
math_blocks=[]
for p in d['pages']:
    file=ROOT/p['path'];s=file.read_text()
    assert p['sha256']==hashlib.sha256(file.read_bytes()).hexdigest()
    assert p['source_image_sha256']==hashlib.sha256((ROOT/f"source-images/pdf-{p['pdf_page']:03}.jpeg").read_bytes()).hexdigest()
    assert s.count('$$')%2==0
    assert '[待核:' not in s
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',s):
        assert (file.parent/link).resolve().exists(),(file,link)
    for m in re.finditer(r'\$\$(.*?)\$\$',s,flags=re.S):
        block=m[1];assert block.count(r'\tag{')<=1
        math_blocks.append((p['pdf_page'],block))
    for m in re.finditer(r'\$(.*?)\$',re.sub(r'\$\$.*?\$\$','',s,flags=re.S),flags=re.S):
        math_blocks.append((p['pdf_page'],m[1]))
qa=LANE/'qa';qa.mkdir(exist_ok=True)
tex=[r'\documentclass[UTF8,fontset=fandol]{ctexart}',r'\usepackage{amsmath,amssymb}',r'\usepackage[paperwidth=420mm,paperheight=297mm,margin=15mm]{geometry}',r'\pagestyle{plain}',r'\begin{document}']
for i,(page,block) in enumerate(math_blocks,1):
    tex.extend([f'PDF {page}, math fragment {i}',r'\['+block+r'\]',r'\par'])
tex.append(r'\end{document}')
(qa/'mathcheck.tex').write_text('\n'.join(tex))
r=subprocess.run(['/Library/TeX/texbin/xelatex','-interaction=nonstopmode','-halt-on-error','mathcheck.tex'],cwd=qa,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(qa/'compile-output.txt').write_text(r.stdout)
assert r.returncode==0,r.stdout[-3000:]
log=(qa/'mathcheck.log').read_text()
missing=re.findall(r'Missing character:[^\n]*',log)
assert not missing,missing
result={'pages':18,'pdf_range':[58,75],'printed_range':[45,62],'numbered_formulas':len(actual),'figures':5,'tables':2,'source_errata':len(d['source_errata']),'unresolved':0,'markdown_links':'passed','page_and_image_sha256':'passed','formula_sequence':'passed','math_fragments':len(math_blocks),'xelatex_math_syntax':'passed','missing_glyphs':missing,'note':'Compilation verifies LaTeX syntax only; source content was checked against each original page image.'}
(qa/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
d=json.loads((LANE/'review.json').read_text());d['validation_notes'] += [f'完整公式编号序列核对通过：3.1.1–3.1.10、3.2.1–3.2.9、3.3.1–3.3.17、3.4.1–3.4.10，共 {len(actual)} 个。',f'{len(math_blocks)} 个行内/独立数学片段通过 XeLaTeX 语法编译且无缺字；编译不作为数学正确性证明。','18 份文件与 18 张原图的 SHA-256 实际计算核对；Markdown 原页和图链接均可解析。','5 幅裁切图已再次打开检查边界及符号标签，2 张公式表全部九行核对。']
(LANE/'review.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
