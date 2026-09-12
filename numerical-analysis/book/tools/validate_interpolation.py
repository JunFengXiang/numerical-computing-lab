#!/usr/bin/env python3
"""Check equations parsed from the Markdown plus source/figure integrity."""
from hashlib import sha256
from datetime import datetime, timezone
import json
import sympy as sp
from interpolation_formulas import ROOT, SOURCE, load_linear, load_quadratic


def main():
    x,a,b,c,u,v,w = sp.symbols('x a b c u v w')
    checks = []
    def zero(name, expression):
        result = sp.simplify(expression)
        checks.append({'check':name,'pass':result == 0,'residual':str(result)})

    expr, basis = load_linear()
    zero('2.2.3 equals 2.2.4',expr['2.2.3']-expr['2.2.4'])
    zero('2.2.5 equals 2.2.4',expr['2.2.5']-expr['2.2.4'])
    zero('L1 left node',expr['2.2.4'].subs(x,a)-u)
    zero('L1 right node',expr['2.2.4'].subs(x,b)-v)
    zero('linear partition of unity',sum(basis)-1)
    for i, f in enumerate(basis):
        for j, node in enumerate([a,b]):
            zero(f'linear basis {i} at node {j}',f.subs(x,node)-int(i==j))

    quadratic, qb, expanded = load_quadratic()
    zero('2.2.7 equals expanded L2',quadratic-expanded)
    zero('quadratic partition of unity',sum(qb)-1)
    for i, f in enumerate(qb):
        for j,node in enumerate([a,b,c]):
            zero(f'quadratic basis {i} at node {j}',f.subs(x,node)-int(i==j))
    for j,(node,y) in enumerate(zip([a,b,c],[u,v,w])):
        zero(f'L2 at node {j}',quadratic.subs(x,node)-y)

    # Exact rational values exercise signs on nonuniform and negative nodes.
    values = {a:sp.Rational(-7,3),b:sp.Rational(2,5),c:sp.Rational(13,4),
              u:sp.Rational(9,7),v:sp.Rational(-3,2),w:sp.Rational(5,8)}
    for j,(node,y) in enumerate(zip([a,b,c],[u,v,w])):
        zero(f'L2 rational nonuniform case {j}',
             expanded.subs(values).subs(x,values[node])-values[y])

    vdm = ROOT/'verified'/'sections'/'2.2.1.md'
    product = r'\prod_{i=1}^{n}\prod_{j=0}^{i-1}(x_i-x_j)'
    checks.append({'check':'Vandermonde product limits and orientation in transcription',
                   'pass':product in vdm.read_text()})
    for n in range(1,5):
        nodes = [sp.Rational(i*i+2*i-5,3) for i in range(n+1)]
        matrix = sp.Matrix([[t**j for j in range(n+1)] for t in nodes])
        factors = sp.prod(nodes[i]-nodes[j] for i in range(1,n+1) for j in range(i))
        zero(f'Vandermonde exact orientation n={n}',matrix.det()-factors)

    # Document the source erratum with a counterexample, without editing the source.
    t = sp.Symbol('t')
    zero('NA5E-E001 repeated-node family satisfies both conditions',(c+t*x).subs(x,0)-c)
    checks.append({'check':'NA5E-E001 family contains distinct polynomials',
                   'pass':sp.simplify((c+x)-(c+2*x)) != 0})

    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    original = ROOT/manifest['source_file']
    checks.append({'check':'Original PDF SHA-256 unchanged',
                   'pass':sha256(original.read_bytes()).hexdigest()==manifest['source_sha256']})
    for page in [27,28,29,30,31]:
        p = manifest['pages'][page-1]
        checks.append({'check':f'Source image integrity PDF {page}',
                       'pass':sha256((ROOT/p['image']).read_bytes()).hexdigest()==p['image_sha256']})
    for fig in json.loads((ROOT/'quality'/'source-figures.json').read_text()):
        checks.append({'check':f'Figure {fig["figure"]} crop integrity',
                       'pass':sha256((ROOT/fig['image']).read_bytes()).hexdigest()==fig['crop_sha256']})
    passed = all(c['pass'] for c in checks)
    report = {
        'status':'pass' if passed else 'fail',
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'checked_markdown_sha256':sha256(SOURCE.read_bytes()).hexdigest(),
        'method':'Parse selected transcribed LaTeX with SymPy/ANTLR and check exact identities.',
        'limitations':'These algebraic and integrity checks do not replace visual transcription review or prove full-book accuracy.',
        'assumptions':['Linear nodes a != b','Quadratic nodes a,b,c pairwise distinct'],
        'passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,
    }
    target = ROOT/'quality'/'interpolation-symbolic-checks.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','passed','total']},ensure_ascii=False))
    if not passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
