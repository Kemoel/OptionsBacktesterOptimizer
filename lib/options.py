from lib.print_data import *
from lib.import_data import *
import scipy.stats as sp
import numpy as np

# Have to create new function to account for options expiring before sell signal.

# Calculate value of option based on Black-Scholes method. No diveden considered and european style option.
def call_option_prc(S, K, T, r, sigma):
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    call_prc = (S * sp.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * sp.norm.cdf(d2, 0.0, 1.0))
    return (call_prc * 100)

def put_option_prc(S, K, T, r, sigma):
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    put_prc = (K * np.exp(-r * T) * sp.norm.cdf(-d2, 0.0, 1.0) - S * sp.norm.cdf(-d1, 0.0, 1.0))
    return (put_prc * 100)

# Cumalitave addition on trade gain and loss for options. Options info: . Maximized contracts. Slower dataframe code.
def acnt_val_cumsum_max_options(data, spec_data, account_value):
    # print_all(account_value)
    # volitility = get_volitility_data()
    # Initilization of variables.
    num_contract = 0
    num_trds = 0
    strk_prc = 0
    trd_strt_dt = pd.to_datetime(strt_dt)
    for i in range(1,len(account_value)):
        # Opening trade
        if ((account_value.iat[i,0] != 0) & (num_contract == 0)):
            # Call trade.
            if(account_value.iat[i,0] < 0):
                strk_prc = np.ceil(abs(account_value.iat[i,0])*(1-delta_strike))
                call_prc = call_option_prc(abs(account_value.iat[i,0]), strk_prc, time_exp, interest_rate, volitility)
                num_contract = ((account_value.iat[i-1,1] * prcnt_acnt_use_options) // call_prc)
                account_value.iat[i,1] = account_value.iat[i-1,1] - (call_prc * num_contract)
                account_value.iat[i,2] = call_prc * num_contract
            # Put trade.
            elif(account_value.iat[i,0] > 0):
                strk_prc = np.floor(abs(account_value.iat[i,0])*(1+delta_strike))
                put_prc = put_option_prc(abs(account_value.iat[i,0]), strk_prc, time_exp, interest_rate, volitility)
                num_contract = ((account_value.iat[i-1,1] * prcnt_acnt_use_options)// put_prc) * (-1)
                account_value.iat[i,1] = account_value.iat[i-1,1] - (put_prc * num_contract * (-1))
                account_value.iat[i,2] = put_prc * num_contract * (-1)
            trd_strt_dt = pd.to_datetime(account_value.iloc[i].name)
            num_trds +=1
        # Closing trade option expiring. Have to fix.
        # elif ((num_contract != 0) & (i != len(account_value)) & (time_exp-((pd.to_datetime(account_value.iloc[(i+1)].name)-trd_strt_dt).days/365) < 0)):
        #     trd_strt_dt = pd.to_datetime(account_value.iloc[i].name)
        # Closing trade strat.
        elif ((account_value.iat[i,0] != 0) & (num_contract != 0)):
            time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
            call_prc = call_option_prc(abs(account_value.iat[i,0]), strk_prc, time_to_exp, interest_rate, volitility)
            account_value.iat[i,1] = account_value.iat[i-1,1] + (call_prc * abs(num_contract))
            account_value.iat[i,2] = 0
            num_contract = 0  
            strk_prc = 0
            trd_strt_dt = 0
        # In trade, no trade.
        else :
            if (num_contract != 0):
                time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                call_prc = call_option_prc(data.loc[account_value.iloc[i].name,spec_data], strk_prc, time_to_exp, interest_rate, volitility)
                account_value.iat[i,2] = call_prc * abs(num_contract)
                print(time_to_exp)
            account_value.iat[i,1] = account_value.iat[i-1,1]
    account_value['account value'] = account_value['cash balance'] + account_value['position value']
    print_all(account_value)
    return account_value, num_trds