import pandas as pd
import matplotlib.pyplot as plt

from src.PortfolioBacktester.interfaces import StrategyBacktest
from src.PortfolioBacktester.modules.performance_functions import summary_stats


class NaiveBacktest(StrategyBacktest):
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
        self.signals_df = signals_df
        self.asset_prices = asset_prices
        self.initial_capital = initial_capital
        self._get_investible_assets()

    def __str__(self):
        return (f"NaiveBacktest(start_date={self.start_date}, end_date={self.end_date})"
                f", investable_assets={self.investable_assets}, ")

    def _get_investible_assets(self):
        """
        Get the investable assets for the strategy.
        This method returns the signals_df index.
        """
        self.investable_assets = list(self.signals_df.index)

    def _asset_returns(self):

        """
        Get the asset returns for the strategy.
        This method calculates daily returns from the asset prices DataFrame.
        """
        self.asset_returns = self.asset_prices.pct_change().iloc[1:]

    def _rebalance_dates(self):
        """
        Get the rebalance days for the strategy.
        This method returns the index of the signals_df DataFrame.
        """
        self.rebalance_dates = self.signals_df.columns

    def price_simulation(self):
        """
        Simulate the price evolution of the portfolio based on the backtested daily weights.
        This method returns a DataFrame with simulated prices.
        """
        returns_to_be_simulated = self.portfolio_returns.loc[
                                  self.start_date:self.end_date
                                  ].copy()
        simulation = self.initial_capital*(1+returns_to_be_simulated).cumprod()
        self.price_simulation = simulation

    def _run_backtest(self):
        """
        Run the backtest strategy and return the backtested daily weights and portfolio returns.
        """
        self._get_investible_assets()
        self._asset_returns()
        self._rebalance_dates()
        self._backtest_strategy()
        self.price_simulation()

    def performance_metrics(self):
        """
        Calculate performance metrics for the backtest.
        This method returns a dictionary with performance metrics.
        """
        self.performance_metrics = summary_stats(self.portfolio_returns)

        return self.performance_metrics

    def normalized_asset_prices(self):
        """
        Normalize the asset prices to start from 1.
        This method returns a DataFrame with normalized asset prices.
        """
        prices = self.asset_prices.loc[self.start_date:self.end_date]
        normalized_returns = prices.pct_change().iloc[1:]
        normalized_prices = self.initial_capital*(1 + normalized_returns).cumprod()

        self.normalized_asset_prices = normalized_prices

        return self.normalized_asset_prices

    def performance_plots(self):
        # Create a 2x2 subplot grid
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # Adjust figsize as needed
        fig.suptitle(f"Portfolio Backtest Overview from {self.start_date} to {self.end_date}", fontsize=16)

        # First plot: Price Simulation
        self.price_simulation.plot(ax=axes[0, 0])
        axes[0, 0].set_title("Price Simulation")
        axes[0, 0].grid(True)

        # Second plot: Asset Returns
        self.asset_returns.loc[self.start_date:self.end_date].plot(ax=axes[0, 1], alpha=0.75)
        axes[0, 1].set_title("Asset Returns")
        axes[0, 1].grid(True)

        # Third plot: Asset Prices
        self.normalized_asset_prices()
        self.normalized_asset_prices.plot(ax=axes[1, 0], alpha=0.75)
        axes[1, 0].set_title("Asset Prices")
        axes[1, 0].grid(True)

        # Fourth plot: Portfolio Returns Histogram
        self.portfolio_returns.loc[self.start_date:self.end_date].hist(
            bins=75, ax=axes[1, 1]
        )
        axes[1, 1].set_title("Portfolio Returns Histogram")
        axes[1, 1].grid(True)

        # Adjust layout to prevent overlap
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()
