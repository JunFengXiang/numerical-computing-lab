from write_page import save,LANE
import json
save(188,r'''
利用式（7.3.1）得到

$$L_{n-1}I_{n-1,i_{n-1}}\cdots L_2I_{2i_2}L_1I_{1i_1}A=A^{(n)}=U,$$

简记作

$$\widetilde{P}A=U,\quad\widetilde{P}b=b^{(n)},$$

其中

$$\widetilde{P}=L_{n-1}I_{n-1,i_{n-1}}\cdots L_2I_{2i_2}L_1I_{1i_1}.$$

下面就 $n=4$ 的情况来考察一下矩阵 $\widetilde{P}$。

$$
\begin{aligned}
U=A^{(4)}&=L_3I_{3i_3}L_2I_{2i_2}L_1I_{1i_1}A\\
&=L_3(I_{3i_3}L_2I_{3i_3})(I_{3i_3}L_{2i_2}L_1I_{2i_2}I_{3i_3})(I_{3i_3}I_{2i_2}I_{1i_1})A\\
&\equiv\widetilde{L}_3\widetilde{L}_2\widetilde{L}_1PA,
\end{aligned}
\tag{7.3.2}
$$

其中

$$\widetilde{L}_1=I_{3i_3}I_{2i_2}L_1I_{2i_2}I_{3i_3},\quad
\widetilde{L}_2=I_{3i_3}L_2I_{3i_3},\quad
\widetilde{L}_3=L_3,\quad P=I_{3i_3}I_{2i_2}I_{1i_1}.$$

由本章的习题 8 知 $\widetilde{L}_k$（$k=1,2,3$）亦为单位下三角阵，其元素的绝对值不大于 1。记 $L^{-1}=\widetilde{L}_3\widetilde{L}_2\widetilde{L}_1$，由式（7.3.2）得到 $PA=LU$，其中 $P$ 为排列矩阵，$L$ 为单位下三角阵，$U$ 为上三角阵。这说明对式（7.2.1）应用列主元素消去法，相当于对 $(A\mid b)$ 先进行一系列行交换后再对 $PAx=Pb$ 应用 Gauss 消去法。在实际计算中只能在计算过程中进行行的交换。

总结以上的讨论可得如下定理。

**定理 7.5（列主元素的三角分解定理）** 如果 $A$ 为非奇异矩阵，则存在排列矩阵 $P$，使

$$PA=LU,$$

其中 $L$ 为单位下三角阵，$U$ 为上三角阵。

$L$ 元素存放在数组 $A$ 的下三角部分，$U$ 元素存放在 $A$ 上三角部分，由整型数组 $\mathrm{Ip}(n)$ 记录可知 $P$ 的情况。

### 7.3.3 Gauss-Jordan 消去法

Gauss 消去法始终是消去对角线下方的元素，现考虑 Gauss 消去法的一种修正，即消去对角线下方和上方的元素，这种方法称为 Gauss-Jordan 消去法。

设用 Gauss-Jordan 消去法已完成 $(k-1)$ 步，于是 $Ax=b$ 化为等价方程组 $A^{(k)}x=b^{(k)}$，其中

$$
(A^{(k)},b^{(k)})=\left(\begin{array}{ccccccc|c}
1&&&&a_{1k}&\cdots&a_{1n}&b_1\\
&1&&&\vdots&&\vdots&\vdots\\
&&\ddots&&\vdots&&\vdots&\vdots\\
&&&1&a_{k-1,k}&\cdots&a_{k-1,n}&\vdots\\
&&&&a_{kk}&\cdots&a_{kn}&b_k\\
&&&&\vdots&&\vdots&\vdots\\
&&&&a_{nk}&\cdots&a_{nn}&b_n
\end{array}\right),\quad k=1,2,\cdots,n.
$$

> 校注（agent 补充）：式（7.3.2）第二行第二个括号内原书印作 $I_{3i_3}L_{2i_2}L_1I_{2i_2}I_{3i_3}$，其中 $L_{2i_2}$ 在本段未定义。本页紧接着定义 $\widetilde{L}_1=I_{3i_3}I_{2i_2}L_1I_{2i_2}I_{3i_3}$，因而该处 $L_{2i_2}$ 疑为 $I_{2i_2}$ 的排印错误；此处保留原式。参见[原式放大裁图](../assets/pdf-188-permutation-detail.png)。
''',[{'id':'7.3.3','title':'Gauss-Jordan 消去法'}],notes=['逐因子复核7.3.2的排列/消元乘积及其展开；原式L_{2i_2}保留并以本页tilde L1定义作独立校注。'])
save(189,r'''
在第 $k$ 步计算时，考虑对上述矩阵的第 $k$ 行上、下都进行消元计算。

**步 1** 按列选主元素，即确定 $i_k$ 使 $|a_{i_kk}|=\max_{k\le i\le n}|a_{ik}|$。

**步 2** 换行（当 $i_k\ne k$）交换 $(A,b)$ 第 $k$ 行与第 $i_k$ 行元素。

**步 3** 计算乘数

$$m_{ik}=-a_{ik}/a_{kk}\quad(i=1,2,\cdots,n;\;i\ne k),\quad m_{kk}=1/a_{kk}.$$

（$m_{ik}$ 可保存在存放 $a_{ik}$ 的单元中。）

**步 4** 消元计算

$$a_{ij}\leftarrow a_{ij}+m_{ik}a_{kj}\quad
\left(\begin{array}{l}i=1,2,\cdots,n;\;i\ne k;\\j=k+1,\cdots,n\end{array}\right),$$

$$b_i\leftarrow b_i+m_{ik}b_k\quad(i=1,2,\cdots,n;\;i\ne k).$$

**步 5** 计算主行 $a_{kj}\leftarrow a_{kj}\cdot m_{kk}$（$j=k,k+1,\cdots,n$），$b_k\leftarrow b_k\cdot m_{kk}$。

上述过程结束后，有

$$
(A,b)\to(A^{(k+1)},b^{(k+1)})=
\left(\begin{array}{cccc|c}
1&&&&\widehat{b}_1\\
&1&&&\widehat{b}_2\\
&&\ddots&&\vdots\\
&&&1&\widehat{b}_n
\end{array}\right)
$$

这说明用 Gauss-Jordan 消去法将 $A$ 约化为单位矩阵，计算解就在常数项位置得到，因此用不着回代求解。用 Gauss-Jordan 消去法解方程组的计算量大约需要 $n^3/2$ 次乘除法运算，比 Gauss 消去法计算量大，但用 Gauss-Jordan 消去法求一个矩阵的逆矩阵还是比较合适的。

**定理 7.6（Gauss-Jordan 消去法求逆矩阵）** 设 $A$ 为非奇异矩阵，方程组 $AX=I_n$ 的增广矩阵为 $C=(A\mathbin{\vdots}I_n)$。如果对 $C$ 应用 Gauss-Jordan 消去法化为 $(I_n\mathbin{\vdots}T)$，则 $A^{-1}=T$。

事实上，求 $A$ 的逆矩阵 $A^{-1}$，即求 $n$ 阶矩阵 $X$，使 $AX=I_n$，其中 $I_n$ 为单位矩阵。将 $X$ 按列分块 $X=(x_1,x_2,\cdots,x_n)$，$I=(e_1,e_2,\cdots,e_n)$，于是求解 $AX=I_n$ 等价于求解 $n$ 个方程组 $Ax_j=e_j$（$j=1,2,\cdots,n$）。我们可用 Gauss-Jordan 消去法求解 $AX=I_n$。

**例 7.4** 用 Gauss-Jordan 消去法求 $A=\begin{pmatrix}1&2&3\\2&4&5\\3&5&6\end{pmatrix}$ 的逆矩阵 $A^{-1}$。

**解**

$$
C=\left(\begin{array}{rrr|rrr}
1&2&3&1&0&0\\
2&4&5&0&1&0\\
3&5&6&0&0&1
\end{array}\right)
\xrightarrow{r_1\leftrightarrow r_3}
\left(\begin{array}{rrr|rrr}
\boxed{3}&5&6&0&0&1\\
2&4&5&0&1&0\\
1&2&3&1&0&0
\end{array}\right)
$$

$$
\xrightarrow{\text{第一次消元}}
\left(\begin{array}{rrr|rrr}
1&5/3&2&0&0&1/3\\
0&2/3&1&0&1&-2/3\\
0&1/3&1&1&0&-1/3
\end{array}\right)
$$

原图标注：上述最后一列 $\begin{pmatrix}1/3\\-2/3\\-1/3\end{pmatrix}$ 以方框标出，标为 $c_3$。

<!-- 例7.4续 PDF190。 -->
''',notes=['逐项核对Gauss-Jordan五步中乘数负号及消元加号、全行范围i≠k；完整转录例7.4两次矩阵与方框c3标注。'])
rp=LANE/'review.json';r=json.loads(rp.read_text())
e={'id':'ch07a-E004','pdf_page':188,'printed_page':175,'formula_id':'7.3.2','type':'suspected_source_typo','original':'第二行第二个括号含L_{2i_2}','agent_note':'本页tilde L1定义对应I_{2i_2}；原L保留并另注。','evidence':'staging/ch07a/assets/pdf-188-permutation-detail.png'}
r['source_errata']=[q for q in r['source_errata'] if q.get('id')!=e['id']]+[e]
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
