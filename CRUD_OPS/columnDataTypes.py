import sqlite3

conn = sqlite3.connect('pead_database.sqlite')
cursor = conn.cursor()

# fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# loop through each table to get column data types
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    print(f"Data types in table {table_name}:")
    
    for column in columns:
        column_name = column[1]
        data_type = column[2]
        
        print(f"  - Column '{column_name}' has data type: {data_type}")

conn.close()
