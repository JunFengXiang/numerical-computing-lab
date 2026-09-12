from build_lane import *
s=normalize(66)
s=s.replace('其内积定义为 $(f, g)',r'其内积定义为 $(\boldsymbol{f}, \boldsymbol{g})',1).replace('向量 $f \\in',r'向量 $\boldsymbol{f} \in',1)
s=s.replace(r'\| f \|_{2} = \left( \sum',r'\| \boldsymbol{f} \|_{2} = \left( \sum',1)
s=s.replace('$1^{\\circ} |(f, g)| \\leqslant \\| f \\|_{2} \\| g \\|_{2}$ (Cauchy-Schwarz 不等式); (3.3.5)', '$1^{\\circ}$\n\n$$\n|(f,g)|\\leqslant\\|f\\|_2\\|g\\|_2\\qquad\\text{(Cauchy-Schwarz 不等式)};\\tag{3.3.5}\n$$')
s=s.replace('$2^{\\circ} \\| f + g \\|_{2} \\leqslant \\| f \\|_{2} + \\| g \\|_{2}$ (三角不等式); (3.3.6)', '$2^{\\circ}$\n\n$$\n\\|f+g\\|_2\\leqslant\\|f\\|_2+\\|g\\|_2\\qquad\\text{(三角不等式)};\\tag{3.3.6}\n$$')
s+='\n\n<!-- 定义 3.7 的正交函数族说明续 PDF 67。 -->'
save(66,s);register(66,notes=['核对全部平方范数、内积、Cauchy-Schwarz 不等式与权正交定义。'])
s=normalize(67)
s=s.replace('就是 $[a,b]$ 上的线性无关函数.', '就是 $[a,b]$ 上的线性无关函数族.')
s=s.replace(r'\Phi = \operatorname{span}\{\varphi_0, \varphi_1, \cdots, \varphi_{n-1}\}.',r'\Phi = \operatorname{span}\{\varphi_0, \varphi_1, \cdots, \varphi_{n-1}\}. \tag{3.3.9}')
s=s.replace(r'\end{array} \right|.',r'\end{array} \right|. \tag{3.3.10}')
s+='\n\n<!-- 本页末句续 PDF 68。 -->\n\n> 校注（agent 补充，原书术语疑误）：原页定理 3.6 写作“Cramer 行列式”，按原文保留。式 (3.3.10) 是由内积组成的 Gram 行列式，通常称“Gram（格拉姆）行列式”。'
save(67,s);register(67,notes=['补回 OCR 遗漏的 (3.3.9)、(3.3.10) 编号及“函数族”的“族”。','逐项核对内积行列式四行四列的省略表示及下标 n-1。','原书术语 Cramer 按原文保留并单列校注。'])
e=json.loads((LANE/'source_errata.json').read_text());e.append({'id':'ch03a-E05','pdf_page':67,'printed_page':54,'kind':'source_terminology_error','location':'定理 3.6','source':'Cramer 行列式','note':'式 (3.3.10) 为内积 Gram 矩阵的行列式，通常应称 Gram 行列式。原文保留并加校注。'});(LANE/'source_errata.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');review()
