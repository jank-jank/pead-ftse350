import sqlite3
import pandas as pd
from scipy.stats import shapiro

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# fetch FTSE350Closing data
ftse350_df = pd.read_sql_query("SELECT * FROM FTSE350Closing", conn)
ftse350_returns = ftse350_df['LogReturn'].dropna()

# Shapiro-Wilk test for FTSE350Closing
stat, p = shapiro(ftse350_returns)
if p > 0.05:
    print("FTSE350Closing returns appear to be normally distributed (p-value:", p, ")")
else:
    print("FTSE350Closing returns do not appear to be normally distributed (p-value:", p, ")")

# fetch all unique RICs from StockData
ric_list = pd.read_sql_query("SELECT DISTINCT RIC FROM StockData", conn)['RIC'].tolist()

# Shapiro-Wilk test for each RIC in StockData
for ric in ric_list:
    ric_df = pd.read_sql_query(f"SELECT * FROM StockData WHERE RIC='{ric}'", conn)
    ric_returns = ric_df['LogReturn'].dropna()
    
    stat, p = shapiro(ric_returns)
    if p > 0.05:
        print(f"{ric} returns appear to be normally distributed (p-value: {p})")
    else:
        print(f"{ric} returns do not appear to be normally distributed (p-value: {p})")

conn.close()