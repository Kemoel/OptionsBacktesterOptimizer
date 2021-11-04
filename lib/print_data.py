from input.initialization import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def prt_grph(data, trd_data, acnt_val_data, acnt_end_val_p, acnt_end_val_year_p, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr, num_trds, tckr=tckr, strt_dt=strt_dt, end_dt=end_dt, spec_data=spec_data, prc_flg=True, sma_flg=True, ema_flg=False, bb_flg=True, kc_flg=True, acnt_val_flg=True):
    fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, figsize=(16,9), facecolor='lightgrey', gridspec_kw={'height_ratios': [3, 1], 'wspace':0, 'hspace':0}, sharex=True)
    if prc_flg == True:
        ax1.plot(pd.to_datetime(data.loc[strt_dt:end_dt].index), data.loc[strt_dt:end_dt, spec_data], label = ('Price '+spec_data))
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
    if acnt_val_flg == True:
        ax2.plot(pd.to_datetime(acnt_val_data.loc[strt_dt:end_dt].index), acnt_val_data.loc[strt_dt:end_dt, 'account value'], label = 'Account Value')
    # Print arrows at trade locations.
    # ax1.quiver(data.loc[strt_dt:end_dt].index,data.loc[strt_dt:end_dt,spec_data],0,0)
    #Print trade characteristics.
    test_length = int((pd.to_datetime(end_dt)-pd.to_datetime(strt_dt)).days)
    years = test_length//365
    months = (test_length - years*365)//30
    days = (test_length - years*365 - months*30)
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax2.text(0.2, 0.75,'Max Value: '+str("{:,}".format(int(np.max(acnt_val_data['account value']))))+'\n' 
                        'Min Value: '+str("{:,}".format(int(np.min(acnt_val_data['account value']))))+'\n'
                        'Start Balance: '+str("{:,}".format(strt_blnc))+'\n'
                        'Return: '+str("{:,}".format(round(acnt_end_val_p*100,2)))+'%'+'\n'
                        'Avg return per year: '+str("{:,}".format(round(acnt_end_val_year_p*100,2)))+'%',
                        ha='center', va='center', transform=ax2.transAxes, bbox=props)
    ax2.text(0.35, 0.85,'Total time: '+ str(years) + ' years ' + str(months) + ' months ' + str(days) + ' days'  +'\n'
                        'Number of trades: '+str(num_trds),
                        ha='center', va='center', transform=ax2.transAxes, bbox=props)                    
    # Formating plots and figure.
    plt.get_current_fig_manager().set_window_title(tckr+' Data')
    ax1.set_title(tckr); ax1.legend(loc='best'); ax1.set_ylabel('USD'); ax1.grid(); ax1.autoscale(enable=True, axis='x', tight=True)
    ax2.legend(loc='upper left'); ax2.set_ylabel('USD'); ax2.set_xlabel('Date'); ax2.grid(); ax2.autoscale(enable=True, axis='x', tight=True)
    # ax1.set_yscale('log');ax2.set_yscale('log')
    fig.tight_layout()
    # Show plot.
    plt.show()
    return

def print_all(data):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # More options can also be specified.
        print(data)
    return