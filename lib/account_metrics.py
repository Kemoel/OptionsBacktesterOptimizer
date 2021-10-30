from input.initialization import *
from lib.import_data import *
from lib.print_data import *

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
    account_value = pd.DataFrame(index = (trd_data.loc[strt_dt:end_dt].index), columns = ['trade value', 'cash value', 'position value', 'account value']).fillna(0)
    account_value['trade value'] = trd_data['trade value']
    account_value.iat[0,1] = strt_blnc
    # Open dates list.
    open_dt = (trd_data['trade loc/typ'].loc[strt_dt:end_dt])[trd_data['trade loc/typ'] == 1]
    # Exit dates list.
    close_dt = (trd_data['trade loc/typ'].loc[strt_dt:end_dt])[trd_data['trade loc/typ'] == -1]
    # Check first open date is before first close date. If not delete first close.
    if (open_dt.index[0] > close_dt.index[0]):
        account_value.at[close_dt.index[0],'trade value'] = 0
        close_dt = close_dt.drop(close_dt.index[0])
    # Check last close date is after last open date. If not delete last open.
    if ((open_dt.index[-1] > close_dt.index[-1]) & (end_open_pos_flg == 1)):
        account_value.at[open_dt.index[-1],'trade value'] = 0
        open_dt = open_dt.drop(open_dt.index[-1])
    # Cumalitive addition of trades and profit/loss.
    account_value = acnt_val_cumsum_max(data, account_value)
    print_all(account_value)
    return account_value

# Cumalitave addition on trade gain and loss. Maximized contracts.
def acnt_val_cumsum_max(data, account_value):
    account_value['cash value'] += account_value['trade value']
    num_contract = 0
    for i in range(1,len(account_value)):
        # Opening trade
        if ((account_value.iat[i,1] != 0) & (num_contract == 0)):
            num_contract = account_value.iat[i-1,1] // abs(account_value.iat[i,1])
            account_value.iat[i,2] = account_value.iat[i,0] * num_contract * (-1)
            account_value.iat[i,1] = (account_value.iat[i,1] * num_contract) + account_value.iat[i-1,1]
        # Closing trade
        elif ((account_value.iat[i,1] != 0) & (num_contract != 0)):
            account_value.iat[i,2] = 0
            account_value.iat[i,1] = (account_value.iat[i,1] * num_contract) + account_value.iat[i-1,1]
            num_contract = 0
        # No trade
        else :
            if (num_contract != 0):
                account_value.iat[i,2] = data.loc[account_value.iloc[i].name,'Adj Close'] * (num_contract)
            account_value.iat[i,1] = account_value.iat[i-1,1]
    account_value['account value'] = account_value['cash value'] + account_value['position value']    
    return account_value

# Account perecent return for specified dates.
def acnt_end_p(acnt_val_data):
    acnt_end_val_p = acnt_val_data.iat[-1,3] / strt_blnc - 1
    return acnt_end_val_p

# Account return standard deviation for specified days.
def acnt_end_std(acnt_val_data):
    acnt_std_val_p = (acnt_val_data['account value']-strt_blnc).std()
    return acnt_std_val_p

# Account return sharpe ratio for specified days vs specified refrence ticker.
def shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std):
    shrp_rt_val = (acnt_end_val_p - ref_return_val_p) / acnt_end_val_std
    return shrp_rt_val