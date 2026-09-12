from build_lane import *
s=normalize(62).replace(r'\parallel P(x) - f(x) \parallel_\infty',r'\|P(x)-f(x)\|_\infty')
s=s.replace('$$\nP(x_k) - f(x_k) = (-1)^k \\sigma \\|P(x)-f(x)\\|_\\infty,\n$$\n\n$$\n\\sigma = \\pm 1, \\quad k = 1, 2, \\cdots, n+2, \\tag{3.2.4}\n$$','$$\n\\begin{aligned}\nP(x_k)-f(x_k)&=(-1)^k\\sigma\\|P(x)-f(x)\\|_\\infty,\\\\\n\\sigma&=\\pm1,\\quad k=1,2,\\cdots,n+2,\n\\end{aligned}\n\\tag{3.2.4}\n$$')
fig='![图 3.2 原图裁切](../assets/fig-3-2.png)\n\n图 3.2（原图）。带状区域及逼近曲线示意；标签为 $x$、$y$、$O$、$a$、$b$、$y=f(x)+E_n$、$y=P(x)$、$y=f(x)-E_n$。图内还画有从曲线接触点向横轴延伸的竖向辅助线。'
s=s.replace('定理 3.4 $P(x)',fig+'\n\n定理 3.4 $P(x)',1)
s+='\n\n<!-- 本页末式 P(x)- 续 PDF 63 的 Q(x)。 -->\n\n> 校注（agent 补充，原书疑误）：图 3.2 旁正文印为“定理 3.1 表明”，按原文保留。此段是在解释正、负偏差点同时存在，应指本页定理 3.3；定理 3.1 是 Weierstrass 定理。'
Image.open(ROOT/'source-images/pdf-062.jpeg').crop((1020,1215,1650,1720)).save(LANE/'assets/fig-3-2.png')
save(62,s);register(62,notes=['补回 OCR 遗漏的图 3.2 原图及完整标签。','正文交叉引用原印“定理 3.1”；保留并添加校注，应指定理 3.3。'],figures=['3.2'])
s=normalize(63)
s=s.replace(r'P(x)-Q(x) \neq 0',r'P(x)-Q(x) \not\equiv 0')
s+='\n\n<!-- 本页末句续 PDF 64。 -->'
save(63,s);register(63,notes=['页首接 PDF 62 的 P(x)-Q(x)；按原图将 OCR 的不等号改为不恒等号。'])
e=json.loads((LANE/'source_errata.json').read_text()); e.append({'id':'ch03a-E02','pdf_page':62,'printed_page':49,'kind':'source_cross_reference_error','location':'图 3.2 旁正文','source':'定理 3.1 表明','note':'上下文在解释定理 3.3 的正、负偏差点性质，应为定理 3.3；定理 3.1 为 Weierstrass 定理。原文保留。'});(LANE/'source_errata.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');review()
