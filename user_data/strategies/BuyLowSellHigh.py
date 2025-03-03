import datetime
from freqtrade.strategy.interface import IStrategy
from freqtrade.persistence import Trade
import talib.abstract as ta
import pandas as pd
import numpy as np

class BuyLowSellHigh(IStrategy):
    """
    Estratégia melhorada baseada em médias móveis, RSI e volume para comprar na baixa e vender na alta.
    """
    # Definição do timeframe usado
    timeframe = '5m'

    # Retorno mínimo esperado para cada tempo de retenção da posição
    minimal_roi = {
        "0": 0.128,
        "24": 0.026,
        "81": 0.014,
        "199": 0
    }

    # Stoploss otimizado pelo Hyperopt
    stoploss = -0.065
    
    # Trailing stop otimizado
    trailing_stop = True
    trailing_stop_positive = 0.256  # Ativa com 25.6% de lucro
    trailing_stop_positive_offset = 0.353  # Protege ganhos a partir de 35.3%
    trailing_only_offset_is_reached = False

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Adiciona indicadores técnicos ao dataframe.
        """
        dataframe['sma20'] = ta.SMA(dataframe, timeperiod=20)
        dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de compra: preço abaixo da SMA20, RSI indicando sobrevenda e volume alto.
        """
        dataframe.loc[
            (dataframe['close'] < dataframe['sma20']) & 
            (dataframe['rsi'] < 40) &  # Compra apenas quando RSI indicar sobrevenda
            (dataframe['volume'] > dataframe['volume_mean']) &  # Garante que há volume alto
            (dataframe['sma20'] > dataframe['sma50']),  # Evita compras em mercados de baixa
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de venda: preço acima da SMA50 ou RSI indicando sobrecompra.
        """
        dataframe.loc[
            (dataframe['close'] > dataframe['sma50']) | 
            (dataframe['rsi'] > 60),  # Sai quando RSI indicar sobrecompra
            'sell'
        ] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                        current_profit: float, **kwargs) -> float:
        """
        Ajusta o stop-loss dinamicamente com base no ATR.
        """
        atr = trade.dataframe['atr'][-1]  # Obtém o último ATR
        return max(-0.03, -1.5 * atr)  # Ajusta o stop-loss dinamicamente
