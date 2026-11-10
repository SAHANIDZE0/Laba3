import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

sns.set_theme(style="whitegrid")
df = pd.read_csv('data/sales.csv')
df['date'] = pd.to_datetime(df['date'])
df['revenue'] = df['qty'] * df['price']
df['month'] = df['date'].dt.to_period('M').astype(str)
df['day_of_week'] = df['date'].dt.day_name()

plt.figure(figsize=(12, 5))
monthly_rev = df.groupby('month')['revenue'].sum().reset_index()
sns.lineplot(data=monthly_rev, x='month', y='revenue', marker='o')
plt.title('Общая динамика выручки по месяцам')
plt.xticks(rotation=45)
plt.show()

avg_price = df.groupby(['month', 'category'])['price'].mean().reset_index()
fig = px.line(avg_price, x='month', y='price', color='category', title='Динамика средней цены по категориям')
fig.show()

plt.figure(figsize=(10, 5))
city_sales = df.groupby('city')['qty'].sum().sort_values()
city_sales.plot(kind='barh', color='skyblue')
plt.title('Объем продаж по городам')
plt.show()

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x='day_of_week', y='qty', order=days_order, color='lightgreen')
plt.title('Распределение продаж по дням недели')
plt.show()

payment_counts = df['payment_method'].value_counts().reset_index()
payment_counts.columns = ['payment_method', 'count']
fig = px.pie(payment_counts, names='payment_method', values='count', title='Структура способов оплаты')
fig.show()

plt.figure(figsize=(6, 4))
promo_sales = df.groupby('promo')['qty'].mean().reset_index()
plt.bar(['Без акции', 'С акцией'], promo_sales['qty'], color=['gray', 'orange'])
plt.title('Средний объем продаж: до/во время акции')
plt.show()