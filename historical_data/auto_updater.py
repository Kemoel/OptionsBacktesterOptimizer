import yfinance as yf
import pandas as pd
import os

# Directory for files to be updated.
directory = r"D:\Code\trading_source\historical_data\1day"

print('Updating files in directory:'+'\n'+directory)

update_flag = 0

for filename in os.listdir(directory):
    tckr = filename.replace('.csv', '')
    if (filename.endswith(".csv")):
        # Read last date of csv.
        data = pd.read_csv(directory + '/' + tckr + '.csv' , index_col = ['Date'])
        final_date = min((pd.to_datetime(data.iloc[-1].name)+pd.offsets.Day(1)),pd.to_datetime('today').normalize())
        # Check if requires update, if not skip to next ticker.
        if (final_date == pd.to_datetime('today').normalize()):
                continue
        # Get missing days from yahoo.
        data_new = yf.download(tckr, final_date) 
        data_new.index = data_new.index.strftime('%Y-%m-%d')
        # Append to dataframe.
        data = data.append(data_new).round(6)
        # Write data back to csv.
        data.to_csv(directory + '/' + tckr + '.csv')
        # Print ticker that are updated.
        print (tckr.replace("('", "").replace("',)", ""))
        update_flag = 1

# Print completed names of files updated.
if (update_flag == 1):      
        print('Updated successfully!')
else:
        print('All files already up to date!')