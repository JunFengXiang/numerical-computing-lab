# 原书疑误与校注索引

以下内容区分原书印字、agent 校注和转录纠错。保留原式不代表该式已通过数学检验；使用公式前必须阅读对应页的校注。所有条目经过第二位 agent 对图复核，数学适用条件、术语差异、舍入误差与排印疑误分别保留原记录性质。

| 编号 | PDF 原页 | 说明 |
|---|---:|---|
| front-toc-ch7-exercises-page-damage | [11](../verified/pages/pdf-011.md) | 第 7 章习题的目录页码前部扫描残损，末位可辨为 8。原印完整数字不能确认；正文实际开始于书页 199（PDF 212）。 |
| CH01-E001 | [17](../verified/pages/pdf-017.md) | 原文照录；由E_n=(-1)^n n!E_0，应指近似值tilde I_n的误差绝对值为初值误差绝对值的n!倍。 |
| CH01-E002 | [21](../verified/pages/pdf-021.md) | 放大原图确认上限是k；由n元函数及式1.3.3，应为n。转录保留k并单列校注。 |
| CH01-E003 | [21](../verified/pages/pdf-021.md) | 原句照录；忽略二阶项相对一阶项应控制／f″(xi)／epsilon(x*)/(2／f′(x*)／)，疑有比值顺序或条件表述问题。 |
| CH01-E004 | [22](../verified/pages/pdf-022.md) | 由两原方程相减得(2-0.00001)x1=1，故x1=100000/199999约0.5000025000125；原列x2与此解一致。原文未改。 |
| CH01-E005 | [23](../verified/pages/pdf-023.md) | 原文保留。第一操作实际为第一方程除以小量；第二种直接消去后四位浮点首行应为10^1乘0.1000x2=10^1乘0.1000。原式可以额外同乘10^5得到但文本未给该步。 |
| CH01-E006 | [23](../verified/pages/pdf-023.md) | 实际A约6091.729809，6130误差约38.270191>5，不满足本章三位有效数字定义；原文照录并附校注。 |
| CH01-E007 | [26](../verified/pages/pdf-026.md) | 原图确认右侧为+1，原样保留。由(x-sqrt(x^2-1))(x+sqrt(x^2-1))=1，相应等价式右侧根号内应为x^2-1。 |
| CH01-E008 | [26](../verified/pages/pdf-026.md) | 原文保留。有限误差取Delta a/a=Delta b/b=0.01且Delta c=0，精确面积相对变化0.0201>0.02；应注明一阶近似/微分解释。由独立校对agent front提出，ch01复核。 |
| NA5E-E001 | [27](../verified/pages/pdf-027.md) | 定义 2.1 印为 x_0 ≤ x_1，与后文互异节点前提不一致；原文与校注分列。 |
| NA5E-E002 | [34](../verified/pages/pdf-034.md) | 原书 cos(0.32)<0.828、余项数值界0.178×10^-7以及中间乘积3.89×10^-4有误；保留印字与独立校注。 |
| CH02A-S01 | [38](../verified/pages/pdf-038.md) | 递推式末项原印f(x,x_0,...,x_n]，左右括号不配，应理解为差商f[...]；原文及校注分列。 |
| CH02A-S02 | [40](../verified/pages/pdf-040.md) | 表2.6首列表头原印x_k，列中为f_0,f_1,...；保留并说明表头应理解为f_k。 |
| CH02A-S03 | [38](../verified/pages/pdf-038.md) | 表2.5混用中间舍入；精确输入重算五阶差商为2/6825≈+0.00029304，原表−0.00012。原表保留，独立说明原书估计与精度边界。 |
| CH02A-S04 | [39](../verified/pages/pdf-039.md) | 例2.3原印N4(0.596)=0.63195；按原印多项式计算为0.63191751982370304，五位小数应0.63192。原文与校注分列。 |
| ch02b-E001 | [46](../verified/pages/pdf-046.md) | {"lane": "ch02b", "id": "ch02b-E001", "pdf_page": 46, "printed_page": 33, "formula_id": "2.7.3", "status": "suspected_source_error", "original": "\\frac{x_j-x_{j+1}}{x-x_{j+1}}", "suggested": "\\frac{x-x_{j+1}}{x_j-x_{j+1}}", "reason": "原式在右端点分母为零，违反分段线性、连续及节点基函数条件；原图确认原式分子分母倒置。", "evidence": "staging/ch02b/assets/pdf-046-eq-2-7-3-detail.png"} |
| ch02b-E002 | [49](../verified/pages/pdf-049.md) | {"lane": "ch02b", "id": "ch02b-E002", "pdf_page": 49, "printed_page": 36, "related_pdf_page": 48, "formula_id": "2.7.13", "status": "suspected_source_omission", "original": "当 f(x)∈C[a,b] 时分段三次 Hermite 插值一致收敛。", "reason": "由 (2.7.13) 推出收敛还需 h max_k ／f′_k／→0；仅连续不足以保证节点导数存在及随网格加密的一致控制。", "suggested": "补充适当导数控制条件，例如 f∈C¹[a,b]；正文保留原文。"} |
| ch02b-E003 | [50](../verified/pages/pdf-050.md) | {"lane": "ch02b", "id": "ch02b-E003", "pdf_page": 50, "printed_page": 37, "formula_id": "unnumbered S″ on [x_{j-1},x_j]", "status": "suspected_source_error", "original": "第三项分母 h_{j-1}²", "suggested": "第三项分母 h_{j-1}³", "reason": "由同页前一个区间公式换下标及下页端点导数式交叉核对，分母应为三次幂。", "evidence": "staging/ch02b/assets/pdf-050-second-derivative-detail.png"} |
| ch02b-E004 | [52](../verified/pages/pdf-052.md) | {"lane": "ch02b", "id": "ch02b-E004", "pdf_page": 52, "printed_page": 39, "formula_id": "unnumbered lambda_n", "status": "suspected_source_error", "original": "λ_n=h_{n-1}/(h_0+h_{n-1})", "suggested": "λ_n=h_0/(h_0+h_{n-1})", "reason": "由前一行未归一化周期方程直接除以 1/h0+1/h_{n-1}。", "evidence": "staging/ch02b/assets/pdf-052-periodic-system-detail.png"} |
| ch02b-E005 | [52](../verified/pages/pdf-052.md) | {"lane": "ch02b", "id": "ch02b-E005", "pdf_page": 52, "printed_page": 39, "formula_id": "2.8.15", "status": "suspected_source_error", "original": "周期方程系数矩阵右上、左下角均为 0。", "suggested": "右上角 λ_1；左下角 μ_n。", "reason": "分别由 m0=mn 代入首行及本页周期端点方程得；普通三对角追赶法需要相应循环系统处理。", "evidence": "staging/ch02b/assets/pdf-052-periodic-system-detail.png"} |
| ch02b-E006 | [54](../verified/pages/pdf-054.md) | {"lane": "ch02b", "id": "ch02b-E006", "pdf_page": 54, "printed_page": 41, "formula_id": "2.8.21", "status": "suspected_source_error", "original": "max_{1≤i≤n}／x_j／", "suggested": "max_{1≤i≤n}／x_i／", "reason": "最大值指标 i 与被取最大值分量 j 不一致。", "evidence": "staging/ch02b/assets/pdf-054-norm-detail.png"} |
| ch02b-E007 | [54](../verified/pages/pdf-054.md) | {"lane": "ch02b", "id": "ch02b-E007", "pdf_page": 54, "printed_page": 41, "formula_id": "2.8.23", "status": "suspected_source_error", "original": "min(／a_ij／−sum_{j≠i}／a_ij／)", "suggested": "min_i(／a_ii／−sum_{j≠i}／a_ij／)", "reason": "逆范数上界的对角占优余量首项应为对角元素。", "evidence": "staging/ch02b/assets/pdf-054-norm-detail.png"} |
| ch02b-E008 | [54](../verified/pages/pdf-054.md) | {"lane": "ch02b", "id": "ch02b-E008", "pdf_page": 54, "printed_page": 41, "table": "2.8", "status": "source_table_condition_mismatch", "original": "S10(−4.8)=0.03758, S10(−4.5)=0.04248", "reason": "按PDF53明定的两端一阶导数条件精确解得0.04162183和0.04716801，原表数字已保持不变。", "evidence": "staging/ch02b/table-2-8-check.txt"} |
| ch02b-E009 | [55](../verified/pages/pdf-055.md) | {"lane": "ch02b", "id": "ch02b-E009", "pdf_page": 55, "printed_page": 42, "formula_id": "2.8.24 following matrix/vector", "status": "suspected_source_error", "original": "自然边界矩阵末行次对角元 λ_n；m 向量第二项 m2。", "suggested": "次对角元 1；向量第二项 m1。", "reason": "与本页引用的自然边界方程 (2.8.14) 不一致；此处未定义自然边界 λ_n。", "evidence": "staging/ch02b/assets/pdf-055-matrix-detail.png"} |
| ch02b-E010 | [55](../verified/pages/pdf-055.md) | {"lane": "ch02b", "id": "ch02b-E010", "pdf_page": 55, "printed_page": 42, "formula_id": "2.8.27", "status": "suspected_source_error", "original": "末项 ／／g／／_∞^m", "suggested": "／／g／／_∞", "reason": "由 ／／A^{-1}／／∞≤1 得 ／／m／／∞≤／／g／／∞；原图多余 m 清楚。", "evidence": "staging/ch02b/assets/pdf-055-eq-2-8-27-detail.png"} |
| ch02b-E011 | [55](../verified/pages/pdf-055.md) | {"lane": "ch02b", "id": "ch02b-E011", "pdf_page": 55, "printed_page": 42, "formula_id": "reference after 2.8.28", "status": "suspected_source_error", "original": "将式 (2.8.9) 及式 (2.8.28) 代入式 (2.8.26)", "suggested": "式 (2.8.9) 应指 (2.8.27)", "reason": "当前推导需将 m 的范数界与 g 的界结合。"} |
| ch02b-E012 | [56](../verified/pages/pdf-056.md) | {"lane": "ch02b", "id": "ch02b-E012", "pdf_page": 56, "printed_page": 43, "table": "2.9", "status": "suspected_source_error", "original": "ln(0.7)=−0.357765", "suggested": "−0.356675 (六位小数)", "reason": "ln(0.7)≈−0.356674944；原表数字原样保留。", "evidence": "staging/ch02b/assets/table-2-9.png"} |
| ch02b-E013 | [57](../verified/pages/pdf-057.md) | {"lane": "ch02b", "id": "ch02b-E013", "pdf_page": 57, "printed_page": 44, "exercise": 18, "status": "source_exercise_incomplete", "original": "P(0)=P(−k+1)，并由此求出分段三次 Hermite 插值的误差限。", "reason": "k 未定义，多项式条件不完整，末句重复前题要求；原意无法从扫描可靠恢复。", "suggested": "保留原文并提示题目疑误，不猜补。", "evidence": "staging/ch02b/assets/pdf-057-exercise-18-detail.png"} |
| ch03a-E01 | [59](../verified/pages/pdf-059.md) | 原图确印 x_k；由 l_k(x_k)=1 左端为 n+1，通常恒等式应为 sum l_k(x)=1。转录保留原文。 |
| ch03a-E02 | [62](../verified/pages/pdf-062.md) | 上下文在解释定理 3.3 的正、负偏差点性质，应为定理 3.3；定理 3.1 为 Weierstrass 定理。原文保留。 |
| ch03a-E03 | [64](../verified/pages/pdf-064.md) | 本页前文三个点编号为 x_1<x_2<x_3，按该编号端点应为 x_1=a, x_3=b。转录保留原书。 |
| ch03a-E04 | [64](../verified/pages/pdf-064.md) | 把印出的舍入系数作为精确数，x=1 时误差 sqrt(2)-1.369=0.04521356237... 大于 0.045。原书数值及不等式均保留。 |
| ch03a-E05 | [67](../verified/pages/pdf-067.md) | 式 (3.3.10) 为内积 Gram 矩阵的行列式，通常应称 Gram 行列式。原文保留并加校注。 |
| ch03a-E06 | [68](../verified/pages/pdf-068.md) | 原图为小写 varphi，而前文子集记为大写 Phi；应指 Phi。原符号保留。 |
| ch03a-E07 | [69](../verified/pages/pdf-069.md) | 该数来自舍入内积；对印出的 S=0.934+0.426x 直接积分，实际平方误差约为 0.0007136323726914。原书数值保留。 |
| ch03a-E08 | [70](../verified/pages/pdf-070.md) | k 是求和哑指标，外部应为 n=1,2,...；原文保留。 |
| ch03a-E09 | [70](../verified/pages/pdf-070.md) | 一般 n 时与 g_0=1 冲突；通常初值应为 g_{-1}(x)=0。原文保留。 |
| ch03a-E10 | [71](../verified/pages/pdf-071.md) | 原图确印 2^2；根据 (3.4.1) 及随后 a_n，应为 1/(2^n n!)。原式保留。 |
| ch03a-E11 | [74](../verified/pages/pdf-074.md) | 应指本页定理 3.7 的最小偏差性质，3.6 为内积行列式判别条件。原文保留。 |
| ch03b-E001 | [76](../verified/pages/pdf-076.md) | 原图明确为e^n；取n=0与同页L_0(x)=1矛盾，保留原式另注。 |
| ch03b-E002 | [77](../verified/pages/pdf-077.md) | 左端原书下标k，右端求和上限n；保留原式另注。 |
| ch03b-E003 | [78](../verified/pages/pdf-078.md) | 例3.4最大误差式未加星号，保留原书记法。 |
| ch03b-E004 | [79](../verified/pages/pdf-079.md) | 原图已放大确认；与同式左侧下限及上页定义不一致，保留并校注。 |
| ch03b-E005 | [80](../verified/pages/pdf-080.md) | 不等式原印星号保留并校注。 |
| ch03b-E006 | [81](../verified/pages/pdf-081.md) | 最终指数模型原印为乘t；与本页y=a exp(b/t)及趋向a的描述矛盾。 |
| ch03b-E007 | [81](../verified/pages/pdf-081.md) | 变换后拟合数据原文漏帽号，保留并校注。 |
| ch03b-E008 | [82](../verified/pages/pdf-082.md) | 式3.6.11原印为拉丁a，递推式为希腊alpha；保留。 |
| ch03b-E009 | [82](../verified/pages/pdf-082.md) | beta_0涉及未定义的P_-1；递推只使用beta_1起。 |
| ch03b-E010 | [83](../verified/pages/pdf-083.md) | l与1已在放大原图核对，原印保留另注。 |
| ch03b-E011 | [83](../verified/pages/pdf-083.md) | 保留原文；不得与递推alpha_k混同。 |
| ch03b-E012 | [84](../verified/pages/pdf-084.md) | 原书多元拟合的系数范围不一致，保留另注。 |
| ch03b-E013 | [84](../verified/pages/pdf-084.md) | 左端为(varphi_k,varphi_j)，右端原图下标明确为i；保留。 |
| ch03b-E014 | [85](../verified/pages/pdf-085.md) | j为求和指标，频率为k,l；原印保留。 |
| ch03b-E015 | [87](../verified/pages/pdf-087.md) | j=1时有N个不同的N次单位根，原文缺少限定；保留并解释。 |
| ch03b-E016 | [87](../verified/pages/pdf-087.md) | 本段原文保留；前段余数定义作用于整数指数m。 |
| ch03b-E017 | [89](../verified/pages/pdf-089.md) | 与3.7.14代入k=0,j=1矛盾；原表保留。 |
| ch03b-E018 | [89](../verified/pages/pdf-089.md) | 与正文记法不一致；原表保留。 |
| ch03b-E019 | [89](../verified/pages/pdf-089.md) | 原图指数斜杠已放大确认；与循环次数不一致。 |
| ch03b-E020 | [90](../verified/pages/pdf-090.md) | 与3.7.16和对应和式偏移不一致；原文保留。 |
| ch03b-E021 | [90](../verified/pages/pdf-090.md) | 原文少-1，循环范围与3.7.16、步5不一致，并可能越界。 |
| ch03b-E022 | [91](../verified/pages/pdf-091.md) | 定义左端原图无星号，后文与题11均为T_n星号；保留另注。 |
| ch03b-E023 | [91](../verified/pages/pdf-091.md) | 原图引用为3.4.5，本章Schwarz实际编号为3.3.5；保留另注。 |
| CH04A-E01 | [97](../verified/pages/pdf-097.md) | 表 4.1 后首段 |
| CH04A-E02 | [100](../verified/pages/pdf-100.md) | 例 4.1 解答第二段 |
| CH04A-E03 | [102](../verified/pages/pdf-102.md) | 表 4.3，k=3 的 T_n |
| CH04A-E04 | [102](../verified/pages/pdf-102.md) | 表 4.3 后首句 |
| CH04A-E05 | [104](../verified/pages/pdf-104.md) | 式（4.3.13）的指标范围 |
| CH04A-E06 | [104](../verified/pages/pdf-104.md) | 定理 4.3 / 式（4.3.7），并涉及式（4.3.14） |
| CH04A-E07 | [102](../verified/pages/pdf-102.md) | 表 4.3，k=5 的 T_n |
| CH04B-E001 | [106](../verified/pages/pdf-106.md) | 式 (4.3.17) 首项 |
| CH04B-E002 | [108](../verified/pages/pdf-108.md) | 表4.5 n=3 第二对节点 |
| CH04B-E003 | [111](../verified/pages/pdf-111.md) | 消去 (x1-x0)A1 后的第二行未编号公式 |
| CH04B-E004 | [113](../verified/pages/pdf-113.md) | 节点多项式 omega_{n+1} 的定义 |
| CH04B-E005 | [117](../verified/pages/pdf-117.md) | 习题1(4)首项分母 |
| CH04B-E006 | [118](../verified/pages/pdf-118.md) | 习题9椭圆周长公式 |
| ch05a-E001 | [124](../verified/pages/pdf-124.md) | 表 5.2，x_n=0.8 的 y_n |
| ch05a-E002 | [124](../verified/pages/pdf-124.md) | 5.2.5 单步法与两步法比较段 |
| ch05a-E003 | [129](../verified/pages/pdf-129.md) | 5.3.4 引入第三阶段节点与预测 K_3 的两处正文 |
| ch05a-E004 | [134](../verified/pages/pdf-134.md) | 式 (5.4.5) |
| ch05a-E005 | [134](../verified/pages/pdf-134.md) | 式 (5.4.9) |
| ch05a-E006 | [135](../verified/pages/pdf-135.md) | 页首无编号不等式 |
| ch05a-E007 | [136](../verified/pages/pdf-136.md) | 例 5.5 稳定性步长说明 |
| ch05b-E001 | [138](../verified/pages/pdf-138.md) | 5.5.2，式（5.5.4）上方未编号差分展开式 |
| ch05b-E002 | [141](../verified/pages/pdf-141.md) | 两条事后估计式及计算方案两条改进式 |
| ch05b-E003 | [141](../verified/pages/pdf-141.md) | 计算方案第一条计算式 |
| ch05b-E004 | [141](../verified/pages/pdf-141.md) | 表5.10最后一行准确值 |
| ch05b-E005 | [143](../verified/pages/pdf-143.md) | 式（5.5.21）右端开头 |
| ch05b-E006 | [152](../verified/pages/pdf-152.md) | 式（5.7.15）后括注 |
| ch05b-E007 | [153](../verified/pages/pdf-153.md) | 小结五处节号 |
| ch05b-E008 | [154](../verified/pages/pdf-154.md) | 习题14 |
| ch06-E001 | [156](../verified/pages/pdf-156.md) | {"lane": "ch06", "id": "ch06-E001", "pdf_page": 156, "printed_page": 143, "kind": "source_cross_reference_anomaly", "original": "误差估计式（6.1.1）", "observation": "对应误差界原页未印编号；转录保留引用且不补造tag。", "evidence": "staging/ch06/assets/detail-p156-audit.png"} |
| ch06-E002 | [165](../verified/pages/pdf-165.md) | {"lane": "ch06", "id": "ch06-E002", "pdf_page": 165, "printed_page": 152, "kind": "suspected_source_missing_subscript", "original": "Newton步4以(x_1,f_1,f')代替(x_0,f_0,f'_0)", "observation": "原扫描第三项f'无下标；按步2定义和替换对象疑应为f'_1。原文已保留。", "evidence": "staging/ch06/assets/detail-p165-step4.png"} |
| ch06-E003 | [170](../verified/pages/pdf-170.md) | {"lane": "ch06", "id": "ch06-E003", "pdf_page": 170, "printed_page": 157, "kind": "suspected_source_sign_error", "original": "f(x_1)=-0.093271, x_1=0.6, f(x)=x exp(x)-1", "observation": "f(0.6)=0.0932712802343052为正；用正值所得一阶差商2.689106448842411与书中2.68910一致。原负号已保留。", "evidence": "staging/ch06/assets/detail-p170-example.png"} |
| ch06-E004 | [170](../verified/pages/pdf-170.md) | {"lane": "ch06", "id": "ch06-E004", "pdf_page": 170, "printed_page": 157, "kind": "suspected_source_cross_reference_error", "original": "代入式（6.4.8）求得", "observation": "该段实际使用的零点式在本页编号6.4.3；原引用已保留。", "evidence": "staging/ch06/assets/detail-p170-example.png"} |
| ch06-E005 | [174](../verified/pages/pdf-174.md) | {"lane": "ch06", "id": "ch06-E005", "pdf_page": 174, "printed_page": 161, "kind": "suspected_source_missing_sign", "original": "用x^2+ux+v除P(x)的商及展开式记作partial P/partial v", "observation": "按同页6.5.11：P=-(x^2+ux+v)(partial P/partial v)+s_0 x+s_1，商应为负的该偏导。正文、展开式及原递推均保留。", "evidence": "staging/ch06/assets/detail-p174-audit.png"} |
| ch06-E006 | [175](../verified/pages/pdf-175.md) | {"lane": "ch06", "id": "ch06-E006", "pdf_page": 175, "printed_page": 162, "kind": "suspected_source_exercise_condition_error", "original": "习题2求1-x sin(x)=0在(0,1)内的根", "observation": "0<x<1时0<x sin(x)<1，因此该区间无根；保留原题，不指定修正区间，不代做。", "evidence": "staging/ch06/assets/detail-p175-audit.png"} |
| ch06-E007 | [161](../verified/pages/pdf-161.md) | {"lane": "ch06", "id": "ch06-E007", "pdf_page": 161, "printed_page": 148, "kind": "suspected_source_exactness_error", "original": "6.2.9: x^* = x_1/(1-L) - Lx_0/(1-L)", "observation": "上一行仅有x_1-x^*约等于L(x_0-x^*)，一般只能推出近似关系；原等号保留并单列校注。", "evidence": "source-images/pdf-161.jpeg"} |
| ch06-E008 | [165](../verified/pages/pdf-165.md) | {"lane": "ch06", "id": "ch06-E008", "pdf_page": 165, "printed_page": 152, "kind": "source_convergence_order_condition", "original": "单根f(x*)=0、f-prime(x*)不为零，推出Newton法平方收敛", "observation": "按定义6.2非零极限常数的严格阶定义，恰为二阶尚需f-double-prime(x*)不为零；通常光滑性条件下单根保证至少二阶。原文保留并加条件校注及f=x+x^3的三阶反例。", "evidence": "source-images/pdf-165.jpeg"} |
| ch06-E009 | [168](../verified/pages/pdf-168.md) | {"lane": "ch06", "id": "ch06-E009", "pdf_page": 168, "printed_page": 155, "kind": "source_geometric_equation_scope", "original": "称弦线方程为P_1(x)=0", "observation": "弦线自身为y=P_1(x)；原式是与x轴交点的条件，保留原文并说明其用途。", "evidence": "source-images/pdf-168.jpeg"} |
| ch06-E010 | [169](../verified/pages/pdf-169.md) | {"lane": "ch06", "id": "ch06-E010", "pdf_page": 169, "printed_page": 156, "kind": "source_convergence_order_condition", "original": "二阶连续导数且一阶导数非零时，弦截法按精确阶(1+sqrt(5))/2收敛", "observation": "按定义6.2非零极限常数的精确阶，需二阶导数在根处非零等非退化条件并排除有限步终止；一次函数可一步得根。原文保留并单列校注。", "evidence": "source-images/pdf-169.jpeg"} |
| ch07a-E001 | [180](../verified/pages/pdf-180.md) | {"lane": "ch07a", "id": "ch07a-E001", "pdf_page": 180, "printed_page": 167, "formula_id": "7.2.12", "type": "suspected_source_typo", "original": "D_i 的矩阵右上角为 a_{1k}", "agent_note": "按第i阶顺序主子式应为a_{1i}；原式保留并另注。", "evidence": "staging/ch07a/assets/pdf-180-principal-minor-detail.png"} |
| ch07a-E002 | [186](../verified/pages/pdf-186.md) | 算法1步8(1) |
| ch07a-E003 | [187](../verified/pages/pdf-187.md) | 页首增广矩阵右下角 |
| ch07a-E004 | [188](../verified/pages/pdf-188.md) | {"lane": "ch07a", "id": "ch07a-E004", "pdf_page": 188, "printed_page": 175, "formula_id": "7.3.2", "type": "suspected_source_typo", "original": "第二行第二个括号含L_{2i_2}", "agent_note": "本页tilde L1定义对应I_{2i_2}；原L保留并另注。", "evidence": "staging/ch07a/assets/pdf-188-permutation-detail.png"} |
| ch07a-E005 | [190](../verified/pages/pdf-190.md) | 解释段m_k列向量 |
| ch07a-E006 | [193](../verified/pages/pdf-193.md) | 分解存储矩阵第r-1行末项 |
| ch07b-E001 | [196](../verified/pages/pdf-196.md) | 式(7.4.8)步4 |
| ch07b-E002 | [196](../verified/pages/pdf-196.md) | LDL^T展开最右矩阵次末行末项 |
| ch07b-E003 | [197](../verified/pages/pdf-197.md) | 式(7.4.11)步4 |
| ch07b-E004 | [202](../verified/pages/pdf-202.md) | 定理7.13证明中所引用定理号 |
| ch07b-E005 | [203](../verified/pages/pdf-203.md) | Ax_0第i_0个分量表达式首个求和下限 |
| ch07b-E006 | [204](../verified/pages/pdf-204.md) | 复矩阵2-范数公式中间项 |
| ch07b-E007 | [205](../verified/pages/pdf-205.md) | 定理7.18证明起始及逆矩阵恒等式 |
| ch07b-E008 | [208](../verified/pages/pdf-208.md) | 例7.9 H6条件数 |
| ch07b-E009 | [209](../verified/pages/pdf-209.md) | 例7.10缩放后条件数分式 |
| ch07b-E010 | [210](../verified/pages/pdf-210.md) | 向后误差段及定理7.22(2)扰动方程 |
| ch07b-E011 | [211](../verified/pages/pdf-211.md) | 式(7.6.14)关系符和适用条件 |
| ch07b-E012 | [214](../verified/pages/pdf-214.md) | 习题27分子 |
| ch07b-E013 | [214](../verified/pages/pdf-214.md) | 习题30(2)左端 |
| ch07b-E014 | [208](../verified/pages/pdf-208.md) | 例7.9所称精确解的小数向量 |
| ch08-E013 | [217](../verified/pages/pdf-217.md) | 式8.2.1下方非零条件 |
| ch08-E009 | [231](../verified/pages/pdf-231.md) | 习题5(1)第二个方程 |
| ch08-E010 | [231](../verified/pages/pdf-231.md) | 习题12残差定义 |
| ch08-E011 | [231](../verified/pages/pdf-231.md) | 习题12(2)误差定义 |
| ch08-E012 | [231](../verified/pages/pdf-231.md) | 习题12(2)误差递推 |
| ch08-E006 | [229](../verified/pages/pdf-229.md) | 定理8.10证明平方差因式 |
| ch08-E007 | [229](../verified/pages/pdf-229.md) | 定理8.10证明分母非零说明 |
| ch08-E008 | [229](../verified/pages/pdf-229.md) | SOR算法步5(1) |
| ch08-E005 | [227](../verified/pages/pdf-227.md) | 例8.11第11次迭代向量与误差界 |
| ch08-E004 | [224](../verified/pages/pdf-224.md) | 定义8.5分块阶数范围 |
| ch08-E003 | [219](../verified/pages/pdf-219.md) | 例8.2误差无穷范数 |
| ch08-E001 | [216](../verified/pages/pdf-216.md) | 例8.1第10次迭代数值 |
| ch08-E002 | [218](../verified/pages/pdf-218.md) | 式8.2.3求和下限 |
| ch09a-E001 | [234](../verified/pages/pdf-234.md) | 定理 9.3 证明不等式 |
| ch09a-E002 | [234](../verified/pages/pdf-234.md) | 定理 9.4 证明范数展开式 |
| ch09a-E003 | [235](../verified/pages/pdf-235.md) | 9.2.3 后 v_k 展开与 epsilon_k 定义 |
| ch09a-E004 | [236](../verified/pages/pdf-236.md) | 式 9.2.8 |
| ch09a-E005 | [237](../verified/pages/pdf-237.md) | 页首 u_k 展开第一行分子 |
| ch09a-E006 | [237](../verified/pages/pdf-237.md) | v_k 展开式分母 |
| ch09a-E007 | [238](../verified/pages/pdf-238.md) | 9.2.2 第一段 |
| ch09a-E008 | [244](../verified/pages/pdf-244.md) | 图 9.1 旁的 Householder 方法说明 |
| ch09a-E009 | [246](../verified/pages/pdf-246.md) | A_2 的二阶分块式右上块 |
| ch09a-E010 | [246](../verified/pages/pdf-246.md) | 式 9.3.2 的 sigma_k 与 rho_k |
| ch09b-E12 | [255](../verified/pages/pdf-255.md) | 分块上三角阵第一个二阶对角块原印 B_l，与末块同名；按顺序编号疑应为 B_1。已据交叉复核回看原图，保留原印并校注。 |
| ch09b-E11 | [252](../verified/pages/pdf-252.md) | 定理 9.16 证明首句原印由定理 9.12；所用平面旋转矩阵三角化结论对应定理 9.15，原引用保留。 |
| ch09b-E09 | [257](../verified/pages/pdf-257.md) | 第 i 次左变换原印及 v_k，对应矩阵为 v_i；保留原印下标。 |
| ch09b-E10 | [257](../verified/pages/pdf-257.md) | P_{i,i+1} 的范围原印 i=1,2,...,n+1，按 n 阶矩阵应至 n-1；保留原文。 |
| ch09b-E07 | [253](../verified/pages/pdf-253.md) | QR 分解左变换引用原印为定理 9.13，所指上三角阵结论对应定理 9.15；保留原文。 |
| ch09b-E08 | [254](../verified/pages/pdf-254.md) | 式（9.4.16）前原印引用式（4.15），本页对应为（9.4.15）；保留原文。 |
| ch09b-E04 | [251](../verified/pages/pdf-251.md) | 引理 1 证明首式末项原印 c alpha_i，按矩阵乘法及下一行疑应为 c alpha_j；保留原文。 |
| ch09b-E05 | [251](../verified/pages/pdf-251.md) | 定理 9.15 证明末行原印 a_{2j}^{(2)}，按第 2 列消元疑应为 a_{j2}^{(2)}；保留原文。 |
| ch09b-E06 | [251](../verified/pages/pdf-251.md) | 算法 1 零向量分支未赋值输出 v，按定义应为 0；原步骤保留。 |
| ch09b-E01 | [247](../verified/pages/pdf-247.md) | P^T y 展开式原印 lambda_k^{-1}，与初等反射阵使用 rho_k^{-1} 不一致；保留原文。 |
| ch09b-E02 | [248](../verified/pages/pdf-248.md) | 算法 3 步 3（2）第一个求和上限原印 n，按下三角存储算法疑应为 i；保留原文。 |
| ch09b-E03 | [249](../verified/pages/pdf-249.md) | 例 9.5（1）u_1 式原印 sigma_1 rho_1，结合列向量疑应为 sigma_1 e_1；保留原文。 |
| CH10-E001 | [271](../verified/pages/pdf-271.md) | {"lane": "ch10", "id": "CH10-E001", "pdf_page": 271, "printed_page": 258, "kind": "matrix_index", "status": "source_preserved_with_agent_note", "source_text": "两组未编号公式的第二式均含 H_{N/2}(N/2+i,j)", "analysis": "N/2 阶矩阵的行指标 N/2+i 超出本章 0 至 N/2-1 的范围。由定理 10.1，两处应为 H_{N/2}(i,j)。原文及式 (10.4.2) 均保留。", "evidence": "staging/ch10/assets/erratum-p271-indices.png"} |
| CH10-E002 | [270](../verified/pages/pdf-270.md) | {"lane": "ch10", "id": "CH10-E002", "pdf_page": 270, "printed_page": 257, "kind": "terminology", "status": "source_preserved_with_agent_note", "source_text": "Hadamard 阵是对称正交阵", "analysis": "按本章未归一化的定义，H_N^T H_N=N I，严格说 H_N/sqrt(N) 才是通常定义的正交矩阵。原文术语照录；其逆变换 1/N 因子正确。"} |
| CH10-E003 | [272](../verified/pages/pdf-272.md) | {"lane": "ch10", "id": "CH10-E003", "pdf_page": 272, "printed_page": 259, "kind": "duplicated_character", "status": "source_preserved_with_agent_note", "source_text": "使问题的的规模减半", "analysis": "原图重复的字已照录。"} |
| CH10-E004 | [274](../verified/pages/pdf-274.md) | {"lane": "ch10", "id": "CH10-E004", "pdf_page": 274, "printed_page": 261, "kind": "algorithm_index_range", "status": "source_preserved_with_agent_note", "formula_id": "10.4.4", "source_text": "l=1,2,...,2^k", "analysis": "算式按 (l-1)N_{k-1} 定位上一阶段的数据段，应有 l=1,...,2^{k-1}。原上限会令数据索引超出 0 至 N-1。前文描述第 k 阶段结果段数的 2^k 不需更改。算法 10.1 对此式的引用受同一范围疑误影响。", "evidence": "staging/ch10/assets/erratum-p274-range.png"} |
| CH11-E001 | [281](../verified/pages/pdf-281.md) | 原样保留；本节上下文应回引数列求和式（11.2.1）。 |
| CH11-E002 | [284](../verified/pages/pdf-284.md) | 并行向量含Nk个系数及xk共Nk+1个分量；在所述完全同步更新安排下疑漏计计算xk的一台。可能忽略常数项或依赖未说明调度；已保留原文并加限定校注。 |
| CH11-E003 | [287](../verified/pages/pdf-287.md) | 放大原图确认指数k+1；与同页推导一致的范围应为i=2^k,2^k+1,...,N-1。已保留原式并加校注。 |
| CH11-E004 | [289](../verified/pages/pdf-289.md) | 放大原图确认x_0；按奇偶拆分及该行后续下标疑应为x_1。已保留原文并加校注。 |
| CH11-E005 | [290](../verified/pages/pdf-290.md) | 分别疑应x_1,x_5,x_3,x_7,x_5；与明确标注的奇数相关链不一致。保留原式并加校注。 |
| CH11-E006 | [290, 291, 292] | 一般形式疑应11.4.1；小节疑应11.3.2；算法编号疑应11.5。原样保留。 |
| CH11-E007 | [291, 292] | 以i=1直接消元可见漏a1c0/b0及a1f0/b0；i=N-2对应漏右邻项。k=n分支重叠及越界。已原样保留并以推导作校注。 |
| CH11-E008 | [291](../verified/pages/pdf-291.md) | 该上界导致x_N、x_{N+1}越界并重复末行，疑应N/2-2。已照录。 |
| CH11-E009 | [291](../verified/pages/pdf-291.md) | 中心变元疑应x_i；放大原图确认x_0并保留。 |
| CH12-E001 | [294](../verified/pages/pdf-294.md) | 原图字形明确，语句疑有排印问题；保留原文，不擅自订正。 |
| CH12-E002 | [294, 302] | 同一阿尔·卡西结果前后不一致。90位精度mpmath计算π=3.141592653589793238...，支持PDF294的792为排印错误；两处均按原图保留。 |
| CH12-E003 | [302](../verified/pages/pdf-302.md) | 直径1时单边长为sin(π/n)，n倍为周长。原文“边长”保留，另加校注。 |
| CH12-E004 | [302, 304] | 本页原式Lhat_n=L_2n+(L_2n-L_n)/3；表12.4的Lhat_24576需要L_49152。独立数值检查确认表中值对应该原式。正文边数与其数据需求不一致，保留原文。 |
| CH12-E005 | [306](../verified/pages/pdf-306.md) | 额外实际打开PDF101（书页88）核实4.3为Romberg算法。这里松弛技术的章节指引疑有误；不擅自猜填正确章节。 |
| CH13-E001 | [307](../verified/pages/pdf-307.md) | 正文每秒 30 万亿次与原式分母 3×10^11 不一致；按原分母约 105.7 年，而原书印约 1 年。保留原文原式并单列校注。 |
| BACK-S001 | [318](../verified/pages/pdf-318.md) | 答案原图为y的n上标；原题明确给y_n=2^n并要求Δ^4y_n、δ^4y_n，故第一式索引与题目不一致。原答案上标保留。 |
| BACK-S002 | [318](../verified/pages/pdf-318.md) | 原答案清楚排为T_1，而原题明确给n=10，下标疑应T_10。原数值和下标仍忠实保留。 |
| BACK-S003 | [320](../verified/pages/pdf-320.md) | 原题明确给精确解(1/2,1,-1/2)^T及无穷范数误差<5e-6。三个原印向量误差∞范数依次为0.8999999、0.8999998、0.0000035；前两组不满足题意，第三组满足。前两组第二分量疑似小数点排印，原答案数字保留。 |
| BACK-S004 | [320](../verified/pages/pdf-320.md) | 原题方程组精确解为(-4,3,2)^T，答案第二、三分量0.2999989、0.2000003量级不符，疑似小数点排印。原答案数字仍保留。 |

机器可读完整记录见 [source-errata.json](source-errata.json)。每页的具体原式、修正推导、未能唯一恢复的原题条件等均在正文相邻校注中，不能只凭本表摘要计算。

转录纠错：独立复核发现的遗漏字、求和限、不恒等符号、矩阵下标与斜点等均在对应 staging/<lane>/cross-review.json 保留闭环记录；这些是转录问题，不归咎于原书。
