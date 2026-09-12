from build_lane import *
s=normalize(68)
s+='\n\n> 校注（agent 补充，原书符号不一致）：式 (3.3.11) 两处下确界下标原印 $S\\in\\varphi$（小写），本页前文子集定义为 $\\Phi$（大写）。此处按原图保留小写，所指应为前文的 $\\Phi$。'
save(68,s);register(68,notes=['逐项核对法方程上下标、D 的展开符号及平方误差式。','(3.3.11) 下标原印小写 varphi；保留并添加符号不一致校注。'])
s=normalize(69)
s=s.replace(r'\begin{bmatrix}',r'\begin{pmatrix}',1).replace(r'\end{bmatrix}',r'\end{pmatrix}',1)
s=s.replace('$H$',r'$\boldsymbol{H}$').replace('\nH =',r'\boldsymbol{H} =')
s=s.replace('a = (a_0',r'\boldsymbol{a} = (a_0').replace('d = (d_0',r'\boldsymbol{d} = (d_0').replace('\nHa = d\n',r'\boldsymbol{H}\boldsymbol{a}=\boldsymbol{d}'+'\n')
s+='\n\n> 校注（agent 补充，数值舍入）：原书例 3.2 的系数与平方误差 $0.0026$ 均按原文保留。该数值来自把 $d_0,d_1$ 分别近似为 $1.147,0.609$ 后代入简化式；对于印出的函数 $S_1^*(x)=0.934+0.426x$，直接计算 $\\int_0^1[\\sqrt{1+x^2}-S_1^*(x)]^2\\,\\mathrm{d}x\\approx0.0007136324$，与 $0.0026$ 不同。舍入后的系数不再严格满足精确内积对应的法方程，不能把简化式的数值视为实际平方误差。'
save(69,s);register(69,notes=['按原图保留 Hilbert 矩阵圆括号及矩阵、向量粗体。','核对 (3.3.16) 的 n+1 阶布局和 1/(2n+1)。','例 3.2 数值舍入与实际平方误差不一致，原数值保留并单列校注。'])
s=normalize(70)
s=s.replace('3.4.1 正交手续','3.4.1 正交化手续').replace('并利用正交方法','并利用正交化方法').replace('正交得到的多','正交化得到的多')
s+='\n\n<!-- 本页末词“多项式”跨页续 PDF 71。 -->\n\n> 校注（agent 补充，原书索引疑误）：本页正交化构造式末尾原印“$k=1,2,\\cdots$”，而 $k$ 已是求和哑指标，外部序号应为 $n=1,2,\\cdots$；转录保留原式。\n\n> 校注（agent 补充，原书初值疑误）：递推初值原印 $g_{n-1}(x)=0$，按原文保留。若对一般 $n$ 成立，会与 $g_0(x)=1$ 冲突；递推通常应以 $g_{-1}(x)=0$ 开始。'
save(70,s);register(70,notes=['实际标题为 3.4.1 正交化手续；补正 OCR 漏字。','构造式末尾 k=1,2,... 和递推初值 g_{n-1}=0 确为原图，保留并单列两条校注。'])
s=normalize(71)
s=s.replace('P_0(x) = 1, \\quad P_n(x) = \\frac{1}{2^n n!} \\frac{d^n}{dx^n} \\{(x^2 - 1)^n\\} \\quad (n = 1, 2, \\cdots).','P_0(x) = 1, \\quad P_n(x) = \\frac{1}{2^n n!} \\frac{\\mathrm{d}^n}{\\mathrm{d}x^n} \\{(x^2 - 1)^n\\} \\quad (n = 1, 2, \\cdots). \\tag{3.4.1}')
s=s.replace(r'\tilde{P}_n(x) = \frac{n!}{(2n)!} \frac{d^n}{dx^n} [(x^2 - 1)^n].',r'\tilde{P}_n(x) = \frac{n!}{(2n)!} \frac{\mathrm{d}^n}{\mathrm{d}x^n} [(x^2 - 1)^n]. \tag{3.4.2}')
s=s.replace(r'\frac{2}{2n + 1}, & m = n. \end{cases}',r'\frac{2}{2n + 1}, & m = n. \end{cases} \tag{3.4.3}',1)
s+='\n\n> 校注（agent 补充，原书系数疑误）：由 $(x^2-1)^n$ 求导后写出的 $P_n(x)$ 首项系数中，原分母明确印为 $2^2n!$，此处按原文保留。依据式 (3.4.1)，该处应为 $2^nn!$；这也与紧随其后的 $a_n=(2n)!/[2^n(n!)^2]$ 一致。'
save(71,s);register(71,notes=['补回 OCR 遗漏的 (3.4.1)、(3.4.2)、(3.4.3) 编号。','逐项核对权 1、区间 [-1,1]、Rodrigues 表达式系数及范数 2/(2n+1)。','原文姓名拼作 Rodrigul；照录。','首项推导的分母原印 2^2 n!，保留并单列系数校注。'])
e=json.loads((LANE/'source_errata.json').read_text());e += [
{'id':'ch03a-E06','pdf_page':68,'printed_page':55,'kind':'source_symbol_case_inconsistency','location':'式 (3.3.11) 两处 inf 下标','source':r'S\in\varphi','note':'原图为小写 varphi，而前文子集记为大写 Phi；应指 Phi。原符号保留。'},
{'id':'ch03a-E07','pdf_page':69,'printed_page':56,'kind':'rounded_inner_product_squared_error','location':'例 3.2 平方误差','source':'||delta||_2^2 = 0.0026','note':'该数来自舍入内积；对印出的 S=0.934+0.426x 直接积分，实际平方误差约为 0.0007136323726914。原书数值保留。'},
{'id':'ch03a-E08','pdf_page':70,'printed_page':57,'kind':'source_index_error','location':'正交化构造式末尾','source':'k=1,2,...','note':'k 是求和哑指标，外部应为 n=1,2,...；原文保留。'},
{'id':'ch03a-E09','pdf_page':70,'printed_page':57,'kind':'source_initial_value_error','location':'三项递推的初值','source':'g_{n-1}(x)=0','note':'一般 n 时与 g_0=1 冲突；通常初值应为 g_{-1}(x)=0。原文保留。'},
{'id':'ch03a-E10','pdf_page':71,'printed_page':58,'kind':'source_coefficient_error','location':'式 (3.4.1) 后展开 P_n 的无编号公式','source':'1/(2^2 n!)','note':'原图确印 2^2；根据 (3.4.1) 及随后 a_n，应为 1/(2^n n!)。原式保留。'}]
(LANE/'source_errata.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');review()
