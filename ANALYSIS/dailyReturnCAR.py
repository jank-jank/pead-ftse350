import sqlite3
import pandas as pd

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# new columns AR_n12 to AR_p60 to Earnings table
for shift in range(-12, 61):
    prefix = "n" if shift < 0 else "p"
    column_name = f"AR_{prefix}{abs(shift)}"
    try:
        conn.execute(f"ALTER TABLE Earnings ADD COLUMN {column_name} REAL;")
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error adding column {column_name}: {e}")

# fetch data
df_earnings = pd.read_sql("SELECT * FROM Earnings", conn)
df_stock = pd.read_sql("SELECT * FROM StockData", conn)
df_market = pd.read_sql("SELECT * FROM FTSE350Closing", conn)

# convert to datetime
df_earnings['EarningsDate'] = pd.to_datetime(df_earnings['EarningsDate'])
df_stock['Date'] = pd.to_datetime(df_stock['Date'])
df_market['Date'] = pd.to_datetime(df_market['Date'])

# counters
row_counter = 0
ar_counter = 0
total_rows = len(df_earnings)
total_ar_calculations = total_rows * (61 + 12)  # for each shift from -12 to 60

# iterate through each row in Earnings
for index, row in df_earnings.iterrows():
    ric = row['RIC']
    earnings_date = row['EarningsDate']
    
    # iterate through each shift from -12 to 60
    for shift in range(-12, 61):
        event_date = earnings_date + pd.Timedelta(days=shift)
        
        # filter data for the specific event date
        stock_data = df_stock[(df_stock['RIC'] == ric) & (df_stock['Date'] == event_date)]
        market_data = df_market[df_market['Date'] == event_date]
        
        # check if lengths match and data exists for the event date
        if len(stock_data) == len(market_data) == 1:
            # calculate Abnormal Returns
            AR = stock_data.iloc[0]['LogReturn'] - market_data.iloc[0]['LogReturn']
            
            # update AR in Earnings
            prefix = "n" if shift < 0 else "p"
            column_name = f"AR_{prefix}{abs(shift)}"
            conn.execute(f"UPDATE Earnings SET {column_name} = ? WHERE RIC = ? AND EarningsDate = ?", (AR, ric, earnings_date.strftime('%Y-%m-%d')))
            conn.commit()
            
            # update and display AR counter
            ar_counter += 1
            print(f"AR Progress: {ar_counter}/{total_ar_calculations}")
        else:
            print(f"Skipping: Data mismatch for RIC {ric} on {event_date}")
    
    row_counter += 1
    print(f"Row Progress: {row_counter}/{total_rows}")

conn.close()
