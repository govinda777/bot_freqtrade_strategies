from freqtrade.strategy.interface import IStrategy

class BuyLowSellHigh(IStrategy):
    timeframe = '1h'
    minimal_roi = {"0": 0.05}  
    stoploss = -0.10  
    trailing_stop = True  
    trailing_stop_positive = 0.02  
    
    def populate_indicators(self, dataframe, metadata):
        dataframe['sma20'] = dataframe['close'].rolling(window=20).mean()
        dataframe['sma50'] = dataframe['close'].rolling(window=50).mean()
        return dataframe

    def populate_buy_trend(self, dataframe, metadata):
        dataframe.loc[(dataframe['close'] < dataframe['sma20']), 'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe, metadata):
        dataframe.loc[(dataframe['close'] > dataframe['sma50']), 'sell'] = 1
        return dataframe
