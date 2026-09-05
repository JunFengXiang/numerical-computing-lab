# Numerical Computing Lab

数值方向课程的学习仓库：保存讲义，整理笔记和作业，用 Python 做小实验，逐步积累与深度学习相关的问题。

## 从这里开始

| 目录 | 内容 |
| --- | --- |
| [linear-algebra](linear-algebra/README.md) | 数值线性代数；已整理上传的资料，并提供第 1、2 讲的笔记起点与实验 |
| [numerical-analysis](numerical-analysis/README.md) | 数值分析；随课程逐章添加 |
| [differential-equations](differential-equations/README.md) | 微分方程数值解；后续课程使用 |
| [experiments](experiments/README.md) | 跨课程及与深度学习相关的小实验 |

## 运行现有实验

使用 Python 3.11 或以上版本，在仓库根目录执行：

```bash
python -m pip install -r requirements.txt
python linear-algebra/01-matvec/lab.py
python linear-algebra/02-orthogonal/lab.py
```

目前只需要 NumPy，不需要 GPU。实验使用 float64；复数部分使用 complex128。

## 每讲怎么用

每讲只有三个文件：`notes.md` 记理解，`homework.md` 写作业和订正，`lab.py` 做数值实验。

先自己推导和完成作业，再运行实验核对。现有笔记和代码是学习起点；作业文件保留待填写，学习进度由自己记录。

原始 HTML、PDF 放在课程的 `materials/` 中。HTML 下载到电脑后用浏览器打开。

新增一讲时，新建如 `03-norms/` 的目录，沿用上面三个文件名；需要图像时再加绘图代码。用到 SciPy、Matplotlib 或 PyTorch 时，再把相应依赖加入 `requirements.txt`。

## 保存进度

建议完成一讲或一个小实验就提交一次，例如“完成第 1 讲作业与验证”。大批临时输出放进 `outputs/`，它已被 Git 忽略；重要的小图和结论放回对应章节。

初期建议使用私有仓库。资料按上传时的原文件保存，相关来源见[数值线性代数目录](linear-algebra/README.md)。
