import sqlite3

conn = sqlite3.connect('pead_database.sqlite')
cursor = conn.cursor()

# delete table
cursor.execute("DROP TABLE IF EXISTS VolBetCap")

# commit the changes and close the DB connection
conn.commit()
conn.close()
