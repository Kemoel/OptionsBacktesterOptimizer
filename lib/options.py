from lib.print_data import *
from lib.import_data import *
import scipy.stats as sp
import numpy as np

# Have to create new function to account for options expiring before sell signal.

# Calculate value of option based on Black-Scholes method. No diveden considered and european style option.
def call_option_prc(S, K, T, r, q, sigma):
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #q: rate of continuous dividend paying asset 
    #sigma: volatility of underlying asset
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    call_prc = (S * np.exp(-q * T) * sp.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * sp.norm.cdf(d2, 0.0, 1.0))
    return (call_prc * 100)

def put_option_prc(S, K, T, r, q, sigma):
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #q: rate of continuous dividend paying asset 
    #sigma: volatility of underlying asset
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    put_prc = (K * np.exp(-r * T) * sp.norm.cdf(-d2, 0.0, 1.0) - S * np.exp(-q * T) * sp.norm.cdf(-d1, 0.0, 1.0))
    return (put_prc * 100)

# Cumalitave addition on trade gain and loss for options. Options info: . Maximized contracts. Slower dataframe code. Ends trade early if option expiring next day.
def acnt_val_cumsum_max_options(data, spec_data, account_value):
    # print_all(account_value)
    volitility_df = get_volitility_data(spec_data)/100
    # Initilization of variables.
    num_contract = 0
    strk_prc = 0
    end_early_flg = 0
    prf_los_per_trd_call = []
    prf_los_per_trd_put = []
    trd_ln = []
    trd_strt_dt = pd.to_datetime(strt_dt)
    for i in range(1,len(account_value)):
        # Opening trade
        if ((account_value.iat[i,0] != 0) & (num_contract == 0)):
            # Call trade.
            if(account_value.iat[i,0] < 0):
                strk_prc = np.ceil(abs(account_value.iat[i,0])*(1-delta_strike))
                call_prc = call_option_prc(abs(account_value.iat[i,0]), strk_prc, time_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                num_contract = ((account_value.iat[i-1,1] * prcnt_acnt_use_options) // call_prc)
                account_value.iat[i,1] = account_value.iat[i-1,1] - (call_prc * num_contract)
                account_value.iat[i,2] = call_prc * num_contract
            # Put trade.
            elif(account_value.iat[i,0] > 0):
                strk_prc = np.floor(abs(account_value.iat[i,0])*(1+delta_strike))
                put_prc = put_option_prc(abs(account_value.iat[i,0]), strk_prc, time_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                num_contract = ((account_value.iat[i-1,1] * prcnt_acnt_use_options)// put_prc) * (-1)
                account_value.iat[i,1] = account_value.iat[i-1,1] - (put_prc * num_contract * (-1))
                account_value.iat[i,2] = put_prc * num_contract * (-1)
            trd_strt_dt = pd.to_datetime(account_value.iloc[i].name)
        # Bypass regular close when closing early due to expiry.
        elif((account_value.iat[i,0] != 0) & (num_contract != 0) & (end_early_flg == 1)):
            end_early_flg = 0   
            num_contract = 0  
            account_value.iat[i,1] = account_value.iat[i-1,1]   
            account_value.iat[i,3] = account_value.iat[i-1,3]
        # Closing trade strat.
        elif((account_value.iat[i,0] != 0) & (num_contract != 0)):
            # Call trade.
            if(num_contract > 0):
                time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                call_prc = call_option_prc(abs(account_value.iat[i,0]), strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                account_value.iat[i,1] = account_value.iat[i-1,1] + (call_prc * num_contract)
                prf_los_per_trd_call.append(((account_value.iat[i-1,2]+account_value.iat[i-1,1])/(account_value.iat[i-1,1]/(1-prcnt_acnt_use_options)))-1)
            # Put trade.
            elif(num_contract < 0):
                time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                put_prc = put_option_prc(abs(account_value.iat[i,0]), strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                account_value.iat[i,1] = account_value.iat[i-1,1] + (put_prc * num_contract * (-1))
                prf_los_per_trd_put.append(((account_value.iat[i-1,2]+account_value.iat[i-1,1])/(account_value.iat[i-1,1]/(1-prcnt_acnt_use_options)))-1)
            account_value.iat[i,2] = 0
            num_contract = 0  
            strk_prc = 0
            trd_ln.append((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days)
            trd_strt_dt = pd.to_datetime(strt_dt)
        # In trade, no trade.
        else :
            if(end_early_flg == 0):
                # Call trade.
                if(num_contract > 0):
                    time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                    call_prc = call_option_prc(data.loc[account_value.iloc[i].name,spec_data], strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                    account_value.iat[i,2] = call_prc * num_contract
                # Put trade.
                elif(num_contract < 0):
                    time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                    put_prc = put_option_prc(data.loc[account_value.iloc[i].name,spec_data], strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                    account_value.iat[i,2] = put_prc * num_contract * (-1)
            else:
                account_value.iat[i,2] = 0
            #Not in trade.
            account_value.iat[i,1] = account_value.iat[i-1,1]
            # Closing trade, option expiring. Or option decay too much.
            if ((num_contract != 0) & (i < (len(account_value)-1)) & (account_value.iat[i,0] == 0) & (end_early_flg == 0)):
                if((time_exp-((pd.to_datetime(account_value.iloc[(i+1)].name)-trd_strt_dt).days/365) < 0) | (account_value.iat[i,2]<(account_value.iat[i,1]/(1-prcnt_acnt_use_options)*prcnt_acnt_use_options*(1-loss_allow)))):
                    # Call trade.
                    if(num_contract > 0):
                        time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                        call_prc = call_option_prc(data.loc[account_value.iloc[i].name,spec_data], strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                        account_value.iat[i,1] = account_value.iat[i-1,1] + (call_prc * num_contract)
                        prf_los_per_trd_call.append(((account_value.iat[i-1,2]+account_value.iat[i-1,1])/(account_value.iat[i-1,1]/(1-prcnt_acnt_use_options)))-1)
                    # Put trade.
                    elif(num_contract < 0):
                        time_to_exp = time_exp-((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days/365)
                        put_prc = put_option_prc(data.loc[account_value.iloc[i].name,spec_data], strk_prc, time_to_exp, interest_rate, div_yield, volitility_df.at[volitility_df.iloc[i].name,spec_data])
                        account_value.iat[i,1] = account_value.iat[i-1,1] + (put_prc * num_contract * (-1))
                        prf_los_per_trd_put.append(((account_value.iat[i-1,2]+account_value.iat[i-1,1])/(account_value.iat[i-1,1]/(1-prcnt_acnt_use_options)))-1)
                    account_value.iat[i,2] = 0
                    end_early_flg = 1
                    
                    trd_ln.append((pd.to_datetime(account_value.iloc[i].name)-trd_strt_dt).days)
                    trd_strt_dt = pd.to_datetime(strt_dt)
    account_value['account value'] = account_value['cash balance'] + account_value['position value']
    # print_all(account_value)
    return account_value, trd_ln, prf_los_per_trd_call, prf_los_per_trd_put