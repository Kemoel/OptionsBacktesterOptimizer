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

# Account value dataframe with starting balance for dates specified.
def acnt_val(trd_data, strt_dt=strt_dt, end_dt=end_dt):
    account_value = pd.DataFrame(index = trd_data.index, columns = ['account value']).fillna(0)
    account_value['account value'] = trd_data['trade value']
    account_value.iat[0,0] = strt_blnc
    account_value = account_value.cumsum()
    return account_value

# Account perecent return for specified dates.
def acnt_end_p(acnt_val_data):
    acnt_end_val_p = acnt_val_data.iat[-1,0] / strt_blnc
    return acnt_end_val_p

# Account return standard deviation for specified days.
def acnt_end_std(acnt_val_data):
    acnt_std_val_p = acnt_val_data['account value'].std() / strt_blnc
    return acnt_std_val_p

# Account return sharpe ratio for specified days vs specified refrence ticker.
def shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std_p):
    shrp_rt_val = (acnt_end_val_p - ref_return_val_p) / acnt_end_val_std_p
    return shrp_rt_val