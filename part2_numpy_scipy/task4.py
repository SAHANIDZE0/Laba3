import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import os

os.makedirs('img', exist_ok=True)

f = lambda x: x * np.sin(x)
val_quad, err_quad = integrate.quad(f, 0, np.pi)
exact_single = np.pi
print(f"Однократный интеграл: {val_quad:.5f}, аналитика: {exact_single:.5f}, погрешность: {abs(val_quad - exact_single):.5e}")

f_double = lambda y, x: x + y
val_dbl, err_dbl = integrate.dblquad(f_double, 0, 1, lambda x: 0, lambda x: x)
exact_double = 0.5
print(f"Двойной интеграл: {val_dbl:.5f}, аналитика: {exact_double:.5f}, погрешность: {abs(val_dbl - exact_double):.5e}")

N_values = [10**3, 10**4, 10**5, 10**6]
errors = []

for N in N_values:
    x_rand = np.random.uniform(0, 1, N)
    y_rand = np.random.uniform(0, x_rand, N)
    mc_estimate = np.mean(x_rand + y_rand)
    errors.append(abs(mc_estimate - exact_double))

plt.figure(figsize=(8, 5))
plt.plot(N_values, errors, marker='o')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('N')
plt.ylabel('Погрешность')
plt.title('Метод Монте-Карло')
plt.grid(True, which="both", ls="--")
plt.savefig('img/monte_carlo.png')
plt.show()