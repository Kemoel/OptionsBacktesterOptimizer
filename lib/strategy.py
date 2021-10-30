from input.initialization import *
from lib.print_data import *
from lib.indicators import *
import pandas as pd

def trade_enter(data, momentum, sqz_sig, bs_sig):
    momentum[momentum['momentum'] > 0] = 1
    momentum[momentum['momentum'] < 0] = -1
    enter_data = pd.DataFrame(index = data.index, columns = ['enter signal']).fillna(0)
    enter_data.at[(momentum['momentum'] > 0) & (sqz_sig['sqz signal'] == 1) & (bs_sig['bs signal'] > 0), 'enter signal'] = 1 # Long
    enter_data.at[(momentum['momentum'] < 0) & (sqz_sig['sqz signal'] == 1) & (bs_sig['bs signal'] < 0), 'enter signal'] = -1 # Short
    return enter_data

def trade_exit(data, sma1, sma2, spec_data=spec_data):
    kc_upr_lim = kc(data, 'upr', 21, 21, 3)
    kc_lwr_lim = kc(data, 'low', 21, 21, 3)
    exit_data = pd.DataFrame(index = data.index, columns = ['exit signal']).fillna(0)
    exit_data.at[(data[spec_data] > kc_upr_lim['kc']) | ((sma1['sma'] > sma2['sma']) & (data[spec_data] < sma2['sma'])), 'exit signal'] = 1 # Long gain and loss
    exit_data.at[(data[spec_data] < kc_lwr_lim['kc']) | ((sma1['sma'] < sma2['sma']) & (data[spec_data] > sma2['sma'])), 'exit signal'] = -1 # Short gain and loss
    return exit_data

def trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig):
    trd_entr = trade_enter(data, momentum, sqz_sig, bs_sig)
    trd_ext = trade_exit(data, sma1, sma2)
    trade_data = pd.DataFrame(index = data.index, columns = ['trade enter price' ,'trade exit price', 'trade loc/typ', 'trade value']).fillna(0)
    trade_data.at[trd_entr['enter signal'] == 1, 'trade enter price'] = data['Adj Close'] * (1) # Long
    trade_data.at[trd_entr['enter signal'] == -1, 'trade enter price'] = data['Adj Close'] * (-1) # Short
    trade_data.at[trd_ext['exit signal'] == 1, 'trade exit price'] = data['Adj Close'] * (1) # Long
    trade_data.at[trd_ext['exit signal'] == -1, 'trade exit price'] = data['Adj Close'] * (-1) # Short
    trd_flg = 0
    # Trade loc/typ: open long/short +, close long/short -.
    for row in trade_data.itertuples():
        # Long/short trade open.
        if ((row._1 != 0) & (trd_flg == 0)):
            trade_data.at[row.Index, 'trade loc/typ'] = 1
            trd_flg = 1
        # Long/short trade close.
        if ((row._2 != 0) & (trd_flg == 1)):
            trade_data.at[row.Index, 'trade loc/typ'] = -1
            trd_flg = 0
    # Trade value: open long -, close long +, open short +, close short -.
    trade_data['trade value'] = ((trade_data['trade loc/typ'] * trade_data['trade enter price']) + (trade_data['trade loc/typ'] * trade_data['trade exit price'])) * (-1)
    return trade_data
