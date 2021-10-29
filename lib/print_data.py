import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

def prt_grph_sns(data, tckr, strt_dt, end_dt, prc, sma, ema, bb, kc, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr):
    sns.set(style='darkgrid',context='talk',palette='Dark2')
    dt_frmt = mdates.DateFormatter('%m/%y')
    fig, ax = plt.subplots(figsize=(16,9))
    if prc == True:
        ax.plot(data.loc[strt_dt:end_dt , :].index, data.loc[strt_dt:end_dt, 'Adj Close'], label = 'Price')
    if sma == True:
        ax.plot(sma1.loc[strt_dt:end_dt, :].index, sma1.loc[strt_dt:end_dt, list(sma1.columns.values)], label = 'SMA1', alpha = 0.5)
        ax.plot(sma2.loc[strt_dt:end_dt, :].index, sma2.loc[strt_dt:end_dt, list(sma2.columns.values)], label = 'SMA2', alpha = 0.5)
    if ema == True:
        ax.plot(ema1.loc[strt_dt:end_dt, :].index, ema1.loc[strt_dt:end_dt, list(ema1.columns.values)], label = 'EMA1', alpha = 0.5)
    if bb == True:
        ax.plot(bb_upr.loc[strt_dt:end_dt, :].index, bb_upr.loc[strt_dt:end_dt, list(bb_upr.columns.values)], label = 'BB', color = 'yellow', alpha = 0.5)
        ax.plot(bb_lwr.loc[strt_dt:end_dt, :].index, bb_lwr.loc[strt_dt:end_dt, list(bb_lwr.columns.values)], color = 'yellow', alpha = 0.5)
    if kc == True:
        ax.plot(kc_upr.loc[strt_dt:end_dt, :].index, kc_upr.loc[strt_dt:end_dt, list(kc_upr.columns.values)], label = 'KC', color = 'black', alpha = 0.5)
        ax.plot(kc_lwr.loc[strt_dt:end_dt, :].index, kc_lwr.loc[strt_dt:end_dt, list(kc_lwr.columns.values)], color = 'black', alpha = 0.5)
    ax.set_title(tckr)
    ax.legend(loc='best')
    ax.set_ylabel('USD')
    ax.set_xlabel('Date')
    ax.xaxis.set_major_formatter(dt_frmt)
    plt.show()
    return

def print_all(data):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # More options can be specified also
        print(data)
    return