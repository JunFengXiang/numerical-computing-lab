from write_page import save,LANE
import json
save(180,r'''
或

$$
\begin{pmatrix}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&a_{1n}^{(1)}\\
&a_{22}^{(2)}&\cdots&a_{2n}^{(2)}\\
&&\ddots&\vdots\\
&&&a_{nn}^{(n)}
\end{pmatrix}
\begin{pmatrix}x_1\\x_2\\\vdots\\x_n\end{pmatrix}
=\begin{pmatrix}b_1^{(1)}\\b_2^{(2)}\\\vdots\\b_n^{(n)}\end{pmatrix}.
$$

由式（7.2.1）约化为式（7.2.10）的过程称为**消元过程**。

求解三角方程组（7.2.10），设 $a_{ii}^{(i)}\ne0$（$i=1,2,\cdots,n-1$），易得求解公式

$$
\begin{cases}
x_n=b_n^{(n)}/a_{nn}^{(n)},\\
x_k=\displaystyle\left(b_k^{(k)}-\sum_{j=k+1}^{n}a_{kj}^{(k)}x_j\right)/a_{kk}^{(k)}
\end{cases}
\quad(k=n-1,n-2,\cdots,2,1).
\tag{7.2.11}
$$

式（7.2.10）的求解过程称为**回代过程**。

如果 $a_{11}^{(1)}=0$，那么，由于 $A$ 为非奇异矩阵，所以 $A$ 的第 1 列一定有元素不等于零，例如 $a_{i_1,1}\ne0$，于是可交换两行元素（$r_1\leftrightarrow r_{i_1}$），将 $a_{i_1,1}$ 调到第 1 行第 1 列的位置，然后进行消元计算，这时 $A^{(2)}$ 右下角矩阵（$n-1$ 阶）亦为非奇异矩阵。继续这一过程，Gauss 消去法照样可进行计算。

总结上述讨论即有如下定理。

**定理 7.1** 如果 $A$ 为 $n$ 阶非奇异矩阵，则可通过 Gauss 消去法（及交换两行的初等变换）将方程组（7.2.1）化为三角方程组（7.2.10）。

$A$ 在什么条件下才能保证 $a_{kk}^{(k)}\ne0$（$k=1,2,\cdots,n$）？下面的引理给出了这个条件。

**引理** 约化的主元素 $a_{ii}^{(i)}\ne0$（$i=1,2,\cdots,k$）的充要条件是矩阵 $A$ 的顺序主子式 $D_i\ne0$（$i=1,2,\cdots,k$），即

$$D_1=a_{11}\ne0,$$

$$
D_i=\begin{vmatrix}
a_{11}&\cdots&a_{1k}\\
\vdots&&\vdots\\
a_{i1}&\cdots&a_{ii}
\end{vmatrix}\ne0\quad(i=2,3,\cdots,k).
\tag{7.2.12}
$$

**证明** 利用归纳法证明引理的充分性。显然，当 $k=1$ 时引理的充分性是成立的，现假设引理对 $k-1$ 是成立的，求证引理对 $k$ 亦成立。由归纳法，设 $a_{ii}^{(i)}\ne0$（$i=1,2,\cdots,k-1$），于是可用 Gauss 消去法将 $A^{(1)}=A$ 约化到 $A^{(k)}$ 中，即

$$
A^{(1)}\to A^{(k)}=\begin{pmatrix}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&\cdots&\cdots&a_{1n}^{(1)}\\
&a_{22}^{(2)}&\cdots&\cdots&\cdots&a_{2n}^{(2)}\\
&&\ddots&&&\vdots\\
&&&a_{kk}^{(k)}&\cdots&a_{kn}^{(k)}\\
&&&\vdots&&\vdots\\
&&&a_{nk}^{(k)}&\cdots&a_{nn}^{(k)}
\end{pmatrix},
$$

<!-- 证明续 PDF181。 -->

> 校注（agent 补充）：式（7.2.12）原书矩阵右上角清楚印作 $a_{1k}$，此处忠实保留。按同式左端 $D_i$、左下角 $a_{i1}$ 和右下角 $a_{ii}$，第 $i$ 阶顺序主子式的右上角应为 $a_{1i}$；这是疑似原书下标排印错误，不是 OCR 改写。参见[原式放大裁图](../assets/pdf-180-principal-minor-detail.png)。
''',notes=['逐式复核三角回代、换行下标i_1、引理与证明；7.2.12原书a_1k保留并附校注和裁图。'])
save(181,r'''
且有

$$
D_2=\begin{vmatrix}a_{11}^{(1)}&a_{12}^{(1)}\\0&a_{22}^{(2)}\end{vmatrix}
=a_{11}^{(1)}a_{22}^{(2)},\qquad
D_3=a_{11}^{(1)}a_{22}^{(2)}a_{33}^{(3)},
$$

$$
D_k=\begin{vmatrix}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&a_{1k}^{(1)}\\
&a_{22}^{(2)}&\cdots&a_{2k}^{(2)}\\
&&\ddots&\vdots\\
&&&a_{kk}^{(k)}
\end{vmatrix}
=a_{11}^{(1)}a_{22}^{(2)}\cdots a_{kk}^{(k)}.
\tag{7.2.13}
$$

由设 $D_i\ne0$（$i=1,2,\cdots,k$）及式（7.2.13），有 $a_{kk}^{(k)}\ne0$，即引理的充分性对 $k$ 成立。

显然，由假设 $a_{ii}^{(i)}\ne0$（$i=1,2,\cdots,k$），利用式（7.2.13）亦可推出 $D_i\ne0$（$i=1,2,\cdots,k$）。

**推论** 如果 $A$ 的顺序主子式 $D_k\ne0$（$k=1,2,\cdots,n-1$），则

$$
\begin{cases}
a_{11}^{(1)}=D_1,\\
a_{kk}^{(k)}=D_k/D_{k-1}\quad(k=2,3,\cdots,n).
\end{cases}
$$

**定理 7.2** 如果 $n$ 阶矩阵 $A$ 的所有顺序主子式均不为零，即 $D_i\ne0$（$i=1,2,\cdots,n$），则可通过 Gauss 消去法（不进行交换两行的初等变换），将方程组（7.2.1）约化为三角方程组（7.2.10）。

计算公式如下：

（1）消元计算（$k=1,2,\cdots,n-1$）。

$$m_{ik}=a_{ik}^{(k)}/a_{kk}^{(k)}\quad(i=k+1,\cdots,n),$$

$$a_{ij}^{(k+1)}=a_{ij}^{(k)}-m_{ik}a_{kj}^{(k)}\quad(i,j=k+1,\cdots,n),$$

$$b_i^{(k+1)}=b_i^{(k)}-m_{ik}b_k^{(k)}\quad(i=k+1,\cdots,n).$$

（2）回代计算。求解公式为式（7.2.11）。

### 7.2.2 矩阵的三角分解

下面借助矩阵理论进一步对消去法作些分析，从而建立 Gauss 消去法与矩阵因式分解的关系。

设式（7.2.1）中 $A$ 的各顺序主子式均不为零。由于对 $A$ 施行行的初等变换相当于用初等矩阵左乘 $A$，于是对式（7.2.1）施行第一次消元后化为式（7.2.7），这时 $A^{(1)}$ 化为 $A^{(2)}$，$b^{(1)}$ 化为 $b^{(2)}$，即

$$L_1A^{(1)}=A^{(2)},\qquad L_1b^{(1)}=b^{(2)},$$

其中

$$
L_1=\begin{pmatrix}
1&&&&\\
-m_{21}&1&&&\\
-m_{31}&&1&&\\
\vdots&&&\ddots&\\
-m_{n1}&&&&1
\end{pmatrix}.
$$
''',[{'id':'7.2.2','title':'矩阵的三角分解'}],notes=['对照原页复核行列式乘积、主元与顺序主子式关系、L1负号及单位对角。'])
rp=LANE/'review.json'
r=json.loads(rp.read_text())
r['source_errata']=[e for e in r['source_errata'] if e.get('id')!='ch07a-E001']+[{'id':'ch07a-E001','pdf_page':180,'printed_page':167,'formula_id':'7.2.12','type':'suspected_source_typo','original':'D_i 的矩阵右上角为 a_{1k}','agent_note':'按第i阶顺序主子式应为a_{1i}；原式保留并另注。','evidence':'staging/ch07a/assets/pdf-180-principal-minor-detail.png'}]
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
