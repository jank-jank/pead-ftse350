import scipy.stats as stats
import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

query = """
SELECT Earnings.GOOD, Earnings.BAD, Earnings.CAR_p2p60
FROM Earnings
"""

# load data into a df
df = pd.read_sql(query, conn)

conn.close()

# extract GOOD and BAD dummy variables
X_good = df[df['GOOD'] == 1]['CAR_p2p60']
X_bad = df[df['BAD'] == 1]['CAR_p2p60']

# calculate statistics for GOOD
good_observations = len(X_good)
good_mean = np.mean(X_good)
good_std = np.std(X_good, ddof=1)  # ddof=1 for sample standard deviation

# calculate statistics for BAD
bad_observations = len(X_bad)
bad_mean = np.mean(X_bad)
bad_std = np.std(X_bad, ddof=1)  # ddof=1 for sample standard deviation

# t-test
t_stat, p_value = stats.ttest_ind(X_good, X_bad, equal_var=False)
df_ttest = len(X_good) + len(X_bad) - 2  # degrees of freedom for unequal variances

# difference in means
diff = good_mean - bad_mean

print(f"Positive Surprise\nObservations: {good_observations}\nMean: {good_mean:.2%}\nStandard Deviation: {good_std:.3f}\n")
print(f"Negative Surprise\nObservations: {bad_observations}\nMean: {bad_mean:.2%}\nStandard Deviation: {bad_std:.3f}\n")
print(f"Difference (diff): {diff:.3f}\nHypothesis (Ha): diff ≠ 0\nt-statistic: {t_stat:.3f}\np-value: {p_value:.3f}\nDegrees of Freedom (df): {df_ttest}")
