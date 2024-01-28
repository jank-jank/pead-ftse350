import pandas as pd
import sqlite3
import eikon as ek
import time

# Refinitiv API key
ek.set_app_key('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# date range
start_date = '2013-01-01'
end_date = '2022-12-31'

conn = sqlite3.connect('pead_database.sqlite')

# fetch daily closing price for the FTSE350
retries = 3
success = False
while retries > 0 and not success:
    try:
        data = ek.get_timeseries(".FTLC", 
                                 fields="CLOSE", 
                                 start_date=start_date, 
                                 end_date=end_date, 
                                 interval="daily")
        
        # reset the index to make 'Date' a column
        data = data.reset_index()
        
        # rename columns for consistency
        data = data.rename(columns={'Date': 'Date', 'CLOSE': 'ClosingPrice'})
        
        # insert data
        data.to_sql('FTSE350ClosingPrice', conn, if_exists='replace', index=False)
        success = True
    except ek.eikonError.EikonError as e:
        if 'Too many requests' in str(e) or 'Gateway Time-out' in str(e):
            retries -= 1
            time.sleep(10)  # wait for 10 seconds
        else:
            raise e

conn.close()
