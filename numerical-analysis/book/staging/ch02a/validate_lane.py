from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import re,json,hashlib,math
root=Path.cwd(); lane=root/'staging/ch02a'; review=json.loads((lane/'review.json').read_text());checks=[]
def check(name,ok,detail=None,source_observation=False):
 checks.append({'check':name,'pass':bool(ok),'source_observation':source_observation,**({'detail':detail} if detail is not None else {})})
 if not ok and not source_observation: raise AssertionError(name)
source=list(root.glob('*.pdf'))[0]
actual=hashlib.sha256(source.read_bytes()).hexdigest()
check('Original PDF SHA256 matches source provenance',actual==review['source_sha256'],actual)
check('Exactly PDF27 through PDF42 in receipts',[x['pdf_page'] for x in review['pages']]==list(range(27,43)))
for entry in review['pages']:
 n=entry['pdf_page'];p=root/entry['path'];s=p.read_text(); prefix=f'PDF{n}'
 check(prefix+' file digest',entry['sha256']==hashlib.sha256(p.read_bytes()).hexdigest())
 check(prefix+' image digest',entry['source_image_sha256']==hashlib.sha256((root/'source-images'/f'pdf-{n:03}.jpeg').read_bytes()).hexdigest())
 check(prefix+' display delimiters and LaTeX environments',s.count('$$')%2==0 and all(s.count('\\begin{'+e+'}')==s.count('\\end{'+e+'}') for e in ['aligned','cases','vmatrix']))
 check(prefix+' page provenance',f'pdf_page: {n}\n' in s and f'printed_page: {n-13}\n' in s and s.count(f'<!-- source-page: {n} -->')==1)
 targets=re.findall(r'(?m)^!?\[[^\]\n]*\]\(([^)\n]+)\)',s)
 check(prefix+' local Markdown links',all((p.parent/t).exists() for t in targets),targets)
 check(prefix+' no unresolved markers','[待核:' not in s)
 expected={27:['2.1.1','2.1.2'],28:['2.2.1','2.2.2'],29:['2.2.3','2.2.4','2.2.5'],30:['2.2.6','2.2.7'],31:['2.2.8','2.2.9','2.2.10','2.2.11','2.2.12'],32:['2.2.13','2.2.14','2.2.15','2.2.16'],33:['2.2.17','2.2.18'],34:[],35:['2.3.1','2.3.2'],36:['2.4.1'],37:['2.4.2','2.4.3','2.4.4','2.4.5'],38:['2.4.6','2.4.7'],39:['2.5.1','2.5.2','2.5.3'],40:['2.5.4','2.5.5','2.5.6','2.5.7','2.5.8','2.5.9'],41:['2.5.10','2.5.11','2.5.12'],42:[]}[n]
 check(prefix+' all original numbered formulas present',re.findall(r'\\tag\{([^}]+)\}',s)==expected)
 # Multiple tags must never occur in one display equation.
 check(prefix+' one tag per display',all(len(re.findall(r'\\tag\{',b))<=1 for b in s.split('$$')[1::2]))
# Parse actual transcribed table cells, not another copy of the data.
def table_rows(n):
 s=(lane/'pages'/f'pdf-{n:03}.md').read_text(); rows=[]
 for line in s.splitlines():
  if line.startswith('| $'):
   cells=[re.sub(r'\\underline\{(.*?)\}',r'\1',v.strip().replace('$','').replace('\\,','')) for v in line.strip('|').split('|')]
   try: Decimal(cells[0]); rows.append(cells)
   except: pass
 return rows
rows=table_rows(42)
check('Table2.7 has all 15 data rows',len(rows)==15)
values=[Decimal(r[2]) for r in rows]
for order in [1,2,3]:
 values=[values[i+1]-values[i] for i in range(len(values)-1)]
 printed=[Decimal(r[2+order]) for r in rows if r[2+order]]
 check(f'Table2.7 order{order} all displayed differences from transcribed values',values==printed)
