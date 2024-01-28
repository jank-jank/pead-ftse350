import sqlite3
import pandas as pd

# read CSV into DataFrame
df = pd.read_csv('/Users/aj/Downloads/DISSERTATION CODE/FTSE350_Constituents.csv')

conn = sqlite3.connect('pead_database.sqlite')

# cursor object
cursor = conn.cursor()

# check if the Companies table already exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Companies'")
if cursor.fetchone():
    # create temporary table without the MarketCap column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Companies_temp (
        Ticker TEXT PRIMARY KEY,
        RIC TEXT,
        Name TEXT
        -- Exclude MarketCap
    )
    ''')
    
    # copy from original Companies table to the temporary table
    cursor.execute('''
    INSERT INTO Companies_temp (RIC, Name)
    SELECT RIC, Name FROM Companies
    ''')
    
    # drop the original Companies
    cursor.execute('DROP TABLE Companies')
    
    # rename the temporary table to Companies
    cursor.execute('ALTER TABLE Companies_temp RENAME TO Companies')

else:
    # create table if not there yet
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Companies (
        Ticker TEXT PRIMARY KEY,
        RIC TEXT,
        Name TEXT
        -- Exclude MarketCap
    )
    ''')

# commit, write, closeDB
conn.commit()
df[['Ticker', 'RIC', 'Name']].to_sql('Companies', conn, if_exists='append', index=False)
conn.close()
