import datetime
from freqtrade.strategy.interface import IStrategy
from freqtrade.persistence import Trade
import talib.abstract as ta
import pandas as pd
import numpy as np

class BuyLowSellHigh(IStrategy):
    """
    Estratégia aprimorada baseada em médias móveis, RSI, volume e ATR para otimizar pontos de entrada e saída.
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

    # Stoploss otimizado pelo Hyperopt e ajustado dinamicamente
    stoploss = -0.065

    # Trailing stop otimizado
    trailing_stop = True
    trailing_stop_positive = 0.08  # Ativa com 8% de lucro
    trailing_stop_positive_offset = 0.156  # Protege ganhos a partir de 15.6%
    trailing_only_offset_is_reached = False

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Adiciona indicadores técnicos ao dataframe.
        """
        dataframe['sma20'] = ta.SMA(dataframe, timeperiod=20)
        dataframe['sma50'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['sma200'] = ta.SMA(dataframe, timeperiod=200)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['atr'] = ta.ATR(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=14)
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # Suporte e resistência
        dataframe['support'] = dataframe['low'].rolling(window=50).min()
        dataframe['resistance'] = dataframe['high'].rolling(window=50).max()

        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de compra: preço abaixo da SMA20, RSI indicando sobrevenda, volume alto e confirmando tendência de alta.
        """
        dataframe.loc[
            (dataframe['close'] < dataframe['sma20']) &  # Preço abaixo da SMA20
            (dataframe['rsi'] < 40) &  # RSI indicando sobrevenda
            (dataframe['volume'] > dataframe['volume_mean']) &  # Volume acima da média
            (dataframe['sma20'] > dataframe['sma50']) &  # SMA20 acima da SMA50 (tendência de alta)
            (dataframe['close'] > dataframe['support']),  # Evita comprar em quedas contínuas
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de venda: preço acima da SMA50, RSI indicando sobrecompra ou atingindo resistência.
        """
        dataframe.loc[
            (dataframe['close'] > dataframe['sma50']) |  # Preço acima da SMA50
            (dataframe['rsi'] > 60) |  # RSI indicando sobrecompra
            (dataframe['close'] >= dataframe['resistance']),  # Preço atingiu resistência
            'sell'
        ] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                        current_profit: float, **kwargs) -> float:
        """
        Ajusta o stop-loss dinamicamente com base no ATR.
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        atr = dataframe['atr'].iloc[-1]

        return max(-0.03, -1.5 * atr)  # Ajusta o stop-loss dinamicamente, nunca menor que -3%
