"""第 1 讲小实验。运行：python linear-algebra/01-matvec/lab.py"""

import numpy as np


def main():
    np.set_printoptions(precision=6, suppress=True)
    print(f"NumPy {np.__version__}；本实验使用 float64")

    # 1. 同一个矩阵乘法：逐行计算、各列的线性组合、NumPy。
    A = np.array([[1, 2], [3, -1], [0, 4]], dtype=np.float64)
    x = np.array([2, -1], dtype=np.float64)
    by_rows = np.array([sum(A[i, j] * x[j] for j in range(A.shape[1]))
                        for i in range(A.shape[0])])
    by_columns = np.zeros(A.shape[0], dtype=np.float64)
    for j in range(A.shape[1]):
        by_columns += x[j] * A[:, j]
    reference = A @ x
    np.testing.assert_allclose(by_rows, reference, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(by_columns, reference, rtol=1e-12, atol=1e-12)
    print("\n逐行计算：", by_rows)
    print("各列的线性组合：", by_columns)
    print("A @ x：", reference)

    # 2. 左乘改变行，右乘改变列。这里只演示单个操作。
    B = np.arange(1, 17, dtype=np.float64).reshape(4, 4)
    row_scale = np.eye(4)
    row_scale[2, 2] = 2  # 数学上的第 3 行，代码下标为 2。
    column_scale = np.eye(4)
    column_scale[0, 0] = 2
    expected_rows = B.copy()
    expected_rows[2, :] *= 2
    expected_columns = B.copy()
    expected_columns[:, 0] *= 2
    np.testing.assert_allclose(row_scale @ B, expected_rows)
    np.testing.assert_allclose(B @ column_scale, expected_columns)
    print("\n原矩阵 B：\n", B)
    print("第 3 行乘以 2，左乘：\n", row_scale @ B)
    print("第 1 列乘以 2，右乘：\n", B @ column_scale)

    # 3. 范德蒙矩阵：列依次是 1、t、t^2 在采样点上的取值。
    nodes = np.array([-1, 0, 2], dtype=np.float64)
    coefficients = np.array([1, -2, 3], dtype=np.float64)
    V = np.vander(nodes, N=3, increasing=True)
    direct_values = 1 - 2 * nodes + 3 * nodes**2
    np.testing.assert_allclose(V @ coefficients, direct_values)
    print("\n范德蒙矩阵 V：\n", V)
    print("p(t) = 1 - 2t + 3t^2 的采样值：", V @ coefficients)
    print("\n以上数值验证均通过。可以修改矩阵和系数，再观察结果。")


if __name__ == "__main__":
    main()
