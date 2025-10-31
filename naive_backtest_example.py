import pandas as pd
import importlib

# import src.kaxanuk.PortfolioBacktester.modules.visualization as viz
import src.PortfolioBacktester.modules.data_wrangling as dw
# import src.kaxanuk.PortfolioBacktester.modules.benchmark_st as bmk
# import src.kaxanuk.PortfolioBacktester.modules.performance_attribution_fun as patt
from src.PortfolioBacktester.entinties import NaiveBacktest

importlib.reload(dw)
# importlib.reload(viz)
# importlib.reload(bmk)
# importlib.reload(patt)

#%%
"""
INPUT PARAMETERS
"""

portfolio_path = "Input/weights_portfolio"
investable_universe_path = "Input/investable_assets"

#%%
"""
LOAD DATA
"""

portfolio_weights = dw.load_csv(portfolio_path, "test_weights_df")
portfolio_weights.columns = pd.to_datetime(portfolio_weights.columns, format="%d/%m/%Y")
start_date = portfolio_weights.columns[0]
end_date = portfolio_weights.columns[-1]
investable_assets = portfolio_weights.index

# TODO Rulo: assert all indexes are datetime objects
# TODO Rulo: start date y end date estan de adorno
#%%
"""
BUILD DFS
"""

series_list = [dw.column_df(investable_universe_path, name, "m_adjusted_close") for name in investable_assets]
asset_prices = pd.concat(series_list, axis=1)
asset_prices.index = pd.to_datetime(asset_prices.index)
asset_prices.sort_index(inplace=True)
#%%

crossvalidated_dates = (
    # ('2017-01-01', '2017-12-31'),
    # ('2018-01-01', '2018-12-31'),
    # ('2019-01-01', '2019-12-31'),
    # ('2020-01-01', '2020-12-31'),
    # ('2021-01-01', '2021-12-31'),
    # ('2022-01-01', '2022-12-31'),
    # ('2023-01-01', '2023-12-31'),
    # ('2024-01-01', '2024-12-31'),
    # ('2025-01-01', '2025-12-31'),
    ('2017-01-01', '2025-12-31'), # Full period for final backtest
)

performance_metrics = []
for start_date, end_date in crossvalidated_dates:
    portfolio_backtest = NaiveBacktest(
        start_date=start_date,
        end_date=end_date,
        signals_df=portfolio_weights,
        asset_prices=asset_prices,
        initial_capital=1
    )
    print(portfolio_backtest)

    portfolio_backtest._run_backtest()

    portfolio_backtest.performance_plots()

    metrics_i = portfolio_backtest.performance_metrics()
    performance_metrics.append(metrics_i)


#%%

cv_metrics = pd.concat(performance_metrics)
print(cv_metrics)