from input.initialization import *
import yfinance as yf
import pandas as pd

# Import data for ticker. in: type of source, ticker name, data start date, data end date. out: dataframe with ticker data for date range
def get_data(data_src=data_src , tckr=tckr):
    if data_src == 'csv':
        data_temp = pd.read_csv('historical_data/' + tckr + '.csv' , index_col = ['Date'])
        return data_temp
    elif data_src == 'txt':
        data_temp = pd.read_csv('historical_data/' + tckr + '.txt' , sep=',', index_col=0, names = ['Date','Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return data_temp        
    elif data_src == 'yf':
        data_temp = yf.download(tckr, yh_data_strt_dt, yh_data_end_dt)
        return data_temp