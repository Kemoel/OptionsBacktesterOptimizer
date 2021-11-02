# Ticker name all caps.
tckr = 'SPY'
# Data source csv or yf.
data_src = 'csv'
# Data start date.
yh_data_strt_dt = '2000-01-01'
# Data end date.
yh_data_end_dt = '2021-10-10'
# Data column to use for calculations. options: 'Open', 'Close', 'High', 'Low', and 'Adj Close'.
spec_data = 'Adj Close'

# Indicator variable values.
# SMA length.
sma1_ln_ini = 8
sma2_ln_ini = 200
# EMA length.
ema1_ln_ini = 21
# BB sma length, std length, and std multiplier.
bb_sma_ln_ini = 14
bb_std_ln_ini = 14
bb_std_mul_ini = 2
# KC sma length, atr length, and atr multiplier.
kc_sma_ln_ini = 3
kc_atr_ln_ini = 14
kc_atr_mul_ini = 1.5
# Momentum length.
momemtum_ln_ini = 9

# Refrence/market compare ticker. options: 'risk free', 'SPY', 'QQQ', 'DIA', and 'IWM'.
ref_tckr = 'risk free'
# Risk free interest rate per year.
rf_i = 0.02
# Risk free interest times compounding period year.
rf_n = 1
# Days per year for interest calculation.
d_per_y = 365

# Starting balance.
strt_blnc = 1000
# Starting date for testing.
strt_dt = '1994-01-01'
# End date for testing.
end_dt = '2020-10-10'

# Trading fees.
trd_fee_per_order_buy = 0
trd_fee_per_contract_buy = 0
trd_fee_per_order_sell = 0
trd_fee_per_contract_sell = 0