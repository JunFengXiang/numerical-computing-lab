from write_pages import write_page,add_errata
write_page(236,r'''
<!-- 续 PDF 235，9.2.1 幂法。 -->

故

$$
\lim_{k\to\infty}\frac{(v_{k+1})_i}{(v_k)_i}=\lambda_1,
\tag{9.2.7}
$$

也就是说，两相邻迭代向量分量的比值收敛到主特征值。

这种由已知非零向量 $v_0$ 及矩阵 $A$ 的乘幂 $A^k$ 构造向量序列 $\{v_k\}$ 以计算 $A$ 的主特征值 $\lambda_1$（利用式（9.2.7））及相应特征向量（利用式（9.2.5））的方法称为幂法。

由式（9.2.6）知，$(v_{k+1})_i/(v_k)_i\to\lambda_1$ 的收敛速度由比值 $r=\lambda_2/\lambda_1$ 来确定，$r$ 越小收敛越快，但当 $r=\lambda_2/\lambda_1\approx1$ 时收敛可能就很慢。

总结上述讨论，有如下定理。

**定理 9.5** 设 $A\in\mathbf R^{n\times n}$ 有 $n$ 个线性无关的特征向量，主特征值 $\lambda_1$ 满足

$$
|\lambda_1|>|\lambda_2|\geq|\lambda_3|\geq\cdots\geq|\lambda_n|,
$$

则对于任何非零初始向量 $v_0\ (a_1\ne0)$，式（9.2.4）、（9.2.7）成立。

设 $A$ 的主特征值为实重根，即 $\lambda_1=\lambda_2=\cdots=\lambda_r$，且 $|\lambda_r|>|\lambda_{r+1}|\geq\cdots\geq|\lambda_n|$，又设 $A$ 有 $n$ 个线性无关的特征向量，$\lambda_1$ 对应的 $r$ 个线性无关特征向量为 $x_1,x_2,\cdots,x_r$，则由式（9.2.2），有

$$
v_k=A^kv_0=\lambda_1^k\left\{\sum_{i=1}^ra_ix_i+\sum_{i=r+1}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right\},\quad
\lim_{k\to\infty}\frac{v_k}{\lambda_1^k}=\sum_{i=1}^ra_ix_i\quad\text{（设 }\sum_{i=1}^ra_ix_i\ne0\text{）}.
$$

这说明当 $A$ 的主特征值是实的重根时，定理 9.5 的结论还是正确的。

应用幂法计算 $A$ 的主特征值 $\lambda_1$ 及对应的特征向量时，如果 $|\lambda_1|>1$（或 $|\lambda_1|<1$），迭代向量 $v_k$ 的各个不等于零的分量将随 $k\to\infty$ 而趋于无穷（或趋于零），这样在用计算机计算时就可能“溢出”。为了克服这个缺点，就需要将迭代向量加以规范化。

设有一向量 $v\ne0$，将其规范化得到向量 $u=\dfrac{v}{\max(v)}$，其中 $\max(v)$ 表示向量 $v$ 的绝对值最大的分量。

在定理 9.5 的条件下幂法可这样进行：任取一初始向量 $v_0\ne0\ (a_1\ne0)$，构造向量序列

$$
\left\{
\begin{aligned}
v_1&=Au_0=Av_0,&u_1&=\frac{v_1}{\max(v_1)}=\frac{Av_0}{\max(Av_0)},\\
v_2&=Au_1=\frac{A^2v_0}{\max(Av_0)},&u_2&=\frac{v_2}{\max(v_2)}=\frac{A^2v_0}{\max(A^2v_0)},\\
&\quad\vdots&&\quad\vdots\\
v_k&=\frac{A^kv_0}{\max(A^{k-1}v_0)},&u_k&=\frac{A^kv_0}{\max(A^kv_0)}.
\end{aligned}
\right.
$$

由式（9.2.3），有

$$
Av_0=\sum_{i=1}^na_i\lambda_i^kx_i=\lambda_i^k\left[a_1x_1+\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right],
\tag{9.2.8}
$$

<!-- 推导续 PDF 237。 -->

> **校注（agent 补充，ch09a-E004）** 式（9.2.8）原图左端为 $Av_0$，右端方括号前为 $\lambda_i^k$，均照录。由 $v_0=\sum_i a_ix_i$ 和 $Ax_i=\lambda_ix_i$，中间求和等于 $A^kv_0$，而提取的公共因子应为 $\lambda_1^k$；故有漏印幂次及因子下标疑误。见[放大原式](../assets/review-p236-9-2-8.png)。
''',[],['实际打开全页原图，确认书页 223；核对定理 9.5、重复主特征值展开、规范化序列和 9.2.7–9.2.8；实际打开 9.2.8 裁切图，确认原印 Av_0、λ_i^k，记 ch09a-E004。'])
write_page(237,r'''
<!-- 续 PDF 236，9.2.1 幂法的规范化推导。 -->

$$
\begin{aligned}
u_k&=\frac{A^kv_0}{\max(A^kv_0)}
=\frac{\lambda_i^k\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right]}{\max\left[\lambda_1^k\left(a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right)\right]}\\
&=\frac{\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right]}{\max\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right]}
\to\frac{x_1}{\max(x_1)}\qquad(k\to\infty).
\end{aligned}
$$

这说明规范化向量序列收敛到主特征值对应的特征向量。

同理，可得到

$$
v_k=\frac{\lambda_1^k\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right]}{\max\left[\lambda_1^{k-1}a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^{k-1}x_i\right]},
$$

$$
\max(v_k)=\frac{\lambda_1\max\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^kx_i\right]}{\max\left[a_1x_1+\displaystyle\sum_{i=2}^na_i\left(\frac{\lambda_i}{\lambda_1}\right)^{k-1}x_i\right]}\to\lambda_1\qquad(k\to\infty).
$$

收敛速度由比值 $r=\lambda_2/\lambda_1$ 确定。

总结上述讨论，有如下定理。

**定理 9.6** 设 $A\in\mathbf R^{n\times n}$ 有 $n$ 个线性无关的特征向量，主特征值 $\lambda_1$ 满足 $|\lambda_1|>|\lambda_2|\geq|\lambda_3|\geq\cdots\geq|\lambda_n|$，则对于任意非零初始向量 $v_0=u_0\ (a_1\ne0)$，按下述方法构造的向量序列

$$
\left\{
\begin{aligned}
v_0&=u_0\ne0,\\
v_k&=Au_{k-1},\\
u_k&=\frac{v_k}{\max(v_k)}
\end{aligned}
\right.\qquad(k=1,2,\cdots),
\tag{9.2.9}
$$

有

$$
\lim_{k\to\infty}u_k=\frac{x_1}{\max(x_1)},\quad\lim_{k\to\infty}\max(v_k)=\lambda_1.
$$

**例 9.1** 用幂法计算 $A=\begin{pmatrix}1.0&1.0&0.5\\1.0&1.0&0.25\\0.5&0.25&2.0\end{pmatrix}$ 的主特征值和相应的特征向量。

**解** 计算过程如表 9.1 所示。

下述结果是用 8 位浮点数字进行运算得到的，$u_k$ 的分量值是舍入值。于是得到

$$
\lambda_1\approx2.536\,532\,3
$$

及相应特征向量 $(0.748\,2,\ 0.649\,7,\ 1)^{\mathrm T}$。$\lambda_1$ 和相应的特征向量真值（8 位数字）为

$$
\lambda_1=2.536\,525\,8,\quad\widetilde{x}_1=(0.748\,221\,16,\ 0.649\,661\,16,\ 1)^{\mathrm T}.
$$

<!-- 表 9.1 在 PDF 238。 -->

> **校注（agent 补充，ch09a-E005）** 页首 $u_k$ 第一行分子方括号前原印 $\lambda_i^k$，分母对应因子为 $\lambda_1^k$，已照录；与 $A^kv_0$ 的展开及下一行相消过程对照，分子因子应为 $\lambda_1^k$。见[放大原式](../assets/review-p237-u-k-numerator.png)。
>
> **校注（agent 补充，ch09a-E006）** 本页 $v_k$ 式分母中，原图 $\lambda_1^{k-1}$ 仅直接乘 $a_1x_1$，随后为加号及求和项，已照录。由上一页 $v_k=A^kv_0/\max(A^{k-1}v_0)$，分母应把 $\lambda_1^{k-1}$ 乘在整个 $a_1x_1+\sum_{i=2}^na_i(\lambda_i/\lambda_1)^{k-1}x_i$ 上，故疑漏一层括号。见[放大原式](../assets/review-p237-v-k-denominator.png)。
''',[],['实际打开全页原图，确认书页 224；核对定理 9.6、公式 9.2.9、例 9.1 的 3×3 矩阵和数值；实际打开页首分子及 v_k 分母裁切图，确认原式疑误 ch09a-E005、ch09a-E006。'])
write_page(238,r'''
<!-- 续 PDF 237，例 9.1。 -->

**表 9.1**

| $k$ | $u_k^{\mathrm T}$（规范化向量） | $\max(v_k)$ |
|---:|:---:|---:|
| 0 | $(1,1,1)$ | |
| 1 | $(0.909\,1,\ 0.818\,2,\ 1)$ | $2.750\,000\,0$ |
| 5 | $(0.765\,1,\ 0.667\,4,\ 1)$ | $2.558\,791\,8$ |
| 10 | $(0.749\,4,\ 0.650\,8,\ 1)$ | $2.538\,002\,9$ |
| 15 | $(0.748\,3,\ 0.649\,7,\ 1)$ | $2.536\,625\,6$ |
| 16 | $(0.748\,3,\ 0.649\,7,\ 1)$ | $2.536\,584\,0$ |
| 17 | $(0.748\,2,\ 0.649\,7,\ 1)$ | $2.536\,559\,8$ |
| 18 | $(0.748\,2,\ 0.649\,7,\ 1)$ | $2.536\,545\,6$ |
| 19 | $(0.748\,2,\ 0.649\,7,\ 1)$ | $2.536\,537\,4$ |
| 20 | $(0.748\,2,\ 0.649\,7,\ 1)$ | $2.536\,532\,3$ |

### 9.2.2 加速方法

#### 1. 原点平移法

由前面讨论知道，应用幂法计算 $A$ 的主特征值时，其收敛速度主要由比值 $r=\dfrac{\lambda_1}{\lambda_2}$ 来决定，但当 $r$ 接近于 1 时，收敛可能很慢。这时，一个补救的办法是采用加速收敛的方法。

引进矩阵 $B=A-pI$，其中 $p$ 为选择参数。

设 $A$ 的特征值为 $\lambda_1,\lambda_2,\cdots,\lambda_n$，则 $B$ 的相应特征值为 $\lambda_1-p,\lambda_2-p,\cdots,\lambda_n-p$，而且 $A,B$ 的特征向量相同。

如果需要计算 $A$ 的主特征值 $\lambda_1$，就要选择适当的 $p$ 使 $\lambda_1-p$ 仍然是 $B$ 的主特征值，且使

$$
\left|\frac{\lambda_2-p}{\lambda_1-p}\right|<\left|\frac{\lambda_2}{\lambda_1}\right|.
$$

对 $B$ 应用幂法，使得在计算 $B$ 的主特征值 $\lambda_1-p$ 的过程中得到加速。这种方法通常称为原点平移法。对于 $A$ 的特征值的某种分布，它是十分有效的。

**例 9.2** 设 $A=(a_{ij})_4$ 有特征值 $\lambda_j=15-j\quad(j=1,2,3,4)$，比值 $r=\lambda_2/\lambda_1\approx0.9$。

作变换

$$
B=A-pI\quad(p=12),
$$

则 $B$ 的特征值为 $\mu_1=2,\ \mu_2=1,\ \mu_3=0,\ \mu_4=-1$。应用幂法计算 $B$ 的主特征值 $\mu_1$ 的收敛速度的比值为

$$
\left|\frac{\mu_2}{\mu_1}\right|=\left|\frac{\lambda_2-p}{\lambda_1-p}\right|=\frac12<\left|\frac{\lambda_2}{\lambda_1}\right|\approx0.9.
$$

> **校注（agent 补充，ch09a-E007）** 本页“原点平移法”首段原印 $r=\lambda_1/\lambda_2$，已照录；前页及本页例 9.2 均用 $r=\lambda_2/\lambda_1$，与幂法误差项 $(\lambda_i/\lambda_1)^k$ 对照，此处疑将分子、分母颠倒。见[放大原式](../assets/review-p238-ratio.png)。
''',[{'id':'9.2.2','title':'加速方法'}],['实际打开全页原图，确认书页 225；另实际打开表 9.1 裁切图，逐行核对 10 个数据行、向量分量和 8 位数值；核对原点平移法、例 9.2，确认首段 r=λ_1/λ_2 原印并记 ch09a-E007。'],[],['9.1'])
add_errata([
 {'id':'ch09a-E004','pdf_page':236,'printed_page':223,'kind':'source_erratum','location':'式 9.2.8','source_form':'Av_0 = sum a_i lambda_i^k x_i = lambda_i^k[...]','explanation':'中间式应为 A^k v_0，提取公共因子应为 lambda_1^k；原图漏幂及下标 i 均保留。','evidence_asset':'staging/ch09a/assets/review-p236-9-2-8.png'},
 {'id':'ch09a-E005','pdf_page':237,'printed_page':224,'kind':'source_erratum','location':'页首 u_k 展开第一行分子','source_form':'lambda_i^k [a_1 x_1 + sum ...]','explanation':'原印 lambda_i^k；根据同式分母及下一行相消应为 lambda_1^k。原式保留。','evidence_asset':'staging/ch09a/assets/review-p237-u-k-numerator.png'},
 {'id':'ch09a-E006','pdf_page':237,'printed_page':224,'kind':'source_erratum','location':'v_k 展开式分母','source_form':'max[lambda_1^(k-1) a_1 x_1 + sum ...]','explanation':'根据 max(A^(k-1)v_0)，lambda_1^(k-1) 应乘整个括号，疑漏括号。原式保留。','evidence_asset':'staging/ch09a/assets/review-p237-v-k-denominator.png'},
 {'id':'ch09a-E007','pdf_page':238,'printed_page':225,'kind':'source_erratum','location':'9.2.2 第一段','source_form':'r=lambda_1/lambda_2','explanation':'与前页及本页例 9.2 的 lambda_2/lambda_1 颠倒；原式保留。','evidence_asset':'staging/ch09a/assets/review-p238-ratio.png'}
])
