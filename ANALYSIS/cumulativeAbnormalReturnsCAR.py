import sqlite3
import pandas as pd

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# add CAR2 to Earnings table
try:
    conn.execute("ALTER TABLE Earnings ADD COLUMN CAR2 REAL;")
    conn.commit()
except sqlite3.OperationalError:
    print("Column CAR2 already exists.")

# fetch data
df_earnings = pd.read_sql("SELECT * FROM Earnings", conn)
df_stock = pd.read_sql("SELECT * FROM StockData", conn)
df_market = pd.read_sql("SELECT * FROM FTSE350Closing", conn)

# convert to datetime
df_earnings['EarningsDate'] = pd.to_datetime(df_earnings['EarningsDate'])
df_stock['Date'] = pd.to_datetime(df_stock['Date'])
df_market['Date'] = pd.to_datetime(df_market['Date'])

# counter
counter = 0
total_rows = len(df_earnings)

# iterate through each row in Earnings
for index, row in df_earnings.iterrows():
    ric = row['RIC']
    earnings_date = row['EarningsDate']
    
    # define post-event window
    start_date = earnings_date + pd.Timedelta(days=2)
    end_date = earnings_date + pd.Timedelta(days=60)
    
    # filter data
    stock_data = df_stock[(df_stock['RIC'] == ric) & (df_stock['Date'] >= start_date) & (df_stock['Date'] <= end_date)]
    market_data = df_market[(df_market['Date'] >= start_date) & (df_market['Date'] <= end_date)]
    
    # if lengths match
    if len(stock_data) == len(market_data):
        # calculate Abnormal Returns
        stock_data['AR'] = stock_data['LogReturn'] - market_data['LogReturn'].values
        
        # calculate CAR2
        CAR2 = stock_data['AR'].sum()
        
        # convert the pandas Timestamp to string
        earnings_date_str = earnings_date.strftime('%Y-%m-%d')
        
        # update CAR2 in Earnings
        conn.execute("UPDATE Earnings SET CAR2 = ? WHERE RIC = ? AND EarningsDate = ?", (CAR2, ric, earnings_date_str))
        conn.commit()
        
        # update / display counter
        counter += 1
        print(f"Progress: {counter}/{total_rows}")
    else:
        print(f"Skipping: Length mismatch for RIC {ric} on {earnings_date}")

conn.close()