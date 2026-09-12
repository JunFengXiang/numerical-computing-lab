"""Agent supplemental check; source table values in transcription remain unchanged."""
import sympy as s
from pathlib import Path
x=[s.Integer(i) for i in range(-5,6)];y=[1/(1+t*t) for t in x]
m0=-2*x[0]/(1+x[0]**2)**2;mn=-2*x[-1]/(1+x[-1]**2)**2
A=s.diag(*([s.Integer(2)]*9));g=s.zeros(9,1)
for j in range(1,10):
 if j>1:A[j-1,j-2]=s.Rational(1,2)
 if j<9:A[j-1,j]=s.Rational(1,2)
 g[j-1]=s.Rational(3,2)*(y[j+1]-y[j-1])
g[0]-=m0/2;g[-1]-=mn/2
m=[m0,*list(A.inv()*g),mn]
assert A*s.Matrix(m[1:-1]) == g
rows=[]
for q in [s.Rational(-48,10),s.Rational(-45,10),s.Rational(-43,10),s.Rational(-23,10)]:
 k=int(s.floor(q))+5;t=q-x[k]
 val=(1-t)**2*(1+2*t)*y[k]+t*t*(3-2*t)*y[k+1]+(1-t)**2*t*m[k]+t*t*(t-1)*m[k+1]
 rows.append(f'x={q}; exact_clamped_S={val}; decimal={float(val):.8f}')
out='Independent agent check of page 53 stated clamped boundary data, using exact rational linear solve.\n'+'m0='+str(m0)+'; mn='+str(mn)+'\n'+'\n'.join(rows)+'\n'
Path(__file__).with_suffix('.txt').write_text(out)
print(out)
