from input.initialization import *
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd

def prt_grph(data, acnt_data, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr, tckr=tckr, strt_dt=strt_dt, end_dt=end_dt, spec_data=spec_data, prc_flg=True, sma_flg=True, ema_flg=True, bb_flg=True, kc_flg=True, acnt_flg=True):
    fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, figsize=(16,9), gridspec_kw={'height_ratios': [3, 1]})
    if prc_flg == True:
        ax1.plot(pd.to_datetime(data.loc[strt_dt:end_dt].index), data.loc[strt_dt:end_dt, spec_data], label = 'Price')
    if sma_flg == True:
        ax1.plot(pd.to_datetime(sma1.loc[strt_dt:end_dt].index), sma1.loc[strt_dt:end_dt, list(sma1.columns.values)], label = 'SMA1', alpha = 0.5)
        ax1.plot(pd.to_datetime(sma2.loc[strt_dt:end_dt].index), sma2.loc[strt_dt:end_dt, list(sma2.columns.values)], label = 'SMA2', alpha = 0.5)
    if ema_flg == True:
        ax1.plot(pd.to_datetime(ema1.loc[strt_dt:end_dt].index), ema1.loc[strt_dt:end_dt, list(ema1.columns.values)], label = 'EMA1', alpha = 0.5)
    if bb_flg == True:
        ax1.plot(pd.to_datetime(bb_upr.loc[strt_dt:end_dt].index), bb_upr.loc[strt_dt:end_dt, list(bb_upr.columns.values)], label = 'BB', color = 'yellow', alpha = 0.7)
        ax1.plot(pd.to_datetime(bb_lwr.loc[strt_dt:end_dt].index), bb_lwr.loc[strt_dt:end_dt, list(bb_lwr.columns.values)], color = 'yellow', alpha = 0.7)
    if kc_flg == True:
        ax1.plot(pd.to_datetime(kc_upr.loc[strt_dt:end_dt].index), kc_upr.loc[strt_dt:end_dt, list(kc_upr.columns.values)], label = 'KC', color = 'black', alpha = 0.5)
        ax1.plot(pd.to_datetime(kc_lwr.loc[strt_dt:end_dt].index), kc_lwr.loc[strt_dt:end_dt, list(kc_lwr.columns.values)], color = 'black', alpha = 0.5)
    if acnt_flg == True:
        ax2.plot(pd.to_datetime(acnt_data.loc[strt_dt:end_dt].index), acnt_data.loc[strt_dt:end_dt, 'account value'], label = 'Account Value')
    ax1.set_title(tckr)
    ax1.legend(loc='best')
    ax1.set_ylabel('USD')
    ax1.set_xlabel('Date')
    ax2.set_ylabel('USD')
    ax2.set_xlabel('Date')
    plt.grid()
    plt.tight_layout()
    plt.show()
    return

def print_all(data):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # More options can be specified also
        print(data)
    return