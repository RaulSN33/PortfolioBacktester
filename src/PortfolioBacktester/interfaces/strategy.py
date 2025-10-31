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

    # def index_backtesting_v3(kn_weights_df, price_data, effective_rebalance_dates):
    # 
    #     price_data = drop_mostly_null_rows(price_data)
    #     effective_rebalance_dates = [
    #         i for
    #         i in
    #         effective_rebalance_dates if
    #         (i >= kn_weights_df.index[0]) and (i <= kn_weights_df.index[-1])
    #     ]
    #     kn_weights_df.index = effective_rebalance_dates
    # 
    #     dict_periodic_price_data = {}
    #     list_periodic_port_value = []
    #     dict_periodic_value_ps_in_port = {}
    #     n_rebalance_dates = len(effective_rebalance_dates)
    #     # ---------------
    #     for i in range(n_rebalance_dates):
    #         try:
    #             date = effective_rebalance_dates[i]
    #             next_date = effective_rebalance_dates[i + 1]
    #             dict_periodic_price_data[date] = price_data.loc[date:next_date]
    #             if i == n_rebalance_dates:
    #                 dict_periodic_price_data[date] = dict_periodic_price_data[date]
    #             else:
    #                 dict_periodic_price_data[date] = dict_periodic_price_data[date].iloc[:-1]
    # 
    #         except:
    #             dict_periodic_price_data[date] = price_data.loc[date:]
    #         # -----------------
    #         # This will give you theta
    #         if i == 0:
    #             rebalance_weights = kn_weights_df.loc[date]
    #         else:
    #             rebalance_weights = kn_weights_df.loc[date] * final_periodic_port_value
    # 
    #         # rebalance_weights = kn_weights_df.loc[date]
    #         price_rebal_date = price_data.loc[date]
    #         num_shares = rebalance_weights / price_rebal_date
    # 
    #         value_ps_in_port = num_shares.mul(dict_periodic_price_data[date], axis=0)
    #         dict_periodic_value_ps_in_port[date] = value_ps_in_port
    #         total_periodic_port_value = value_ps_in_port.sum(axis=1)
    #         list_periodic_port_value.append(total_periodic_port_value)
    #         # final_val_i2 = ind_port2.sum(axis=1)
    #         final_periodic_port_value = total_periodic_port_value.iloc[-1]
    # 
    #     total_port_ts = pd.concat(list_periodic_port_value)
    # 
    #     portfolio_daily_returns = total_port_ts.pct_change()
    #     portfolio_daily_weights = pd.DataFrame()
    # 
    #     return portfolio_daily_returns, portfolio_daily_weights

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


