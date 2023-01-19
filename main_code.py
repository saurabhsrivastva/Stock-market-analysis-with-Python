from tvDatafeed import TvDatafeed,Interval
import pandas as pd
import numpy as np
from datetime import datetime
from pandas import DataFrame,Series
import matplotlib.pyplot as plt

#displaying all the rows and columns
pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 891)

username = 'Your id from trading view'
password = 'your password from trading view'
tv = TvDatafeed(username,password)
NIFTY_5m = tv.get_hist('NIFTY','NSE', Interval.in_5_minute,n_bars=4875,fut_contract=1,extended_session=False)
#random data is collected, so removing first day data
NIFTY_5m = NIFTY_5m[NIFTY_5m.index.date>NIFTY_5m.index.date[0]]
NIFTY_1d = tv.get_hist('NIFTY','NSE', Interval.in_daily,n_bars=70,fut_contract=1,extended_session=False)
#reindexing & deleting useless column
del NIFTY_5m['symbol']
NIFTY_5m.index = pd.MultiIndex.from_arrays([NIFTY_5m.index.date, NIFTY_5m.index.time], names=['Date','Time'])
print(NIFTY_5m)
#print(NIFTY_1d)


#CPR plotting on daily data
NIFTY_1d_CPR = pd.DataFrame()
NIFTY_1d_CPR['TC'] = (NIFTY_1d['high'] + NIFTY_1d['low'])/2
NIFTY_1d_CPR['PP'] = (NIFTY_1d['high'] + NIFTY_1d['low'] + NIFTY_1d['close'])/3
NIFTY_1d_CPR['BC'] = (NIFTY_1d_CPR['PP'] - NIFTY_1d_CPR['TC']) + NIFTY_1d_CPR['PP']
NIFTY_1d_CPR['TC_actual'] = NIFTY_1d_CPR['TC']
NIFTY_1d_CPR['BC_actual'] = NIFTY_1d_CPR['BC']
for i in NIFTY_1d_CPR.index:
    if NIFTY_1d_CPR['BC'][i] > NIFTY_1d_CPR['TC'][i]:
        NIFTY_1d_CPR['TC'][i] = NIFTY_1d_CPR['BC'][i]
        NIFTY_1d_CPR['BC'][i] = NIFTY_1d_CPR['TC_actual'][i]
del NIFTY_1d_CPR['TC_actual']
del NIFTY_1d_CPR['BC_actual']

NIFTY_1d_CPR.index = NIFTY_1d_CPR.index.date
NIFTY_1d_CPR.index.name = 'Date'
NIFTY_1d_CPR = NIFTY_1d_CPR.shift(periods=1)
#print(NIFTY_1d_CPR)

#Merging CPR with 5m data
NIFTY_5m = pd.merge(NIFTY_5m,NIFTY_1d_CPR,left_index=True,right_index=True)
print(NIFTY_5m)

#Finding four consective green bars on 6th
l=0
A1 = 0
strong_trends = 0
for ind in NIFTY_5m.index:
    if NIFTY_5m['open'][ind] < NIFTY_5m['close'][ind]:
        l=l+1
    else:
        l = 0
    if l==4:
            strong_trends = strong_trends+1
            if (NIFTY_5m['close'][ind] > NIFTY_5m['TC'][ind]) and (NIFTY_5m['open'][ind] < NIFTY_5m['TC'][ind]):
                A1 = A1+1
                print(ind)

print('No. of bullish A1 Cpr setup = ' + str(A1))

#Finding four consective bearish bars on 6th
lb=0
A1b = 0
strong_trends_b = 0
for ind in NIFTY_5m.index:
    if NIFTY_5m['open'][ind] > NIFTY_5m['close'][ind]:
        lb=lb+1
    else:
        lb = 0
    if lb==4:
            strong_trends_b = strong_trends_b+1
            if (NIFTY_5m['close'][ind] < NIFTY_5m['BC'][ind]) and (NIFTY_5m['open'][ind] > NIFTY_5m['BC'][ind]):
                A1b = A1b+1
                print(ind)

print('No. of bearish A1 Cpr setup = ' + str(A1b))


