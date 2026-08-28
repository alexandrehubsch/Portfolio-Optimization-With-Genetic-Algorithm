import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf
import config 

def compute_log_returns(prices_df):
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.log(prices_df / prices_df.shift(1)).fillna(0.0)

def get_market_estimators(prices_df, lookback_long, lookback_short):
    log_rets = compute_log_returns(prices_df)
    data_short = log_rets.tail(lookback_short)
    
    if data_short.shape[0] < 2:
        sigma = np.eye(prices_df.shape[1]) * 0.01
    else:
        lw = LedoitWolf().fit(data_short)
        sigma = lw.covariance_ * 252 
    
    if config.USE_EMA_ESTIMATOR:
        ema_fast = prices_df.ewm(span=config.EMA_FAST_WINDOW, adjust=False).mean().iloc[-1].fillna(0)
        ema_slow = prices_df.ewm(span=config.EMA_SLOW_WINDOW, adjust=False).mean().iloc[-1].fillna(0)
        
        expected_returns = np.where(ema_slow != 0, (ema_fast / ema_slow) - 1.0, 0.0)
    else:
        long_prices = prices_df.tail(lookback_long)
        total_period_return = (long_prices.iloc[-1] / long_prices.iloc[0].replace(0, 1)) - 1
        expected_returns = total_period_return.fillna(0).values * (252 / lookback_long)

    returns_slice = log_rets.tail(lookback_long)
    return np.nan_to_num(expected_returns), sigma, returns_slice