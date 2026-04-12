# PortfolioBacktester

A Python library for backtesting portfolio strategies using historical price data and rebalancing signals.

## Installation

```bash
pip install git+https://github.com/RaulSN33/PortfolioBacktester.git@main
```

## NaiveBacktest

`NaiveBacktest` is the core class of this library. It simulates portfolio performance by applying a sequence of asset weights across rebalancing periods, tracking daily weight drift between rebalances, and computing portfolio returns and performance metrics.

The algorithm supports **long-only**, **long-short**, and **leveraged** portfolios without modification — the behavior is entirely driven by the weights you provide.

### How it works

At each rebalancing date, the algorithm sets the portfolio weights to the values defined in `signals_df`. Between rebalances, weights drift naturally as asset prices move, mimicking a real portfolio that is not continuously rebalanced. At the next rebalancing date, weights are reset. Portfolio returns are computed period by period and concatenated into a full daily return series.

### Inputs

#### `signals_df` — Weights DataFrame *(required)*

A `pd.DataFrame` with the following structure:
- **Index** (rows): asset identifiers (e.g., ticker symbols)
- **Columns**: rebalancing dates as `datetime` objects, one per rebalancing event
- **Values**: portfolio weight for each asset on each rebalancing date

Each column is a rebalancing date. The weights defined in that column are applied starting on that date and drift naturally until the next rebalancing date. Weights do not need to sum to 1 — long-short and leveraged portfolios are supported by simply providing the appropriate signed or >1 weights.

Example structure (assets as rows, rebalancing dates as columns):

```
       2017-06-08  2017-09-11  2018-01-31  ...
XLB          0.00        0.00        0.00
XLE          1.00        1.00        0.00
XLF          0.00        0.00        0.00
XLK          0.00        0.00        0.00
...
```

#### `asset_prices` — Price DataFrame *(required)*

A `pd.DataFrame` where:
- **Index**: dates as `datetime` objects, sorted ascending
- **Columns**: asset identifiers matching those in `signals_df`
- **Values**: close prices (adjusted close recommended)

The price DataFrame must cover at least the full date range from `start_date` to `end_date` and must contain a column for every asset present in `signals_df`.

#### `start_date` *(required)*

A date string (e.g., `"2017-01-01"`) defining the start of the backtest window used for performance reporting and price simulation output.

#### `end_date` *(required)*

A date string (e.g., `"2025-12-31"`) defining the end of the backtest window.

#### `initial_capital` *(optional, default: `1`)*

The starting portfolio value used to compute the simulated price series. Set to `1` for normalized returns, or any other value to simulate a specific capital amount.

### Usage

```python
import pandas as pd
from PortfolioBacktester.entinties import NaiveBacktest

# Load your weights and prices
# signals_df: assets as index, rebalancing dates as columns
# asset_prices: dates as index, assets as columns

portfolio = NaiveBacktest(
    start_date="2017-01-01",
    end_date="2025-12-31",
    signals_df=signals_df,
    asset_prices=asset_prices,
    initial_capital=1,
)

portfolio._run_backtest()

# Get performance metrics
metrics = portfolio.performance_metrics()
print(metrics)

# Plot results
portfolio.performance_plots()
```

### Outputs

After calling `_run_backtest()`, the following attributes are available:

| Attribute | Description |
|---|---|
| `portfolio.portfolio_returns` | Daily portfolio return series |
| `portfolio.backtested_daily_weights` | Daily weight DataFrame showing weight drift between rebalances |
| `portfolio.price_simulation` | Cumulative portfolio value series starting from `initial_capital` |

### Performance Metrics

`performance_metrics()` returns a DataFrame with the following statistics computed on the daily return series:

| Metric | Description |
|---|---|
| Annualized Return | Compounded annual growth rate |
| Annualized Vol | Annualized standard deviation (252 trading days) |
| Sharpe Ratio | Annualized excess return over volatility |
| Max Drawdown | Largest peak-to-trough decline |
| Skewness | Return distribution asymmetry |
| Kurtosis | Tail heaviness of the return distribution |
| Cornish-Fisher VaR (5%) | Modified VaR adjusted for skewness and kurtosis |
| Historic CVaR (5%) | Average loss in the worst 5% of days |

### Performance Plots

`performance_plots()` displays a 2×2 figure with:
- **Price Simulation**: cumulative portfolio value over time
- **Asset Returns**: daily returns for each asset in the portfolio
- **Asset Prices**: normalized asset prices starting from `initial_capital`
- **Portfolio Returns Histogram**: distribution of daily portfolio returns

## Dependencies

- `pandas`
- `matplotlib`
- `numpy`
- `scipy`

## License

See [LICENSE](LICENSE).
