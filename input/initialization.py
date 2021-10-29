import pandas as pd
from lib.import_data import get_data

# Ticker name all caps.
tckr = 'SPY'
# Data source csv or yf.
data_src = 'csv'
# Data start date.
data_strt_dt = '2000-01-01'
# Data end date.
data_end_dt = '2021-10-10'
# Data column to use for calculations. options: 'Open', 'Close', 'High', 'Low', and 'Adj Close'.
spec_data = 'Adj Close'

# Refrence/market compare ticker. options: 'risk free', 'SPY', 'QQQ', 'DIA', and 'IWM'.
ref_tckr = 'risk free'
# Risk free interest rate per year.
rf_i = 0.02
# Risk free interest times compounding period year.
rf_n = 1

# Starting balance.
strt_blnc = 1000
# Starting date for testing.
strt_dt = '2019-01-01'
# End date for testing.
end_dt = '2021-01-01'

# Days per year for interest calculation.
d_per_y = 365