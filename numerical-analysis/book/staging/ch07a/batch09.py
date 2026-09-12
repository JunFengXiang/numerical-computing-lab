from write_page import save,LANE
import json
save(192,r'''
**步 1** $u_{1i}=a_{1i}$（$i=1,2,\cdots,n$），$l_{i1}=a_{i1}/u_{11}$（$i=2,3,\cdots,n$），计算 $U$ 第 $r$ 行，$L$ 的第 $r$ 列元素，$r=2,3,\cdots,n$。

**步 2**

$$u_{ri}=a_{ri}-\sum_{k=1}^{r-1}l_{rk}u_{ki}\quad(i=r,r+1,\cdots,n).\tag{7.4.2}$$

**步 3**

$$l_{ir}=\left(a_{ir}-\sum_{k=1}^{r-1}l_{ik}u_{kr}\right)/u_{rr}\quad(i=r+1,\cdots,n;\;r\ne n),\tag{7.4.3}$$

求解 $Ly=b,Ux=y$ 计算公式。

**步 4**

$$
\begin{cases}
y_1=b_1,\\
y_i=\displaystyle b_i-\sum_{k=1}^{i-1}l_{ik}y_k\quad(i=2,3,\cdots,n).
\end{cases}
\tag{7.4.4}
$$

**步 5**

$$
\begin{cases}
x_n=y_n/u_{nn},\\
x_i=\displaystyle\left(y_i-\sum_{k=i+1}^{n}u_{ik}x_k\right)/u_{ii}\quad(i=n-1,n-2,\cdots,1).
\end{cases}
\tag{7.4.5}
$$

**例 7.5** 用直接三角分解法解 $\begin{pmatrix}1&2&3\\2&5&2\\3&1&5\end{pmatrix}\begin{pmatrix}x_1\\x_2\\x_3\end{pmatrix}=\begin{pmatrix}14\\18\\20\end{pmatrix}$。

**解** 用分解公式（7.4.2）、（7.4.3）计算，得

$$A=\begin{pmatrix}1&0&0\\2&1&0\\3&-5&1\end{pmatrix}
\begin{pmatrix}1&2&3\\0&1&-4\\0&0&-24\end{pmatrix}=LU.$$

求解

$$Ly=(14,18,20)^{\mathrm T},$$

得

$$y=(14,-10,-72)^{\mathrm T},$$

求解

$$Ux=(14,-10,-72)^{\mathrm T},$$

得

$$x=(1,2,3)^{\mathrm T}.$$

在用计算机计算时，由于计算好 $u_{ri}$ 后 $a_{ri}$ 就不用了，因此计算好 $L,U$ 的元素后就存放在 $A$ 的相应位置。例如

$$
A=\begin{pmatrix}
a_{11}&a_{12}&a_{13}&a_{14}\\
a_{21}&a_{22}&a_{23}&a_{24}\\
a_{31}&a_{32}&a_{33}&a_{34}\\
a_{41}&a_{42}&a_{43}&a_{44}
\end{pmatrix}
\to\begin{pmatrix}
u_{11}&u_{12}&u_{13}&u_{14}\\
l_{21}&u_{22}&u_{23}&u_{24}\\
l_{31}&l_{32}&u_{33}&u_{34}\\
l_{41}&l_{42}&l_{43}&u_{44}
\end{pmatrix}.
$$

最后在存放 $A$ 的数组中得到 $L,U$ 的元素。

由直接三角分解计算公式，需要计算形如 $\sum a_i b_i$ 的式子，可采用“双精度累加”，以提高精度。

直接分解法大约需要 $n^3/3$ 次乘、除法运算，和 Gauss 消去法的计算量基本相同。

如果已经实现了 $A=LU$ 的分解计算，且 $L,U$ 保存在 $A$ 的相应位置，则用直接三

<!-- 本页末句未完，续 PDF193。 -->
''',notes=['逐式核对7.4.2–7.4.5循环上下界、例7.5矩阵/中间解、LU存储的16个元素；原存储图以阶梯虚线区分l与u。'])
save(193,r'''
<!-- 接 PDF192 页末。 -->

角分解法解具有相同系数的方程组 $Ax=(b_1,b_2,\cdots,b_m)$ 是相当方便的，每解一个方程组 $Ax=b_j$ 仅需要增加 $n^2$ 次乘除法运算。

矩阵 $A$ 的分解公式（7.4.2）、（7.4.3）又称为 **Doolittle 分解公式**。

**2. 选主元的三角分解法**

从直接三角分解公式可看出，当 $u_{rr}=0$ 时计算将中断或者当 $u_{rr}$ 绝对值很小时，按分解公式计算可能引起舍入误差的累积。但如果 $A$ 非奇异，就可通过交换 $A$ 的行实现矩阵 $PA$ 的 LU 分解，因此可采用与列主元素消去法类似的方法（可以证明下述方法与列主元素消去法等价），将直接三角分解法修改为（部分）选主元的三角分解法。

设第 $r-1$ 步分解已完成，这时有

$$
A\to\begin{pmatrix}
u_{11}&u_{12}&\cdots&\cdots&\cdots&\cdots&u_{1n}\\
l_{21}&u_{22}&&&&&\vdots\\
l_{31}&l_{32}&\ddots&&&&\vdots\\
\vdots&&\ddots&u_{r-1,r-1}&\cdots&\cdots&u_{n-1,n}\\
\vdots&&&l_{r,r-1}&a_{rr}&\cdots&a_{rn}\\
\vdots&&&\vdots&\vdots&&\vdots\\
l_{n1}&l_{n2}&\cdots&l_{n,r-1}&a_{nr}&\cdots&a_{nn}
\end{pmatrix}.
$$

第 $r$ 步分解需用到式（7.4.2）及式（7.4.3），为了避免用小的数 $u_{rr}$ 作除数，引进量

$$s_i=a_{ir}-\sum_{k=1}^{r-1}l_{ik}u_{kr}\quad(i=r,r+1,\cdots,n),$$

于是有

$$u_{rr}=s_r,\quad l_{ir}=s_i/s_r\quad(i=r+1,\cdots,n),\quad \max_{r\le i\le n}|s_i|=|s_{i_r}|.$$

用 $s_{i_r}$ 作为 $u_{rr}$，交换 $A$ 的 $r$ 行与 $i_r$ 行元素（将 $(i,j)$ 位置的新元素仍记作 $l_{ij}$ 及 $a_{ij}$），于是有 $|l_{ir}|\le1$（$i=r+1,\cdots,n$）。由此再进行第 $r$ 步分解计算。

**算法 4** 选主元的三角分解法，其步骤如下：

设 $Ax=b$，其中 $A$ 为非奇异矩阵。本算法采用列主元的三角分解法，用 $PA=I_{n-1,i_{n-1}}\cdots I_{1i_1}A$ 的三角分解冲掉 $A$，用整型数组 $\mathrm{Ip}(n)$ 记录主行，解 $x$ 存放在 $b$ 内。

对于 $r=1,2,\cdots,n$，做到步 4。

**步 1** 计算 $s_i$

$$a_{ir}\leftarrow s_i=a_{ir}-\sum_{k=1}^{r-1}l_{ik}u_{kr}\quad(i=r,r+1,\cdots,n).$$

**步 2** 选主元 $|s_{i_r}|=\max_{r\le i\le n}|s_i|$，$\mathrm{Ip}(r)\leftarrow i_r$。

**步 3** 交换 $A$ 的 $r$ 行与 $i_r$ 行元素 $a_{ri}\leftrightarrow a_{i_ri}$（$i=1,2,\cdots,n$）。

**步 4** 计算 $U$ 的第 $r$ 行元素，$L$ 的第 $r$ 列元素

$$a_{rr}=u_{rr}=s_r,$$

<!-- 算法4步4续 PDF194。 -->

> 校注（agent 补充）：本页分解存储矩阵在对角元 $u_{r-1,r-1}$ 所在行的最右侧，原书印作 $u_{n-1,n}$，已保留；按该行是第 $r-1$ 行，应为 $u_{r-1,n}$。疑似原书下标排印错误，参见[原矩阵放大裁图](../assets/pdf-193-storage-detail.png)。
''',notes=['逐式目视核对s_i与换行次序、算法4起始4步及跨页公式；原存储矩阵u_{n-1,n}保留并另注。'])
rp=LANE/'review.json';r=json.loads(rp.read_text())
e={'id':'ch07a-E006','pdf_page':193,'printed_page':180,'location':'分解存储矩阵第r-1行末项','type':'suspected_source_typo','original':'u_{n-1,n}','agent_note':'所在行为r-1，应对应u_{r-1,n}；原下标保留另注。','evidence':'staging/ch07a/assets/pdf-193-storage-detail.png'}
r['source_errata']=[q for q in r['source_errata'] if q.get('id')!=e['id']]+[e]
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