rows=table_rows(38)
check('Table2.5 has all 6 data rows',len(rows)==6)
nodes=[Decimal(r[0]) for r in rows];values=[Decimal(r[1]) for r in rows]
quant=Decimal('0.00001')
for order in range(1,6):
 values=[((values[i+1]-values[i])/(nodes[i+order]-nodes[i])).quantize(quant,rounding=ROUND_HALF_UP) for i in range(len(values)-1)]
 printed=[Decimal(r[1+order]) for r in rows if r[1+order]]
 check(f'Table2.5 order{order} sequential rounded differences match transcribed table',values==printed,{'recomputed':[str(v) for v in values],'source_printed':[str(v) for v in printed]},source_observation=True)
x=Decimal('.596')
y=Decimal('.41075')+Decimal('1.116')*(x-Decimal('.4'))+Decimal('.28')*(x-Decimal('.4'))*(x-Decimal('.55'))+Decimal('.19733')*(x-Decimal('.4'))*(x-Decimal('.55'))*(x-Decimal('.65'))+Decimal('.03134')*(x-Decimal('.4'))*(x-Decimal('.55'))*(x-Decimal('.65'))*(x-Decimal('.8'))
check('Example2.3 N4 rounds to printed0.63195',y.quantize(quant,rounding=ROUND_HALF_UP)==Decimal('.63195'),{'computed':str(y),'rounded5dp':str(y.quantize(quant,rounding=ROUND_HALF_UP)),'printed':'0.63195'},source_observation=True)
product=abs(Decimal('-.00012')*math.prod([x-z for z in nodes[:5]]))
check('Example2.3 printed fifth difference estimate below3.63e-9',product<=Decimal('3.63e-9'),str(product))
y=Decimal('1.58')+Decimal('.4')*Decimal('.11')+Decimal('.4')*Decimal('-.6')/2*Decimal('.01')
check('Example2.4 computation rounds to1.62',y.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)==Decimal('1.62'),str(y))
# Detect OCR's sign error using odd n; the n-j exponent is essential.
for n in [1,2,3,4,5]:
 k=8;f=lambda j: j**4+3*j**2-2*j+7
 expected=sum((-1)**j*math.comb(n,j)*f(k-j) for j in range(n+1))
 actual=sum((-1)**(n-j)*math.comb(n,j)*f(k+j-n) for j in range(n+1))
 check(f'Formula2.5.5 n={n} backward difference sign',expected==actual)
result={'lane':'ch02a','status':'transcription_checks_pass_with_documented_source_numerical_discrepancies','human_review':False,'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'limitations':['Structure and arithmetic checks supplement actual agent visual review; neither is human review or proof of absolute accuracy.','The Example2.3 error quantity is a heuristic using the printed next divided difference; no global function error bound is proved from finite data alone.','Full manuscript Markdown/LaTeX rendering and central index integration belong to root acceptance.']}
(lane/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
review['validation_notes'].extend(['原PDF SHA256已在本轮直接计算匹配；16页文件和原图哈希、实际编号公式集、分页面标记、全部本地链接及LaTeX环境检查通过。','数值复核：表2.7全部一至三阶差分一致；表2.5统一逐层舍入的重算发现原书差异，已单列CH02A-S03；例2.3结果原书有数值错误已单列CH02A-S04；例2.4结果舍入一致。','式2.5.5以奇偶阶后向差分复核n-j符号；报告见staging/ch02a/validation.json。'])
review['validation_notes']=list(dict.fromkeys(review['validation_notes']))
(lane/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print('Transcription structure checks PASS;',sum(c['pass'] for c in checks),'/',len(checks),'all checks;',sum(not c['pass'] for c in checks),'documented source numerical differences;',len(review['pages']),'visually reviewed pages')
print('Numbered equations:',sum(len(x['formula_ids']) for x in review['pages']))
print('Source errors / notation issues:',[x['id'] for x in review['source_errata']])
