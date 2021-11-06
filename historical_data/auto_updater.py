import os
import yfinance as yf
import pandas as pd

directory = r"D:\Code\trading_source\historical_data\1day"

for filename in os.listdir(directory):
    tckr = filename.replace('.csv', '')
    if (filename.endswith(".csv")):
        # Read last date of csv.
        with open('1day/'+filename, "r", encoding="utf-8", errors="ignore") as scraped:
                final_date = pd.to_datetime(scraped.readlines()[-1][0:10])
        # Get missing days from yahoo.
        data_temp = yf.download(tckr, final_date + pd.offsets.Day(1))
        # Append data to csv.
        with open('1day/'+filename,'a', encoding="utf-8", errors="ignore") as f:
            data_temp.to_csv(f, mode='a', header=False, line_terminator='\n')

print(directory)
for tckr in (os.listdir(directory)):
        print (tckr.replace("('", "").replace("',)", ""))
print('Updated successfully')