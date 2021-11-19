# -*- coding: utf-8 -*-

# -- Sheet --

# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 22:58:48 2021

@author: TL
"""
import requests
import pandas as pd
from io import StringIO
import datetime
import os
import pandas_ta as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf


total_profit = []

# path = ('C:/Users/yeunglo/OneDrive - The Hong Kong Polytechnic University/Python/投資/company stock information/')
path = ('company stock information/')

for filename in os.listdir(path):
    if filename.endswith('.csv'):
        df = pd.read_csv(str(path) + str(filename))
        print (" ETF - "+str(filename))


################## buy signal ################
    buy = []
    for i in range(len(df)):

        buy_indicator_option = (
                # df['EMA_20'][i] > df['EMA_60'][i] > df['EMA_120'][i]
                # and
                df['close'][i] > df['EMA_20'][i] > df['EMA_60'][i] > df['EMA_120'][i]
                # and
                # df['K_9_3'][i-1] < df['K_9_3'][i-1]
                # and
                # df['K_9_3'][i] >df['D_9_3'][i]
                # and
                # df['K_9_3'][i] >25
                # and
                # df['D_9_3'][i] >45
                # # and
                # # df['K_9_3'][i] < df['K_9_3'][i-1]
                and
                df['RSI_5'][i] >25
        )

        if buy_indicator_option:
            buy.append(1)
        else:
            buy.append(0)

    df["buy"] = buy
    buy.count(1)


    ################## sell signal ##############
    sell =[]
    for i in range (len(df)):

        sell_indicator_option = (
                        df['close'][i] < df['EMA_20'][i]
                        # and
                        # df['close'][i] < df['EMA_20'][i] <df['EMA_60'][i] < df['EMA_120'][i]
                        # and
                        # df['K_9_3'][i] < df['D_9_3'][i]
                        # and
                        # df['K_9_3'][i] < 80
                        #  and
                        # df['K_9_3'][i-1] > df['D_9_3'][i-1]
                        # and
                        # df['K_9_3'][i-1] >85
                        and
                        df['RSI_14'][i] < 40
            )

        if sell_indicator_option:
            sell.append(-1)
        else:
            sell.append(0)

    df["sell"]=sell
    sell.count(-1)

    ################### buy and sell #############

    position = 0  # 倉位, 1 = 持有, 0 = 沒持有

    for i in range(len(df)):
        if position == 0:
            if df["buy"][i] == 1:
                position += 1
                df.loc[[i], "buy_mark"] = (df["high"][i] + 10)  # for buy execute & plot graph marking
                # print("buy done{}".format(str(df.loc[[i], ['close']])))

        if position == 1:
            if df["sell"][i] == -1:
                position -= 1
                df.loc[[i], "sell_mark"] = (df["low"][i] - 10)  # for sell execute & plot graph marking
                # print("sell done{}".format(str(df.loc[[i], ['close']])))

    ######### profit calculiation ############

    cash = 100 #每隻ETF的本金

    buy1 = df.loc[df["buy_mark"].notna()].reset_index()
    sell1 = df.loc[df["sell_mark"].notna()]
    if len(buy1.count()) != len(sell1.count()):
        sell1 = sell1.append(df.iloc[-1:,:]).reset_index()  #如果結算日postion = 1 , 在回測的最後一天當作無條件賣出

    print("買進次數 : " + str(len(buy1)) + "次")
    print("賣出次數 : " + str(len(sell1)) + "次")

    return_rate = []
    for i in range(len(buy1)):
        rate = round((sell1["close"][i] - buy1['close'][i]) / buy1['close'][i]  * 100,2) # 每次交易賺蝕%
        return_rate.append(rate) 
        
        # 本金變化
        cash = cash*(1+(rate/100)) 
    
    return_rate = np.array(return_rate)
    print (return_rate)
    print ("max profit "+str(return_rate.max()))
    print ("max downdraw "+str(return_rate.min()))
    print('total profit '+ str(np.array(return_rate).sum()))
    print('Change of cash: '+ str((round(cash - 100,2))))

     #勝率
    win = len([i for i in return_rate if i > 0])
    lose = len([i for i in return_rate if i <= 0])
    sum_t = len(return_rate)
    print("Win Rate : " + str(round(win / sum_t*100,2)) + "%")

    # 賺蝕百份比相加
    total_profit.append(np.array(return_rate).sum())
    print()
    print()

total_profit = np.array(total_profit)
print("All ETF profit performances = "+ str(total_profit.sum()))

    ####### plot graph #######
    #
    # df.index  = pd.DatetimeIndex(df['dt'])
    # stock_id = "QQQ"
    # mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    # s  = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    # add_plot =[mpf.make_addplot(df["buy_mark"],scatter=True, markersize=50, marker='v', color='r'),
    #            mpf.make_addplot(df["sell_mark"],scatter=True, markersize=50, marker='^', color='g'),
    #            mpf.make_addplot(df["K_9_3"],panel= 2,color="b"),
    #            mpf.make_addplot(df["D_9_3"],panel= 2,color="r")]
    # kwargs = dict(type='candle', volume = True,figsize=(20, 10),title = stock_id, style=s,addplot=add_plot)
    # mpf.plot(df, **kwargs)

from fastquant import get_stock_data

stock = get_stock_data("^HSI", "2008-01-01", "2021-11-05")
stock.to_csv("/opt/python/envs/default/lib/python3.8/site-packages/HSI-raw.csv")

stock.iloc[-5:,:]

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, "HSI-raw.csv")

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2008, 11, 11),
        # Do not pass values before this date
        todate=datetime.datetime(2021, 12, 31),
        # Do not pass values after this date
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

