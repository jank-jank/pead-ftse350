import pandas as pd
import sqlite3
import eikon as ek

def is_ric_in_earnings_ref(ric, conn):
    """Check if a given RIC is already in the EarningsREF table."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='EarningsREF'")
    if not cursor.fetchone():
        return False
    existing_data = pd.read_sql_query(f"SELECT * FROM EarningsREF WHERE RIC='{ric}'", conn)
    return not existing_data.empty

# Refinitiv API key
ek.set_app_key('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# SQLite database connection
conn = sqlite3.connect('pead_database.sqlite')

# fetch distinct RICs
rics = pd.read_sql_query("SELECT DISTINCT RIC FROM StockData", conn)

# initialize counter
counter = 0

# fetch earnings release dates for each RIC
for ric in rics['RIC']:
    if not is_ric_in_earnings_ref(ric, conn):
        try:
            print(f"fetching earnings release dates for {ric}...")
            
            # fetch earnings release dates
            earnings_dates, err = ek.get_data([ric], ['TR.EventStartDate(SDate=2013-01-01,EDate=2022-12-31,EventType=RES)'])
            
            # RIC column
            earnings_dates['RIC'] = ric
            
            # rename the columns
            earnings_dates.rename(columns={'Event Start Date': 'EarningsDate'}, inplace=True)
            
            # data to the database
            earnings_dates.to_sql('EarningsREF', conn, if_exists='append', index=False)
            
            counter += 1
            print(f"Earnings release dates for {ric} saved successfully. Total RICs processed: {counter}")
            
        except Exception as e:
            print(f"Error fetching earnings release dates for {ric}: {e}")

# close the database 
conn.close()
