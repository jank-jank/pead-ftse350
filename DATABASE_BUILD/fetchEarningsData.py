import pandas as pd
import sqlite3
import eikon as ek

# mnemonics of the data needed (see HSUP in Refinitiv)
# SUE --> TR.RevenueActSueScore
# Actual EPS --> TR.EPSActValue
# Forecasted EPS --> TR.EPSMean
# %Surprise --> TR.EPSActSurprise

def is_ric_in_database(ric, conn):
    """Check if a given RIC is already in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='EarningsREFall'")
    if not cursor.fetchone():
        return False
    existing_data = pd.read_sql_query(f"SELECT * FROM EarningsREFall WHERE RIC='{ric}'", conn)
    return not existing_data.empty

# Refinitiv API key
ek.set_app_key('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

conn = sqlite3.connect('pead_database.sqlite')

# extract distinct RICs
rics = pd.read_sql_query("SELECT DISTINCT RIC FROM StockData", conn)

# initialize counter
counter = 0

# iterate through RICs to fetch earnings data
for ric in rics['RIC']:
    if not is_ric_in_database(ric, conn):
        try:
            print(f"Fetching data for {ric}...")
            
            # fetch earnings data from Refinitiv
            earnings_data, err = ek.get_data(
                [ric],
                ['TR.EPSMean.date', 'TR.EPSMean', 'TR.EPSActValue', 'TR.EPSActSurprise', 'TR.RevenueActSueScore'],
                {'SDate': "2013-01-01", 'EDate': "2022-12-31", 'FRQ': 'D', 'Curn': 'GBP', 'Period': "FY1"}
            )
            
            # rename the columns
            earnings_data.rename(columns={
                'TR.EPSMean.date': 'Date',
                'TR.EPSMean': 'EstimateEPS',
                'TR.EPSActValue': 'ActualEPS',
                'TR.EPSActSurprise': 'Surprise',
                'TR.RevenueActSueScore': 'SUE'
            }, inplace=True)
            
            # add the RIC column
            earnings_data['RIC'] = ric
            
            # data to the database
            earnings_data.to_sql('EarningsREFall', conn, if_exists='append', index=False)
            
            counter += 1
            print(f"Data for {ric} saved successfully. Total RICs processed: {counter}")
            
        except Exception as e:
            print(f"Error fetching data for {ric}: {e}")

# close the database
conn.close()
