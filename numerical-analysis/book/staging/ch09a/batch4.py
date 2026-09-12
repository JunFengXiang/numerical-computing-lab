from write_pages import write_page,add_errata
write_page(242,r'''
<!-- 续 PDF 241，9.2.3 反幂法。 -->

由定理 9.9 知，对 $A-pI$（其中 $p\approx\lambda_j$）应用反幂法，可计算特征向量 $x_j$。只要选择的 $p$ 是 $\lambda_j$ 的一个较好的近似且特征值分离情况较好，一般 $r$ 很小，常常只要迭代一两次就可完成特征向量的计算。

反幂法迭代公式中的 $v_k$ 是通过解方程组 $(A-pI)v_k=u_{k-1}$ 求得的。为了节省工作量，可以先将 $(A-pI)$ 进行三角分解，即

$$
P(A-pI)=LU,
$$

其中 $P$ 为某个置换矩阵，于是求 $v_k$ 相当于解两个三角形方程组 $Ly_k=Pu_{k-1},Uv_k=y_k$。

反幂法迭代公式可写为

$$
\left\{
\begin{aligned}
Ly_k&=Pu_{k-1},\\
Uv_k&=y_k,\\
u_k&=\frac{v_k}{\max(v_k)}
\end{aligned}
\right.\qquad(k=1,2,\cdots).
\tag{9.2.13}
$$

实验表明，按下述方法选择 $v_0=u_0$ 是较好的：选 $u_0$ 使

$$
Uv_1=L^{-1}Pu_0=(1,1,\cdots,1)^{\mathrm T},
\tag{9.2.14}
$$

用回代求解式（9.2.14）即得 $v_1$，然后再按式（9.2.13）迭代。

**例 9.4** 用反幂法求

$$
A=\begin{pmatrix}
2&1&0\\
1&3&1\\
0&1&4
\end{pmatrix}
$$

的对应计算特征值 $\lambda=1.267\,9$（精确特征值为 $\lambda_3=3-\sqrt3$）的特征向量（用 5 位浮点数进行运算）。

**解** 用部分选主元的三角分解将 $A-pI$（其中 $p=1.267\,9$）分解为

$$
P(A-pI)=LU,
$$

其中

$$
P=\begin{pmatrix}
0&1&0\\
0&0&1\\
1&0&0
\end{pmatrix},
$$

$$
L=\begin{pmatrix}
1&0&0\\
0&1&0\\
0.732\,1&-0.268\,07&1
\end{pmatrix},\quad
U=\begin{pmatrix}
1&1.732\,1&1\\
0&1&2.732\,1\\
0&0&0.294\,05\times10^{-3}
\end{pmatrix}.
$$

由 $Uv_1=(1,1,1)^{\mathrm T}$，得

$$
v_1=(12\,692,\ -9\,290.3,\ 3\,400.8)^{\mathrm T},\quad
u_1=(1,\ -0.731\,98,\ 0.267\,95)^{\mathrm T},
$$

由 $LUv_2=Pu_1$，得

$$
v_2=(20\,404,\ -14\,937,\ 5\,467.4)^{\mathrm T},\quad
u_2=(1,\ -0.732\,06,\ 0.267\,96)^{\mathrm T}.
$$

$\lambda_3$ 对应的特征向量是

$$
x_3=(1,\ 1-\sqrt3,\ 2-\sqrt3)^{\mathrm T}\approx(1,\ -0.732\,05,\ 0.267\,95)^{\mathrm T}.
$$

<!-- 例 9.4 的结语续 PDF 243。 -->
''',[],['实际打开全页原图，确认书页 229；核对 9.2.13–9.2.14、例 9.4 的 A、P、L、U 四个矩阵；另实际打开 LU 与迭代向量裁切图，核对 0.29405×10^-3、负号、v_1/v_2/u_1/u_2 的全部数值。'])
write_page(243,r'''
<!-- 续 PDF 242，例 9.4 的结语。 -->

由此可以看出，$u_2$ 是 $x_3$ 的相当好的近似。

## 9.3 Householder 方法

### 9.3.1 引言

前面几节讨论的是求解矩阵最大（小）特征值及其对应特征向量的方法。若要求求出所有特征值及其特征向量，应该用什么方法呢？下面将讨论的以正交相似变换为基础的一类方法即是解决这类问题的方法。

首先，讨论对于一般实矩阵 $A\in\mathbf R^{n\times n}$ 利用正交相似变换约化到什么程度的问题。由代数知识可知如下定理。

**定理 9.10** 设 $A\in\mathbf R^{n\times n}$，则存在一个正交阵 $R$，使

$$
R^{\mathrm T}AR=\begin{pmatrix}
T_{11}&T_{12}&\cdots&T_{1s}\\
&T_{22}&\cdots&T_{2s}\\
&&\ddots&\vdots\\
&&&T_{ss}
\end{pmatrix},
$$

其中对角块为一阶或二阶矩阵，每一个一阶对角块即为 $A$ 的实特征值，每一个二阶对角块的两个特征值是 $A$ 的一对共轭复特征值。

**定义 9.2** 一方阵 $B$，如果当 $i>j+1$ 时有 $b_{ij}=0$，则称 $B$ 为上 Hessenberg 阵，即

$$
B=\begin{pmatrix}
b_{11}&b_{12}&\cdots&b_{1n}\\
b_{21}&b_{22}&\cdots&b_{2n}\\
&\ddots&\ddots&\vdots\\
&&b_{n,n-1}&b_{nn}
\end{pmatrix}.
$$

本节讨论如下两个问题：

（1）用正交相似变换约化一般实矩阵为上 Hessenberg 阵；

（2）用正交相似变换约化对称阵为三对角阵。

这样，求原矩阵特征值问题，就转化为求上 Hessenberg 阵或对称三对角阵的特征值问题。

**定义 9.3** 设向量 $w$ 满足 $\|w\|_2=1$，矩阵 $H=I-2ww^{\mathrm T}$ 称为初等反射阵，记作 $H(w)$，即

$$
H(w)=\begin{pmatrix}
1-2w_1^2&-2w_1w_2&\cdots&-2w_1w_n\\
-2w_2w_1&1-2w_2^2&\ddots&\vdots\\
\vdots&\ddots&\ddots&-2w_{n-1}w_n\\
-2w_nw_1&\cdots&-2w_nw_{n-1}&1-2w_n^2
\end{pmatrix},
$$

<!-- 定义中的向量分量续 PDF 244。 -->
''',[{'id':'9.3','title':'Householder 方法'},{'id':'9.3.1','title':'引言'}],['实际打开全页原图，确认书页 230；核对定理 9.10 的上三角分块、定义 9.2 的 Hessenberg 条件和定义 9.3；实际打开首段文字裁切，保留原印“若要求求出”；实际打开 H(w) 矩阵裁切，逐项核对 n-1/n 下标和全部负号。'])
write_page(244,r'''
<!-- 续 PDF 243，9.3.1 引言，定义 9.3。 -->

其中

$$
w=(w_1,w_2,\cdots,w_n)^{\mathrm T}.
$$

**定理 9.11** 初等反射阵 $H$ 是对称阵（$H^{\mathrm T}=H$）、正交阵（$H^{\mathrm T}H=I$）和对合阵（$H^2=I$）。

**证明** 只证 $H$ 的正交性，其他显然。

$$
H^{\mathrm T}H=H^2=(I-2ww^{\mathrm T})(I-2ww^{\mathrm T})=I-4ww^{\mathrm T}+4w(w^{\mathrm T}w)w^{\mathrm T}=I.
$$

设向量 $u\ne0$，则显然 $H=I-2\dfrac{uu^{\mathrm T}}{\|u\|_2^2}$ 是一个初等反射阵。

下面考察初等反射阵的几何意义。考虑以 $w$ 为法向量过原点 $O$ 的超平面

$$
S:w^{\mathrm T}x=0.
$$

设任意向量 $v\in\mathbf R^n$，则 $v=x+y$，其中 $x\in S,y\in S^{\perp}$。于是

$$
Hx=(I-2ww^{\mathrm T})x=x-2ww^{\mathrm T}x=x.
$$

对于 $y\in S^{\perp}$，易知 $Hy=-y$，从而对于任意向量 $v\in\mathbf R^n$，总有

$$
Hv=x-y=v',
$$

其中 $v'$ 为 $v$ 关于平面 $S$ 的镜面反射（见图 9.1）。

![图 9.1，初等反射阵的几何意义，原图裁切](../assets/fig-9-1.png)

图 9.1（原图裁切）。图中符号为 $w,v,x,y,O,S,v'$。超平面 $S$ 经过原点 $O$，$w$ 为法向量；$v=x+y$ 分解为平面内分量 $x$ 与垂直分量 $y$，$v'$ 位于平面另一侧，表示镜面反射所得 $x-y$。原图用虚线连接 $O$、$v'$ 端点及垂直分量方向。

初等反射阵在计算上的意义是它能用来约化矩阵，例如设向量 $a\ne0$，可选择一初等反射阵 $H$ 使 $H_a=\sigma e_1$。这种约化矩阵的方法称为 Householder 方法。为此给出下面定理。

**定理 9.12** 设 $x,y$ 为两个不相等的 $n$ 维向量，$\|x\|_2=\|y\|_2$，则存在一个初等反射阵 $H$，使 $Hx=y$。

**证明** 令 $w=\dfrac{x-y}{\|x-y\|_2}$，则得到一个初等反射阵

$$
H=I-2ww^{\mathrm T}=I-2\frac{(x-y)}{\|x-y\|_2^2}(x^{\mathrm T}-y^{\mathrm T}),
$$

而且

$$
Hx=x-2\frac{x-y}{\|x-y\|_2^2}(x^{\mathrm T}-y^{\mathrm T})x=x-2\frac{(x-y)(x^{\mathrm T}x-y^{\mathrm T}x)}{\|x-y\|_2^2},
$$

因为

$$
\|x-y\|_2^2=(x-y)^{\mathrm T}(x-y)=2(x^{\mathrm T}x-y^{\mathrm T}x),
$$

所以

$$
Hx=x-(x-y)=y.
$$

易知，$w=\dfrac{x-y}{\|x-y\|_2}$ 是使 $Hx=y$ 成立的唯一长度等于 1 的向量（不计符号）。

**推论** 设向量 $x\in\mathbf R^n\ (x\ne0)$，$\sigma=\pm\|x\|_2$，且 $x\ne-\sigma e_1$，则存在一个初等反射阵

$$
H=I-2\frac{uu^{\mathrm T}}{\|u\|_2^2}\equiv I-\rho^{-1}uu^{\mathrm T},
$$

使 $Hx=-\sigma e_1$，其中 $u=x+\sigma e_1$，$\rho=\|u\|_2^2/2$。

设

$$
x=(\alpha_1,\alpha_2,\cdots,\alpha_n)^{\mathrm T}\ne0,\quad u=(u_1,u_2,\cdots,u_n)^{\mathrm T},
$$

<!-- 推论的分量推导续 PDF 245。 -->

> **校注（agent 补充，ch09a-E008）** 在“可选择一初等反射阵 $H$ 使”后，原图把 $a$ 印在 $H$ 的下标位置，故照录为 $H_a=\sigma e_1$。依本段语义及随后定理的矩阵作用，应为乘积 $Ha=\sigma e_1$；疑为原书排版错误。见[放大原式](../assets/review-p244-Ha.png)。
''',[],['实际打开全页原图，确认书页 231；核对定理 9.11–9.12 全证明及推论的符号、范数平方、ρ 定义；实际打开 Ha 文字裁切，确认 a 下标位置并记录 ch09a-E008；实际打开图 9.1 原图裁切，确认 w/v/x/y/O/S/v′ 全部标签及虚线。'],['9.1'])
add_errata([{'id':'ch09a-E008','pdf_page':244,'printed_page':231,'kind':'suspected_source_erratum','location':'图 9.1 旁的 Householder 方法说明','source_form':'H_a = sigma e_1','explanation':'原图 a 印为 H 的下标；由语义及后续定理应是矩阵向量乘积 Ha。原排式保留。','evidence_asset':'staging/ch09a/assets/review-p244-Ha.png'}])
