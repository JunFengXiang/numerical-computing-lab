from build_lane import *
s=normalize(64)
s=s.replace(r'\end{cases}',r'\end{cases} \tag{3.2.6}',1)
s=s.replace('$a_1 = \\frac{f(b) - f(a)}{b - a} = f\'(x_2)$，(3.2.7)', '$$\na_1 = \\frac{f(b)-f(a)}{b-a} = f\'(x_2), \\tag{3.2.7}\n$$')
s=s.replace(r'\frac{x_2}{\sqrt{1+x^2}}',r'\frac{x_2}{\sqrt{1+x_2^2}}')
s=s.replace(r'f(x_2) = \sqrt{1+x^2}',r'f(x_2) = \sqrt{1+x_2^2}')
s=s.replace(r'a_0 = \frac{1 + \sqrt{1+x^2}}{2}',r'a_0 = \frac{1 + \sqrt{1+x_2^2}}{2}')
s=s.replace('例3.1 求', '![图 3.3 原图裁切](../assets/fig-3-3.png)\n\n图 3.3（原图）。最佳一次逼近的几何意义；标签为 $x$、$y$、$O$、$a$、$x_2$、$b$、$M$、$N$、$Q$、$D$、$y=P_1(x)$。弦 $MN$、逼近直线以及通过 $Q$ 的平行线构成图中的三条斜线，$D$ 为 $MQ$ 的中点。\n\n例3.1 求')
s+='\n\n> 校注（agent 补充，原书疑误）：本页开头先把三个交错点记为 $x_1<x_2<x_3$，随后原印“$x_0=a,x_1=b$”，此处忠实保留。按前文编号应为 $x_1=a,x_3=b$。\n\n> 校注（agent 补充，数值舍入）：原书对所写 $P_1(x)=0.955+0.414x$ 给出误差限 $0.045$，这里保留原文。若把这两个已舍入系数当作精确数，则在 $x=1$ 处误差为 $\\sqrt2-1.369\\approx0.04521356>0.045$，故所印误差限不适用于这组舍入后的系数。'
Image.open(ROOT/'source-images/pdf-064.jpeg').crop((1120,1000,1620,1510)).save(LANE/'assets/fig-3-3.png')
save(64,s);register(64,notes=['补回 OCR 漏失的公式编号 (3.2.6) 与图 3.3。','纠正例 3.1 中 OCR 把 x_2^2 识为 x^2 的三处下标。','原书交错点编号不一致，以及舍入后误差限问题已按原文保留并单列校注。'],figures=['3.3'])
s=normalize(65).replace(r'f = (f_1, f_2, \cdots, f_n)',r'\boldsymbol{f} = (f_1, f_2, \cdots, f_n)').replace(r'g = (g_1, g_2, \cdots, g_n)',r'\boldsymbol{g} = (g_1, g_2, \cdots, g_n)')
s+='\n\n<!-- 本页末句续 PDF 66。 -->'
save(65,s);register(65,notes=['核对权函数条件中的 |x|^n、非负连续函数以及积分区间。'])
e=json.loads((LANE/'source_errata.json').read_text());e += [
{'id':'ch03a-E03','pdf_page':64,'printed_page':51,'kind':'source_index_inconsistency','location':'“另外两个偏差点必在区间端点”后','source':'x_0=a, x_1=b','note':'本页前文三个点编号为 x_1<x_2<x_3，按该编号端点应为 x_1=a, x_3=b。转录保留原书。'},
{'id':'ch03a-E04','pdf_page':64,'printed_page':51,'kind':'rounded_coefficient_error_bound','location':'例 3.1 页末误差限','source':'max |sqrt(1+x^2)-P_1(x)| <= 0.045, P_1=0.955+0.414x','note':'把印出的舍入系数作为精确数，x=1 时误差 sqrt(2)-1.369=0.04521356237... 大于 0.045。原书数值及不等式均保留。'}]
(LANE/'source_errata.json').write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n');review()
