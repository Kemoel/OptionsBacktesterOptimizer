from input.initialization import *
from lib.account_metrics import *
from lib.import_data import *
from lib.indicators import *
from lib.strategy import *
from lib.print_data import *
import time

# Beggining of timer.
# t0 = time.time()

# Data for ticker from data start to end date range. open, close, high, low, adj close, volume.
data = get_data()

# Simple moving average for adj close 8 and 34 day.
sma1 = sma(data, sma1_ln_ini)
sma2 = sma(data, sma2_ln_ini)

# Exponential moving average for adj close 21 day.
ema1 = ema(data, ema1_ln_ini)

# Bollinger bands for adj close 21 day sma, 21 day std, and 2X std.
bb_upr = bb(data, 'upr', bb_sma_ln_ini, bb_std_ln_ini, bb_std_mul_ini)
bb_lwr = bb(data, 'low', bb_sma_ln_ini, bb_std_ln_ini, bb_std_mul_ini)

# Keltner channel for adj close 21 day sma, 21 day atr, and 2X atr.
kc_upr = kc(data, 'upr', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
kc_lwr = kc(data, 'low', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)

# Momentum for adj close 10 day.
momentum = momen(data, momemtum_ln_ini)

# Squeeze for adj close based on previously specified bollinger bands and keltner channels.
sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)

# Buy/sell signal based on previously specified simple moving averages.
bs_sig = bs_rng(data, sma1, sma2)

# Strategy entry exit calculations dataframe.
trd_data = jfc_trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig)

 # Test if there are trades in range and return account info. If not return 0 for return.
if(trd_data['trade loc/typ'].loc[strt_dt:end_dt].any()):
    # Trade value dataframe solved for specified dates.
    acnt_val_data = acnt_val(data, trd_data)
    # Return percentage for account for dates specified.
    acnt_end_val_p = acnt_end_p(acnt_val_data)
    # Std for account for dates specified.
    acnt_end_val_std = acnt_end_std(acnt_val_data)
else:
    acnt_end_val_p = 0
    acnt_end_val_std = 0
    print('No trades for initilization values specified')
# Return percentage for refrence ticker for dates specified.
ref_return_val_p = ref_rtrn(ref_tckr)
# Sharpe ratio for account for dates specified.
shrp_rt = shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std)

# Print time taken.
# print(time.time()-t0)

# Graph out all required indicators.
prt_grph(data, acnt_val_data, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr)