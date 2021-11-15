from scipy.stats.morestats import Mean
from input.initialization import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def prt_grph(data, trd_data, acnt_val_data, acnt_end_val_p, acnt_end_val_year_p, sma1, sma2, sma3, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr, trd_ln, prf_los_per_trd_long, prf_los_per_trd_short, tckr=tckr, strt_dt=strt_dt, end_dt=end_dt, spec_data=spec_data, prc_flg=True, sma_flg=True, ema_flg=False, bb_flg=True, kc_flg=True, acnt_val_flg=True):
    fig, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1, figsize=(16,9), facecolor='lightgrey', gridspec_kw={'height_ratios': [3, 1], 'wspace':0, 'hspace':0}, sharex=True)
    if prc_flg == True:
        ax1.plot(pd.to_datetime(data.loc[strt_dt:end_dt].index), data.loc[strt_dt:end_dt, spec_data], label = ('Price '+spec_data))
    if sma_flg == True:
        ax1.plot(pd.to_datetime(sma1.loc[strt_dt:end_dt].index), sma1.loc[strt_dt:end_dt, list(sma1.columns.values)], label = 'SMA1', alpha = 0.5)
        ax1.plot(pd.to_datetime(sma2.loc[strt_dt:end_dt].index), sma2.loc[strt_dt:end_dt, list(sma2.columns.values)], label = 'SMA2', alpha = 0.5)
        ax1.plot(pd.to_datetime(sma3.loc[strt_dt:end_dt].index), sma3.loc[strt_dt:end_dt, list(sma3.columns.values)], label = 'SMA3', alpha = 0.5)
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
    years = test_length//d_per_y
    months = (test_length - years*d_per_y)//d_per_m
    days = (test_length - years*d_per_y - months*d_per_m)
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax1.text(0.15, 0.9,'Max/Min Value: '+str("{:,}".format(int(np.max(acnt_val_data['account value']))))+' : '+str("{:,}".format(int(np.min(acnt_val_data['account value']))))+'\n' 
                        'Start Balance: '+str("{:,}".format(strt_blnc))+'\n'
                        'Return: '+str("{:,}".format(round(acnt_end_val_p*100,2)))+'%'+'\n'
                        'Avg return per year: '+str("{:,}".format(round(acnt_end_val_year_p*100,2)))+'%',
                        ha='left', va='center', transform=ax1.transAxes, bbox=props, fontsize=7)
    ax1.text(0.3, 0.9,'Total time: '+str(years)+' years '+str(months)+' months '+ str(days) +' days'+'\n'
                        'Average trade length: '+str(round(np.mean(trd_ln),2))+' days'+'\n'
                        'Max/Min trade length: '+str(round(np.max(trd_ln),2))+' days : '+str(round(np.min(trd_ln),2))+' days''\n'
                        'Average profit/loss per trade: '+str("{:,}".format(round(np.mean(prf_los_per_trd_long+prf_los_per_trd_short)*100,2)))+'%'+'\n'
                        'Max/Min profit/loss per trade: '+str("{:,}".format(round(np.max(prf_los_per_trd_long+prf_los_per_trd_short)*100,2)))+'% : '+str("{:,}".format(round(np.min(prf_los_per_trd_long+prf_los_per_trd_short)*100,2)))+'%'+'\n'
                        'Number of trades: '+str(len(prf_los_per_trd_long+prf_los_per_trd_short))+'\n'
                        'Percent of trades profitable/unprofitable: '+str("{:,}".format(round(len(list(filter(lambda i: i > 0, prf_los_per_trd_long+prf_los_per_trd_short)))/len(prf_los_per_trd_long+prf_los_per_trd_short)*100,2)))+'% : '+str("{:,}".format(round(len(list(filter(lambda i: i <= 0, prf_los_per_trd_long+prf_los_per_trd_short)))/len(prf_los_per_trd_long+prf_los_per_trd_short)*100,2)))+'%',
                        ha='left', va='center', transform=ax1.transAxes, bbox=props, fontsize=7)               
    ax1.text(0.5, 0.9,'Average call profit/loss per trade: '+str("{:,}".format(round(np.mean(prf_los_per_trd_long)*100,2)))+'%'+'\n'
                        'Max/Min call profit/loss per trade: '+str("{:,}".format(round(np.max(prf_los_per_trd_long)*100,2)))+'% : '+str("{:,}".format(round(np.min(prf_los_per_trd_long)*100,2)))+'%'+'\n'
                        'Number of call trades: '+str(len(prf_los_per_trd_long))+'\n'
                        'Percent of call trades profitable/unprofitable: '+str("{:,}".format(round(len(list(filter(lambda i: i > 0, prf_los_per_trd_long)))/len(prf_los_per_trd_long)*100,2)))+'% : '+str("{:,}".format(round(len(list(filter(lambda i: i <= 0, prf_los_per_trd_long)))/len(prf_los_per_trd_long)*100,2)))+'%',
                        ha='left', va='center', transform=ax1.transAxes, bbox=props, fontsize=7)
    ax1.text(0.75, 0.9,'Average put profit/loss per trade: '+str("{:,}".format(round(np.mean(prf_los_per_trd_short)*100,2)))+'%'+'\n'
                        'Max/Min put profit/loss per trade: '+str("{:,}".format(round(np.max(prf_los_per_trd_short)*100,2)))+'% : '+str("{:,}".format(round(np.min(prf_los_per_trd_short)*100,2)))+'%'+'\n'
                        'Number of put trades: '+str(len(prf_los_per_trd_short))+'\n'
                        'Percent of put trades profitable/unprofitable: '+str("{:,}".format(round(len(list(filter(lambda i: i > 0, prf_los_per_trd_short)))/len(prf_los_per_trd_short)*100,2)))+'% : '+str("{:,}".format(round(len(list(filter(lambda i: i <= 0, prf_los_per_trd_short)))/len(prf_los_per_trd_short)*100,2)))+'%',
                        ha='left', va='center', transform=ax1.transAxes, bbox=props, fontsize=7)         
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