import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Установка темы для графиков
sns.set_theme(style="whitegrid")

# Путь к датасету (поддерживает запуск как из корня, так и из папки week3)
if os.path.exists("vidar_iocs_normalized.csv"):
    DATASET_PATH = "vidar_iocs_normalized.csv"
elif os.path.exists("data.csv"):
    DATASET_PATH = "data.csv"
elif os.path.exists("../vidar_iocs_normalized.csv"):
    DATASET_PATH = "../vidar_iocs_normalized.csv"
else:
    DATASET_PATH = "week3/vidar_iocs_normalized.csv"

if not os.path.exists(DATASET_PATH):
    print(f"[-] Ошибка: Датасет не найден.")
    exit(1)

# 1. Загрузка данных
df = pd.read_csv(DATASET_PATH)

print("=== Исходный датасет ===")
print(df.info())

# 2. Очистка наименований колонок и типов
df.columns = df.columns.str.strip().str.lower()
df['ioc_type'] = df['ioc_type'].str.lower().str.strip()

# 3. Удаление дубликатов
initial_count = len(df)
df = df.drop_duplicates(subset=["value", "ioc_type"])
print(f"\n[+] Обработано записей: {len(df)} (Удалено дубликатов: {initial_count - len(df)})")

# 4. Вывод метрик EDA в консоль
print("\n=== Распределение по типам IOC ===")
print(df["ioc_type"].value_counts())

print("\n=== Источники данных ===")
print(df["source"].value_counts())

print("\n=== Уровни доверия (Confidence Level) ===")
print(df["confidence"].value_counts())

# Определяем правильный путь для сохранения графиков (в зависимости от того, где запущен скрипт)
is_week3_dir = os.path.basename(os.getcwd()) == "week3"
chart1_path = "ioc_distribution.png" if is_week3_dir else "week3/ioc_distribution.png"
chart2_path = "confidence_distribution.png" if is_week3_dir else "week3/confidence_distribution.png"

# 5. Генерация первого графика: Распределение по типам IoC
plt.figure(figsize=(9, 5))
ax1 = sns.countplot(data=df, x='ioc_type', order=df['ioc_type'].value_counts().index, palette='crest')
plt.title('Vidar Stealer IOC Breakdown by Type', fontsize=12, fontweight='bold')
plt.xlabel('Indicator Type', fontsize=10)
plt.ylabel('Count', fontsize=10)
plt.xticks(rotation=45)

for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"[+] Первый график сохранен в {chart1_path}")

# 6. Генерация второго графика: Распределение по уровню доверия (Confidence Level)
plt.figure(figsize=(8, 5))
order_conf = ['high', 'medium', 'low']
ax2 = sns.countplot(data=df, x='confidence', order=order_conf, palette='magma')
plt.title('Vidar Stealer IOC Distribution by Confidence Level', fontsize=12, fontweight='bold')
plt.xlabel('Confidence Level', fontsize=10)
plt.ylabel('Count', fontsize=10)

for p in ax2.patches:
    ax2.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 5), textcoords='offset points')

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"[+] Второй график сохранен в {chart2_path}")

print("\n[+] Data processing complete. Both charts generated successfully.")