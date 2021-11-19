

import pandas_ta as ta
import pandas as pd
import os
from fastquant import get_stock_data


ETF_list = ['XLF' , 'IWM', 'EFA', 'QQQ', 'SPY', "ARKK", 'ARKG', 'VUG','HDV', 'VWO', 'DSI', 'VEU']
startdate = "2008-01-01"
enddate = "2021-11-05"

"""
### Popular ETF ###
XLF  金融
IWM  羅素
EFA  歐澳遠東指數
QQQ  NASDAQ100 科技股
SPY 標普500
ARKK 木頭姐
ARKG 木頭姐 Growth
VUG Vanguard Growth ETF with big IT company
HDV  iShares Core High Dividend ETF
VWO   Vanguard FTSE Emerging Markets ETF
DSI   iShares MSCI KLD 400 Social ETF
VEU  Vanguard FTSE All-World ex-US ETF


#### Industrial ETF ####
VGT	Vanguard Information Technology ETF	0.10%	資訊科技類股(300多檔)
XLK	Technology Select Sector SPDR Fund	0.13%	科技類股(約75檔)
XLY	Consumer Discretionary Select Sector SPDR Fund	0.13%	非必須消費、媒體、通路(約60檔)
XLP	Consumer Staples Select Sector SPDR Fund	0.13%	日常消費品產業(僅30多檔)
XLF	Financial Select Sector SPDR Fund	0.13%	金融類股(約70檔)
XLE	Energy Select Sector SPDR Fund	0.13%	能源類股(僅30檔)
XLV	Health Care Select Sector SPDR Fund	0.13%	健康醫療類股(約60檔)
XLI	Industrial Select Sector SPDR Fund	0.13%	工業類股(約75檔)
GDX	VanEck Vectors Gold Miners ETF	0.53%	金礦開採公司類股(約50檔)
XLB	Materials Select Sector SPDR ETF	0.13%	原材料類股(約30檔)
VOX	Vanguard Communication Services ETF	0.13%	電信服務股(約110檔)
XLU	Utilities Select Sector SPDR Fund	0.13%	公用事業類股(約30檔)
XLI	Industrial Select Sector SPDR Fund	Broad Industrials
VIS	Vanguard Industrials ETF	Broad Industrials
JETS U.S. Global Jets ETF	Airlines
ITA	iShares U.S. Aerospace & Defense ETF	Aerospace & Defense
PHO	Invesco Water Resources ETF	Water
FXR	First Trust Industrials/Producer Durables AlphaDEX Fund	Broad Industrials
IYT	iShares US Transportation ETF	Transportation
IYJ	iShares U.S. Industrials ETF	Broad Industrials
FIW	First Trust Water ETF	Water
CGW	Invesco S&P Global Water Index ETF	Water
FTXR	First Trust Nasdaq Transportation ETF	Transportation
XAR	SPDR S&P Aerospace & Defense ETF	Aerospace & Defense
XTN	SPDR S&P Transportation ETF	Transportation
FIDU	Fidelity MSCI Industrial Index ETF	Broad Industrials
PPA	Invesco Aerospace & Defense ETF	Broad Industrials
ARKX	ARK Space Exploration & Innovation ETF	Aerospace & Defense

"""


path = ('C:/Users/yeunglo/OneDrive - The Hong Kong Polytechnic University/Python/投資/company stock information/')

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


if __name__ == '__main__':
    for x in ETF_list:
        df = get_stock_data( x , startdate, enddate)
        df.ta.strategy(MyStrategy)
        df.to_csv(str(path)+str(x)+"_indicator.csv")