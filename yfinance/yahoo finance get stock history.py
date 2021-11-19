# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 19:50:57 2021

@author: TL
"""

# coding=utf-8


import pandas as pd
import pandas_datareader as pdr
code = '^HSI'
data = pdr.get_data_yahoo(code, start='1992-01-02', end='2021-10-22')
data.to_excel("HSI.xlsx")


import pandas_datareader.data as web
import pandas as pd
import datetime as dt
df = web.DataReader('IWM', '2019-01-02','2021-02-01')


################################################
# Import packages
import yfinance as yf
import pandas as pd

# Set the start and end date
start_date = '1990-01-01'
end_date = '2021-07-12'

# Define the ticker list
tickers_list = ['AAPL', 'IBM', 'MSFT', 'WMT']

# Create placeholder for data
data = pd.DataFrame(columns=tickers_list)

# Fetch the data
for ticker in tickers_list:
    data[ticker] = yf.download(ticker,
                               start_date,
                               end_date)['Adj Close']

# Print first 5 rows of the data
data.head()


##################################################
# coding=utf-8
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
code='IWM'
stock = pdr.get_data_yahoo(code,'2019-01-02','2021-10-01')
print(stock)    # 输出内容
# 保存为excel和csv文件
stock.to_excel('C:\\Users\TL\Desktop\Stock\\'+code+'.xlsx')

