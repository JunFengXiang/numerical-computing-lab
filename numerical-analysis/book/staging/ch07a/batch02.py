from write_page import save
save(178,r'''
### 7.2.1 消元手续

设有线性方程组

$$
\begin{cases}
a_{11}x_1+a_{12}x_2+\cdots+a_{1n}x_n=b_1,\\
a_{21}x_1+a_{22}x_2+\cdots+a_{2n}x_n=b_2,\\
\qquad\qquad\vdots\\
a_{n1}x_1+a_{n2}x_2+\cdots+a_{nn}x_n=b_n,
\end{cases}
\tag{7.2.1}
$$

或写成矩阵形式 $Ax=b$，其中

$$
A=\begin{pmatrix}
a_{11}&a_{12}&\cdots&a_{1n}\\
a_{21}&a_{22}&\cdots&a_{2n}\\
\vdots&\vdots&&\vdots\\
a_{n1}&a_{n2}&\cdots&a_{nn}
\end{pmatrix},\quad
x=\begin{pmatrix}x_1\\x_2\\\vdots\\x_n\end{pmatrix},\quad
b=\begin{pmatrix}b_1\\b_2\\\vdots\\b_n\end{pmatrix},
$$

$A$ 为非奇异矩阵。下面举一个简单的例子来说明消去法的基本思想。

**例 7.1** 用消去法解方程组

$$x_1+x_2+x_3=6,\tag{7.2.2}$$

$$4x_2-x_3=5,\tag{7.2.3}$$

$$2x_1-2x_2+x_3=1.\tag{7.2.4}$$

**解** 第一步，将式（7.2.2）乘以 $-2$ 加到式（7.2.4）上去，消去式（7.2.4）中的未知数 $x_1$，得到

$$-4x_2-x_3=-11.\tag{7.2.5}$$

第二步，将式（7.2.3）加到式（7.2.5）上，消去式（7.2.5）中的未知数 $x_2$，得到与原方程组等价的三角方程组

$$
\begin{cases}
x_1+x_2+x_3=6,\\
4x_2-x_3=5,\\
-2x_3=-6.
\end{cases}
\tag{7.2.6}
$$

显然方程组（7.2.6）是容易求解的，解为 $x^*=(1,2,3)^{\mathrm T}$。上述过程相当于

$$
(A\mathbin{\vdots}b)=
\left(\begin{array}{rrr|r}1&1&1&6\\0&4&-1&5\\2&-2&1&1\end{array}\right)
\longrightarrow
\left(\begin{array}{rrr|r}1&1&1&6\\0&4&-1&5\\0&-4&-1&-11\end{array}\right)
\longrightarrow
\left(\begin{array}{rrr|r}1&1&1&6\\0&4&-1&5\\0&0&-2&-6\end{array}\right).
$$

$$(-2)\times r_1{}^{\text{①}}+r_3\to r_3,\qquad r_2+r_3\to r_3.$$

由此看出，用消去法解方程组的基本思想是，用逐次消去未知数的方法把原来方程组 $Ax=b$ 化为与其等价的三角方程组，而求解三角方程组就容易了。换句话说，上

> ① $r_i$ 表示矩阵的第 $i$ 行。

<!-- 本页末句未完，续 PDF179。 -->
''',[{'id':'7.2.1','title':'消元手续'}],notes=['原图逐式复核7.2.1–7.2.6及三次增广矩阵；保留脚注和跨页断句。'])
save(179,r'''
<!-- 接 PDF178 页末。 -->

述过程就是用行的初等变换将原方程组系数矩阵化为简单形式，从而将求解原方程组（7.2.1）的问题转化为求解简单方程组的问题。

下面来讨论一般的解 $n$ 阶方程组的 Gauss 消去法。

将式（7.2.1）记作 $A^{(1)}x=b^{(1)}$，其中 $A^{(1)}=(a_{ij}^{(1)})=(a_{ij})$，$b^{(1)}=b$。

（1）第一次消元。设 $a_{11}^{(1)}\ne0$，首先对行计算乘数 $m_{i1}=a_{i1}^{(1)}/a_{11}^{(1)}$（$i=2,3,\cdots,n$），用 $-m_{i1}$ 乘式（7.2.1）的第 1 个方程，加到第 $i$（$i=2,3,\cdots,n$）个方程上，消去式（7.2.1）的第 2 个方程直到第 $n$ 个方程中的未知数 $x_1$，得与式（7.2.1）等价的方程组

$$
\begin{pmatrix}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&a_{1n}^{(1)}\\
0&a_{22}^{(2)}&\cdots&a_{2n}^{(2)}\\
\vdots&\vdots&&\vdots\\
0&a_{n2}^{(2)}&\cdots&a_{nn}^{(2)}
\end{pmatrix}
\begin{pmatrix}x_1\\x_2\\\vdots\\x_n\end{pmatrix}
=\begin{pmatrix}b_1^{(1)}\\b_2^{(2)}\\\vdots\\b_n^{(2)}\end{pmatrix},
\tag{7.2.7}
$$

简记作 $A^{(2)}x=b^{(2)}$，其中

$$
a_{ij}^{(2)}=a_{ij}^{(1)}-m_{i1}a_{1j}^{(1)},\quad
b_i^{(2)}=b_i^{(1)}-m_{i1}b_1^{(1)}\quad(i,j=2,3,\cdots,n).
$$

（2）一般第 $k$（$1\le k\le n-1$）次消元。设第 $k-1$ 步计算已经完成，即已计算好与式（7.2.1）等价的方程组

$$A^{(k)}x=b^{(k)},\tag{7.2.8}$$

且已消去未知数 $x_1,x_2,\cdots,x_{k-1}$，其中 $A^{(k)}$ 具有如下形式：

$$
A^{(k)}=\begin{pmatrix}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&\cdots&\cdots&a_{1n}^{(1)}\\
&a_{22}^{(2)}&\cdots&\cdots&\cdots&a_{2n}^{(2)}\\
&&\ddots&&&\vdots\\
&&&a_{kk}^{(k)}&\cdots&a_{kn}^{(k)}\\
&&&\vdots&&\vdots\\
&&&a_{nk}^{(k)}&\cdots&a_{nn}^{(k)}
\end{pmatrix}.
$$

设 $a_{kk}^{(k)}\ne0$，计算乘数 $m_{ik}=a_{ik}^{(k)}/a_{kk}^{(k)}$（$i=k+1,\cdots,n$），用 $-m_{ik}$ 乘式（7.2.8）的第 $k$ 个方程加上第 $i$（$i=k+1,\cdots,n$）个方程，消去第 $k+1$ 个方程直到第 $n$ 个方程的未知数 $x_k$，得到与式（7.2.1）等价的方程组 $A^{(k+1)}x=b^{(k+1)}$。

$A^{(k+1)}$ 元素的计算公式为

$$
\begin{cases}
a_{ij}^{(k+1)}=a_{ij}^{(k)}-m_{ik}a_{kj}^{(k)}& (i,j=k+1,\cdots,n),\\
b_i^{(k+1)}=b_i^{(k)}-m_{ik}b_k^{(k)}& (i=k+1,\cdots,n).
\end{cases}
\tag{7.2.9}
$$

显然 $A^{(k+1)}$ 的第 1 行直到第 $k$ 行与 $A^{(k)}$ 相同。

（3）继续这一过程，直到完成第 $n-1$ 次消元。最后得到与原方程组等价的三角方程组

$$A^{(n)}x=b^{(n)}\tag{7.2.10}$$
''',notes=['逐式目视复核上标迭代次数和乘数下标；原7.2.7及A^(k)用细框标示右下角待消元子块，转录保留其全部元素。'])
