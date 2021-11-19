# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 00:06:50 2021

@author: TL
"""

# Run this on your terminal
# pip install fastquant

from fastquant import get_stock_data
stock = get_stock_data("IWM", "2015-01-01", "2021-11-05")
print(stock.head())


from fastquant import backtest
backtest('emac', stock, fast_period=20, slow_period=60)





from fastquant import get_crypto_data
crypto = get_crypto_data("BTC/USDT", "2018-12-01", "2019-12-31")
crypto.head()

from fastquant import backtest
backtest('smac', crypto, fast_period=15, slow_period=40)

# Starting Portfolio Value: 100000.00
# Final Portfolio Value: 102272.90



from fastquant import get_crypto_data, backtest
from fbprophet import Prophet
from matplotlib import pyplot as plt

# Pull crypto data
df = get_crypto_data("BTC/USDT", "2019-01-01", "2021-10-31")

# Fit model on closing prices
ts = df.reset_index()[["dt", "close"]]
ts.columns = ['ds', 'y']
m = Prophet(daily_seasonality=True, yearly_seasonality=True).fit(ts)
forecast = m.make_future_dataframe(periods=0, freq='D')

# Predict and plot
pred = m.predict(forecast)
fig1 = m.plot(pred)
plt.title('BTC/USDT: Forecasted Daily Closing Price', fontsize=25)