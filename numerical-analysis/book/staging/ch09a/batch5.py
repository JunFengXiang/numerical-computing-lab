from write_pages import write_page,add_errata
write_page(245,r'''
<!-- 续 PDF 244，9.3.1 引言，定理 9.12 推论。 -->

则

$$
u=(\alpha_1+\sigma,\alpha_2,\cdots,\alpha_n)^{\mathrm T},
$$

$$
\rho=\frac12\|u\|_2^2=\frac12\left[(\alpha_1+\sigma)^2+\alpha_2^2+\cdots+\alpha_n^2\right]=\sigma(\sigma+\alpha_1).
$$

如果 $\sigma$ 和 $\alpha_1$ 异号，那么计算 $\alpha_1+\sigma$ 时有效数字可能损失，取 $\sigma$ 和 $\alpha_1$ 有相同的符号，即取

$$
\sigma=\operatorname{sgn}(\alpha_1)\|x\|_2.
$$

**算法 1** 已知向量 $x=(\alpha_1,\alpha_2,\cdots,\alpha_n)^{\mathrm T}\ne0$，本算法算出 $\sigma,\rho$ 及 $u$，使 $(I-\rho^{-1}uu^{\mathrm T})x=-\sigma e_1$，$u$ 的分量冲掉 $x$ 的分量。

**步 1** 计算 $\sigma=\operatorname{sgn}(\alpha_1)\left(\displaystyle\sum_{i=1}^n\alpha_i^2\right)^{\frac12}$。

**步 2** $\alpha_1\to u_1=\alpha_1+\sigma$。

**步 3** $\rho=\sigma u_1$。

在计算 $\sigma$ 时，可能上溢或下溢。为了避免溢出，将 $x$ 规范化

$$
\eta=\max_i|\alpha_i|,\quad x'=\frac{x}{\eta},
$$

显然

$$
\sigma'=\sigma/\eta,\quad H'=H.
$$

**算法 2** 已知 $x=(\alpha_1,\alpha_2,\cdots,\alpha_n)^{\mathrm T}\ne0$，本算法算出 $H$ 及 $\sigma$ 使 $Hx=-\sigma e_1$，$u$ 的分量冲掉 $x$ 的分量。

**步 1** $\eta=\max_i|\alpha_i|$。

**步 2** $\alpha_i\leftarrow u_i=\dfrac{\alpha_i}{\eta}\quad(i=1,2,\cdots,n)$。

**步 3** $\sigma=\operatorname{sgn}(u_1)\left(\displaystyle\sum_{i=1}^nu_i^2\right)^{\frac12}$。

**步 4** $u_1\leftarrow u_1+\sigma$。

**步 5** $\rho=\sigma u_1$。

**步 6** $\sigma\leftarrow\eta\sigma$。

关于 $HA$ 的计算，设 $A=(a_1,a_2,\cdots,a_n)$，其中 $a_i$ 为 $A$ 的第 $i$ 列向量，则

$$
HA=(Ha_1,Ha_2,\cdots,Ha_n),
$$

因此计算 $HA$ 就是要计算

$$
Ha_i=(I-\rho^{-1}uu^{\mathrm T})a_i=a_i-(\rho^{-1}u^{\mathrm T}a_i)u\quad(i=1,2,\cdots,n).
$$

于是计算 $Ha_i$ 只需要计算两向量的数量积和两向量的加法即可，且计算 $HA$ 共需要 $2n^2$ 次乘法运算。

### 9.3.2 用正交相似变换约化矩阵

下面考虑用初等反射阵来正交相似约化一般矩阵和对称矩阵。设

<!-- 矩阵及约化推导续 PDF 246。 -->
''',[{'id':'9.3.2','title':'用正交相似变换约化矩阵'}],['实际打开全页原图，确认书页 232；逐项核对两个算法共 9 个步骤及 HA 运算公式；实际打开算法裁切图，辨认 Greek alpha、算法 1 的右箭头和算法 2 的左箭头；保留“冲掉”的原书措辞。'])
write_page(246,r'''
<!-- 续 PDF 245，9.3.2 用正交相似变换约化矩阵。 -->

$$
A=\left(\begin{array}{c|ccc}
a_{11}&a_{12}&\cdots&a_{1n}\\\hline
a_{21}&a_{22}&\cdots&a_{2n}\\
\vdots&\vdots&&\vdots\\
a_{n1}&a_{n2}&\cdots&a_{nn}
\end{array}\right)
\equiv\begin{pmatrix}
a_{11}&A_{12}^{(1)}\\
a_{21}^{(1)}&A_{22}^{(1)}
\end{pmatrix},
$$

**步 1** 不妨设 $a_{21}^{(1)}\ne0$，否则这一步不需约化，选择初等反射阵 $R_1$ 使 $R_1a_{21}^{(1)}=-\sigma_1e_1$，其中

$$
\left\{
\begin{aligned}
\sigma_1&=\operatorname{sgn}(a_{21})\left(\sum_{i=2}^na_{i1}^2\right)^{\frac12},\\
u_1&=a_{21}^{(1)}+\sigma_1e_1,\\
\rho_1&=\frac12\|u_1\|_2^2=\sigma_1(\sigma_1+a_{21}),\\
R_1&=I-\rho_1^{-1}u_1u_1^{\mathrm T}.
\end{aligned}
\right.
\tag{9.3.1}
$$

令 $U_1=\begin{pmatrix}I&0\\0&R_1\end{pmatrix}$，则

$$
A_2=U_1A_1U_1=\begin{pmatrix}
a_{11}&A_{21}^{(1)}R_1\\
R_1a_{21}^{(1)}&R_1A_{22}^{(1)}R_1
\end{pmatrix}
\equiv\begin{pmatrix}
A_{11}^{(2)}&a_{12}^{(2)}&A_{13}^{(2)}\\
O&a_{22}^{(2)}&A_{23}^{(2)}
\end{pmatrix},
$$

其中 $A_{11}^{(2)}\in\mathbf R^{2\times1},\quad a_{22}^{(2)}\in\mathbf R^{n-2},\quad A_{23}^{(2)}\in\mathbf R^{(n-2)\times(n-2)}$。

**步 $k$** 设对 $A$ 已进行了第 $k-1$ 步正交相似约化，即 $A_k$ 有形式

$$
\begin{aligned}
A_k&=U_{k-1}A_{k-1}U_{k-1}\\
&=\left(\begin{array}{ccc|c|ccc}
a_{11}&a_{12}^{(2)}&\cdots&a_{1k}^{(k)}&a_{1,k+1}^{(k)}&\cdots&a_{1n}^{(k)}\\
-\sigma_1&a_{22}^{(2)}&\cdots&a_{2k}^{(k)}&a_{2,k+1}^{(k)}&\cdots&a_{2n}^{(k)}\\
&\ddots&\ddots&\vdots&\vdots&&\vdots\\
&&-\sigma_{k-1}&a_{kk}^{(k)}&a_{k,k+1}^{(k)}&\cdots&a_{k,n}^{(k)}\\\hline
&&&a_{k+1,k}^{(k)}&a_{k+1,k+1}^{(k)}&\cdots&a_{k+1,n}^{(k)}\\
&&&\vdots&\vdots&&\vdots\\
&&&a_{nk}^{(k)}&a_{n,k+1}^{(k)}&\cdots&a_{nn}^{(k)}
\end{array}\right)\\
&\equiv\begin{pmatrix}
A_{11}^{(k)}&a_{12}^{(k)}&A_{13}^{(k)}\\
O&a_{22}^{(k)}&A_{23}^{(k)}
\end{pmatrix},
\end{aligned}
$$

其中 $A_{11}^{(k)}\in\mathbf R^{k\times(k-1)},\quad a_{22}^{(k)}\in\mathbf R^{n-k},\quad A_{23}^{(k)}\in\mathbf R^{(n-k)\times(n-k)}$。

设 $a_{22}^{(k)}\ne0$，选择初等反射阵 $R_k$，使 $R_ka_{22}^{(k)}=-\sigma_ke_1$，其中

$$
\left\{
\begin{aligned}
\sigma_k&=\operatorname{sgn}(a_{k+1,k}^{(k)})\left(\sum_{i=k+1}^na_{ik}^2\right)^{\frac12},\\
u_k&=a_{22}^{(k)}+\sigma_ke_1,\\
\rho_k&=\frac12\|u_k\|_2^2=\sigma_k(\sigma_k+a_{k+1,n}^{(k)}),\\
R_k&=I-\rho_k^{-1}u_ku_k^{\mathrm T}.
\end{aligned}
\right.
\tag{9.3.2}
$$

<!-- 约化推导续 PDF 247（不在本 lane 范围内）。 -->

> **校注（agent 补充，ch09a-E009）** 本页 $A_2$ 的二阶分块表达式右上块原印 $A_{21}^{(1)}R_1$，已照录。由页首定义的右上块 $A_{12}^{(1)}$ 和 $U_1$ 的分块乘法，此处应为 $A_{12}^{(1)}R_1$。见[页首分块](../assets/review-p246-initial-partition.png)和[放大原式](../assets/review-p246-A-2.png)。
>
> **校注（agent 补充，ch09a-E010）** 式（9.3.2）原图 $\sigma_k$ 求和内为 $a_{ik}^2$，未印迭代上标；$\rho_k$ 最后一个矩阵元为 $a_{k+1,n}^{(k)}$，均照录。由本页 $a_{22}^{(k)}=(a_{k+1,k}^{(k)},\ldots,a_{nk}^{(k)})^{\mathrm T}$ 和 $u_k=a_{22}^{(k)}+\sigma_ke_1$，求和应使用当前列元素 $(a_{ik}^{(k)})^2$，而范数平方恒等式给出 $\rho_k=\sigma_k(\sigma_k+a_{k+1,k}^{(k)})$。故前者疑漏迭代上标，后者列下标疑将 $k$ 印成 $n$。见[放大原式](../assets/review-p246-9-3-2.png)。
''',[],['实际打开全页原图，确认书页 233；实际逐一打开初始分块、A_2、一般 A_k、9.3.2 四个裁切图；逐项核对块尺寸、全部行列下标、两处正交变换公式与 9.3.1–9.3.2；原图分块虚线以 LaTeX 数组分隔线表达；疑误 ch09a-E009、ch09a-E010 保留原式另注。'])
add_errata([
 {'id':'ch09a-E009','pdf_page':246,'printed_page':233,'kind':'source_erratum','location':'A_2 的二阶分块式右上块','source_form':'A_21^(1) R_1','explanation':'与页首 A 的分块及分块乘法不符，应为 A_12^(1) R_1；原式保留。','evidence_asset':'staging/ch09a/assets/review-p246-A-2.png'},
 {'id':'ch09a-E010','pdf_page':246,'printed_page':233,'kind':'source_erratum','location':'式 9.3.2 的 sigma_k 与 rho_k','source_form':'sum a_ik^2; rho_k=sigma_k(sigma_k+a_(k+1,n)^(k))','explanation':'求和疑漏迭代上标 (k)；由 u_k 的首分量和范数平方恒等式，rho_k 中列下标应为 k 而非原印 n。原式保留。','evidence_asset':'staging/ch09a/assets/review-p246-9-3-2.png'}
])
