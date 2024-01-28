import sqlite3

conn = sqlite3.connect('pead_database.sqlite')
cursor = conn.cursor()

# fetch all RICs with NULL VARIABLE values
cursor.execute("SELECT DISTINCT RIC FROM StockData WHERE Volume IS NULL")
rics_with_nulls = [row[0] for row in cursor.fetchall()]

for ric in rics_with_nulls:
    # fetch all dates with NULL VARIABLE values for the current RIC
    cursor.execute("SELECT Date FROM StockData WHERE RIC = ? AND Volume IS NULL", (ric,))
    null_dates = [row[0] for row in cursor.fetchall()]

    for date in null_dates:
        # fetch the nearest previous non-NULL VARIABLE value
        cursor.execute("""
            SELECT Volume
            FROM StockData
            WHERE RIC = ? AND Date < ? AND Volume IS NOT NULL
            ORDER BY Date DESC
            LIMIT 1
        """, (ric, date))
        prev_value = cursor.fetchone()

        # fetch the nearest next non-NULL VARIABLE value
        cursor.execute("""
            SELECT Volume
            FROM StockData
            WHERE RIC = ? AND Date > ? AND Volume IS NOT NULL
            ORDER BY Date ASC
            LIMIT 1
        """, (ric, date))
        next_value = cursor.fetchone()

        # calculate average of two values
        if prev_value and next_value:
            avg_value = (prev_value[0] + next_value[0]) / 2
        elif prev_value:
            avg_value = prev_value[0]
        elif next_value:
            avg_value = next_value[0]
        else:
            avg_value = None

        # update row with calculated average
        if avg_value is not None:
            cursor.execute("UPDATE StockData SET Volume = ? WHERE RIC = ? AND Date = ?", (avg_value, ric, date))

    # commit changes for current RIC
    conn.commit()

conn.close()
