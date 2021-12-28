# Ticker name all caps.
tckr = 'SPY'
# Data source folder.
data_src_folder = '1day'
# Data source type csv, txt, or yf.
data_src_type = 'csv'
# Data yahoo start date.
yh_data_strt_dt = '2000-01-01'
# Data yahoo end date.
yh_data_end_dt = '2021-10-10'
# Data column to use for calculations. options: 'Open', 'Close', 'High', 'Low', and 'Adj Close'.
spec_data = 'Adj Close'

# Indicator variable values.
# SMA length.
sma1_ln_ini = 8
sma2_ln_ini = 200
sma3_ln_ini = 300
# EMA length.
ema1_ln_ini = 21
# BB sma length, std length, and std multiplier.
bb_sma_ln_ini = 14
bb_std_ln_ini = 14
bb_std_mul_ini = 2
# KC sma length, atr length, and atr multiplier. For sqz.
kc_sma_ln_ini = 3
kc_atr_ln_ini = 14
kc_atr_mul_ini = 1.5
# KC sma length, atr length, and atr multiplier. For strat exit.
kc_sma_ln_exit = 14
kc_atr_ln_exit = 14
kc_atr_mul_exit = 2
# Momentum length.
momemtum_ln_ini = 9

# Days in squeeze for strategy.
sqz_strat_ln = 0

# Refrence/market compare ticker. options: 'risk free', 'SPY', 'QQQ', 'DIA', and 'IWM'.
ref_tckr = 'risk free'
# Risk free interest rate per year.
rf_i = 0.02
# Risk free interest times compounding period year.
rf_n = 1
# Days per year for interest calculation.
d_per_y = 365
# Days per month.
d_per_m = 30

# Starting balance.
strt_blnc = 10000
# Starting date for testing.
strt_dt = '1994-01-01'
# End date for testing.
end_dt = '2021-10-10'

# Volitility ticker name all caps.
tckr_volitlity = '^VIX'

# Percent of underlying price. + in the money, - out the money.
delta_strike = -0.01
# Years to expiry.
time_exp = 3/12
# Risk free interest rate.
interest_rate = rf_i 
# Dividend of underlying.
div_yield = 0.0123
# Volitility of underlying.
volitility_con = 0.16
# Percent of account used on each trade.
prcnt_acnt_use_options = 0.2
# Loss of value allowed on contract
loss_allow = 0.5

# Trading fees.
trd_fee_per_order_buy = 0
trd_fee_per_contract_buy = 0
trd_fee_per_order_sell = 0
trd_fee_per_contract_sell = 0