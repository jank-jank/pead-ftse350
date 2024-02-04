import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

output_dir = '/Users/aj/Downloads/DISSERTATION CODE/PLOTS_GRAPHS'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

conn = sqlite3.connect('/Users/aj/Downloads/DISSERTATION CODE/DATABASE_BUILD/pead_database.sqlite')

# fetch table names
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# loop through each table and plot histograms and box plots
for table in tables:
    table_name = table[0]
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    print(f"plots for table {table_name}...")
    
    # filter out non-numerical columns
    num_cols = df.select_dtypes(include=['float64', 'int']).columns
    
    # histograms
    for col in num_cols:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col], bins=30, kde=True)
        plt.title(f"Histogram of {col} in {table_name}")
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.savefig(f"{output_dir}/Histogram_{table_name}_{col}.png")
        plt.close()
        
    # box plots
    for col in num_cols:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot of {col} in {table_name}")
        plt.xlabel(col)
        plt.savefig(f"{output_dir}/Boxplot_{table_name}_{col}.png")
        plt.close()

conn.close()
