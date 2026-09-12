from write_pages import write_page,add_errata
write_page(233,r'''
# 第 9 章 矩阵的特征值与特征向量计算

## 9.1 引言

物理、力学和工程技术中的很多问题在数学上都归结为求矩阵特征值的问题，例如振动问题（桥梁的振动、机械的振动、电磁振荡、地震引起的建筑物的振动等）、物理学中某些临界值的确定问题以及理论物理中的一些问题。这些实际问题可归结为如下数学问题。

（1）已知 $A=(a_{ij})_{n\times n}$，要求代数方程

$$
\varphi(\lambda)=\det(\lambda I-A)=0
\tag{9.1.1}
$$

的根。$\varphi(\lambda)$ 称为 $A$ 的特征多项式。式（9.1.1）展开即有

$$
\varphi(\lambda)=\lambda^n+c_1\lambda^{n-1}+\cdots+c_n=0.
$$

一般 $\varphi(\lambda)$ 有 $n$ 个零点，称为 $A$ 的特征值。

（2）设 $\lambda$ 为 $A$ 的特征值，要求相应的齐次方程组

$$
(\lambda I-A)x=0
\tag{9.1.2}
$$

的非零解（即求 $Ax=\lambda x$ 的非零解）。

式（9.1.2）的非零解 $x$ 称为矩阵 $A$ 的对应于 $\lambda$ 的特征向量。下面叙述一些有关特征值问题的结论。

**定理 9.1** 如果 $\lambda_i\ (i=1,2,\cdots,n)$ 是矩阵 $A$ 的特征值，则有

$$
1^\circ\quad \sum_{i=1}^n\lambda_i=\sum_{i=1}^na_{ii}=\operatorname{tr}A;
$$

$$
2^\circ\quad \det A=\lambda_1\lambda_2\cdots\lambda_n.
$$

**定理 9.2** 设 $A$ 与 $B$ 为相似矩阵（即存在非奇异阵 $T$ 使 $B=T^{-1}AT$），则

$1^\circ$ $A$ 与 $B$ 有相同的特征值；

$2^\circ$ 若 $x$ 是 $B$ 的一个特征向量，则 $Tx$ 是 $A$ 的特征向量。

**定理 9.3（Gerschgorin's 定理）** 设 $A=(a_{ij})_{n\times n}$，则 $A$ 的每一个特征值必属于下述某个圆盘之中：

$$
|\lambda-a_{ii}|\leq\sum_{\substack{j=1\\j\ne i}}^n|a_{ij}|\qquad(i=1,2,\cdots,n).
$$

**证明** 设 $\lambda$ 为 $A$ 的任意一个特征值，$x$ 为对应的特征向量，即

$$
(\lambda I-A)x=0,
$$

<!-- 本页证明未完，续 PDF 234。 -->
''',[{'id':'9','title':'矩阵的特征值与特征向量计算'},{'id':'9.1','title':'引言'}],['实际打开全页原图，目视确认书页 220；核对定理 9.1–9.3、公式 9.1.1–9.1.2、特征多项式及圆盘求和上下限；证明跨页续 PDF 234。'])
write_page(234,r'''
<!-- 续 PDF 233，9.1 引言，定理 9.3 的证明。 -->

记 $x=(x_1,x_2,\cdots,x_n)^{\mathrm T}\ne0$ 及 $|x_i|=\max_k|x_k|$，$x_i\ne0$，所以从式（9.1.2）的第 $i$ 个方程

$$
(\lambda-a_{ii})x_i=\sum_{\substack{j=1\\j\ne i}}^na_{ij}x_j
$$

以及 $|x_j/x_i|\leq1\ (j\ne i)$，有

$$
|\lambda-a_{ii}|\leq\sum_{j\ne i}|a_{ij}|,\quad |x_j/x_i|\leq\sum_{j\ne i}|a_{ij}|.
$$

这说明 $\lambda$ 属于复平面上以 $a_{ii}$ 为圆心、$\sum_{j\ne i}|a_{ij}|$ 为半径的一个圆盘。

定理的证明，不仅指出了 $A$ 的每一个特征值必属于 $A$ 的一个圆盘中，而且指出，若一个特征向量的第 $i$ 个分量最大，则对应的特征值一定属于第 $i$ 个圆盘中。

**定义 9.1** 设 $A$ 为 $n$ 阶实对称矩阵，对于任一非零向量 $x$，称 $R(x)=\dfrac{(Ax,x)}{(x,x)}$ 为对应于向量 $x$ 的 Rayleigh 商。

**定理 9.4** 设 $A\in\mathbf R^{n\times n}$ 为对称矩阵（其特征值依次记作 $\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_n$，对应的特征向量 $x_1,x_2,\cdots,x_n$ 组成规范化正交组，即 $(x_i,x_j)=\delta_{ij}$），则

$$
1^\circ\quad \lambda_n\leq\frac{(Ax,x)}{(x,x)}\leq\lambda_1\qquad\text{（对于任何非零 }x\in\mathbf R^n\text{）};
$$

$$
2^\circ\quad \lambda_1=\max_{\substack{x\in\mathbf R^n\\x\ne0}}\frac{(Ax,x)}{(x,x)};
$$

$$
3^\circ\quad \lambda_n=\min_{\substack{x\in\mathbf R^n\\x\ne0}}\frac{(Ax,x)}{(x,x)}.
$$

**证明** 只证结论 $1^\circ$，结论 $2^\circ$、$3^\circ$ 留作习题。

设 $x\ne0$ 为 $\mathbf R^n$ 中任一向量，则有展开式

$$
x=\sum_{i=1}^na_ix_i,\quad \|x\|_2=\left(\sum_{i=1}^na_i^2\right)^2\ne0,
$$

于是

$$
\frac{(Ax,x)}{(x,x)}=\frac{\displaystyle\sum_{i=1}^na_i^2\lambda_i}{\displaystyle\sum_{i=1}^na_i^2},
$$

从而结论 $1^\circ$ 成立。结论 $1^\circ$ 说明 Rayleigh 商必位于 $\lambda_n$ 和 $\lambda_1$ 之间。

关于计算矩阵 $A$ 的特征值问题，当 $n=2,3$ 时，还可按行列式展开的办法求 $\varphi(\lambda)=0$ 的根。但当 $n$ 较大时，如果按展开行列式的办法，首先求出 $\varphi(\lambda)$ 的系数，再求 $\varphi(\lambda)$ 的根，工作量就非常大了。用这种办法求矩阵特征值是不切实际的，由此需要研究求 $A$ 的特征值及特征向量的数值方法。

本章将介绍计算机上常用的两类方法，一类是幂法及反幂法（迭代法），另一类是正交相似变换的方法（变换法）。

> **校注（agent 补充，ch09a-E001）** 原图中 Gerschgorin 证明的上述不等式在 $\sum_{j\ne i}|a_{ij}|$ 后印有逗号，接着印 $|x_j/x_i|\leq\sum_{j\ne i}|a_{ij}|$，已照录。由上一行除以 $x_i$ 后取绝对值，能推出的是 $|\lambda-a_{ii}|\leq\sum_{j\ne i}|a_{ij}|\,|x_j/x_i|\leq\sum_{j\ne i}|a_{ij}|$；故原排式疑有标点或连乘排版错误。见[放大原式](../assets/review-p234-gershgorin.png)。
>
> **校注（agent 补充，ch09a-E002）** 原图范数展开式的括号外指数印为 $2$，已照录。由规范化正交性，$\|x\|_2^2=\sum_i a_i^2$，故该处指数应为 $1/2$；这是原书疑误，非转录时补成的指数。见[放大原式](../assets/review-p234-norm.png)。
''',[],['实际打开全页原图，目视确认书页 221；逐项核对定义 9.1、定理 9.4 的三条结论及证明；另裁切并实际打开 Gerschgorin 不等式和范数展开式，确认原页逗号及指数 2，记录 ch09a-E001、ch09a-E002。'])
write_page(235,r'''
## 9.2 幂法及反幂法

### 9.2.1 幂法

在一些工程、物理问题中，通常只需要求出矩阵的按模最大的特征值（称为 $A$ 的主特征值）和相应的特征向量，对于解这种特征值问题，应用幂法是合适的。

幂法是一种计算实矩阵 $A$ 的主特征值的一种迭代法，它最大的优点是方法简单，对于稀疏矩阵较合适，但有时收敛速度很慢。

设实矩阵 $A=(a_{ij})_n$ 有一个完全的特征向量组，其特征值为 $\lambda_1,\lambda_2,\cdots,\lambda_n$，相应的特征向量为 $x_1,x_2,\cdots,x_n$。已知 $A$ 的主特征值是实根，且满足条件

$$
|\lambda_1|>|\lambda_2|\geq|\lambda_3|\geq\cdots\geq|\lambda_n|.
\tag{9.2.1}
$$

幂法的基本思想是任取一个非零的初始向量 $v_0$，由矩阵 $A$ 构造一向量序列

$$
\left\{
\begin{aligned}
v_1&=Av_0,\\
v_2&=Av_1=A^2v_0,\\
&\quad\vdots\\
v_{k+1}&=Av_k=A^{k+1}v_0,\\
&\quad\vdots
\end{aligned}
\right.
\tag{9.2.2}
$$

称为迭代向量。由假设，$v_0$ 可表示为

$$
v_0=a_1x_1+a_2x_2+\cdots+a_nx_n\quad\text{（设 }a_1\ne0\text{）},
\tag{9.2.3}
$$

于是

$$
\begin{aligned}
v_k&=Av_{k-1}=A^kv_0=a_1\lambda_1^kx_1+a_2\lambda_2^kx_2+\cdots+a_n\lambda_n^kx_n\\
&=\lambda_1^k\left[a_1x_1+\sum_{i=2}^na_1(\lambda_i/\lambda_1)^kx_i\right]=\lambda_1^k(a_1x_1+\varepsilon_k),
\end{aligned}
$$

其中 $\varepsilon_k=\displaystyle\sum_{i=2}^na_1(\lambda_i/\lambda_1)^kx_i$。由假设 $|\lambda_i/\lambda_1|<1\ (i=2,3,\cdots,n)$，故 $\varepsilon_k\to0\ (k\to\infty)$，从而

$$
\lim_{k\to\infty}\frac{v_k}{\lambda_1^k}=a_1x_1.
\tag{9.2.4}
$$

这说明序列 $\dfrac{v_k}{\lambda_1^k}$ 越来越接近 $A$ 的对应于 $\lambda_1$ 的特征向量，或者说当 $k$ 充分大时

$$
v_k\approx a_1\lambda_1^kx_1,
\tag{9.2.5}
$$

即迭代向量 $v_k$ 为 $\lambda_1$ 的特征向量的近似向量（除一个因子外）。

下面再考虑主特征值 $\lambda_1$ 的计算。用 $(v_k)_i$ 表示 $v_k$ 的第 $i$ 个分量，则

$$
\frac{(v_{k+1})_i}{(v_k)_i}=\lambda_1\left\{\frac{a_1(x_1)_i+(\varepsilon_{k+1})_i}{a_1(x_1)_i+(\varepsilon_k)_i}\right\},
\tag{9.2.6}
$$

<!-- 本段续 PDF 236。 -->

> **校注（agent 补充，ch09a-E003）** 本页 $v_k$ 第二行求和项及 $\varepsilon_k$ 定义中的系数下标，原图均印为 $a_1$，已照录；与前一行 $a_i\lambda_i^kx_i$ 的展开相比较，两处应为 $a_i$ 才能保持恒等，属原书疑误。见[放大原式](../assets/review-p235-power-expansion.png)。
''',[{'id':'9.2','title':'幂法及反幂法'},{'id':'9.2.1','title':'幂法'}],['实际打开全页原图，目视确认书页 222；核对迭代向量序列、9.2.1–9.2.6 和跨页末公式；放大实际查看两处求和系数，确认印作 a_1，记录 ch09a-E003。'])
add_errata([
 {'id':'ch09a-E001','pdf_page':234,'printed_page':221,'kind':'suspected_source_erratum','location':'定理 9.3 证明不等式','source_form':'|lambda-a_ii| <= sum |a_ij|, |x_j/x_i| <= sum |a_ij|','explanation':'原图逗号将所需连乘拆开；由上一行应为 sum |a_ij||x_j/x_i| 的链式不等式。原式保留。','evidence_asset':'staging/ch09a/assets/review-p234-gershgorin.png'},
 {'id':'ch09a-E002','pdf_page':234,'printed_page':221,'kind':'source_erratum','location':'定理 9.4 证明范数展开式','source_form':'norm(x,2)=(sum a_i^2)^2','explanation':'括号外指数原印 2；规范化正交性给出指数 1/2。原式保留。','evidence_asset':'staging/ch09a/assets/review-p234-norm.png'},
 {'id':'ch09a-E003','pdf_page':235,'printed_page':222,'kind':'source_erratum','location':'9.2.3 后 v_k 展开与 epsilon_k 定义','source_form':'sum_{i=2}^n a_1(lambda_i/lambda_1)^k x_i','explanation':'两处系数原印 a_1，前一行展开要求 a_i。原式保留。','evidence_asset':'staging/ch09a/assets/review-p235-power-expansion.png'}
])
