# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 07:08:14 2021

@author: TL
"""

import pandas as pd
import pandas_ta as ta

df = pd.read_excel('C:/Users/TL/OneDrive - The Hong Kong Polytechnic University/Python/投資/HSI - Copy.xlsx')

CustomStrategy = ta.Strategy(
    name="Momo and Volatility",
    description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "rsi","length": 5},
        {"kind": "rsi","length": 14},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "kdj"}
    ]
)
# To run your "Custom Strategy"
df.ta.strategy(CustomStrategy)

df.to_excel('C:/Users/TL/OneDrive - The Hong Kong Polytechnic University/Python/投資/HSI - Copy.xlsx')


##########################################################

import pandas as pd
import pandas_ta as ta

code = "AAPL"

df = pd.DataFrame()
df = df.ta.ticker(code ,period = '5y' )

df.info

MyStrategy = ta.Strategy(
    name="RSI, KDJ, MACD EMA",
    ta=[
        {"kind": "rsi","length": 5},
        {"kind": "rsi","length": 14},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "kdj"},
        {"kind": "ema","length": 20},
        {"kind": "ema","length": 60},
        {"kind": "ema","length": 120},
    ]
)

# (2) Run the Strategy
df.ta.strategy(MyStrategy)

df.to_excel('%s-with indicator.xlsx'%(code))


############################################################
from fastquant import get_stock_data

stock = get_stock_data("^HSI", "2008-01-01", "2021-11-05")
# print(stock.head())

from fastquant import backtest
backtest('rsi', stock, rsi_lower=15, rsi_upper=60, rsi_period=7,  plot=0)
# backtest('smac', stock, fast_period=15, slow_period=40, plot=False)

#########################################################
from fastquant import get_stock_data
from fastquant import backtest
import pandas as pd

code = "^HSI"
stock = get_stock_data(code, "2000-01-01", "2021-11-07")

# Utilize single set of parameters
strats = { 
    "macd": {"fast_period": 5, "slow_period": 16, "signal_period": 18, 'sma_period': 10, "dir_period": 10 },
    "rsi": {"rsi_lower": 30, "rsi_upper": 70} 
}

res = backtest("multi", stock, strats=strats,  plot=0)
res.shape

#########################################################

code = "^HSI"
stock = get_stock_data(code, "2015-01-01", "2021-11-07")

strats_opt = { 
    "macd": {"fast_period": [3,5,8], "slow_period": [10,13,16], "signal_period": [9,18], 'sma_period': [10,20], "dir_period":[10, 14]}, 
    "rsi": {"rsi_lower": [20, 25], "rsi_upper": [75, 80]} 
}

res_opt = backtest("multi", stock, strats=strats_opt)
# (4, 16)

res_opt.to_excel(str(code)+("-res_opt.xlsx"))

df = res_opt
df.to_csv("output.csv")  

#######################################################
from fastquant import backtest, get_stock_data
df = get_stock_data("^HSI", "2007-01-01", "2021-11-07")

# Utilize single set of parameters
strats = { 
     # "macd": {"fast_period": 5, "slow_period": 13, "signal_period": 9, 'sma_period': 20, "dir_period": 14 }, 
    "rsi": {"rsi_lower": 15, "rsi_upper": 40, "rsi_period": 6}
} 
res = backtest("multi", df, strats=strats)
res.shape
# (1, 16)
df.to_csv(str(code)+("-res_opt(MACD, RSI).csv"))
################################## RSI  OPT ##########################################
code = "^HSI"
stock = get_stock_data(code, "2005-01-01", "2021-11-07")

strats_opt = { 
    # "macd": {"fast_period": [3,5,8], "slow_period": [10,13,16], "signal_period": [9,18], 'sma_period': [10,20], "dir_period":[10, 14]}, 
    "rsi": {"rsi_lower": [15,20,25], "rsi_upper": [40, 60, 80], "rsi_period":[5,6,14,20]} 
}

res_opt = backtest("multi", stock, strats=strats_opt)
# (4, 16)

# res_opt.to_excel(str(code)+("-res_opt.xlsx"))

res_opt.to_csv(str(code)+("-res_opt(RSI).csv"))



####################################### MACD OPT ############################################
code = "^HSI"
stock = get_stock_data(code, "2005-01-01", "2021-11-07")

strats_opt = { 
    "macd": {"fast_period": [3,5,8], "slow_period": [10,13,16], "signal_period": [9,18], 'sma_period': [5,10,20], "dir_period":[7, 14, 21]}, 
    # "rsi": {"rsi_lower": [15,20, 25], "rsi_upper": [40, 60, 80], "rsi_period":[6,14,20]} 
}

res_opt = backtest("multi", stock, strats=strats_opt)
# (4, 16)

# res_opt.to_excel(str(code)+("-res_opt.xlsx"))

res_opt.to_csv(str(code)+("-res_opt(MACD).csv"))

####################################### MIX RSI & MACD OPT ###########################################
code = "^HSI"
stock = get_stock_data(code, "2005-01-01", "2021-11-07")

strats_opt = { 
    "macd": {"fast_period": 8, "slow_period": 13, "signal_period": 18, 'sma_period': 5, "dir_period":7}, 
    "rsi": {"rsi_lower": 25, "rsi_upper": 80, "rsi_period":14} 
}

res_opt = backtest("multi", stock, strats=strats_opt)
# (4, 16)

# res_opt.to_excel(str(code)+("-res_opt.xlsx"))

res_opt.to_csv(str(code)+("-res_opt(MACD+RSI).csv"))


