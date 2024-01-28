import pandas as pd
import sqlite3
import os

companies_info_path = "/Users/aj/Downloads/Earnings_Companies.xlsx"
earnings_folder_path = "/Users/aj/Downloads/earnings_BLP_excel"
database_path = "pead_database.sqlite"

# read xlsx
companies_info = pd.read_excel(companies_info_path, engine='openpyxl')

conn = sqlite3.connect(database_path)

# empty DataFrame to store earnings data
earnings_data = pd.DataFrame()

# iterate over each row in the companies info DataFrame
for _, row in companies_info.iterrows():
    number = row['Number']
    ric = row['RIC']
    available = row['Available']

    # if company data available -> read the corresponding Excel file
    if available == 1:
        file_path = os.path.join(earnings_folder_path, f"{number}.xlsx")
        
        # does file exists?
        if os.path.exists(file_path):
            # read earnings
            company_df = pd.read_excel(file_path, engine='openpyxl')
            
            # filter out rows where any of required columns have missing values
            company_df = company_df.dropna(subset=['Ann Date', 'Reported', 'Estimate'])
            
            # add the company number and RIC to DataFrame
            company_df['Number'] = number
            company_df['RIC'] = ric
            
            # append data to the DataFrame
            earnings_data = pd.concat([earnings_data, company_df[['Number', 'RIC', 'Ann Date', 'Estimate', 'Reported']]], ignore_index=True)

# save earnings data to DB
earnings_data.to_sql('Earnings', conn, if_exists='replace', index=False)

conn.close()
