#!/usr/bin/env python3
"""Exact arithmetic audit of source example 2.1 and its explicit errata."""
from hashlib import sha256
from datetime import datetime,timezone
from pathlib import Path
import json
import re
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'verified'/'sections'/'2.2.4.md'


def main():
    text=SOURCE.read_text()
    textbook,notes=re.split(r'^#{2,6}\s*校注[^\n]*NA5E-E002[^\n]*',text,maxsplit=1,flags=re.M)
    checks=[]
    def check(name,value,detail=None):
        item={'check':name,'pass':bool(value)}
        if detail is not None:
            item['detail']=detail
        checks.append(item)
    def decimal(latex):
        return sp.Rational(latex.replace(r'\,','').replace(' ',''))
    # Extract the data from the transcribed example, rather than retyping it.
    example=textbook.split('**解**',1)[1].split('用线性插值计算',1)[0]
    xs=[decimal(re.search(r'x_'+str(i)+r'=([\d.]+)',example)[1]) for i in range(3)]
    ys=[decimal(re.search(r'y_'+str(i)+r'=([\d.\\,]+)',example)[1]) for i in range(3)]
    target=decimal(re.search(r'计算 \$\\sin([\d.\\,]+)\$',textbook)[1])
    lb=[sp.prod((target-xs[j])/(xs[k]-xs[j]) for j in range(3) if j!=k) for k in range(3)]
    q=sum(ys[k]*lb[k] for k in range(3))
    L1=ys[0]+(ys[1]-ys[0])/(xs[1]-xs[0])*(target-xs[0])
    alt=ys[1]+(ys[2]-ys[1])/(xs[2]-xs[1])*(target-xs[1])
    output_values={'linear':L1,'linear_alternative':alt,'quadratic':q}
    expected=[('linear',r'L_1\(0\.3367\)&=([\d.]+)'),
              ('linear_alternative',r'\\widetilde L_1\(0\.3367\)&=([\d.]+)'),
              ('quadratic',r'L_2\(0\.3367\)&=([\d.]+)')]
    for key,pattern in expected:
        printed=re.search(pattern,notes)[1].rstrip('.')
        check('Corrected '+key+' matches exact interpolation',output_values[key]==sp.Rational(printed))
    check('R2 derivative order is three in 2.2.18',
          r"R_2(x)=\frac16 f'''(\xi)" in textbook)
    check('General derivative order and factorial retained',
          r'\frac{f^{(n+1)}(\xi)}{(n+1)!}' in textbook)
    cosine=sp.N(sp.cos(xs[0]),30)
    check('Source cos bound is demonstrably false',cosine>sp.Rational('.828'),str(cosine))
    check('Corrected conservative cos bound is valid',cosine<sp.Rational('.95'))
    factor=abs(sp.prod(target-node for node in xs))/6
    wrong_bound=sp.Rational('.828')*factor
    check('Source exponent understates its own product',
          wrong_bound>sp.Rational('.178')*10**(-7),str(sp.N(wrong_bound,18)))
    correct_bound=sp.Rational('.95')*factor
    check('Corrected bound multiplication',correct_bound==sp.Rational('2.03309975e-7'))
    exact_middle=abs((target-xs[0])*(target-xs[2]))
    check('Middle product preserves all digits',exact_middle==sp.Rational('0.00038911'))
    printed_substitution=(ys[0]*sp.Rational('.00007689')/sp.Rational('.0008')
                          +ys[1]*sp.Rational('.000389')/sp.Rational('.0004')
                          +ys[2]*sp.Rational('-.00005511')/sp.Rational('.0008'))
    check('Printed substitution does not equal reported final value',
          abs(printed_substitution-sp.Rational('.330374'))>sp.Rational('0.0000005'),
          str(sp.N(printed_substitution,18)))
    check('Corrected quadratic rounds to textbook final six significant digits',
          round(float(q),6)==.330374)
    data_bound=sp.Rational('0.0000005')*sum(abs(t) for t in lb)
    check('Node rounding bound',data_bound==sp.Rational('5.688875e-7'))
    check('Combined conservative bound',data_bound+correct_bound==sp.Rational('7.72197475e-7'))
    check('Actual tabulated-data result is within combined bound',
          abs(sp.N(sp.sin(target)-q,25))<data_bound+correct_bound)
    report={'status':'pass' if all(c['pass'] for c in checks) else 'fail',
            'created_utc':datetime.now(timezone.utc).isoformat(),
            'source_markdown':str(SOURCE.relative_to(ROOT)),
            'source_markdown_sha256':sha256(SOURCE.read_bytes()).hexdigest(),
            'passed':sum(c['pass'] for c in checks),'total':len(checks),
            'nodes':[str(t) for t in xs],'values':[str(t) for t in ys],
            'evaluation_point':str(target),'computed_values':{k:str(sp.N(v,20)) for k,v in output_values.items()},
            'sin_target':str(sp.N(sp.sin(target),25)),
            'checks':checks,
            'limitations':'Audits this one source example and the displayed derivative order; it does not validate all textbook arithmetic.'}
    (ROOT/'quality'/'remainder-example-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','passed','total']},ensure_ascii=False))
    if report['status']!='pass':
        raise SystemExit(1)


if __name__=='__main__':
    main()
