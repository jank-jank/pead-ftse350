import sqlite3
import pandas as pd

conn = sqlite3.connect('pead_database.sqlite')

# read the Companies table into DataFrame
df = pd.read_sql_query("SELECT * FROM Companies", conn)

# save the DataFrame to Excel
df.to_excel('Companies.xlsx', index=False)

conn.close()
