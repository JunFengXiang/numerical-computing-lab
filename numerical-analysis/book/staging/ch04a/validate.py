import hashlib, json, re, subprocess
from pathlib import Path
import sympy as s
import yaml

lane=Path(__file__).resolve().parent
book=lane.parent.parent
checks=[]
parsed_pages=[]
all_math=[]
all_tags=[]

def add(name,passed,details):
    checks.append({'name':name,'passed':bool(passed),'details':details})

def visit(node,out):
    if isinstance(node,dict):
        if node.get('t')=='Math':out.append(node['c'])
        for v in node.values():visit(v,out)
    elif isinstance(node,list):
        for v in node:visit(v,out)

for n in range(93,106):
    p=lane/f'pages/pdf-{n:03}.md';text=p.read_text()
    meta=yaml.safe_load(text.split('---',2)[1]);body=text.split('---',2)[2]
    assert meta['pdf_page']==n and meta['printed_page']==n-13
    assert meta['status']=='agent_reviewed_transcription'
    assert f'<!-- source-page: {n} -->' in body
    assert '[待核:' not in text
    for url in re.findall(r'\]\(([^)]+)\)',text):
        if not re.match(r'\w+://',url):assert (p.parent/url).exists(),url
    ast=json.loads(subprocess.check_output(['/opt/homebrew/bin/pandoc','-f','markdown+tex_math_dollars','-t','json',str(p)]))
    math=[];visit(ast,math)
    parsed_pages.append({'pdf_page':n,'math_nodes':len(math),'markdown_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    all_math.extend((n,typ['t'],expr) for typ,expr in math)
    all_tags += re.findall(r'\\tag\{([^}]+)\}',text)
add('page_metadata_and_local_links',len(parsed_pages)==13,parsed_pages)
expected=[f'4.{sec}.{k}' for sec,count in [(1,7),(2,17),(3,15)] for k in range(1,count+1)]
add('formula_number_coverage',all_tags==expected,{'count':len(all_tags),'expected_count':39,'duplicate_ids':[x for x in set(all_tags) if all_tags.count(x)>1]})

coef={}
for page in [96,97]:
    for line in (lane/f'pages/pdf-{page:03}.md').read_text().splitlines():
        cells=[x.strip() for x in line.strip('|').split('|')]
        if not (cells and cells[0].isdigit()):continue
        n=int(cells[0]);out=[]
        for cell in cells[1:]:
            if not cell:continue
            m=re.fullmatch(r'\$\\frac(\{-?\d+\}|-?\d)(\{-?\d+\}|-?\d)\$',cell)
            assert m,cell
            out.append(s.Rational(int(m[1].strip('{}')),int(m[2].strip('{}'))))
        coef[n]=out
x,a,b=s.symbols('x a b',real=True)
for n,values in sorted(coef.items()):
    exact=[s.factor(s.integrate(s.prod((x-j)/(s.Integer(k)-j) for j in range(n+1) if j!=k),(x,0,n))/n) for k in range(n+1)]
    degree=n+(n%2==0)
    moments=[s.simplify(sum(v*s.Rational(k,n)**m for k,v in enumerate(values))-s.Rational(1,m+1))==0 for m in range(degree+1)]
    add(f'cotes_table_n_{n}',values==exact and len(values)==n+1 and all(moments),{'coefficients':[str(v) for v in values],'sum':str(sum(values)),'moments_through_degree':degree})
for n,power in [(1,2),(2,4),(4,6)]:
    values=coef[n]
    err=s.integrate(x**power,(x,a,b))-(b-a)*sum(v*(a+s.Rational(k,n)*(b-a))**power for k,v in enumerate(values))
    remainder={1:-(b-a)**3/s.Integer(12)*s.factorial(2),2:-(b-a)/s.Integer(180)*((b-a)/2)**4*s.factorial(4),4:-2*(b-a)/s.Integer(945)*((b-a)/4)**6*s.factorial(6)}[n]
    add(f'remainder_sign_scale_derivative_n_{n}',s.simplify(err-remainder)==0,{'tested_function':f'x^{power}','exact_error':str(s.factor(err)),'derivative_factor':str(s.factorial(power))})
n=9
c9=[s.factor(s.integrate(s.prod((x-j)/(s.Integer(k)-j) for j in range(n+1) if j!=k),(x,0,n))/n) for k in range(n+1)]
add('source_errata_E01_counterexample',all(v>0 for v in c9),{'n':9,'coefficients':[str(v) for v in c9]})
diff=abs(s.Rational('0.9460831')-s.Rational('0.9456909'))
add('source_errata_E02_significant_digits',s.Rational('0.00005')<diff<s.Rational('0.0005'),{'absolute_error':str(diff),'decimal_error':str(s.N(diff,10)),'significant_digits':3,'definition':'book 1.3.3, equation (1.3.2)'})

# Evaluate the composite trapezoid sum from exact rational nodes before rounding.
n=32
trap_expr=(1+s.sin(1))/(2*n)+sum(s.sin(s.Rational(k,n))/s.Rational(k,n) for k in range(1,n))/n
trap=s.N(trap_expr,80)
add('source_errata_E07_trapezoid_table_k5',s.Rational('0.94605855')<trap<s.Rational('0.94605865'),{'function':'sin(x)/x, f(0)=1','interval':[0,1],'n':n,'working_decimal_digits':80,'computed_value':str(trap),'rounded_to_7_decimal_places':'0.9460586','source_table_value_preserved':'0.9460596'})

# Compile only extracted math to establish syntax validity; this is not visual-content verification.
tex=['\\documentclass[UTF8,fontset=fandol]{ctexart}','\\usepackage{amsmath,amssymb}','\\begin{document}']
for n,typ,expr in all_math:
    tex += [f'% PDF page {n}', '\\[ '+expr+' \\]' if typ=='DisplayMath' else '$'+expr+'$\\par']
tex+=['\\end{document}']
(lane/'math-syntax.tex').write_text('\n'.join(tex)+'\n')
result=subprocess.run(['/Library/TeX/texbin/xelatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(lane),str(lane/'math-syntax.tex')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(lane/'math-syntax-build.log').write_text(result.stdout)
add('latex_math_syntax',result.returncode==0,{'exit_code':result.returncode,'math_nodes':len(all_math),'log':'staging/ch04a/math-syntax-build.log','scope':'LaTeX syntax only; typesetting overflow is not evaluated in this math-only diagnostic.'})
report={'lane':'ch04a','passed':all(c['passed'] for c in checks),'checks':checks,'limits':['符号计算不能替代原页视觉核验。','数学语法诊断 PDF 不作为教材排版交付；中央稿件合并和最终渲染由 root 完成。']}
(lane/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'checks':len(checks),'pages':len(parsed_pages),'math_nodes':len(all_math),'failed':[c['name'] for c in checks if not c['passed']]},ensure_ascii=False))
if result.returncode: print(result.stdout[-4000:])
