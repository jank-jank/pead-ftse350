import sqlite3
import pandas as pd
import statsmodels.api as sm
from datetime import timedelta

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# query data from EarningsREF, StockData, and FTSE350Closing
df_earnings = pd.read_sql("SELECT EarningsDate, RIC, GOOD, BAD FROM EarningsREF", conn)
df_stock = pd.read_sql("SELECT Date, RIC, LogReturn FROM StockData", conn)
df_market = pd.read_sql("SELECT Date, LogReturn FROM FTSE350Closing", conn)

# convert to datetime
df_earnings['EarningsDate'] = pd.to_datetime(df_earnings['EarningsDate'])
df_stock['Date'] = pd.to_datetime(df_stock['Date'])
df_market['Date'] = pd.to_datetime(df_market['Date'])

# initialize an empty list to store Abnormal Returns and SURPRISE
results_list = []

# loop through each earnings event
for index, row in df_earnings.iterrows():
    earnings_date = row['EarningsDate']
    ric = row['RIC']
    
    # filter stock and market data for the event window [-1, 1]
    stock_data = df_stock[(df_stock['RIC'] == ric) & (df_stock['Date'].between(earnings_date - timedelta(days=1), earnings_date + timedelta(days=1)))]
    market_data = df_market[df_market['Date'].between(earnings_date - timedelta(days=1), earnings_date + timedelta(days=1))]
    
    # merge stock and market data
    merged_data = pd.merge(stock_data, market_data, on='Date')
    
    # calculate Abnormal Returns (AR)
    merged_data['AR'] = merged_data['LogReturn_x'] - merged_data['LogReturn_y']
    
    # calculate SURPRISE based on GOOD and BAD
    surprise = row['GOOD'] - row['BAD']
    
    # add to results list
    for ar in merged_data['AR']:
        results_list.append({'EarningsDate': earnings_date, 'RIC': ric, 'AR': ar, 'SURPRISE': surprise})

# create DataFrame from the results list
df_results = pd.DataFrame(results_list)

# drop rows with missing values
df_results.dropna(inplace=True)

# conduct OLS regression
X = df_results['SURPRISE'].astype(float)
X = sm.add_constant(X)  # add constant term to the predictor
y = df_results['AR'].astype(float)

model = sm.OLS(y, X)
results = model.fit()

print(results.summary())
