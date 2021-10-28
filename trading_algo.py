from input.initialization import *
from lib.account_metrics import *
from lib.import_data import *
from lib.indicators import *
from lib.strategy import *
from lib.print_data import *

# Data for ticker from data start to end date range. open, close, high, low, adj close, volume.
data = get_data(data_src, tckr, data_strt_dt, data_end_dt)

# Simple moving average for adj close 8 and 34 day.
sma1 = ma(data, spec_data, 'sma', 8)
sma2 = ma(data, spec_data, 'sma', 34)

# Exponential moving average for adj close 21 day.
ema1 = ma(data, spec_data, 'ema', 21)

# Bollinger bands for adj close 21 day sma, 21 day std, and 2X std.
bb_upr = bb(data, spec_data, 'upr', 21, 21, 2)
bb_lwr = bb(data, spec_data, 'low', 21, 21, 2)

# Keltner channel for adj close 21 day sma, 21 day atr, and 2X atr.
kc_upr = kc(data, spec_data, 'upr', 21, 21, 1.5)
kc_lwr = kc(data, spec_data, 'low', 21, 21, 1.5)

# Momentum for adj close 10 day.
momentum = momen(data, spec_data, 10)

# Squeeze for adj close based on previously specified bollinger bands and keltner channels.
sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)

# Buy/sell signal based on previously specified simple moving averages.
bs_sig = bs_rng(data, spec_data, sma1, sma2)

# Strategy entry exit calculations dataframe.
trd_data = trade_strat(data, spec_data, sma1, sma2, momentum, sqz_sig, bs_sig)

# Account value dataframe solved for specified dates.
acnt_val_data = acnt_val(trd_data)

# Return percentage for refrence ticker for dates specified.
ref_return_val_p = ref_rtrn(ref_tckr)
# Return percentage for account for dates specified.
acnt_end_val_p = acnt_end_p(acnt_val_data)
# Std for account for dates specified.
acnt_end_val_std_p = acnt_end_std(acnt_val_data)
# Sharpe ratio for account for dates specified.
shrp_rt = shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std_p)

# Graph out all required indicators.
prt_grph(data, tckr, strt_dt, end_dt, True, True, True, True, True, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr)