import numpy as np

A = np.array([
    [4, -1.5, 2, 0.5],
    [1, 5, -2, 1.2],
    [-2, 1, 6, -1],
    [0.5, 2, -1, 7]
], dtype=float)

B = np.array([11.05, -6.82, 11.5, -0.5], dtype=float)

det_A = np.linalg.det(A)
print(f"Определитель: {det_A:.3f}")

cond_A = np.linalg.cond(A)
print(f"Число обусловленности: {cond_A:.3f}")

X_inv = np.linalg.inv(A) @ B
X_solve = np.linalg.solve(A, B)

print(f"Решение через обратную матрицу: {X_inv}")
print(f"Решение через solve: {X_solve}")

diff_norm = np.linalg.norm(X_inv - X_solve)
print(f"Норма разности: {diff_norm}")

residual = np.linalg.norm(A @ X_inv - B)
print(f"Проверка подстановкой: {residual}")

print(f"Округленный ответ: {np.round(X_inv, 1)}")