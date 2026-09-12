from write_page import save
save(194,r'''
<!-- 接 PDF193 算法4步4。 -->

$$a_{ir}\leftarrow l_{ir}=s_i/u_{rr}=a_{ir}/a_{rr}\quad(i=r+1,\cdots,n),$$

$$a_{ri}\leftarrow u_{ri}=a_{ri}-\sum_{k=1}^{r-1}l_{rk}u_{ki}\quad(i=r+1,\cdots,n),$$

这时有 $|l_{ir}|\le1$。

上述计算过程完成后就实现了 $PA$ 的 LU 分解，且 $U$ 保存在 $A$ 上三角部分，$L$ 保存在 $A$ 的下三角部分，排列阵 $P$ 由 $\mathrm{Ip}(n)$ 最后记录可知。

求解 $Ly=Pb$ 及 $Ux=y$。

**步 5** $i=1,2,\cdots,n-1$。

（1）$t\leftarrow\mathrm{Ip}(i)$；（2）如果 $i=t$，则转（3），否则 $b_i\leftrightarrow b_t$；（3）继续循环。

**步 6**

$$b_i\leftarrow b_i-\sum_{k=1}^{i-1}l_{ik}b_k\quad(i=2,3,\cdots,n).$$

**步 7**

$$b_n\leftarrow b_n/u_{nn},\quad b_i\leftarrow\left(b_i-\sum_{k=i+1}^{n}u_{ik}b_k\right)/u_{ii}\quad(i=n-1,\cdots,1).$$

利用算法 4 的结果（实现 $PA=LU$ 三角分解），则可以计算 $A$ 的逆矩阵

$$A^{-1}=U^{-1}L^{-1}P.$$

利用 $PA$ 的三角分解计算 $A^{-1}$ 步骤：

（1）计算上三角阵的逆矩阵 $U^{-1}$；

（2）计算 $U^{-1}L^{-1}$；

（3）交换 $U^{-1}L^{-1}$ 列（利用 $\mathrm{Ip}(n)$ 最后记录）。

上述方法求 $A^{-1}$ 大约需要 $n^3$ 次乘法运算。

### 7.4.2 平方根法

应用有限元法解结构力学问题，最后归结为求解线性方程组，这时系数矩阵大多具有对称正定性质。所谓平方根法，就是利用对称正定矩阵的三角分解而得到的求解对称正定方程组的一种有效方法，目前在计算机上广泛应用平方根法解此类方程组。

设 $A$ 为对称阵，且 $A$ 的所有顺序主子式均不为零。由定理 7.3 知，$A$ 可唯一分解为式（7.4.1）的形式。

为了利用 $A$ 的对称性，将 $U$ 再分解，即

$$
U=\begin{pmatrix}
u_{11}&&&\\
&u_{22}&&\\
&&\ddots&\\
&&&u_{nn}
\end{pmatrix}
\begin{pmatrix}
1&\dfrac{u_{12}}{u_{11}}&\cdots&\dfrac{u_{1n}}{u_{11}}\\
&\ddots&\ddots&\vdots\\
&&\ddots&\dfrac{u_{n-1,n}}{u_{n-1,n-1}}\\
&&&1
\end{pmatrix}=DU_0,
$$

其中 $D$ 为对角阵，$U_0$ 为单位上三角阵。于是

$$A=LU=LDU_0.\tag{7.4.6}$$
''',[{'id':'7.4.2','title':'平方根法'}],notes=['逐式核对算法4后半、逆矩阵乘积次序与单位上三角分解U=DU0。'])
save(195,r'''
又

$$A=A^{\mathrm T}=U_0^{\mathrm T}(DL^{\mathrm T}),$$

由分解的唯一性即得 $U_0^{\mathrm T}=L$，代入式（7.4.6）得到对称矩阵 $A$ 的分解式 $A=LDL^{\mathrm T}$。

总结上述讨论，有以下定理。

**定理 7.7（对称阵的三角分解定理）** 设 $A$ 为 $n$ 阶对称阵，且 $A$ 的所有顺序主子式均不为零，则 $A$ 可唯一分解为

$$A=LDL^{\mathrm T},$$

其中 $L$ 为单位下三角阵，$D$ 为对角阵。

现设 $A$ 为对称正定矩阵。首先说明 $A$ 的分解式 $A=LDL^{\mathrm T}$ 中 $D$ 的对角元素 $d_i$ 均为正数。事实上，由 $A$ 的对称正定性，7.2 节的推论成立，即

$$d_1=D_1>0,\quad d_i=D_i/D_{i-1}>0\quad(i=2,3,\cdots,n).$$

于是

$$
D=\begin{pmatrix}d_1&&\\&\ddots&\\&&d_n\end{pmatrix}
=\begin{pmatrix}\sqrt{d_1}&&\\&\ddots&\\&&\sqrt{d_n}\end{pmatrix}
\begin{pmatrix}\sqrt{d_1}&&\\&\ddots&\\&&\sqrt{d_n}\end{pmatrix}
=D^{\frac12}D^{\frac12},
$$

由定理 7.7 得到

$$A=LDL^{\mathrm T}=LD^{\frac12}D^{\frac12}L^{\mathrm T}=(LD^{\frac12})(LD^{\frac12})^{\mathrm T}=L_1L_1^{\mathrm T},$$

其中 $L_1=LD^{\frac12}$ 为下三角阵。

**定理 7.8（对称正定矩阵的三角分解或 Cholesky 分解）** 如果 $A$ 为 $n$ 阶对称正定矩阵，则存在一个实的非奇异下三角阵 $L$ 使 $A=LL^{\mathrm T}$，当限定 $L$ 的对角元素为正时，这种分解是唯一的。

下面用直接分解方法来确定计算 $L$ 元素的递推公式。因为

$$
A=\begin{pmatrix}
l_{11}&&&\\
l_{21}&l_{22}&&\\
\vdots&\vdots&\ddots&\\
l_{n1}&l_{n2}&\cdots&l_{nn}
\end{pmatrix}
\begin{pmatrix}
l_{11}&l_{21}&\cdots&l_{n1}\\
&l_{22}&\cdots&l_{n2}\\
&&\ddots&\vdots\\
&&&l_{nn}
\end{pmatrix},
$$

其中 $l_{ii}>0$（$i=1,2,\cdots,n$）。由矩阵乘法及 $l_{jk}=0$（当 $j<k$ 时），得

$$a_{ij}=\sum_{k=1}^{n}l_{ik}l_{jk}=\sum_{k=1}^{j-1}l_{ik}l_{jk}+l_{jj}l_{ij},$$

于是得到以下解对称正定方程组 $Ax=b$ 的平方根法计算公式。

对于 $j=1,2,\cdots,n$，

**步 1**

$$l_{jj}=\left(a_{jj}-\sum_{k=1}^{j-1}l_{jk}^2\right)^{\frac12}.\tag{7.4.7}$$

**步 2**

$$l_{ij}=\left(a_{ij}-\sum_{k=1}^{j-1}l_{ik}l_{jk}\right)/l_{jj}\quad(i=j+1,\cdots,n),$$

<!-- 平方根法步骤续 PDF196。本页步2式旁未印编号，不补写下一页编号。 -->
''',notes=['原图逐式复核正定假设、d_i与D_i、LDL^T至Cholesky分解、平方根指数1/2及递推上下界。步2本页未印公式编号。'])
