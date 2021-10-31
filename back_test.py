from input.initialization import *
from lib.account_metrics import *
from lib.import_data import *
from lib.indicators import *
from lib.strategy import *
from lib.print_data import *

# Data for ticker from data start to end date range. open, close, high, low, adj close, volume.
data = get_data()

# Simple moving average for adj close 8 and 34 day.
sma1 = ma(data, 'sma', 8)
sma2 = ma(data, 'sma', 34)

# Exponential moving average for adj close 21 day.
ema1 = ma(data, 'ema', 21)

# Bollinger bands for adj close 21 day sma, 21 day std, and 2X std.
bb_upr = bb(data, 'upr', 21, 21, 2)
bb_lwr = bb(data, 'low', 21, 21, 2)

# Keltner channel for adj close 21 day sma, 21 day atr, and 2X atr.
kc_upr = kc(data, 'upr', 21, 21, 1.5)
kc_lwr = kc(data, 'low', 21, 21, 1.5)

# Momentum for adj close 10 day.
momentum = momen(data, 10)

# Squeeze for adj close based on previously specified bollinger bands and keltner channels.
sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)

# Buy/sell signal based on previously specified simple moving averages.
bs_sig = bs_rng(data, sma1, sma2)

# Strategy entry exit calculations dataframe.
trd_data = trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig)

# Trade value dataframe solved for specified dates.
acnt_val_data = acnt_val(data, trd_data)

# Return percentage for refrence ticker for dates specified.
ref_return_val_p = ref_rtrn(ref_tckr)
# Return percentage for account for dates specified.
acnt_end_val_p = acnt_end_p(acnt_val_data)
# Std for account for dates specified.
acnt_end_val_std = acnt_end_std(acnt_val_data)
# Sharpe ratio for account for dates specified.
shrp_rt = shrp_ratio(acnt_end_val_p, ref_return_val_p, acnt_end_val_std)

# Graph out all required indicators.
prt_grph(data, acnt_val_data, sma1, sma2, ema1, bb_upr, bb_lwr, kc_upr, kc_lwr)