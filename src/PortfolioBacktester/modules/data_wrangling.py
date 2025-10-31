
import pandas as pd
import os
import pandas_market_calendars as mcal


def load_csv(path: str, csv_name: str) -> pd.DataFrame:

    file_path = os.path.join(path, f"{csv_name}.csv")
    df = pd.read_csv(file_path, index_col = 0)

    return df


def column_df(path: str, csv_name: str, column: str) -> pd.DataFrame:

    df = load_csv(path, csv_name)
    df_close = df[[column]].copy()
    df_close = df_close.rename(columns = {column: csv_name})

    return df_close


def reweight_from_df(df) -> pd.DataFrame:

    reweighted = df.copy()
    row_sum = reweighted.sum(axis = 1)
    safe_row_sums = row_sum.replace(0, 1)
    reweighted = reweighted.div(safe_row_sums, axis = 0)
    reweighted[row_sum == 0] = 0

    return reweighted


def get_investable_assets(df):

    inv_assets = list(df.columns)

    return inv_assets


def get_date_range(start_d, end_d):

    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_date = start_d, end_date = end_d)
    trading_days = schedule.index
    quarter_ends = pd.date_range(start=start_d, end=end_d, freq='Q')
    adjusted = []
    # adjust to closest previous trading day

    for qe in quarter_ends:
        pos = trading_days.get_indexer([qe], method='pad')[0]
        date = trading_days[pos]
        adjusted.append(date)

    return pd.DatetimeIndex(adjusted)


def get_dates(df):

    df = df
    start_date = df.index[0]
    end_date = df.index[-1]

    return start_date, end_date


def get_equal_weights(df) -> pd.DataFrame:

    signals = df.copy()
    active_rows = signals.sum(axis = 1)
    weights = signals.div(active_rows, axis = 0).fillna(0)

    return weights


def cumulative_returns(returns_df):

    cum_return_series = (1 + returns_df).cumprod()
    cum_return_benchmark = cum_return_series.to_frame("cum_returns")
    cum_return_benchmark.index = pd.to_datetime(cum_return_benchmark.index)

    return cum_return_benchmark
