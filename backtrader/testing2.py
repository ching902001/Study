from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader.feeds as btfeeds
import backtrader as bt


if __name__ == '__main__':
    import backtrader as bt
    from Strategy.EMACrossOver import TestStrategy

    from datetime import datetime
    import backtrader as bt


    # Create a subclass of Strategy to define the indicators and logic


    ############### use fastquant get data and generate csv ##########
    from fastquant import get_stock_data
    import yfinance as yf

    # import backtrader as bt
    # code = "IWM"
    # df = get_stock_data(code, "2008-01-01", "2021-11-05")
    # df.to_csv("%s.csv" %(code))
    #
    # data = btfeeds.GenericCSVData(
    #     dataname=("%s.csv" % (code)),
    #     fromdate=datetime.datetime(2008, 1, 1),
    #     todate=datetime.datetime(2021, 12, 31),
    #
    #     nullvalue=0.0,
    #
    #     dtformat=('%Y-%m-%d'),
    #     tmformat=('%H.%M.%S'),
    #
    #     datetime=0,
    #     high=2,
    #     low=3,
    #     open=1,
    #     close=4,
    #     volume=5,
    #     openinterest=-1
    # )

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # get data from yahoo online
    import yfinance as yf
    data = bt.feeds.PandasData(dataname=yf.download('^HSI', '2019-01-01', '2021-11-11'))

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(1000000)

    # 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)
    #cerebro.addsizer(bt.sizers.FixedSize, stake=5)

    #sizer
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 50)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()




