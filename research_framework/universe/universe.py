import pandas as pd

class Universe:
    def __init__(self, assets: list, data: pd.DataFrame):
        """
        Initialize the universe with a list of assets and historical data.
        :param assets: List of asset symbols (e.g., ["AAPL", "BTC", "ETH"])
        :param data: Pandas DataFrame with historical price data for all assets.
        """
        self.assets = assets
        self.data = data

    def filter_by_liquidity(self, min_volume: float):
        """Filter assets by liquidity (e.g., average daily volume)."""
        self.assets = [
            asset for asset in self.assets
            if self.data[self.data['symbol'] == asset]['volume'].mean() > min_volume
        ]

    def get_asset_data(self, asset: str) -> pd.DataFrame:
        """Retrieve historical data for a specific asset."""
        return self.data[self.data['symbol'] == asset]

    def get_universe(self) -> list:
        """Return the current list of assets in the universe."""
        return self.assets
