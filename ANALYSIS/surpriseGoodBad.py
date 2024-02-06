import sqlite3

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')
cursor = conn.cursor()

# new columns GOOD, BAD, and SURPRISE to the Earnings table
cursor.execute("ALTER TABLE Earnings ADD COLUMN GOOD INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE Earnings ADD COLUMN BAD INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE Earnings ADD COLUMN SURPRISE INTEGER DEFAULT 0")

conn.commit()

# update the columns based on the conditions
cursor.execute("""
    UPDATE Earnings
    SET 
        GOOD = CASE 
            WHEN "Surprise%" > 2.5 THEN 1
            ELSE 0
        END,
        BAD = CASE 
            WHEN "Surprise%" < -2.5 THEN 1
            ELSE 0
        END,
        SURPRISE = CASE 
            WHEN "Surprise%" > 2.5 THEN 1
            WHEN "Surprise%" < -2.5 THEN -1
            ELSE 0
        END
""")

conn.commit()
conn.close()
