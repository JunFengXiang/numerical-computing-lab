import matplotlib.pyplot as plt
def plot_interpolation(x_plot, y_plot, x_nodes, y_nodes,y_true):
    fig, ax = plt.subplots(figsize = (8,5))
    #蓝色实线:线性插值
    ax.plot(
        x_plot,
        y_plot,
        color = "blue",
        label = "Linear interpolation"
    )

    #橙色虚线: 原函数sin(x)
    ax.plot(
        x_plot,
        y_true,
        color = "orange",
        linestyle = "--",
        label = "sin(x)"
    )

    #红色散点：参与插值的两个已知节点
    ax.scatter(
        x_nodes, y_nodes,
        color = "red",
        label = "Nodes",
        zorder = 3
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    plt.show()
