import sqlite3
import pandas as pd

conn = sqlite3.connect('pead_database.sqlite')

# query for RIC of top 10 companies by X
query = """
SELECT RIC 
FROM Companies 
ORDER BY MarketCap DESC 
LIMIT 10
"""

df_top10 = pd.read_sql_query(query, conn)

conn.close()

print(df_top10)