import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import backtrader.feeds as btfeeds

# Create a Stratey
class StochasticRSI(bt.Strategy):

    params = (
        ('stoch_k_period', 3),
        ('stoch_d_period', 3),
        ('stoch_rsi_period', 14),
        ('stoch_period', 14),
        ('stoch_upperband', 80.0),
        ('stoch_lowerband', 20.0),

        ('take_profit', 0.04),
        ('stop_loss', 0.01),

        ('size', 20),
        ('debug', False),
    )

    def __init__(self):

        self.stoch = StochasticRSI(k_period=self.p.stoch_k_period,
                                   d_period=self.p.stoch_d_period,
                                   rsi_period=self.p.stoch_rsi_period,
                                   stoch_period=self.p.stoch_period,
                                   upperband=self.p.stoch_upperband,
                                   lowerband=self.p.stoch_lowerband)

    def next(self):

        if not self.position:
            close = self.data.close[0]
            price1 = close
            price2 = price1 - self.p.stop_loss * close
            price3 = price1 + self.p.take_profit * close

            if self.stoch.l.fastk[0] < 20:
                self.buy_bracket(price=price1, stopprice=price2, limitprice=price3, exectype=bt.Order.Limit)

            if self.stoch.l.fastk[0] > 80:
                self.sell_bracket(price=price1, stopprice=price3, limitprice=price2, exectype=bt.Order.Limit)


if __name__ == '__main__':

    from fastquant import get_stock_data

    code = "IWM"
    df = get_stock_data(code, "2008-01-01", "2021-11-05")
    df.to_csv("%s.csv" % (code))

# Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(StochasticRSI)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, 'TSLA-USD.csv')

    # Create a Data Feed
    data = btfeeds.GenericCSVData(
        dataname=("%s.csv" % (code)),
        fromdate=datetime.datetime(2008, 1, 1),
        todate=datetime.datetime(2021, 12, 31),

        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),
        tmformat=('%H.%M.%S'),

        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=5)

    # Set the commission
    cerebro.broker.setcommission(commission=0.002)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Plot the result
    cerebro.plot()