import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

db_path = '/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite'
try:
    conn = sqlite3.connect(db_path)
except Exception as e:
    print(f"Error connecting to the database at {db_path}: {e}")
    exit()

# fetch data
query = "SELECT * FROM Earnings"
try:
    df_earnings = pd.read_sql(query, conn)
except Exception as e:
    print(f"Error executing query: {e}")
    conn.close()
    exit()

conn.close()

if df_earnings.empty:
    print("DataFrame is empty. Exiting.")
    exit()

# print df columns
print("DataFrame Columns:")
print(df_earnings.columns)

# average AR for each AR_number, grouped by SURPRISE
ar_columns = [f"AR_{i}" for i in range(-12, 61)]

# check if all ar_columns exist in DataFrame
missing_columns = set(ar_columns) - set(df_earnings.columns)
if missing_columns:
    print(f"Missing columns: {missing_columns}")
    exit()

ar_averages = df_earnings.groupby('SURPRISE')[ar_columns].mean().T
ar_averages.index = ar_averages.index.str.extract('([-\d]+)').astype(int)
ar_averages.sort_index(inplace=True)

# the cumulative average AR (CAR) for each group
car_averages = ar_averages.cumsum()

# plotting
plt.figure(figsize=(10, 6))
marker_shapes = {-1: 's', 0: 'o', 1: '^'}
legend_labels = {-1: 'Negative Surprise', 0: 'No Significant Surprise', 1: 'Positive Surprise'}

for surprise, shape in marker_shapes.items():
    plt.plot(car_averages.index[::4], car_averages[surprise][::4], marker=shape, linestyle='-', markersize=8, label=legend_labels[surprise])

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xticks(car_averages.index[::4], car_averages.index[::4])
plt.xlabel('Event Time (Days)')
plt.ylabel('Cumulative Average Abnormal Return (CAR)')
plt.legend(loc='lower left')
plt.title('Cumulative Average Abnormal Returns over Event Time by SURPRISE Category')

plt.savefig('CAR_over_Event_Time_by_SURPRISE.png', dpi=300)

plt.show()
