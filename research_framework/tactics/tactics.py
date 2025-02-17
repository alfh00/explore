class Tactics:
    @staticmethod
    def apply_stop_loss(data: pd.DataFrame, entry_price: float, sl_pct: float) -> bool:
        """Check if stop loss is triggered."""
        return data['low'].min() <= entry_price * (1 - sl_pct)

    @staticmethod
    def apply_take_profit(data: pd.DataFrame, entry_price: float, tp_pct: float) -> bool:
        """Check if take profit is triggered."""
        return data['high'].max() >= entry_price * (1 + tp_pct)

    @staticmethod
    def apply_trailing_stop(data: pd.DataFrame, entry_price: float, trail_pct: float) -> float:
        """Update the trailing stop level."""
        max_price = data['high'].max()
        return max(entry_price, max_price * (1 - trail_pct))
