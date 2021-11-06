from input.initialization import *
import yfinance as yf
import pandas as pd

# Import data for ticker. in: type of source, ticker name, data start date, data end date. out: dataframe with ticker data for date range
def get_data(data_src_type=data_src_type , data_src_folder=data_src_folder, tckr=tckr):
    if data_src_type == 'csv':
        data_temp = pd.read_csv('historical_data/' + data_src_folder + '/' + tckr + '.csv' , index_col = ['Date'])
        return data_temp
    elif data_src_type == 'txt':
        data_temp = pd.read_csv('historical_data/' + data_src_folder + '/' + tckr + '.txt' , sep=',', index_col=[0], names = ['Date','Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        return data_temp        
    elif data_src_type == 'yf':
        data_temp = yf.download(tckr, yh_data_strt_dt, yh_data_end_dt)
        return data_temp

def get_volitility_data(spec_data, tckr=tckr_volitlity):
    data_temp = pd.read_csv('historical_data/1day/' + tckr + '.csv' , index_col = ['Date'], usecols=['Date',spec_data])
    return data_temp