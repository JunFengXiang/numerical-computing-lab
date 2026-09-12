from write_page import save,LANE
import json
save(190,r'''
$$
\xrightarrow{\text{第二次消元}}
\left(\begin{array}{rrr|rrr}
1&0&-1/2&0&-5/2&2\\
0&1&3/2&0&3/2&-1\\
0&0&\boxed{1/2}&1&-1/2&0
\end{array}\right)
$$

原图标注：上述右侧第二列 $\begin{pmatrix}-5/2\\3/2\\-1/2\end{pmatrix}$ 以方框标出，标为 $c_2$。

$$
\xrightarrow{\text{第三次消元}}
\left(\begin{array}{rrr|rrr}
1&0&0&1&-3&2\\
0&1&0&-3&3&-1\\
0&0&1&2&-1&0
\end{array}\right)=(I_n\mid A^{-1}).
$$

原图标注：上述右侧第一列 $\begin{pmatrix}1\\-3\\2\end{pmatrix}$ 以方框标出，标为 $c_1$。

小方框内为每次按列所选的主元素，且

$$m_1=(m_{11},m_{21},m_{31})^{\mathrm T}=c_3,\quad
m_2=(m_{12},m_{22},m_{32})^{\mathrm T}=c_2,\quad
m_3=(m_{13},m_{23},m_{33})^{\mathrm T}=c_1.$$

为了节省内存单元，不必将单位矩阵存放起来，$c_3$ 存放在 $A$ 的第 1 列位置，$c_2$ 存放在 $A$ 的第 2 列位置，$c_1$ 存放在 $A$ 的第 3 列位置，经消元计算，最后再调整一下列就可在 $A$ 的位置得到 $A^{-1}$。注意第 $k$ 步消元时，由 $A$ 的第 $k$ 列

$$a_k=(a_{1k},\cdots,a_{kk},\cdots,a_{nk})^{\mathrm T}$$

计算 $m_k=\left(-\dfrac{a_{1k}}{a_{kk}},\cdots,-1,\cdots,-\dfrac{a_{nk}}{a_{kk}}\right)^{\mathrm T}$ 且冲掉 $a_k$。

最后，在 $A$ 位置如何调整列呢？事实上，在 $A$ 位置最后得到矩阵 $PA\equiv A_1$（其中 $P$ 为排列矩阵）的逆矩阵 $A_1^{-1}$，于是 $A^{-1}=A_1^{-1}P$。

**算法 3** Gauss-Jordan 列主元素方法求逆，其步骤如下。

本算法是用列主元素的 Gauss-Jordan 方法求 $A^{-1}$，计算结果存放在原矩阵 $A$ 的数组中。用整型数组 $\mathrm{Ip}(n)$ 记录主行，$A$ 的行列式值存放在 $\det A$。

**步 1** $\det A\leftarrow1$；对于 $k=1,2,\cdots,n$ 做到步 8。

**步 2** 按列选主元素 $|a_{i_kk}|=\max_{k\le i\le n}|a_{ik}|$；$c_0\leftarrow a_{i_kk}$，$\mathrm{Ip}(k)\leftarrow i_k$。

**步 3** 如果 $c_0=0$，则计算停止（此时 $A$ 为奇异矩阵）。

**步 4** 如果 $i_k=k$，则转步 5，否则换行：$a_{kj}\leftrightarrow a_{i_kj}$（$j=1,2,\cdots,n$），$\det A\leftarrow-\det A$。

**步 5** $\det A\leftarrow\det A\cdot c_0$。

**步 6** 计算 $h\leftarrow a_{kk}\leftarrow1/c_0$；$a_{ik}\leftarrow m_{ik}=-a_{ik}\cdot h$（$i=1,2,\cdots,n;\;i\ne k$）。

**步 7** 消元计算

$$a_{ij}\leftarrow a_{ij}+m_{ik}a_{kj}\quad
\left(\begin{array}{l}i=1,2,\cdots,n;\;i\ne k\\j=1,2,\cdots,n;\;j\ne k\end{array}\right).$$

**步 8** 计算主行 $a_{kj}\leftarrow a_{kj}\cdot h$（$j=1,2,\cdots,n;\;j\ne k$）。

**步 9** 交换列对于 $k=n-1,n-2,\cdots,2,1$，

（1）$t=\mathrm{Ip}(k)$；

（2）如果 $t\le k$，则转（3），否则换列：$a_{ik}\leftrightarrow a_{it}$（$i=1,2,\cdots,n$）；

（3）继续循环。

> 校注（agent 补充）：解释段中 $m_k$ 的第 $k$ 个分量原书印作 $-1$，此处保留。按上一页所给 $m_{kk}=1/a_{kk}$、本页算法 3 步 6 的 $a_{kk}\leftarrow1/c_0$，以及例 7.4 第一次消元的 $m_1=c_3=(1/3,-2/3,-1/3)^{\mathrm T}$，用于原地求逆时该位置应为 $1/a_{kk}$；疑似原书公式错误。参见[原文放大裁图](../assets/pdf-190-multiplier-detail.png)。
''',notes=['逐项核对例7.4后两次矩阵、c2/c1框注以及算法3九步；步8放大确认条件是j≠k；解释段m_k中心-1保留另注。'])
save(191,r'''
## 7.4 Gauss 消去法的变形

Gauss 消去法有很多变形，有的是 Gauss 消去法的改进、改写，有的是用于某一类特殊性质矩阵的 Gauss 消去法的简化。

### 7.4.1 直接三角分解法

将 Gauss 消去法改写为紧凑形式，可以直接从矩阵 $A$ 的元素得到计算 $L,U$ 元素的递推公式，而不需任何中间步骤，这就是所谓**直接三角分解法**。一旦实现了矩阵 $A$ 的 LU 分解，那么求解式（7.2.1）的问题就等价于求解以下两个三角方程组：

（1）$Ly=b$，求 $y$；（2）$Ux=y$，求 $x$。

**1. 不选主元的三角分解法**

设 $A$ 为非奇异矩阵，且有分解式 $A=LU$，其中 $L$ 为单位下三角阵，$U$ 为上三角阵，即

$$
A=\begin{pmatrix}
1&&&\\
l_{21}&1&&\\
\vdots&\ddots&\ddots&\\
l_{n1}&\cdots&l_{n,n-1}&1
\end{pmatrix}
\begin{pmatrix}
u_{11}&u_{12}&\cdots&u_{1n}\\
&u_{22}&\cdots&u_{2n}\\
&&\ddots&\vdots\\
&&&u_{nn}
\end{pmatrix}.
\tag{7.4.1}
$$

下面说明 $L,U$ 的元素可以由 $n$ 步直接计算定出，其中第 $r$ 步定出 $U$ 的第 $r$ 行和 $L$ 的第 $r$ 列元素。由式（7.4.1），有

$$a_{1i}=u_{1i}\quad(i=1,2,\cdots,n),$$

于是得 $U$ 的第 1 行元素；

$$a_{i1}=l_{i1}u_{11},\quad l_{i1}=a_{i1}/u_{11}\quad(i=2,\cdots,n),$$

于是得 $L$ 的第 1 列元素。

设已经定出 $U$ 的第 1 行到第 $r-1$ 行元素与 $L$ 的第 1 列到第 $r-1$ 列元素。由式（7.4.1），利用矩阵乘法，有

$$a_{ri}=\sum_{k=1}^{n}l_{rk}u_{ki}=\sum_{k=1}^{r-1}l_{rk}u_{ki}+u_{ri}\quad\text{（当 $r<k$，$l_{rk}=0$ 时）},$$

故

$$u_{ri}=a_{ri}-\sum_{k=1}^{r-1}l_{rk}u_{ki}\quad(i=r,r+1,\cdots,n),$$

又由式（7.4.1）有

$$a_{ir}=\sum_{k=1}^{n}l_{ik}u_{kr}=\sum_{k=1}^{r-1}l_{ik}u_{kr}+l_{ir}u_{rr}.$$

总结上述讨论，得到用直接三角分解法解 $Ax=b$（要求 $A$ 所有顺序主子式都不为零）的计算公式，步骤如下。

<!-- 步骤续 PDF192。 -->
''',[{'id':'7.4','title':'Gauss 消去法的变形'},{'id':'7.4.1','title':'直接三角分解法'}],notes=['目视核对LU矩阵中小写l/u、行列递推及两个三角方程；保持标题与全部假设。'])
rp=LANE/'review.json';r=json.loads(rp.read_text())
e={'id':'ch07a-E005','pdf_page':190,'printed_page':177,'location':'解释段m_k列向量','type':'suspected_source_formula_error','original':'m_k第k个分量为-1','agent_note':'与m_kk=1/a_kk、例7.4的c3以及算法3步6不符；原式保留并另注。','evidence':'staging/ch07a/assets/pdf-190-multiplier-detail.png'}
r['source_errata']=[q for q in r['source_errata'] if q.get('id')!=e['id']]+[e]
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
