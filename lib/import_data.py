import yfinance as yf
import pandas as pd

# Import data for ticker. in: type of source, ticker name, data start date, data end date. out: dataframe with ticker data for date range
def get_data(data_src , tckr, data_strt_dt, data_end_dt):
    if data_src == 'csv':
        data_temp = pd.read_csv('historical_data/' + tckr + '.csv' , index_col = ['Date'])
        data_temp = data_temp.loc[data_strt_dt:data_end_dt, :]
        return data_temp
    elif data_src == 'yf':
        data_temp = yf.download(tckr, data_strt_dt, data_end_dt)
        return data_temp