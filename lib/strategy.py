from lib.print_data import *
from lib.indicators import *
import scipy.optimize as spo
import pandas as pd

def trade_enter(data, momentum, sqz_sig, bs_sig):
    momentum[momentum['momentum'] > 0] = 1
    momentum[momentum['momentum'] < 0] = -1
    enter_data = pd.DataFrame(index = data.index, columns = ['enter signal']).fillna(0)
    enter_data.at[(momentum['momentum'] > 0) & (sqz_sig['sqz signal'] == 1) & (bs_sig['bs signal'] > 0), 'enter signal'] = 1 #long
    enter_data.at[(momentum['momentum'] < 0) & (sqz_sig['sqz signal'] == 1) & (bs_sig['bs signal'] < 0), 'enter signal'] = -1 #short
    return enter_data

def trade_exit(data, spec_data, sma1, sma2):
    kc_upr_lim = kc(data, spec_data, 'upr', 21, 21, 3)
    kc_lwr_lim = kc(data, spec_data, 'low', 21, 21, 3)
    exit_data = pd.DataFrame(index = data.index, columns = ['exit signal']).fillna(0)
    exit_data.at[(data[spec_data] > kc_upr_lim['kc']) | ((sma1['sma'] > sma2['sma']) & (data[spec_data] < sma2['sma'])), 'exit signal'] = 1 #long gain and los
    exit_data.at[(data[spec_data] < kc_lwr_lim['kc']) | ((sma1['sma'] < sma2['sma']) & (data[spec_data] > sma2['sma'])), 'exit signal'] = -1 #short gain and loss
    return exit_data

def trade_strat(data, spec_data, sma1, sma2, momentum, sqz_sig, bs_sig):
    trd_entr = trade_enter(data, momentum, sqz_sig, bs_sig)
    trd_ext = trade_exit(data, spec_data, sma1, sma2)
    trade_data = pd.DataFrame(index = data.index, columns = ['trade enter price' ,'trade exit price', 'in trade', 'trade value']).fillna(0)
    trade_data.at[trd_entr['enter signal'] == 1, 'trade enter price'] = data['Adj Close'] * (1) #long
    trade_data.at[trd_entr['enter signal'] == -1, 'trade enter price'] = data['Adj Close'] * (-1) #short
    trade_data.at[trd_ext['exit signal'] == 1, 'trade exit price'] = data['Adj Close'] * (1) #long
    trade_data.at[trd_ext['exit signal'] == -1, 'trade exit price'] = data['Adj Close'] * (-1) #short
    trade_data.at[trade_data['trade enter price'] > 0, 'in trade'] = 1 #long
    trade_data.at[trade_data['trade enter price'] < 0, 'in trade'] = -1 #short
    flg = 0
    for row in trade_data.itertuples():
        if ((row._3 != 0) & (row._2 == 0)):
            flg = 1
        if ((row._2 != 0) & (flg != 0)):
            trade_data.loc[row.Index, 'in trade'] = row._2/abs(row._2)
            flg = 0
    # trade value, open long -, close long +, open short +, close short -
    trade_data['trade value'] = (trade_data['in trade'] * trade_data['trade enter price'] * (-1)) + (trade_data['in trade'] * trade_data['trade exit price'] )
    return trade_data
