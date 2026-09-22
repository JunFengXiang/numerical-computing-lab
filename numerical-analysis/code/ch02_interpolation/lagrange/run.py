import numpy as np
from lagrange import linear_interpolation
from plotting import plot_interpolation
x_nodes = np.array([0.32,0.34,0.36])
y_nodes = np.array([0.314567, 0.333487, 0.352274])

x_target = 0.3367

print(x_nodes)
print(y_nodes)
print(x_target)

value = linear_interpolation(
    x_target,
    x_nodes[0], x_nodes[1],
    y_nodes[0], y_nodes[1]
)

print(f"线性插值结果: {value:.7f}")
reference = np.sin(x_target)
print(f"sin(x) 参考值: {reference:.10f}")
print(f"绝对误差: {abs(value - reference):.10e}")


#在两个插值节点之间， 生成200个绘图位置
x_plot = np.linspace(x_nodes[0],x_nodes[1],200)
y_plot = linear_interpolation(
    x_plot,
    x_nodes[0], x_nodes[1],
    y_nodes[0], y_nodes[1]
)

#画插值直线和参与计算的两个节点
y_true = np.sin(x_plot)

plot_interpolation(
    x_plot,
    y_plot,
    x_nodes[:2],
    y_nodes[:2],
    y_true
)
