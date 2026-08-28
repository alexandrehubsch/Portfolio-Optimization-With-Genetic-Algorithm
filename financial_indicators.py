import numpy as np
from numba import njit

@njit
def portfolio_variance(weights, sigma):
    return np.dot(weights.T, np.dot(sigma, weights))

@njit
def turnover(w_new, w_old):
    return np.sum(np.abs(w_new - w_old))

@njit
def portfolio_moments(weights, returns_history):
    port_returns = np.dot(returns_history, weights)
    mean = np.mean(port_returns)
    std = np.std(port_returns)
    
    if std < 1e-8: # Évite division par zéro
        return 0.0, 0.0
        
    normalized = (port_returns - mean) / std
    s = np.mean(normalized**3) # Skewness
    k = np.mean(normalized**4) - 3.0 # Kurtosis centrée
    
    return s, k

@njit
def diversification_ratio(weights, sigma):
    indiv_vols = np.sqrt(np.diag(sigma))
    weighted_vols = np.dot(weights, indiv_vols)
    port_var = np.dot(weights.T, np.dot(sigma, weights))
    port_vol = np.sqrt(port_var)
    
    if port_vol < 1e-8:
        return 1.0 # Évite division par zéro
        
    return weighted_vols / port_vol