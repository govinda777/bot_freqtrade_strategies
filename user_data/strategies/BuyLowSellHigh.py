from freqtrade.strategy.interface import IStrategy
from freqtrade.plugins.protections import StoplossGuard, MaxDrawdown

class BuyLowSellHigh(IStrategy):
    timeframe = '1h'
    minimal_roi = {"0": 0.05}  
    stoploss = -0.10  
    trailing_stop = True  
    trailing_stop_positive = 0.02  
    
    @property
    def protections(self):
        return [
            {
                "method": StoplossGuard,
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 4,
                "only_per_pair": False
            },
            {
                "method": MaxDrawdown,
                "lookback_period_candles": 12,
                "max_allowed_drawdown": 0.2,
                "stop_duration_candles": 12,
                "only_per_pair": False
            }
        ]

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
