import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# read EarningsREF table into DataFrame
df = pd.read_sql_query("SELECT * FROM EarningsREF", conn)

conn.close()

sns.set(style="whitegrid")

# figure and a grid of subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12))

# annotate summary statistics
def annotate_stats(ax, series):
    stats = series.describe()
    stats_text = f"""Count: {int(stats['count'])}
Mean: {stats['mean']:.3f}
Std Dev: {stats['std']:.3f}
Min: {stats['min']:.3f}
25th: {stats['25%']:.3f}
Median: {stats['50%']:.3f}
75th: {stats['75%']:.3f}
Max: {stats['max']:.3f}"""
    ax.annotate(stats_text, xy=(0.7, 0.5), xycoords='axes fraction')

# histograms
sns.histplot(df['ForecastedEPS'], kde=False, bins=30, ax=axes[0, 0])
axes[0, 0].set_title('ForecastedEPS Distribution')
annotate_stats(axes[0, 0], df['ForecastedEPS'])

sns.histplot(df['ActualEPS'], kde=False, bins=30, ax=axes[0, 1])
axes[0, 1].set_title('ActualEPS Distribution')
annotate_stats(axes[0, 1], df['ActualEPS'])

sns.histplot(df['Surprise%'], kde=False, bins=30, ax=axes[0, 2])
axes[0, 2].set_title('Surprise% Distribution')
annotate_stats(axes[0, 2], df['Surprise%'])

# boxplots
sns.boxplot(x=df['ForecastedEPS'], ax=axes[1, 0])
axes[1, 0].set_title('ForecastedEPS Boxplot')

sns.boxplot(x=df['ActualEPS'], ax=axes[1, 1])
axes[1, 1].set_title('ActualEPS Boxplot')

sns.boxplot(x=df['Surprise%'], ax=axes[1, 2])
axes[1, 2].set_title('Surprise% Boxplot')

plt.tight_layout()

# save 
save_path = '/Users/aj/Downloads/DISSERTATION CODE/PLOTS_GRAPHS/summary_statistics.png'
plt.savefig(save_path)

plt.show()
