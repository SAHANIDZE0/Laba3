import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial
import os

os.makedirs('img', exist_ok=True)

# 1. Загрузка данных (создаем тестовые, если файла нет)
try:
    df = pd.read_csv('../part3_synthetic_data/data/sales.csv')
    print("Данные успешно загружены из Части 3.")
except FileNotFoundError:
    print("Файл из Части 3 не найден. Генерируем синтетические данные...")
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    np.random.seed(42)
    df = pd.DataFrame({
        'date': np.random.choice(dates, 1000),
        'category': np.random.choice(['Электроника', 'Одежда', 'Продукты'], 1000),
        'qty': np.random.randint(1, 10, 1000),
        'price': np.random.uniform(100, 5000, 1000)
    })

# Убедимся, что дата в правильном формате
df['date'] = pd.to_datetime(df['date'])
df['revenue'] = df['qty'] * df['price']

df['date'] = pd.to_datetime(df['date'])
df['revenue'] = df['qty'] * df['price']

# 2. Агрегация по неделям для каждой категории
df['week'] = df['date'].dt.to_period('W').dt.start_time

# Создаем сводную таблицу: строки - недели, столбцы - категории
weekly_sales = df.pivot_table(index='week', columns='category', values='revenue', aggfunc='sum').fillna(0)

# 3. Разделение на Train и Test (последние 8 недель - тест)
test_size = 8
train = weekly_sales.iloc[:-test_size]
test = weekly_sales.iloc[-test_size:]

print(f"Данные разделены: Обучение - {len(train)} недель, Тест - {len(test)} недель.")

# 4. Прогнозирование и графики
categories = weekly_sales.columns

for cat in categories:
    sales = train[cat]
    actual = test[cat]
    
    # Метод 1: Скользящее среднее (прогноз на основе среднего за последние 4 недели)
    # Берем последнее известное значение среднего и переносим его на все 8 недель теста
    ma_forecast_value = sales.rolling(window=4).mean().iloc[-1]
    ma_forecast = np.full(len(actual), ma_forecast_value)
    
    # Метод 2: Линейный тренд
    x_train = np.arange(len(sales))
    coeffs = np.polyfit(x_train, sales, deg=1)
    
    # Экстраполируем на 8 недель вперед
    x_test = np.arange(len(sales), len(sales) + len(actual))
    trend_forecast = np.polyval(coeffs, x_test)
    
    # 5. Вычисление метрики качества MAE
    mae_ma = np.mean(np.abs(actual - ma_forecast))
    mae_trend = np.mean(np.abs(actual - trend_forecast))
    
    print(f"\n--- Категория: {cat} ---")
    print(f"MAE (Скользящее среднее): {mae_ma:.2f}")
    print(f"MAE (Линейный тренд): {mae_trend:.2f}")
    
    # 6. Построение графика «Факт vs Прогноз»
    plt.figure(figsize=(10, 5))
    plt.plot(sales.index, sales.values, label='История (Train)', color='blue')
    plt.plot(actual.index, actual.values, label='Факт (Test)', color='green', marker='o')
    plt.plot(actual.index, ma_forecast, label='Прогноз (Скользящее среднее)', color='orange', linestyle='--')
    plt.plot(actual.index, trend_forecast, label='Прогноз (Линейный тренд)', color='red', linestyle='-.')
    
    plt.title(f'Факт vs Прогноз: {cat}')
    plt.xlabel('Дата')
    plt.ylabel('Выручка')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Сохраняем график в папку img
    filename = f"img/forecast_{cat.replace(' ', '_')}.png"
    plt.savefig(filename)
    plt.close()

print("\nАнализ завершен. Графики сохранены в папку img.")