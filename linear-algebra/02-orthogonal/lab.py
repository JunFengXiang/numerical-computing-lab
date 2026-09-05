"""第 2 讲小实验。运行：python linear-algebra/02-orthogonal/lab.py"""

import numpy as np


def main():
    np.set_printoptions(precision=6, suppress=True)
    print(f"NumPy {np.__version__}；实数用 float64，复数用 complex128")

    # 一个二维子空间，嵌在三维空间中。
    q1 = np.array([1, 1, 0], dtype=np.float64) / np.sqrt(2)
    q2 = np.array([0, 0, 1], dtype=np.float64)
    Q = np.column_stack([q1, q2])
    v = np.array([3, 1, 2], dtype=np.float64)
    projection = Q @ (Q.conj().T @ v)
    residual = v - projection

    np.testing.assert_allclose(Q.conj().T @ Q, np.eye(2), atol=1e-12)
    np.testing.assert_allclose(projection, [2, 2, 2], atol=1e-12)
    np.testing.assert_allclose(residual, [1, -1, 0], atol=1e-12)
    np.testing.assert_allclose(Q.conj().T @ residual, np.zeros(2), atol=1e-12)
    np.testing.assert_allclose(np.linalg.norm(v)**2,
                               np.linalg.norm(projection)**2 + np.linalg.norm(residual)**2,
                               atol=1e-12)

    print("\n原向量 v：", v)
    print("投影 p：", projection)
    print("残差 r = v - p：", residual)
    print(f"残差的长度：{np.linalg.norm(residual):.6f}")
    print(f"残差正交性误差 ||Q* r||：{np.linalg.norm(Q.conj().T @ residual):.3e}")

    # 复数内积：第一个向量需要取共轭。
    q = np.array([1, 1j], dtype=np.complex128) / np.sqrt(2)
    z = np.array([2, 1], dtype=np.complex128)
    complex_projection = q * np.vdot(q, z)
    complex_residual = z - complex_projection
    np.testing.assert_allclose(np.vdot(q, q), 1, atol=1e-12)
    np.testing.assert_allclose(np.vdot(q, complex_residual), 0, atol=1e-12)
    print("\n复向量 q 的普通点积 q @ q：", q @ q)
    print("复向量 q 的内积 np.vdot(q, q)：", np.vdot(q, q))
    print(f"复数残差正交性误差：{abs(np.vdot(q, complex_residual)):.3e}")
    print("\n以上数值验证均通过。")


if __name__ == "__main__":
    main()
