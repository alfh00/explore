class SignalLogic:
    @staticmethod
    def ma_crossover(short_ma: pd.Series, long_ma: pd.Series) -> pd.Series:
        """Generate buy/sell signals based on moving average crossover."""
        signal = (short_ma > long_ma).astype(int) - (short_ma < long_ma).astype(int)
        return signal

    @staticmethod
    def rsi_signal(rsi: pd.Series, lower: float = 30, upper: float = 70) -> pd.Series:
        """Generate buy/sell signals based on RSI levels."""
        return (rsi < lower).astype(int) - (rsi > upper).astype(int)
