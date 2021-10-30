from input.initialization import *
import numpy as np
import pandas as pd

def ma(data, type, ma_ln, spec_data=spec_data):
    ma_data = pd.DataFrame(index = data.index, columns = [type]).fillna(0)
    if type == 'sma':
        ma_data[type] = data[spec_data].rolling(window=ma_ln).mean()
        return ma_data
    elif type == 'ema':
        ma_data[type] = data[spec_data].ewm(span=ma_ln).mean()
        return ma_data

def bb(data, upr_low, ma_ln, std_ln, std_mul, spec_data=spec_data):
    bb_data = pd.DataFrame(index = data.index, columns = ['bb']).fillna(0)
    bb_data1 = ma(data, 'sma', ma_ln)['sma']
    bb_data2 = data[spec_data].rolling(window=std_ln).std() * std_mul
    if upr_low == 'upr':
        bb_data['bb'] = bb_data1 + bb_data2
        return bb_data
    elif upr_low == 'low':
        bb_data['bb'] = bb_data1 - bb_data2
        return bb_data

def kc(data, upr_low, atr_ln, ma_ln, atr_mul):
    high_low = data['High'] - data['Low']
    high_cls = np.abs(data['High'] - data['Close'].shift())
    low_cls = np.abs(data['Low'] - data['Close'].shift())
    rngs = pd.concat([high_low, high_cls, low_cls], axis=1)
    tru_rng = np.max(rngs, axis=1)
    tru_rng_df = pd.DataFrame(tru_rng , columns = ['kc'])
    kc_data = pd.DataFrame(index = data.index, columns = ['kc']).fillna(0)
    kc_data1 = ma(data, 'sma', ma_ln)['sma']
    kc_data2 = tru_rng_df['kc'].rolling(atr_ln).sum()/atr_ln * atr_mul
    if upr_low == 'upr':
        kc_data['kc'] = kc_data1 + kc_data2
        return kc_data
    elif upr_low == 'low':
        kc_data['kc'] = kc_data1 - kc_data2
        return kc_data

def momen(data, momen_ln, spec_data=spec_data):
    momen_data = pd.DataFrame(index = data.index, columns = ['momentum']).fillna(0)
    momen_data['momentum'] = data[spec_data] - data[spec_data].shift(momen_ln)
    return momen_data

def sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr):
    sqz_data = pd.DataFrame(index = data.index, columns = ['sqz signal']).fillna(0)
    sqz_data[(bb_upr['bb']<= kc_upr['kc']) & (bb_lwr['bb']>=kc_lwr['kc'])] = 1
    return sqz_data

def bs_rng(data, sma1, sma2, spec_data=spec_data):
    bs_data = pd.DataFrame(index = data.index, columns = ['bs signal']).fillna(0)
    bs_data[(data[spec_data] <= sma1['sma']) & (data[spec_data] >= sma2['sma']) & (sma1['sma'] > sma2['sma'])] = 1
    bs_data[(data[spec_data] >= sma1['sma']) & (data[spec_data] <= sma2['sma']) & (sma1['sma'] < sma2['sma'])] = -1     
    return bs_data
