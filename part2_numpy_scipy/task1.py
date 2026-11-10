import numpy as np

expenses = np.array([3200, 3100, 2600, 1900, 1500, 1300, 1250, 1400, 1800, 2300, 2900, 3500])

winter_indices = [11, 0, 1]
summer_indices = [5, 6, 7]

winter_sum = np.sum(expenses[winter_indices])
summer_sum = np.sum(expenses[summer_indices])

print(f"Зима: {winter_sum}, лето: {summer_sum} -> {'больше тратится зимой' if winter_sum > summer_sum else 'больше тратится летом'}")

max_val = np.max(expenses)
max_months = np.where(expenses == max_val)[0] + 1
print(f"Максимум ({max_val}) в месяцах: {', '.join(map(str, max_months))}")