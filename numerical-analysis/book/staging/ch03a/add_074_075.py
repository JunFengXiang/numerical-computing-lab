from build_lane import *
s=normalize(74)
s=s.replace(r'\frac{T_n(x)T_m(x)dx}{\sqrt{1-x^2}}',r'\frac{T_n(x)T_m(x)\,\mathrm{d}x}{\sqrt{1-x^2}}')
s=s.replace(r'\pi, & n = m = 0. \end{cases}',r'\pi, & n = m = 0. \end{cases} \tag{3.4.8}',1)
s+='\n\n> 校注（agent 补充，原书交叉引用疑误）：例 3.3 中原文写“由定理 3.6 可知”，照录。此处使用的是本页定理 3.7 的最小偏差性质；定理 3.6 是线性无关与内积行列式的判别条件。'
save(74,s);register(74,notes=['补回 OCR 遗漏的 (3.4.8) 编号。','逐项核对 n=m=0 时为 pi，n=m 非零时为 pi/2。','例 3.3 原书定理号为 3.6，保留并单列校注，应指 3.7。'])
s=normalize(75)
before,tail=s.split('\n\n表 3.2\n\n',1)
tail=tail.split('### 3.4.4',1)[1]
s=before+'\n\n表 3.2\n\n| 幂函数 | Chebyshev 多项式表示 |\n| --- | --- |\n'
rows=[('1','T_0'),('x','T_1'),('x^2',r'\frac12(T_0+T_2)'),('x^3',r'\frac14(3T_1+T_3)'),('x^4',r'\frac18(3T_0+4T_2+T_4)'),('x^5',r'\frac1{16}(10T_1+5T_3+T_5)'),('x^6',r'\frac1{32}(10T_0+15T_2+6T_4+T_6)'),('x^7',r'\frac1{64}(35T_1+21T_3+7T_5+T_7)'),('x^8',r'\frac1{128}(35T_0+56T_2+28T_4+8T_6+T_8)')]
for f,ex in rows:s+=f'| ${f}$ | ${ex}$ |\n'
s+='\n### 3.4.4'+tail
s=s.replace('\n1. 第二类 Chebyshev 多项式','\n#### 1. 第二类 Chebyshev 多项式')
s+='\n\n<!-- 3.4.4 的第二类 Chebyshev 多项式内容续 PDF 76；本页积分等式到此。 -->\n\n> 校注（agent 补充，记号约定）：式 (3.4.9) 后原文规定 $T_0=1/2$，而表 3.2 首行原印 $1=T_0$；两处均忠实保留。式 (3.4.9) 的求和使用临时的半权常数项约定，表 3.2 则与前文通常定义 $T_0=1$ 一致。使用时须区分这两种约定。'
save(75,s);register(75,notes=['完整转录表 3.2 共九行，包括原表 1=T_0。','式 (3.4.9) 的求和上限为 [n/2]，并保留公式后的特殊规定 T_0=1/2；已添加约定说明。','核对第二类 Chebyshev 权 sqrt(1-x^2) 与正交常数 pi/2；末式无原编号。'],tables=['3.2'])
e=json.loads((LANE/'source_errata.json').read_text());e.append({'id':'ch03a-E11','pdf_page':74,'printed_page':61,'kind':'source_cross_reference_error','location':'例 3.3','source':'由定理 3.6 可知','note':'应指本页定理 3.7 的最小偏差性质，3.6 为内积行列式判别条件。原文保留。'});(LANE/'source_errata.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');review()
