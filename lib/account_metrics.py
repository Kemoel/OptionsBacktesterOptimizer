from input.initialization import *
from lib.import_data import *
from lib.print_data import *
from lib.options import *
import numpy as np

# Ticker percent return for specified dates.
def rtrn_p(tckr, strt_dt=strt_dt, end_dt=end_dt):
    rtrn_data = get_data('csv', tckr, strt_dt, end_dt)
    rtrn_p_val = rtrn_data.iat[-1,4] / rtrn_data.iat[0,4] - 1
    return rtrn_p_val

# Refrence ticker percent return for specified dates.
def ref_rtrn(ref_tckr_i, strt_dt=strt_dt, end_dt=end_dt):
    d_time = (pd.to_datetime(end_dt) - pd.to_datetime(strt_dt)).days
    if ref_tckr_i == 'risk free':
        rf_rtrn = (1 + rf_i/rf_n) ** (d_time/d_per_y*rf_n) - 1
        return rf_rtrn
    else:
        return rtrn_p(ref_tckr_i)

# Trade value dataframe with starting balance for dates specified.
def acnt_val(data, trd_data, strt_dt=strt_dt, end_dt=end_dt, end_open_pos_flg=0):
    account_value = pd.DataFrame(index = (trd_data.loc[strt_dt:end_dt].index), columns = ['stock price', 'cash balance', 'position value', 'account value']).fillna(0)
    account_value['stock price'] = trd_data['stock price']
    account_value.iat[0,1] = strt_blnc
    avg_trd_ln = 0
    # Open dates list.
    open_dt = (trd_data['trade loc/typ'].loc[strt_dt:end_dt])[trd_data['trade loc/typ'] == 1]
    # Exit dates list.
    close_dt = (trd_data['trade loc/typ'].loc[strt_dt:end_dt])[trd_data['trade loc/typ'] == -1]
    # Check first open date is before first close date. If not delete first close.
    if (open_dt.index[0] > close_dt.index[0]):
        account_value.at[close_dt.index[0],'stock price'] = 0
        close_dt = close_dt.drop(close_dt.index[0])
    # Check last close date is after last open date. If not delete last open.
    if ((open_dt.index[-1] > close_dt.index[-1]) & (end_open_pos_flg == 1)):
        account_value.at[open_dt.index[-1],'stock price'] = 0
        open_dt = open_dt.drop(open_dt.index[-1])
    # Cumalitive addition of trades and profit/loss. Fast and slow options availible.
    # account_value_full, avg_trd_ln, prf_los_per_trd_long, prf_los_per_trd_short = acnt_val_cumsum_max_fast(data, spec_data, account_value)

    account_value_full, avg_trd_ln, prf_los_per_trd_long, prf_los_per_trd_short = acnt_val_cumsum_max_options(data, spec_data, account_value)

    # print_all(account_value)
    return account_value_full, avg_trd_ln, prf_los_per_trd_long, prf_los_per_trd_short

# Cumalitave addition on trade gain and loss. Maximized contracts. Slower dataframe code.
def acnt_val_cumsum_max(data, spec_data, account_value):
    num_contract = 0
    trd_ln = []
    for i in range(1,len(account_value)):
        # Opening trade
        if ((account_value.iat[i,0] != 0) & (num_contract == 0)):
            num_contract = abs(account_value.iat[i-1,1] // abs(account_value.iat[i,0]))
            account_value.iat[i,1] = account_value.iat[i-1,1] - (account_value.iat[i,0] * num_contract * (-1))
            account_value.iat[i,2] = account_value.iat[i,0] * num_contract * (-1)
        # Closing trade
        elif ((account_value.iat[i,0] != 0) & (num_contract != 0)):
            account_value.iat[i,1] = account_value.iat[i-1,1] + (account_value.iat[i,0] * num_contract)
            account_value.iat[i,2] = 0
            num_contract = 0  
        # No trade
        else :
            if (num_contract != 0):
                account_value.iat[i,2] = data.loc[account_value.iloc[i].name,spec_data] * num_contract * np.sign(account_value.iat[i-1,2])
            account_value.iat[i,1] = account_value.iat[i-1,1]
    account_value['account value'] = account_value['cash balance'] + account_value['position value']
    return account_value


# Cumalitave addition on trade gain and loss. Maximized contracts. Faster array code.
def acnt_val_cumsum_max_fast(data_df, spec_data, account_value_df):
    # Dataframe to numpy array for speed.
    account_value_arr = account_value_df.to_numpy()
    data_arr = data_df.to_numpy()
    # Initilization values for tracking and calling.
    data_strt_dt_idx = data_df.index.get_loc(account_value_df.iloc[0].name)
    spec_data_idx = data_df.columns.get_loc(spec_data)
    stk_prc_idx = account_value_df.columns.get_loc('stock price')
    csh_blc_idx = account_value_df.columns.get_loc('cash balance')
    pos_val_idx = account_value_df.columns.get_loc('position value')
    num_contract = 0   
    for i in range(1,len(account_value_arr)):
        # Opening trade
        if ((account_value_arr[i,stk_prc_idx] != 0) & (num_contract == 0)):
            num_contract = abs(account_value_arr[i-1,csh_blc_idx] // abs(account_value_arr[i,stk_prc_idx]))
            account_value_arr[i,csh_blc_idx] = account_value_arr[i-1,csh_blc_idx] - (account_value_arr[i,stk_prc_idx] * num_contract * (-1))
            account_value_arr[i,pos_val_idx] = account_value_arr[i,stk_prc_idx] * num_contract * (-1)
        # Closing trade
        elif ((account_value_arr[i,stk_prc_idx] != 0) & (num_contract != 0)): 
            account_value_arr[i,csh_blc_idx] = account_value_arr[i-1,csh_blc_idx] + (account_value_arr[i,stk_prc_idx] * num_contract)
            account_value_arr[i,pos_val_idx] = 0
            num_contract = 0
        # No trade
        else :
            if (num_contract != 0):
                account_value_arr[i,pos_val_idx] = data_arr[data_strt_dt_idx+i,spec_data_idx] * num_contract * np.sign(account_value_arr[i-1,pos_val_idx])
            account_value_arr[i,csh_blc_idx] = account_value_arr[i-1,csh_blc_idx]
    account_value_df = pd.DataFrame(data = account_value_arr, index = account_value_df.index, columns = account_value_df.columns)
    account_value_df['account value'] = account_value_df['cash balance'] + account_value_df['position value']
    return account_value_df
# Account perecent return for specified dates.
def acnt_end_p(acnt_val_data):
    acnt_end_val_p = acnt_val_data.iat[-1,acnt_val_data.columns.get_loc('account value')]/strt_blnc-1
    acnt_end_val_year_p = (acnt_end_val_p+1)**(1/((pd.to_datetime(end_dt)-pd.to_datetime(strt_dt)).days/365))-1
    return acnt_end_val_p, acnt_end_val_year_p 

# Account return standard deviation for specified days.
def acnt_daily_return_std(acnt_val_data):
    acnt_std_val_p = (acnt_val_data['account value'].pct_change()).std()
    return acnt_std_val_p

# Account return sharpe ratio for specified days vs specified refrence ticker.
def shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std):
    shrp_rt_val = (acnt_end_val_p - ref_return_val_p) / acnt_end_val_std
    return shrp_rt_val