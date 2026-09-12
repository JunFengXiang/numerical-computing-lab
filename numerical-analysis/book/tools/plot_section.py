#!/usr/bin/env python3
"""Acceptance example: resolve a section request, parse its verified LaTeX and plot."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import os

ROOT=Path(__file__).resolve().parents[1]
os.environ['MPLCONFIGDIR']=str(ROOT/'.work'/'matplotlib')
os.environ['XDG_CACHE_HOME']=str(ROOT/'.work'/'cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import sympy as sp
from interpolation_formulas import SOURCE, load_linear
from lookup import resolve


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--request',default='根据2.2.2的线性插值画出图')
    parser.add_argument('--left',type=float,default=1.0)
    parser.add_argument('--right',type=float,default=3.0)
    args=parser.parse_args()
    resolution=resolve(args.request)
    if resolution.get('resolved_section')!='2.2.2':
        raise SystemExit('这个验收脚本只绘制已核验的 2.2.2 线性插值；其他章节应另行实现。')
    if any(word in args.request for word in ['二次','抛物']):
        raise SystemExit('这个验收脚本只绘制线性插值，不能把二次插值请求当作线性插值。')
    if not (np.isfinite(args.left) and np.isfinite(args.right) and 0<args.left<args.right):
        raise SystemExit('演示函数为 1+ln(x)，要求 0 < left < right；节点必须互异。')
    checks=json.loads((ROOT/'quality'/'interpolation-symbolic-checks.json').read_text())
    if checks['status']!='pass' or checks['checked_markdown_sha256']!=sha256(SOURCE.read_bytes()).hexdigest():
        raise SystemExit('核验记录缺失、未通过或已经过期；先运行 validate_interpolation.py。')
    expr,basis=load_linear()
    x,a,b,u,v=sp.symbols('x a b u v')
    left,right=args.left,args.right
    y0,y1=1+np.log(left),1+np.log(right)
    values={a:left,b:right,u:y0,v:y1}
    L=sp.lambdify(x,expr['2.2.4'].subs(values),'numpy')
    basis_functions=[sp.lambdify(x,q.subs({a:left,b:right}),'numpy') for q in basis]
    assert np.allclose(L(np.array([left,right])),[y0,y1],rtol=0,atol=1e-12)
    grid=np.linspace(left,right,501)
    font=FontProperties(fname='/System/Library/Fonts/Supplemental/Songti.ttc')
    plt.rcParams.update({'font.size':12,'mathtext.fontset':'stix','axes.spines.top':False,
                         'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,3,figsize=(12.8,4.2),gridspec_kw={'width_ratios':[1.35,1,1]})
    fig.subplots_adjust(left=.066,right=.985,bottom=.235,top=.77,wspace=.38)
    blue,orange='#245d89','#b95b26'
    axes[0].plot(grid,1+np.log(grid),color=blue,lw=2.4,label=r'$f(x)=1+\ln x$')
    axes[0].plot(grid,L(grid),color=orange,lw=2.1,label=r'$L_1(x)$')
    axes[0].scatter([left,right],[y0,y1],color='#222222',s=32,zorder=5)
    for xv,yv in [(left,y0),(right,y1)]:
        axes[0].vlines(xv,0,yv,color='#8b8b8b',lw=.9,ls='--')
    axes[0].set_ylim(0,max(y0,y1)*1.23)
    axes[0].legend(loc='upper left',frameon=False,fontsize=11)
    axes[0].set_title('两节点确定一条插值直线',fontproperties=font,pad=12)
    for j,fn in enumerate(basis_functions):
        ax=axes[j+1]
        ax.plot(grid,fn(grid),color=[blue,orange][j],lw=2.4)
        yy=fn(np.array([left,right]))
        ax.scatter([left,right],yy,color='#222222',s=28,zorder=5)
        ax.set_ylim(-.08,1.15)
        ax.set_yticks([0,1])
        ax.set_title([r'$l_k(x)=\frac{x-x_{k+1}}{x_k-x_{k+1}}$',
                      r'$l_{k+1}(x)=\frac{x-x_k}{x_{k+1}-x_k}$'][j],pad=17)
        ax.grid(axis='y',color='#e2e2e2',lw=.7)
    for ax in axes:
        ax.set_xlim(left-(right-left)*.12,right+(right-left)*.12)
        ax.set_xticks([left,right],[r'$x_k$',r'$x_{k+1}$'])
        ax.set_xlabel('$x$',labelpad=7)
        ax.tick_params(length=3,color='#555555')
    fig.suptitle('2.2.2 线性插值：从教材公式生成图',fontproperties=font,fontsize=18,y=.97)
    fig.text(.066,.082,f'另选的演示例子：f(x)=1+ln(x)，节点为 {left:g}、{right:g}。原书图 2.2、2.3 未给具体数值。',
             fontproperties=font,fontsize=11,color='#444444')
    fig.text(.066,.026,'依据：书页 16 / PDF 页 29；公式 (2.2.3) 至 (2.2.5)。曲线由已核验 Markdown 中的 LaTeX 解析计算。',
             fontproperties=font,fontsize=10,color='#555555')
    out=ROOT/'figures'/'generated'
    out.mkdir(parents=True,exist_ok=True)
    files=[]
    for ext in ['svg','png']:
        path=out/f'section-2.2.2-linear.{ext}'
        fig.savefig(path,dpi=190,facecolor='white')
        files.append(str(path.relative_to(ROOT)))
    plt.close(fig)
    report={'request_resolution':resolution,
            'formula_source':str(SOURCE.relative_to(ROOT)),
            'formula_source_sha256':sha256(SOURCE.read_bytes()).hexdigest(),
            'formula_id':'2.2.4','basis_source':'2.2.2 linear basis display equations',
            'function':'1+log(x)','nodes':[left,right],'values':[float(y0),float(y1)],
            'example_status':'agent_chosen_demonstration_not_original_book_data',
            'node_residual_max':float(np.max(np.abs(L(np.array([left,right]))-[y0,y1]))),
            'outputs':files,'visual_review_status':'pending'}
    (ROOT/'quality'/'plot-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'outputs':files,'warnings':resolution['warnings'],
                      'node_residual_max':report['node_residual_max']},ensure_ascii=False))


if __name__=='__main__':
    main()
