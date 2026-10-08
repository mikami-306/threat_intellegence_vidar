import os
import pandas as pd
import matplotlib.pyplot as plt

# Путь к датасету
DATASET_PATH = "data.csv" if os.path.exists("data.csv") else "../data.csv"

if not os.path.exists(DATASET_PATH):
    print(f"[-] Ошибка: {DATASET_PATH} не найден.")
    exit(1)

df = pd.read_csv(DATASET_PATH)

print("=== Исходный датасет ===")
print(df.info())

# 1. Очистка наименований колонок
df.columns = df.columns.str.strip().str.lower()

# 2. Удаление дубликатов
initial_count = len(df)
df = df.drop_duplicates(subset=["value", "ioc_type"])
print(f"\n[+] Обработано записей: {len(df)} (Удалено дубликатов: {initial_count - len(df)})")

# 3. Вывод метрик EDA
print("\n=== Распределение по типам IOC ===")
print(df["ioc_type"].value_counts())

print("\n=== Источники данных ===")
print(df["source"].value_counts())

# 4. Сохранение графика
plt.figure(figsize=(9, 5))
df["ioc_type"].value_counts().plot(kind="bar", color="#2b5c8f", edgecolor="black")
plt.title("Vidar Stealer IOC Breakdown by Type")
plt.xlabel("Indicator Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

chart_path = "ioc_distribution.png" if os.path.basename(os.getcwd()) == "week3" else "week3/ioc_distribution.png"
plt.savefig(chart_path)
print(f"[+] График сохранен в {chart_path}")