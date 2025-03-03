from freqtrade.strategy.interface import IStrategy
import pandas as pd
import numpy as np

class BuyLowSellHigh(IStrategy):
    """
    Estratégia simples baseada em médias móveis para comprar na baixa e vender na alta.
    """
    # Definição do timeframe usado
    timeframe = '5m'  # Igual ao que foi configurado no config.json

    # Retorno mínimo esperado para cada tempo de retenção da posição
    minimal_roi = {
        "0": 0.05  # Sai quando atingir 5% de lucro
    }

    # Stoploss fixo em -10%
    stoploss = -0.10

    # Trailing stop habilitado
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03  # Só ativa quando já tiver 3% de lucro
    trailing_only_offset_is_reached = True

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Adiciona indicadores técnicos ao dataframe.
        """
        dataframe['sma20'] = dataframe['close'].rolling(window=20).mean()
        dataframe['sma50'] = dataframe['close'].rolling(window=50).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de compra: preço atual abaixo da média de 20 períodos.
        """
        dataframe.loc[
            (dataframe['close'] < dataframe['sma20']),
            'buy'
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Define a condição de venda: preço atual acima da média de 50 períodos.
        """
        dataframe.loc[
            (dataframe['close'] > dataframe['sma50']),
            'sell'
        ] = 1
        return dataframe
