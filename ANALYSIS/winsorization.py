import sqlite3
import pandas as pd
from scipy.stats import mstats

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# fetch data from EarningsREF table into DataFrame
df = pd.read_sql_query("SELECT * FROM EarningsREF", conn)

# identify numerical columns
num_cols = df.select_dtypes(include=['float64']).columns

# 1% Winsorization on each numerical column
for col in num_cols:
    df[col] = mstats.winsorize(df[col], limits=[0.01, 0.01])

# update EarningsREF with Winsorized data
df.to_sql('EarningsREF', conn, if_exists='replace', index=False)

conn.close()
