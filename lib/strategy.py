from input.initialization import *
from lib.print_data import *
from lib.indicators import *
import pandas as pd

def jfc_trade_enter(data, sma3, momentum, sqz_sig, bs_sig):
    momentum[momentum['momentum'] > 0] = 1
    momentum[momentum['momentum'] < 0] = -1
    enter_data = pd.DataFrame(index = data.index, columns = ['enter signal']).fillna(0)
    # print('********',(momentum['momentum'] > 0) & (sqz_sig['sqz signal'] == 1) & (sqz_sig['sqz signal'].shift(sqz_strat_ln) == 1) & (bs_sig['bs signal'] > 0) & (data[spec_data] > sma3['sma']))
    enter_data.loc[(momentum['momentum'] > 0) & (sqz_sig['sqz signal'] == 1) & (sqz_sig['sqz signal'].shift(sqz_strat_ln) == 1) & (bs_sig['bs signal'] > 0) & (data[spec_data] > sma3['sma']), 'enter signal'] = 1 # Long enter
    enter_data.loc[(momentum['momentum'] < 0) & (sqz_sig['sqz signal'] == 1) & (sqz_sig['sqz signal'].shift(sqz_strat_ln) == 1) & (bs_sig['bs signal'] < 0) & (data[spec_data] < sma3['sma']), 'enter signal'] = -1 # Short enter
    return enter_data

def jfc_trade_exit(data, sma1, sma2, spec_data=spec_data):
    kc_upr_lim_exit = kc(data, 'upr', kc_sma_ln_exit, kc_atr_ln_exit, kc_atr_mul_exit)
    kc_lwr_lim_exit = kc(data, 'low', kc_sma_ln_exit, kc_atr_ln_exit, kc_atr_mul_exit)
    exit_data = pd.DataFrame(index = data.index, columns = ['exit signal']).fillna(0)
    exit_data.loc[(data[spec_data] > kc_upr_lim_exit['kc']) | ((sma1['sma'] > sma2['sma']) & (data[spec_data] < sma2['sma'])) , 'exit signal'] = 1 # Long take gain and loss
    exit_data.loc[(data[spec_data] < kc_lwr_lim_exit['kc']) | ((sma1['sma'] < sma2['sma']) & (data[spec_data] > sma2['sma'])) , 'exit signal'] = -1 # Short take gain and loss
    return exit_data

def trade_strat(data, sma1, sma2, sma3, momentum, sqz_sig, bs_sig, spec_data=spec_data):
    trd_entr = jfc_trade_enter(data, sma3, momentum, sqz_sig, bs_sig)
    trd_ext = jfc_trade_exit(data, sma1, sma2)
    trade_data = pd.DataFrame(index = data.index, columns = ['trade enter price' ,'trade exit price', 'trade loc/typ', 'stock price']).fillna(0)
    trade_data.loc[trd_entr['enter signal'] == 1, 'trade enter price'] = data[spec_data] * (1) # Long
    trade_data.loc[trd_entr['enter signal'] == -1, 'trade enter price'] = data[spec_data] * (-1) # Short
    trade_data.loc[trd_ext['exit signal'] == 1, 'trade exit price'] = data[spec_data] * (1) # Long
    trade_data.loc[trd_ext['exit signal'] == -1, 'trade exit price'] = data[spec_data] * (-1) # Short
    trd_flg = 0 # In trade long 1. In short -1.
    # Trade loc/typ: open long/short +, close long/short -.
    for row in trade_data.itertuples():
        # Long trade open.
        if ((row._1 > 0) & (trd_flg == 0)):
            trade_data.loc[row.Index, 'trade loc/typ'] = 1
            trd_flg = 1
        # Long trade close.
        elif ((row._2 > 0) & (trd_flg == 1)):
            trade_data.loc[row.Index, 'trade loc/typ'] = -1
            trd_flg = 0
        # Short trade open.
        if ((row._1 < 0) & (trd_flg == 0)):
            trade_data.loc[row.Index, 'trade loc/typ'] = 1
            trd_flg = -1
        # Short trade close.
        elif ((row._2 < 0) & (trd_flg == -1)):
            trade_data.loc[row.Index, 'trade loc/typ'] = -1
            trd_flg = 0
    # Trade value: open long -, close long +, open short +, close short -.
    trade_data['stock price'] = ((trade_data['trade loc/typ'] * trade_data['trade enter price']) + (trade_data['trade loc/typ'] * trade_data['trade exit price'])) * (-1)
    return trade_data
