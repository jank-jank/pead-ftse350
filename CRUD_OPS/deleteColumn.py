import sqlite3

def delete_column_from_table(database_path, table_name, column_to_delete):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # fetch columns of the original table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    columns.remove(column_to_delete)  # remove the column to be deleted

    # create new table without the column
    new_table_name = table_name + "_new"
    cursor.execute(f"CREATE TABLE {new_table_name} AS SELECT {', '.join(columns)} FROM {table_name}")

    # drop the original table
    cursor.execute(f"DROP TABLE {table_name}")

    # rename the new table to the original table's name
    cursor.execute(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")

    # commit the changes and close the DB connection
    conn.commit()
    conn.close()

# function to delete the column from the table
delete_column_from_table('pead_database.sqlite', 'StockData', 'Beta')