import pandas as pd
import numpy as np
import argparse
import sys
import os
from datetime import date, timedelta
from faker import Faker

class InvalidConfigError(Exception):
    pass

def generate_sales_data(seed: int, years: int, stores_count: int, output_file: str):
    """Генерирует синтетические данные о продажах и сохраняет их в CSV."""
    if years <= 0:
        raise InvalidConfigError("Количество лет должно быть положительным")
    if stores_count < 5:
        raise InvalidConfigError("Количество магазинов должно быть не менее 5")
    if not output_file:
        raise InvalidConfigError("Имя файла не может быть пустым")

    np.random.seed(seed)
    fake = Faker('ru_RU')
    Faker.seed(seed)

    end_date = date.today()
    start_date = end_date - timedelta(days=365 * years)
    dates = pd.date_range(start_date, end_date, freq='D')

    cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород']
    stores = [{'store_id': i+1, 'city': np.random.choice(cities)} for i in range(stores_count)]
    
    categories = {
        'Электроника': ['Смартфон', 'Ноутбук', 'Наушники'],
        'Одежда': ['Футболка', 'Джинсы', 'Куртка'],
        'Продукты': ['Хлеб', 'Молоко', 'Сыр']
    }
    
    rows = []
    for d in dates:
        is_weekend = d.weekday() >= 5
        month = d.month
        
        for store in stores:
            for category, products in categories.items():
                for product in products:
                    base_price = np.random.uniform(500, 50000)
                    
                    seasonal_mult = 1.0
                    if category == 'Электроника' and month in [11, 12]:
                        seasonal_mult = 1.5
                    elif category == 'Одежда' and month in [3, 4, 9, 10]:
                        seasonal_mult = 1.3
                    
                    weekend_mult = 1.2 if is_weekend else 1.0
                    
                    trend = 1.0 + (d.date() - start_date).days / (365 * years) * np.random.uniform(-0.2, 0.3)
                    
                    promo = 1 if np.random.rand() < 0.1 else 0
                    promo_mult = 1.8 if promo else 1.0
                    
                    qty = int(np.random.poisson(5) * weekend_mult * promo_mult)
                    if qty == 0:
                        continue
                        
                    price = round(base_price * seasonal_mult * trend * np.random.uniform(0.9, 1.1), 2)
                    cost = round(price * np.random.uniform(0.5, 0.8), 2)
                    
                    if np.random.rand() < 0.005:
                        price = np.nan
                    
                    payment = np.random.choice(['наличные', 'карта', 'онлайн'])
                    if np.random.rand() < 0.005:
                        payment = np.nan
                        
                    rows.append({
                        'date': d.strftime('%Y-%m-%d'),
                        'store_id': store['store_id'],
                        'city': store['city'],
                        'category': category,
                        'product': product,
                        'qty': qty,
                        'price': price,
                        'cost': cost,
                        'promo': promo,
                        'payment_method': payment
                    })

    df = pd.DataFrame(rows)
    
    anomaly_indices = df.sample(frac=0.01).index
    df.loc[anomaly_indices, 'qty'] = df.loc[anomaly_indices, 'qty'] * 10
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Успешно сгенерировано {len(df)} строк. Сохранено в {output_file}")
    except Exception as e:
        raise IOError(f"Не удалось сохранить файл: {e}")

def main():
    parser = argparse.ArgumentParser(description="Генератор синтетических данных о продажах")
    parser.add_argument("--seed", type=int, default=42, help="Сид для воспроизводимости")
    parser.add_argument("--years", type=int, default=3, help="Количество лет")
    parser.add_argument("--stores", type=int, default=5, help="Количество магазинов")
    parser.add_argument("--out", type=str, default="data/sales.csv", help="Путь к файлу")
    
    args = parser.parse_args()
    
    try:
        generate_sales_data(args.seed, args.years, args.stores, args.out)
    except InvalidConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка ввода-вывода: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Неизвестная ошибка: {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()