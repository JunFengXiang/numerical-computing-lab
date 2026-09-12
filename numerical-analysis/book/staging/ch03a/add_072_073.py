from build_lane import *
s=normalize(72)
s=s.replace('性质 4 在所有','![图 3.4 原图裁切](../assets/fig-3-4.png)\n\n图 3.4（原图）。Legendre 多项式 $P_0(x)$、$P_1(x)$、$P_2(x)$、$P_3(x)$ 的图形。全部标签：$x$、$y$、$O$、$-1$、$1$、$P_0(x)$、$P_1(x)$、$P_2(x)$、$P_3(x)$；图中包含区间端点处的竖向及下边界虚线。\n\n性质 4 在所有',1)
s+='\n\n<!-- 性质 4 的证明续 PDF 73。 -->'
Image.open(ROOT/'source-images/pdf-072.jpeg').crop((1000,1650,1640,2240)).save(LANE/'assets/fig-3-4.png')
save(72,s);register(72,notes=['逐项核对递推系数 n/(2n+1)、(n+1)/(2n+1) 及 P_2 至 P_6 的全部系数。','补回 OCR 遗漏图 3.4 原图及标签。'],figures=['3.4'])
s=normalize(73).replace('正交得到的正交多项式','正交化得到的正交多项式')
s=s.split('\n\n表 3.1\n\n',1)[0]+'\n\n表 3.1\n\n'
s+='| 多项式 | 表达式 |\n| --- | --- |\n'
rows=[(0,'1'),(1,'x'),(2,'2x^2-1'),(3,'4x^3-3x'),(4,'8x^4-8x^2+1'),(5,'16x^5-20x^3+5x'),(6,'32x^6-48x^4+18x^2-1'),(7,'64x^7-112x^5+56x^3-7x'),(8,'128x^8-256x^6+160x^4-32x^2+1')]
for k,poly in rows:s+=f'| $T_{k}(x)$ | ${poly}$ |\n'
s+='\n![图 3.5 原图裁切](../assets/fig-3-5.png)\n\n图 3.5（原图）。Chebyshev 多项式 $T_0(x)$、$T_1(x)$、$T_2(x)$、$T_3(x)$ 的图形。全部标签：$x$、$y$、$O$、横轴的 $-1$、$1$、纵轴的 $1$、$-1$、$T_0(x)$、$T_1(x)$、$T_2(x)$、$T_3(x)$；在 $x=\\pm1$ 处画有辅助线。'
Image.open(ROOT/'source-images/pdf-073.jpeg').crop((985,1860,1600,2540)).save(LANE/'assets/fig-3-5.png')
save(73,s);register(73,notes=['完整转录表 3.1 的 T_0 至 T_8 九项表达式。','核对 Chebyshev 权函数 1/sqrt(1-x^2)、区间与角变量范围。','补回图 3.5 原图及所有标签。'],figures=['3.5'],tables=['3.1'])
