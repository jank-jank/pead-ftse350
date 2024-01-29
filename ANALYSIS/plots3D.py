import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# define AR columns
ar_columns = [f"AR_n{i}" for i in range(12, 0, -1)] + ["AR_p0"] + [f"AR_p{i}" for i in range(1, 61)]

# fetch data
query = "SELECT SUE, [Surprise%], " + ", ".join(ar_columns) + " FROM Earnings"
df = pd.read_sql(query, conn)

conn.close()

# new DataFrame for the surface plot
surface_df = pd.DataFrame(columns=['SUE', 'Surprise%'] + ar_columns)

# surface DataFrame -> average AR values for each unique combination of SUE and Surprise%
for _, group_df in df.groupby(['SUE', 'Surprise%']):
    avg_ar_values = group_df[ar_columns].mean().tolist()
    surface_df = surface_df.append({'SUE': group_df['SUE'].iloc[0], 'Surprise%': group_df['Surprise%'].iloc[0], **dict(zip(ar_columns, avg_ar_values))}, ignore_index=True)

# 3D plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# grid for SUE, Surprise%, and AR
sue = surface_df['SUE'].unique()
surprise = surface_df['Surprise%'].unique()
ar = np.arange(len(ar_columns))
sue, surprise, ar = np.meshgrid(sue, surprise, ar, indexing='ij')

# single surface plot
z = np.array(surface_df[ar_columns].T)
ax.plot_surface(ar, sue, surprise, facecolors=cm.coolwarm(z), rstride=1, cstride=1, shade=False, alpha=0.5)

ax.set_xlabel('AR')
ax.set_ylabel('SUE')
ax.set_zlabel('Surprise%')
ax.set_xticks(range(len(ar_columns)))
ax.set_xticklabels(ar_columns, rotation=90)

# static plot
plt.show()
