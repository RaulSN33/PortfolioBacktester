import pandas as pd

from src.PortfolioBacktester.interfaces import StrategyBacktest


class BenchmarkBacktest(StrategyBacktest):
    def __init__(
            self,
            start_date: str,
            end_date: str,
            signals_df: pd.DataFrame,
            asset_prices: pd.DataFrame,
            initial_capital: int = 1,
    ):
        self.start_date = start_date
        self.end_date = end_date
        # self.signals_df = signals_df
        self.asset_prices = asset_prices
        self.initial_capital = initial_capital
        # self._get_investible_assets()

    def __str__(self):
        return (f"BenchmarkBacktest(start_date={self.start_date}, end_date={self.end_date})"
                f", investable_assets={self.investable_assets}, ")

    def _get_investible_assets(self):
        """
        Get the investable assets for the strategy.
        This method returns the signals_df index.
        """

    def _asset_returns(self):

        """
        Get the asset returns for the strategy.
        This method calculates daily returns from the asset prices DataFrame.
        """

    def _rebalance_dates(self):
        """
        Get the rebalance days for the strategy.
        This method returns the index of the signals_df DataFrame.
        """


    def price_simulation(self):
        """
        Simulate the price evolution of the portfolio based on the backtested daily weights.
        This method returns a DataFrame with simulated prices.
        """


    def run(self):
        """
        Run the backtest strategy and return the backtested daily weights and portfolio returns.
        """
        self._get_investible_assets()
        self._asset_returns()
        self._rebalance_dates()
        self._backtest_strategy()
        self.price_simulation()

