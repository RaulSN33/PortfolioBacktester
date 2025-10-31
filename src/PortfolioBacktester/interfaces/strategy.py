import abc
import pandas as pd

class StrategyBacktest(metaclass=abc.ABCMeta):
    def __init__(
            self,
            start_date,
            end_date,
            # signals_df,
            asset_prices,
            initial_capital,
    ):
        self.start_date = start_date
        self.end_date = end_date
        # self.signals_df = signals_df
        self.asset_prices = asset_prices
        self.initial_capital = initial_capital

        #TODO esto cambiarlo a postinit para asegurarnos que estas variables existen al intanciarla class

    @abc.abstractmethod
    def _get_investible_assets(self):

        """
        Get the investable assets for the strategy.
        This method should be implemented by subclasses to return a list of investable assets.
        """
        return self.investable_assets

    def _asset_returns(self):
        """
        Get the asset returns for the strategy.
        This method should be implemented by subclasses to return a DataFrame of asset returns.
        """
        return self.asset_returns

    def _rebalance_dates(self):
        """
        Get the asset returns for the strategy.
        This method should be implemented by subclasses to return a DataFrame of asset returns.
        """
        return self.rebalance_dates

    # @abc.abstractmethod
    def _backtest_strategy(self):
        """
        Main function of the class, it backtest the strategy WITHOUT transaction costs.
        This method calculates the backtested daily weights and portfolio returns.
        """
        dfs_weights = []
        dfs_returns = []

        kn_weights_df = self.signals_df.T
        self.asset_returns = self.asset_returns[kn_weights_df.columns]
        actual_rebal_d = self.rebalance_dates
        for n in range(len(actual_rebal_d)):
            try:
                m_returns = self.asset_returns.loc[actual_rebal_d[n]:actual_rebal_d[n + 1]].copy()
            except:
                m_returns = self.asset_returns.loc[actual_rebal_d[n]:].copy()

            periodic_portfolio_weights = pd.DataFrame().reindex_like(m_returns)

            periodic_portfolio_weights.iloc[0] = kn_weights_df.iloc[n]

            for i in range(1, len(periodic_portfolio_weights.iloc[1:])):
                periodic_portfolio_weights.iloc[i] = (periodic_portfolio_weights.iloc[i - 1]).mul(1 + m_returns.iloc[i])

            periodic_portfolio_weights.iloc[-1] = (periodic_portfolio_weights.iloc[-2]).mul(1 + m_returns.iloc[-1])
            periodic_total_weights = periodic_portfolio_weights.sum(axis=1)

            periodic_strategy_returns = periodic_total_weights.pct_change().iloc[1:]

            dfs_returns.append(periodic_strategy_returns)
            dfs_weights.append(periodic_portfolio_weights)

        daily_weights = pd.concat(dfs_weights, axis=0)
        duplicated_indexes = daily_weights.index.duplicated(keep='last')

        self.backtested_daily_weights = daily_weights[~duplicated_indexes]
        self.portfolio_returns = pd.concat(dfs_returns, axis=0)
        self.portfolio_returns = self.portfolio_returns.fillna(0)
        self.portfolio_returns = self.portfolio_returns.loc[
            self.start_date:self.end_date
        ]
        self.portfolio_returns.name = 'strategy_returns'

    def _reweight_daily_weights(self, df):
        """
        Reweight the daily weights of the portfolio.
        This method should be implemented by subclasses to perform the reweighting logic.
        """
        reweighted = df.copy()
        row_sum = reweighted.sum(axis=1)
        safe_row_sums = row_sum.replace(0, 1)
        reweighted = reweighted.div(safe_row_sums, axis=0)
        reweighted[row_sum == 0] = 0
        self.reweighted_daily_weights = reweighted

        return self.reweighted_daily_weights

    @abc.abstractmethod
    def _run_backtest(self):
        """
        Run the backtest for the strategy.
        This method orchestrates the backtesting process by calling the necessary methods.
        """
        ...


