import pandas as pd
import sqlite3
import eikon as ek

def is_ric_in_database(ric, conn):
    """Check if a given RIC is already in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RICData'")
    if not cursor.fetchone():
        return False
    existing_data = pd.read_sql_query(f"SELECT * FROM RICData WHERE RIC='{ric}'", conn)
    return not existing_data.empty

# Refinitiv API key
ek.set_app_key('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# date range
start_date = '2013-01-01'
end_date = '2022-12-31'

# SQLite database connection
conn = sqlite3.connect('pead_database.sqlite')

# fetch RICs from database
ric_list = pd.read_sql_query("SELECT RIC FROM Companies", conn)['RIC'].tolist()

# base DataFrame with the full date range
base_df = pd.DataFrame({
    'Date': pd.date_range(start=start_date, end=end_date)
})

# loop through RICs and fetch the data
for ric in ric_list:
    if not is_ric_in_database(ric, conn):
        try:
            print(f"Fetching data for {ric}...")
            data, err = ek.get_data(
                instruments = [ric],
                fields = [
                    f'TR.WACCBeta(SDate={start_date},EDate={end_date},Frq=C)',
                    f'TR.Volume(SDate={start_date},EDate={end_date},Frq=C)',
                    f'TR.CompanyMarketCapitalization(SDate={start_date},EDate={end_date},Frq=C)'
                ]
            )
            
            # rename the columns
            data.columns = ['RIC', 'Beta', 'Volume', 'MarketCap']
            
            # generate the date range and assign it to data DataFrame
            date_range = pd.date_range(start=start_date, end=end_date)
            data['Date'] = date_range
            
            # merge the base DataFrame with the fetched data to fill in gaps
            merged_data = base_df.merge(data, on='Date', how='left')
            merged_data['RIC'] = ric
            
            # save the merged data for the current RIC to the RICData table in the database
            merged_data.to_sql('RICData', conn, if_exists='append', index=False)
            
            print(f"Data for {ric} saved successfully.")
            
        except Exception as e:
            print(f"Error fetching data for {ric}: {e}")

conn.close()
