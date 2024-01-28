import sqlite3

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')
cursor = conn.cursor()

# list tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f"- {table[0]}")

# list columns for each table
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nColumns in the table '{table_name}':")
    for column in columns:
        print(f"- {column[1]} (Type: {column[2]}, Not Null: {bool(column[3])}, Default Value: {column[4]})")

conn.close()
