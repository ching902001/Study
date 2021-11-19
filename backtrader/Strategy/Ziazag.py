from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

############## create a CSV #############


# import backtrader as bt

# if __name__ == '__main__':
#     #Create a cerebro
#     cerebro = bt.Cerebro()
#     cerebro.broker.setcash(1000000.0)

#     print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

#     cerebro.run()

#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# # Starting Portfolio Value: 1000000.00
# # Final Portfolio Value: 1000000.00


import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader.feeds as btfeed

# Import the backtrader platform
import backtrader as bt
import backtrader.indicators as btind

class ZigZag(bt.ind.PeriodN):
    '''
      Identifies Peaks/Troughs of a timeseries
    '''
    lines = (
        'trend', 'last_pivot_t', 'last_pivot_x', 'last_pivot_ago',
        'zigzag_peak', 'zigzag_valley', 'zigzag',
    )

    # Fancy plotting name
    # plotlines = dict(logreturn=dict(_name='log_ret'))
    plotinfo = dict(
        subplot=False,
        plotlinelabels=True, plotlinevalues=True, plotvaluetags=True,
    )

    plotlines = dict(
        trend=dict(marker='', markersize=0.0, ls='', _plotskip=True),
        last_pivot_t=dict(marker='', markersize=0.0, ls='', _plotskip=True),
        last_pivot_x=dict(marker='', markersize=0.0, ls='', _plotskip=True),
        last_pivot_ago=dict(marker='', markersize=0.0, ls='', _plotskip=True),
        zigzag_peak=dict(marker='v', markersize=4.0, color='red',
                         fillstyle='full', ls=''),
        zigzag_valley=dict(marker='^', markersize=4.0, color='red',
                           fillstyle='full', ls=''),
        zigzag=dict(_name='zigzag', color='blue', ls='-', _skipnan=True),
    )

    # update value to standard for Moving Averages
    params = (
        ('period', 2),
        ('up_retrace', 0.1),
        ('dn_retrace', 0.1),
        ('bardist', 0.015),  # distance to max/min in absolute perc
    )

    def __init__(self):
        super(ZigZag, self).__init__()

        if not self.p.up_retrace:
            raise ValueError('Upward retracement should not be zero.')

        if not self.p.dn_retrace:
            raise ValueError('Downward retracement should not be zero.')

        if self.p.up_retrace < 0:
            self.p.up_retrace = -self.p.up_retrace

        if self.p.dn_retrace > 0:
            self.p.dn_retrace = -self.p.dn_retrace

        self.p.up_retrace = self.p.up_retrace / 100
        self.p.dn_retrace = self.p.dn_retrace / 100

        self.missing_val = float('NaN')

    def prenext(self):
        self.lines.trend[0] = 0
        self.lines.last_pivot_t[0] = 0
        self.lines.last_pivot_x[0] = self.data[0]
        self.lines.last_pivot_ago[0] = 0
        self.lines.zigzag_peak[0] = self.missing_val
        self.lines.zigzag_valley[0] = self.missing_val
        self.lines.zigzag[0] = self.missing_val

    def next(self):
        data = self.data
        trend = self.lines.trend
        last_pivot_t = self.lines.last_pivot_t
        last_pivot_x = self.lines.last_pivot_x
        last_pivot_ago = self.lines.last_pivot_ago
        zigzag_peak = self.lines.zigzag_peak
        zigzag_valley = self.lines.zigzag_valley
        zigzag = self.lines.zigzag

        x = data[0]
        r = x / last_pivot_x[-1] - 1
        curr_idx = len(data) - 1

        trend[0] = trend[-1]
        last_pivot_x[0] = last_pivot_x[-1]
        last_pivot_t[0] = last_pivot_t[-1]
        last_pivot_ago[0] = curr_idx - last_pivot_t[0]
        zigzag_peak[0] = self.missing_val
        zigzag_valley[0] = self.missing_val
        zigzag[0] = self.missing_val

        if trend[-1] == 0:
            if r >= self.p.up_retrace:
                piv = last_pivot_x[0] * (1 - self.p.bardist)
                zigzag_valley[-int(last_pivot_ago[0])] = piv
                zigzag[-int(last_pivot_ago[0])] = last_pivot_x[0]
                trend[0] = 1
                last_pivot_x[0] = x
                last_pivot_t[0] = curr_idx
            elif r <= self.p.dn_retrace:
                piv = last_pivot_x[0] * (1 + self.p.bardist)
                zigzag_peak[-int(last_pivot_ago[0])] = piv
                zigzag[-int(last_pivot_ago[0])] = last_pivot_x[0]
                trend[0] = -1
                last_pivot_x[0] = x
                last_pivot_t[0] = curr_idx
        elif trend[-1] == -1:
            if r >= self.p.up_retrace:
                piv = last_pivot_x[0] * (1 - self.p.bardist)
                zigzag_valley[-int(last_pivot_ago[0])] = piv
                zigzag[-int(last_pivot_ago[0])] = last_pivot_x[0]
                trend[0] = 1
                last_pivot_x[0] = x
                last_pivot_t[0] = curr_idx
            elif x < last_pivot_x[-1]:
                last_pivot_x[0] = x
                last_pivot_t[0] = curr_idx
        elif trend[-1] == 1:
            if r <= self.p.dn_retrace:
                piv = last_pivot_x[0] * (1 + self.p.bardist)
                zigzag_peak[-int(last_pivot_ago[0])] = piv
                zigzag[-int(last_pivot_ago[0])] = last_pivot_x[0]
                trend[0] = -1
                last_pivot_x[0] = x
                last_pivot_t[0] = curr_idx
            elif x > last_pivot_x[-1]:
                last_pivot_t[0] = curr_idx

if __name__ == '__main__':
    from fastquant import get_stock_data

    code = "IWM"
    df = get_stock_data(code, "2008-01-01", "2021-11-05")
    df.to_csv("%s.csv" % (code))

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(ZigZag)

    # Create a Data Feed
    data = btfeed.GenericCSVData(
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
    cerebro.broker.setcash(1000000)

    # 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.01)

    # sizer
    cerebro.addsizer(bt.sizers.PercentSizer, percents=80)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()




