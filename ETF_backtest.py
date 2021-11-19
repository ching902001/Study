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

df= pd.read_csv('QQQ_indicator.csv')

"""
header

Date	Open	High	Low	Close	Volume	Dividends	Stock Splits	RSI_5	RSI_14	MACD_8_21_9	MACDh_8_21_9	MACDs_8_21_9	K_9_3	D_9_3	J_9_3	EMA_20	EMA_60	EMA_120

"""

df.iloc[120:,:]

################## buy signal ################
buy = []
for i in range(len(df)):

    buy_indicator_option = (
            # df['EMA_20'][i] > df['EMA_60'][i] > df['EMA_120'][i]
            # and
            df['close'][i] > df['EMA_20'][i] > df['EMA_60'][i] > df['EMA_120'][i]
            # and
            # df['K_9_3'][i-1] < df['K_9_3'][i-1]
            and
            df['K_9_3'][i] > df['D_9_3'][i]
            # and
            # df['K_9_3'][i] >25
            and
            df['D_9_3'][i] >45
            # # and
            # # df['K_9_3'][i] < df['K_9_3'][i-1]
            # and
            # df['RSI_5'][i] >40
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
                    df['EMA_20'][i] > df['EMA_60'][i]  > df['EMA_120'][i]
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
                    df['RSI_5'][i] < 30
        )
    
    if sell_indicator_option:
        sell.append(-1)
    else:
        sell.append(0)

df["sell"]=sell
sell.count(-1)

################### buy and sell #############

position = 0 #倉位, 1 = 持有, 2 = 沒持有

for i in range(len(df)):
    if position == 0:
        if df["buy"][i] == 1:
            position += 1
            df.loc[[i], "buy_mark"] = (df["high"][i] + 10)
            print("buy done{}".format(str(df.loc[[i], ['close']])))


    if position == 1:
        if df["sell"][i] == -1:
            position -= 1
            df.loc[[i], "sell_mark"] = (df["low"][i] - 10)
            print("sell done{}".format(str(df.loc[[i], ['close']])))


# sell_mark = []
# position = 0 #倉位, 1 = 持有, 2 = 沒持有
# print(len(df))
# for i in range(len(df)):
#     if position == 0:
#         if df["buy"][i] == 1:
#             position += 1
#             print("buy done{}".format(str(df.loc[[i], ['close']])))
#             buy_mark.append(df["high"][i] + 10) # for plot graph marking
#         else:
#             sell_mark.append(np.nan)
#             buy_mark.append(np.nan)
#
#     if position == 1:
#         if df["sell"][i] == -1:
#             position -= 1
#             print("sell done{}".format((df.loc[[i], ['close']])))
#             sell_mark.append(df["low"][i] - 10) # for plot graph marking
#         else:
#             sell_mark.append(np.nan)
#             buy_mark.append(np.nan)
#
# # buy_mark = buy_mark[0:-1] # 唔知點解會出左970 data, df得969, 所以要扣返最尾個數
# df["buy_mark"] = buy_mark
# df["sell_mark"] = sell_mark

# buy_mark = []
######### profit calculiation ############

buy1 = df.loc[df["buy_mark"].notna()].reset_index()
sell1 = df.loc[df["sell_mark"].notna()]
sell1 = sell1.append(df.iloc[-1:,:]).reset_index()  #在回測的最後一天當作無條件賣出

print("買進次數 : " + str(len(buy1)) + "次")
print("賣出次數 : " + str(len(sell1)) + "次")

return_rate = []
for i in range(len(buy1)):
    rate = round((sell1["close"][i] - buy1['close'][i]) / buy1['close'][i]  * 100,2)
    return_rate.append(rate)
return_rate = np.array(return_rate)
print (return_rate)
print ("max profit "+str(return_rate.max()))
print ("max downdraw "+str(return_rate.min()))
print('total profit '+ str(np.array(return_rate).sum()))



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
