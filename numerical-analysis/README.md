# 数值分析

教材整理在 [book/](book/README.md)：《数值分析》第 5 版的 Markdown + LaTeX、原页依据、章节索引与数学核验记录。

全书 322 个原扫描页的转录和 agent 独立交叉复核已记录；交付验收见 [STATUS.json](book/STATUS.json)，其中 `human_review: false`。检索入口为 [章节目录](book/index/INDEX.md)。

## 按章节做实验

| 章节与主题 | 实验 | 当前范围 |
| --- | --- | --- |
| §2.2 插值多项式 | [线性插值与正弦函数比较](code/ch02_interpolation/lagrange/README.md) | 使用两个节点计算、绘图并报告目标点误差；二次插值待扩展 |

在仓库根目录安装 `requirements.txt` 后运行：

```bash
.venv/bin/python numerical-analysis/code/ch02_interpolation/lagrange/run.py
```

本版 **2.2.1 是存在唯一性**；[2.2.2 是线性插值与抛物插值](book/verified/sections/2.2.2.md)。实验的正弦函数表值来自 [2.2.4 插值余项](book/verified/sections/2.2.4.md)中的例 2.1，公式位置和例题位置分别标注。

教材库还保留独立的[线性插值绘图验收入口](book/README.md#按章节交给-agent-使用)，其函数和节点是另选的演示；章节学习代码使用上述正弦例题。
