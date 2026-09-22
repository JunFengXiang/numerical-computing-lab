# 数值计算实验室 · Numerical Computing Lab

**从数学推导到可复现的 Python 实验。**

围绕数值线性代数、数值分析与微分方程数值解，整理课程资料、学习笔记和算法实现。每个实验尽量回答三个问题：算法为什么成立，计算误差有多大，怎样用代码验证。

## 课程与当前进度

| 方向 | 已有内容 | 入口 |
| --- | --- | --- |
| 数值线性代数 | 第 1–5 讲资料；第 1、2 讲笔记、作业模板与 NumPy 实验 | [课程目录](linear-algebra/README.md) |
| 数值分析 | 教材转录、章节与公式索引；两节点线性插值实验 | [教材与实验](numerical-analysis/README.md) |
| 微分方程数值解 | 已建立课程入口，具体实验待开展 | [课程目录](differential-equations/README.md) |
| 跨课程探索 | 条件数、低秩近似、精度比较与 PDE 求解的候选问题 | [实验路线](experiments/README.md) |

教材整理、代码验证和个人学习进度分别记录。现有作业文件仍是待填写模板；研究路线中的问题尚未形成实验结论。

## 快速开始

建议使用 Python 3.12 或更新版本。以下为 macOS / Linux 命令：

```bash
git clone https://github.com/JunFengXiang/numerical-computing-lab.git
cd numerical-computing-lab
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# 矩阵与向量相乘
.venv/bin/python linear-algebra/01-matvec/lab.py

# 正交投影与复数内积
.venv/bin/python linear-algebra/02-orthogonal/lab.py

# 线性插值：数值结果与函数曲线
.venv/bin/python numerical-analysis/code/ch02_interpolation/lagrange/run.py
```

Windows 创建环境后，将 `.venv/bin/python` 换成 `.venv\Scripts\python.exe`。在 VS Code 中也选择该环境的 Python 解释器。

当前三个实验使用 NumPy 和 Matplotlib，均可在 CPU 上运行。实数使用 `float64`，复数使用 `complex128`。插值程序会打开绘图窗口；无图形界面时，可在命令前加 `MPLBACKEND=Agg`，仅检查数值输出。

本次验证环境：Python 3.14.4、NumPy 2.5.3、Matplotlib 3.11.2（2026-09-22）。教材转录与 LaTeX 编译另见[教材环境说明](numerical-analysis/book/README.md#编译与运行环境)。

## 可以复现什么

| 实验 | 核心问题 | 当前例子的结果 |
| --- | --- | --- |
| [矩阵与向量相乘](linear-algebra/01-matvec/lab.py) | 按行计算、列的线性组合与 `A @ x` 是否一致？ | 三种方式均得到 `[0, 7, -4]` |
| [正交投影](linear-algebra/02-orthogonal/lab.py) | 投影后的残差是否与子空间正交？ | 投影为 `[2, 2, 2]`，残差为 `[1, -1, 0]`；包含正交性断言 |
| [线性插值](numerical-analysis/code/ch02_interpolation/lagrange/README.md) | 用两个表值近似 `sin(0.3367)`，误差有多大？ | 插值值 `0.3303652`，相对 `numpy.sin` 参考值的绝对误差约 `8.9916 × 10⁻⁶` |

插值实验使用教材给出的有限精度表值，误差包含表值舍入的影响。第三个节点保留供后续二次插值使用，当前程序只使用前两个节点。

## 怎样记录一个实验

数值线性代数沿用 `notes.md`、`homework.md`、`lab.py`；数值分析代码按章节放在 `numerical-analysis/code/`，较长的实验再拆分计算、绘图和运行入口。

每个实验的说明写清以下内容：

1. **问题与原理**：对应课程章节、算法公式和适用条件。
2. **输入与环境**：数据来源、节点或矩阵、数值精度；随机实验记录种子。
3. **运行与结果**：可直接执行的命令、参考解、误差或残差。
4. **观察与限制**：解释现象，记录未完成部分和下一步问题。

临时输出放入已被 Git 忽略的 `outputs/`；需要长期保留的小图和结果放回对应实验目录。完成一个独立实验后再提交，提交信息描述具体内容。

## 接下来做什么

- 扩展三节点二次插值，比较节点选择与误差。
- 比较不同条件数下的线性方程组残差与解误差。
- 从具有已知解的 Poisson 问题开始，验证离散误差、网格收敛和 CG / PCG 求解。
- 在数值基线稳定后，再评估预条件器复用与学习方法能否降低总求解成本。

以上为待开展的路线，进度以对应代码、运行结果和说明为准。

## 教材与资料来源

数值线性代数参考 Trefethen 与 Bau 的《Numerical Linear Algebra》；数值分析参考李庆扬、王能超、易大义《数值分析》第 5 版。资料入口见各课程目录。

数值分析教材已整理为覆盖 322 个原扫描页的转录与索引，范围和核验记录见 [STATUS.json](numerical-analysis/book/STATUS.json)。记录中的校核由 agent 完成，`human_review: false`；使用公式或例题时，应结合原页和[校注](numerical-analysis/book/quality/ERRATA.md)回查。
