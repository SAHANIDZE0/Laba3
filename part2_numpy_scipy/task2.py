import numpy as np

def get_valid_input(prompt, check_func):
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                continue
            return check_func(user_input)
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")

def parse_array(s):
    arr = np.array([float(x) for x in s.split()])
    if len(arr) == 0:
        raise ValueError("Массив не может быть пустым")
    return arr

def parse_int(s):
    val = int(s)
    if val <= 0:
        raise ValueError("Значение должно быть положительным")
    return val

lengths = get_valid_input("Длины: ", parse_array)
speeds = get_valid_input("Скорости: ", parse_array)

if len(lengths) != len(speeds):
    raise ValueError("Количество длин и скоростей должно совпадать")

k = get_valid_input("k = ", parse_int)
p = get_valid_input("p = ", parse_int)

if k > p:
    raise ValueError("k не может быть больше p")
if k < 1 or p > len(lengths):
 raise ValueError("Номера участков вне диапазона")

t = get_valid_input("t = ", lambda x: float(x))

length_segment = np.sum(lengths[k-1:p])
times = lengths / speeds
time_segment = np.sum(times[k-1:p])
avg_speed = length_segment / time_segment

cum_times = np.cumsum(times)
if t > cum_times[-1]:
    raise ValueError("t больше общего времени в пути")

idx = np.searchsorted(cum_times, t)
if idx == 0:
    dist_from_start = t * speeds[0]
else:
    dist_from_start = (t - cum_times[idx-1]) * speeds[idx]

print(f"S = {length_segment:.0f} км, T = {time_segment:.2f} ч, V = {avg_speed:.2f} км/ч")
print(f"Через {t} ч автомобиль на участке {idx + 1}, в {dist_from_start:.1f} км от его начала")