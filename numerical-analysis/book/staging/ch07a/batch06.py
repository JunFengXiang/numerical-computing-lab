from write_page import save,LANE
import json
save(186,r'''
第 $k$ 步选主元素（在 $A^{(k)}$ 右下角方框内选），即确定 $i_k,j_k$ 使

$$|a_{i_kj_k}|=\max_{\substack{k\le i\le n\\k\le j\le n}}|a_{ij}|\ne0.$$

交换 $(A^{(k)},b^{(k)})$ 第 $k$ 行与 $i_k$ 行元素，交换 $(A^{(k)})$ 第 $k$ 列与 $j_k$ 列元素，将 $a_{i_kj_k}$ 调到 $(k,k)$ 位置，再进行消元计算，最后将原方程组化为

$$
\begin{pmatrix}
a_{11}&a_{12}&\cdots&a_{1n}\\
&a_{22}&\cdots&a_{2n}\\
&&\ddots&\vdots\\
&&&a_{nn}
\end{pmatrix}
\begin{pmatrix}y_1\\y_2\\\vdots\\y_n\end{pmatrix}
=\begin{pmatrix}b_1\\b_2\\\vdots\\b_n\end{pmatrix},
$$

其中 $y_1,y_2,\cdots,y_n$ 的次序为未知数 $x_1,x_2,\cdots,x_n$ 调换后的次序。回代求解得

$$
\begin{cases}
y_n=b_n/a_{nn},\\
y_i=\displaystyle\left(b_i-\sum_{j=i+1}^{n}a_{ij}y_j\right)/a_{ii}\quad(i=n-1,\cdots,2,1).
\end{cases}
$$

**算法 1** 完全主元素消去法，其步骤如下：

设 $Ax=b$。本算法用 $A$ 的带有行、列交换的 Gauss 消去法①，消元结果冲掉 $A$，乘数 $m_{ij}$ 冲掉 $a_{ij}$，计算解 $x$ 冲掉常数项 $b$，用 $k$ 表示对 $A$ 的消元次数。用一整型数组 $\mathrm{Iz}(n)$ 开始记录未知数 $x_1,x_2,\cdots,x_n$ 的次序（即下标 $1,2,\cdots,n$），最后记录调换后未知数的下标。

**步 1** 对于 $i=1,2,\cdots,n$，有 $\mathrm{Iz}(i)\leftarrow i$；对于 $k=1,2,\cdots,n-1$，做到步 6。

**步 2** 选主元素 $|a_{i_kj_k}|=\max_{\substack{k\le i\le n\\k\le j\le n}}|a_{ij}|$。

**步 3** 如果 $a_{i_kj_k}=0$，则计算停止（这时 $\det A=0$）。

**步 4** （1）如果 $i_k=k$，则转（2），否则换行：$a_{kj}\leftrightarrow a_{i_kj}$（$j=k,k+1,\cdots,n$），$b_k\leftrightarrow b_{i_k}$；（2）如果 $j_k=k$，则转步 5，否则换列：$a_{ik}\leftrightarrow a_{ij_k}$（$i=1,2,\cdots,n$），$\mathrm{Iz}(k)\leftrightarrow\mathrm{Iz}(j_k)$。

**步 5** 计算乘数

$$a_{ik}\leftarrow m_{ik}=a_{ik}/a_{kk}\quad(i=k+1,\cdots,n).$$

**步 6** 消元计算

$$a_{ij}\leftarrow a_{ij}-m_{ik}a_{kj}\quad(i=k+1,\cdots,n;\;j=k+1,\cdots,n);$$

$$b_i\leftarrow b_i-m_{ik}b_k\quad(i=k+1,\cdots,n).$$

**步 7** 回代求解

（1）$b_n\leftarrow b_n/a_{n,n}$；（2）对于 $i=n-1,n-2,\cdots,2,1$，$b_i\leftarrow\left(b_i-\sum_{j=i+1}^{n}a_{ij}b_j\right)/a_{ii}$。

**步 8** 调整未知数的次序

（1）对于 $i=1,2,\cdots,n$；$a_i,\mathrm{Iz}(i)\leftarrow b_i$；（2）对于 $i=1,2,\cdots,n$；$b_i\leftarrow a_{1i}$。

### 7.3.2 列主元素消去法

完全主元素消去法在选主元素时要花费较多机器时间。下面介绍另一种常用的

> ① 在实际计算中可以考虑设计不进行行、列交换的算法。

<!-- 本页末句未完，续 PDF187。 -->

> 校注（agent 补充）：算法 1 步 8（1）原书印作 $a_i,\mathrm{Iz}(i)\leftarrow b_i$（逗号及 Iz 为基线排印），本转录保留。按该步（2）$b_i\leftarrow a_{1i}$ 及“调整未知数的次序”，（1）应把 $b_i$ 暂存到第一行第 $\mathrm{Iz}(i)$ 列，即 $a_{1,\mathrm{Iz}(i)}\leftarrow b_i$；疑似原书下标排印错误。参见[原步骤放大裁图](../assets/pdf-186-step8-detail.png)。
''',[{'id':'7.3.2','title':'列主元素消去法'}],notes=['算法1所有8步、循环界和脚注逐项目视核对；Iz为原书整型数组名。步8(1)原排印异常已保留另注。'])
save(187,r'''
<!-- 接 PDF186 页末。 -->

方法即列主元素消去法。它仅考虑依次按列选主元素，然后换行使之变到主元位置上，再进行消元计算。设用列主元素消去法解 $Ax=b$ 已完成 $k-1$ 步计算，即有

$$
(A,b)\to(A^{(k)},b^{(k)})=
\left(\begin{array}{cccccc|c}
a_{11}^{(1)}&a_{12}^{(1)}&\cdots&\cdots&\cdots&a_{1n}^{(1)}&b_1^{(1)}\\
&a_{22}^{(2)}&\cdots&\cdots&\cdots&a_{2n}^{(2)}&b_2^{(2)}\\
&&\ddots&&&\vdots&\vdots\\
&&&a_{kk}^{(k)}&\cdots&a_{kn}^{(k)}&b_k^{(k)}\\
&&&\vdots&&\vdots&\vdots\\
&&&a_{nk}^{(k)}&\cdots&a_{nn}^{(k)}&b_n^{(n)}
\end{array}\right),
$$

且 $A^{(k)}x=b^{(k)}$ 与 $Ax=b$ 等价，第 $k$ 步选主元素（在 $A^{(k)}$ 第 $k$ 列方框内选），即确定 $i_k$ 使

$$|a_{i_k,k}^{(k)}|=\max_{k\le i\le n}|a_{ik}^{(k)}|.$$

**算法 2** 列主元素消去法，其步骤如下：

设 $Ax=b$。本算法用 $A$ 的具有行交换的列主元素消去法①，消元结果冲掉 $A$，乘数 $m_{ij}$ 冲掉 $a_{ij}$，计算解 $x$ 冲掉常数项 $b$，行列式存放在 $\det A$。

**步 1** $\det A\leftarrow1$，对于 $k=1,2,\cdots,n-1$ 做到步 7。

**步 2** 按列选主元素 $|a_{i_kk}|=\max_{k\le i\le n}|a_{ik}|$。

**步 3** 如果 $a_{i_kk}=0$，则 $\det A\leftarrow0$，计算停止。

**步 4** 如果 $i_k=k$，则转步 5，否则换行：

$$a_{kj}\leftrightarrow a_{i_kj}\quad(j=k,k+1,\cdots,n),\quad b_k\leftrightarrow b_{i_k},\quad \det A\leftarrow-\det A.$$

**步 5** 计算乘数 $m_{ik}$

$$a_{ik}\leftarrow m_{ik}=a_{ik}/a_{kk}\quad(i=k+1,\cdots,n)\;(|m_{ik}|\le1).$$

**步 6** 消元计算

$$a_{ij}\leftarrow a_{ij}-m_{ik}a_{kj}\quad(i,j=k+1,\cdots,n),\quad b_i\leftarrow b_i-m_{ik}b_k\quad(i=k+1,\cdots,n).$$

**步 7** $\det A\leftarrow a_{kk}\det A$。

**步 8** 回代求解

$$b_n\leftarrow b_n/a_{nn},\quad b_i\leftarrow\left(b_i-\sum_{j=i+1}^{n}a_{ij}b_j\right)/a_{ii}\quad(i=n-1,n-2,\cdots,1).$$

**步 9** $\det A\leftarrow a_{nn}\det A$。

例 7.3 的方法 2 用的就是列主元素消去法。

下面用矩阵运算来描述解式（7.2.1）的列主元素消去法：

$$
\begin{cases}
L_1I_{1i_1}A^{(1)}=A^{(2)},\quad L_1I_{1i_1}b^{(1)}=b^{(2)},\\
L_kI_{ki_k}A^{(k)}=A^{(k+1)},\quad L_kI_{ki_k}b^{(k)}=b^{(k+1)},
\end{cases}
\tag{7.3.1}
$$

其中 $L_k$ 的元素满足 $|m_{ik}|\le1$（$k=1,2,\cdots,n-1$），$I_{ki_k}$ 是初等排列矩阵（由交换单位矩阵 $I$ 的第 $k$ 行与第 $i_k$ 行得到）。

> ① 在列主元素消去法中，可考虑用一整型数组 $\mathrm{Ip}(n)$ 来记录主行。

> 校注（agent 补充）：本页首个增广矩阵右下角原书印作 $b_n^{(n)}$，已保留。此处描述第 $k-1$ 步完成后的 $(A^{(k)},b^{(k)})$，同列第 $k$ 行是 $b_k^{(k)}$，所以末行相应应为 $b_n^{(k)}$；疑似原书上标排印错误。参见[原矩阵放大裁图](../assets/pdf-187-rhs-detail.png)。
''',notes=['原页算法2九步、行列式符号翻转、乘数上界和排列矩阵逐项复核；首矩阵b_n^(n)保留并另注。'])
rp=LANE/'review.json'; r=json.loads(rp.read_text())
errata=[{'id':'ch07a-E002','pdf_page':186,'printed_page':173,'location':'算法1步8(1)','type':'suspected_source_typo','original':'a_i, Iz(i) ← b_i（Iz在基线）','agent_note':'调整次序应把b_i暂存a_{1,Iz(i)}，再按(2)复制a_{1i}；原排印保留并另注。','evidence':'staging/ch07a/assets/pdf-186-step8-detail.png'},{'id':'ch07a-E003','pdf_page':187,'printed_page':174,'location':'页首增广矩阵右下角','type':'suspected_source_typo','original':'b_n^{(n)}','agent_note':'此处为第k步前的b^(k)，右下角应为b_n^(k)；原上标保留并另注。','evidence':'staging/ch07a/assets/pdf-187-rhs-detail.png'}]
ids={e['id'] for e in errata}; r['source_errata']=[e for e in r['source_errata'] if e.get('id') not in ids]+errata
rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
