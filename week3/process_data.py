import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for charts
sns.set_theme(style="whitegrid")

# Path to the dataset (supports execution from root or week3 directory)
if os.path.exists("vidar_iocs_normalized.csv"):
    DATASET_PATH = "vidar_iocs_normalized.csv"
elif os.path.exists("data.csv"):
    DATASET_PATH = "data.csv"
elif os.path.exists("../vidar_iocs_normalized.csv"):
    DATASET_PATH = "../vidar_iocs_normalized.csv"
else:
    DATASET_PATH = "week3/vidar_iocs_normalized.csv"

if not os.path.exists(DATASET_PATH):
    print(f"[-] Error: Dataset not found at {DATASET_PATH}.")
    exit(1)

# 1. Load data
df = pd.read_csv(DATASET_PATH)

print("=== Initial Dataset Info ===")
print(df.info())

# 2. Clean column names and types
df.columns = df.columns.str.strip().str.lower()
df['ioc_type'] = df['ioc_type'].str.lower().str.strip()

# 3. Remove duplicates
initial_count = len(df)
df = df.drop_duplicates(subset=["value", "ioc_type"])
print(f"\n[+] Processed records: {len(df)} (Duplicates removed: {initial_count - len(df)})")

# 4. Print EDA metrics to console
print("\n=== IOC Type Distribution ===")
print(df["ioc_type"].value_counts())

print("\n=== Data Sources ===")
print(df["source"].value_counts())

print("\n=== Confidence Levels ===")
print(df["confidence"].value_counts())

# Determine correct paths for saving charts
is_week3_dir = os.path.basename(os.getcwd()) == "week3"
chart1_path = "ioc_distribution.png" if is_week3_dir else "week3/ioc_distribution.png"
chart2_path = "confidence_distribution.png" if is_week3_dir else "week3/confidence_distribution.png"

# 5. Generate first chart: IOC Breakdown by Type
plt.figure(figsize=(9, 5))
ax1 = sns.countplot(data=df, x='ioc_type', order=df['ioc_type'].value_counts().index, palette='crest')
plt.title('Vidar Stealer IOC Breakdown by Type', fontsize=12, fontweight='bold')
plt.xlabel('Indicator Type', fontsize=10)
plt.ylabel('Count', fontsize=10)
plt.xticks(rotation=45)

# Automatic Y-axis extension to prevent labels from clipping
max_y1 = df['ioc_type'].value_counts().max()
ax1.set_ylim(0, max_y1 * 1.15)

for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 6), textcoords='offset points')

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"[+] First chart successfully saved to {chart1_path}")

# 6. Generate second chart: Distribution by Confidence Level
plt.figure(figsize=(8, 5))
order_conf = ['high', 'medium', 'low']
ax2 = sns.countplot(data=df, x='confidence', order=order_conf, palette='magma')
plt.title('Vidar Stealer IOC Distribution by Confidence Level', fontsize=12, fontweight='bold')
plt.xlabel('Confidence Level', fontsize=10)
plt.ylabel('Count', fontsize=10)

# Automatic Y-axis extension for the second chart
max_y2 = df['confidence'].value_counts().max()
ax2.set_ylim(0, max_y2 * 1.15)

for p in ax2.patches:
    ax2.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', xytext=(0, 6), textcoords='offset points')

plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"[+] Second chart successfully saved to {chart2_path}")

print("\n[+] Data processing complete. Both charts generated successfully.")