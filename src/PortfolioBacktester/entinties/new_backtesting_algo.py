import pandas as pd
import numpy as np
import datetime
import os

#TODO: wire this thing properly!
# https://claude.ai/share/eaef2a17-92f3-4a84-b6a8-fffdf9327615
def drop_mostly_null_rows(df, threshold=0.99):
    """
    Drops all rows from a DataFrame that contain more than `threshold` proportion of null values.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        threshold (float): The fraction of nulls allowed before a row is dropped (default = 0.99).

    Returns:
        pd.DataFrame: A DataFrame with mostly-null rows removed.
    """
    # Calculate the minimum number of non-null values required to keep the row
    min_non_nulls = int((1 - threshold) * df.shape[1])

    # Drop rows that don't meet the minimum non-null count
    cleaned_df = df.dropna(thresh=min_non_nulls)

    return cleaned_df

def index_backtesting_v2(kn_weights_df, price_data, effective_rebalance_dates):
    # EL COMAPRISON  ESTA EN EL INDEX repo
    price_data = drop_mostly_null_rows(price_data)
    effective_rebalance_dates = [
        i for
        i in
        effective_rebalance_dates if
                                 (i >= kn_weights_df.index[0]) and (i <= kn_weights_df.index[-1])
    ]
    kn_weights_df.index = effective_rebalance_dates

    dict_periodic_price_data = {}
    list_periodic_port_value = []
    dict_periodic_value_ps_in_port = {}
    n_rebalance_dates = len(effective_rebalance_dates)
    # ---------------
    for i in range(n_rebalance_dates):
        try:
            date = effective_rebalance_dates[i]
            next_date = effective_rebalance_dates[i + 1]
            dict_periodic_price_data[date] = price_data.loc[date:next_date]
            if i == n_rebalance_dates:
                dict_periodic_price_data[date] = dict_periodic_price_data[date]
            else:
                dict_periodic_price_data[date] = dict_periodic_price_data[date].iloc[:-1]

        except:
            dict_periodic_price_data[date] = price_data.loc[date:]
        # -----------------
        # This will give you theta
        if i ==0:
            rebalance_weights = kn_weights_df.loc[date]
        else:
            rebalance_weights = kn_weights_df.loc[date]*final_periodic_port_value

        # rebalance_weights = kn_weights_df.loc[date]
        price_rebal_date = price_data.loc[date]
        num_shares = rebalance_weights/price_rebal_date

        value_ps_in_port = num_shares.mul(dict_periodic_price_data[date], axis=0)
        dict_periodic_value_ps_in_port[date] = value_ps_in_port
        total_periodic_port_value = value_ps_in_port.sum(axis = 1)
        list_periodic_port_value.append(total_periodic_port_value)
        # final_val_i2 = ind_port2.sum(axis=1)
        final_periodic_port_value = total_periodic_port_value.iloc[-1]

    total_port_ts = pd.concat(list_periodic_port_value)

    portfolio_daily_returns = total_port_ts.pct_change()
    portfolio_daily_weights = pd.DataFrame()

    return portfolio_daily_returns, portfolio_daily_weights