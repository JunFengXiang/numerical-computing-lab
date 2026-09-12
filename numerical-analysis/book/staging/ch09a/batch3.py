from write_pages import write_page
write_page(239,r'''
<!-- 续 PDF 238，9.2.2 加速方法，1. 原点平移法。 -->

虽然常常能够选择有利的 $p$ 值，使幂法得到加速，但设计一个自动选择适当参数 $p$ 的过程是困难的。

下面考虑当 $A$ 的特征值是实数时，怎样选择 $p$ 使用幂法计算 $\lambda_1$ 以得到加速。

设 $A$ 的特征值满足

$$
\lambda_1>\lambda_2\geq\cdots\geq\lambda_{n-1}>\lambda_n,
\tag{9.2.10}
$$

则不管 $p$ 如何选择，$B=A-pI$ 的主特征值为 $\lambda_1-p$ 或 $\lambda_n-p$。当希望计算 $\lambda_1$ 及 $x_1$ 时，首先应选择 $p$ 使 $|\lambda_1-p|>|\lambda_n-p|$，且使收敛速度的比值

$$
\omega=\max\left\{\frac{|\lambda_2-p|}{|\lambda_1-p|},\frac{|\lambda_n-p|}{|\lambda_1-p|}\right\}=\min,
$$

显然，当 $\lambda_2-p=-(\lambda_n-p)$，$p=\dfrac{\lambda_2+\lambda_n}{2}\equiv p^*$ 时 $\omega$ 为最小，这时收敛速度的比值为

$$
\frac{\lambda_2-p^*}{\lambda_1-p^*}=-\frac{\lambda_n-p^*}{\lambda_1-p^*}\equiv\frac{\lambda_2-\lambda_n}{2\lambda_1-\lambda_2-\lambda_n}.
$$

当 $A$ 的特征值满足式（9.2.10）且 $\lambda_2,\lambda_n$ 能初步估计时，就能确定 $p^*$ 的近似值。

当希望计算 $\lambda_n$ 时，应选择 $p=\dfrac{\lambda_1+\lambda_{n-1}}{2}=p^*$，使得应用幂法计算 $\lambda_n$ 得到加速。

**例 9.3** 计算例 9.1 矩阵 $A$ 的主特征值。

**解** 作变换 $B=A-pI$，取 $p=0.75$，则

$$
B=\begin{pmatrix}
0.25&1&0.5\\
1&0.25&0.25\\
0.5&0.25&1.25
\end{pmatrix}.
$$

对 $B$ 应用幂法，计算结果如表 9.2 所示。

**表 9.2**

| $k$ | $u_k^{\mathrm T}$（规范化向量） | $\max(v_k)$ |
|---:|:---:|---:|
| 0 | $(1,1,1)$ | |
| 5 | $(0.751\,6,\ 0.652\,2,\ 1)$ | $1.791\,401\,1$ |
| 6 | $(0.749\,1,\ 0.651\,1,\ 1)$ | $1.788\,844\,3$ |
| 7 | $(0.748\,8,\ 0.650\,1,\ 1)$ | $1.787\,330\,0$ |
| 8 | $(0.748\,4,\ 0.649\,9,\ 1)$ | $1.786\,915\,2$ |
| 9 | $(0.748\,3,\ 0.649\,7,\ 1)$ | $1.786\,658\,7$ |
| 10 | $(0.748\,2,\ 0.649\,7,\ 1)$ | $1.786\,591\,4$ |

由此得 $B$ 的主特征值为 $\mu_1\approx1.786\,591\,4$，$A$ 的主特征值 $\lambda_1$ 为

$$
\lambda_1\approx\mu_1+0.75=2.536\,591\,4.
$$

这个结果比例 9.1 迭代 15 次得到的结果还要好。若迭代 15 次，$\mu_1=1.786\,525\,8$（相应的 $\lambda_1=2.536\,525\,8$）。
''',[],['实际打开全页原图，确认书页 226；核对 9.2.10 的不等号、最优位移公式、例 9.3 矩阵及结尾数值；另实际打开表 9.2 放大图，逐行核对全部 7 行和空白初始 max 单元格。'],[],['9.2'])
write_page(240,r'''
<!-- 续 PDF 239，9.2.2 加速方法。 -->

原点位移的加速方法，是一个矩阵变换方法。这种变换容易计算，又不破坏矩阵 $A$ 的稀疏性，但 $p$ 的选择依赖于对 $A$ 的特征值分布的大致了解。

#### 2. Rayleigh 商加速法

由定理 9.4 知，对称矩阵 $A$ 的 $\lambda_1$ 及 $\lambda_n$ 可用 Rayleigh 商的极值来表示。下面将把 Rayleigh 商应用到用幂法计算实对称矩阵 $A$ 的主特征值的加速收敛上来。

**定理 9.7** 设 $A\in\mathbf R^{n\times n}$ 为对称矩阵，特征值满足 $|\lambda_1|>|\lambda_2|\geq|\lambda_3|\geq\cdots\geq|\lambda_n|$，对应的特征向量满足 $(x_i,x_j)=\delta_{ij}$，应用幂法（式（9.2.9））计算 $A$ 的主特征值 $\lambda_1$，则规范化向量 $u_k$ 的 Rayleigh 商给出 $\lambda_1$ 的较好的近似，即

$$
\frac{(Au_k,u_k)}{(u_k,u_k)}=\lambda_1+O\left(\left(\frac{\lambda_2}{\lambda_1}\right)^{2k}\right).
$$

**证明** 由式（9.2.8）及 $u_k=\dfrac{A^ku_0}{\max(A^ku_0)}$，$v_{k+1}=Au_k=\dfrac{A^{k+1}u_0}{\max(A^ku_0)}$，得

$$
\frac{(Au_k,u_k)}{(u_k,u_k)}=\frac{(A^{k+1}u_0,A^ku_0)}{(A^ku_0,A^ku_0)}=\frac{\displaystyle\sum_{j=1}^na_j^2\lambda_j^{2k+1}}{\displaystyle\sum_{j=1}^na_j^2\lambda_j^{2k}}=\lambda_1+O\left(\left(\frac{\lambda_2}{\lambda_1}\right)^{2k}\right).
\tag{9.2.11}
$$

### 9.2.3 反幂法

反幂法用来计算矩阵按模最小的特征值及其特征向量，及计算对应于一个给定近似特征值的特征向量。

设 $A\in\mathbf R^{n\times n}$ 为非奇异矩阵，$A$ 的特征值依次记作 $|\lambda_1|\geq|\lambda_2|\geq\cdots\geq|\lambda_n|$，相应的特征向量为 $x_1,x_2,\cdots,x_n$，则 $A^{-1}$ 的特征值为 $\left|\dfrac1{\lambda_n}\right|\geq\left|\dfrac1{\lambda_{n-1}}\right|\geq\cdots\geq\left|\dfrac1{\lambda_1}\right|$，对应的特征向量为 $x_n,x_{n-1},\cdots,x_1$。

因此，计算 $A$ 的按模最小的特征值 $\lambda_n$ 的问题就是计算 $A^{-1}$ 的按模最大的特征值问题。

对 $A^{-1}$ 应用幂法迭代法（称为反幂法），可求得矩阵 $A^{-1}$ 的主特征值 $1/\lambda_n$，从而求得 $A$ 的按模最小的特征值 $\lambda_n$。

反幂法迭代公式为任取初始向量 $v_0=u_0\ne0$，构造向量序列

$$
\left\{
\begin{aligned}
v_k&=A^{-1}u_{k-1},\\
u_k&=\frac{v_k}{\max(v_k)}
\end{aligned}
\right.\qquad(k=1,2,\cdots).
$$

迭代向量 $v_k$ 可以通过解方程组 $Av_k=u_{k-1}$ 求得。

**定理 9.8** 设

$1^\circ$ $A$ 有 $n$ 个线性无关的特征向量，

$2^\circ$ $A$ 为非奇异矩阵且其特征值满足

<!-- 定理 9.8 的第二条条件及结论续 PDF 241。 -->
''',[{'id':'9.2.3','title':'反幂法'}],['实际打开全页原图，确认书页 227；核对 Rayleigh 商加速法、定理 9.7、反幂法序列和定理 9.8 跨页起始；实际打开 9.2.11 裁切图，确认求和索引 j、系数 a_j^2 及幂次 2k+1/2k。'])
write_page(241,r'''
<!-- 续 PDF 240，9.2.3 反幂法，定理 9.8 的第二条条件。 -->

$$
|\lambda_1|\geq|\lambda_2|\geq\cdots\geq|\lambda_{n-1}|>|\lambda_n|>0,
$$

则对任何初始非零向量 $u_0=v_0\ (a_n\ne0)$，由反幂法构造的向量序列 $\{v_k\},\{u_k\}$ 满足

$$
\lim_{k\to\infty}u_k=\frac{x_n}{\max(x_n)},\quad\lim_{k\to\infty}\max(v_k)=\frac1{\lambda_n}.
$$

收敛速度的比值为 $\left|\dfrac{\lambda_n}{\lambda_{n-1}}\right|$。

在反幂法中也可以用原点平移法来加速迭代过程或求其他特征值及特征向量。

如果矩阵 $(A-pI)^{-1}$ 存在，显然其特征值为 $\dfrac1{\lambda_1-p},\dfrac1{\lambda_2-p},\cdots,\dfrac1{\lambda_n-p}$，对应的特征向量仍然是 $x_1,x_2,\cdots,x_n$。现对矩阵 $(A-pI)^{-1}$ 应用幂法，得到反幂法的迭代公式

$$
\left\{
\begin{aligned}
u_0&=v_0\ne0\quad\text{（初始向量）},\\
v_k&=(A-pI)^{-1}u_{k-1},\\
u_k&=\frac{v_k}{\max(v_k)}
\end{aligned}
\right.\qquad(k=1,2,\cdots).
\tag{9.2.12}
$$

如果 $p$ 是 $A$ 的特征值 $\lambda_j$ 的一个近似值，且 $|\lambda_j-p|<|\lambda_i-p|\ (i\ne j)$，就是说，$\dfrac1{\lambda_j-p}$ 是 $(A-pI)^{-1}$ 的主特征值，可用反幂法式（9.2.12）计算其特征值及特征向量。

设 $A\in\mathbf R^{n\times n}$ 有 $n$ 个线性无关的特征向量 $x_1,x_2,\cdots,x_n$，则

$$
u_0=\sum_{i=1}^na_ix_i\quad(a_i\ne0),\quad
v_k=\frac{(A-pI)^{-k}u_0}{\max((A-pI)^{-(k-1)}u_0)},
$$

$$
u_k=\frac{(A-pI)^{-k}u_0}{\max((A-pI)^{-k}u_0)},
$$

其中

$$
(A-pI)^{-k}u_0=\sum_{i=1}^na_i(\lambda_i-p)^{-k}x_i.
$$

**定理 9.9** 设

$1^\circ$ $A\in\mathbf R^{n\times n}$ 有 $n$ 个线性无关的特征向量，$A$ 的特征值及对应的特征向量记作 $\lambda_i$ 及 $x_i\ (i=1,2,\cdots,n)$；

$2^\circ$ $p$ 为 $\lambda_j$ 的近似值，$(A-pI)^{-1}$ 存在，且 $|\lambda_j-p|<|\lambda_i-p|\ (i\ne j)$；

$3^\circ$ $u_0=\displaystyle\sum_{i=1}^na_ix_i\ne0$ 为给定的初始向量 $(a_i\ne0)$，

则由反幂法迭代公式（9.2.12）构造的向量序列 $\{v_k\},\{u_k\}$ 满足

$$
\lim_{k\to\infty}u_k=\frac{x_j}{\max(x_j)},
$$

$$
\lim_{k\to\infty}\max(v_k)=\frac1{\lambda_j-p},\quad\text{即}\quad p+\frac1{\max(v_k)}\to\lambda_j\quad\text{（当 }k\to\infty\text{）},
$$

且收敛速度由比值 $r=\displaystyle\max_{i\ne j}\left|\dfrac{\lambda_j-p}{\lambda_i-p}\right|$ 确定。
''',[],['实际打开全页原图，确认书页 228；核对定理 9.8 后半、9.2.12、定理 9.9 三项条件与两个极限；实际打开初始向量系数和定理 9.9 第三项的裁切，确认原印均为 a_i≠0，按原式保留。'])
