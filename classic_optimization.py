import numpy as np
from scipy.optimize import minimize
from numba import njit
import config

@njit
def newton_raphson_variance(sigma, max_iter=20, tol=1e-5):
    n = sigma.shape[0]
    w = np.ones(n) / n 
    ones = np.ones(n)
    H = sigma + np.outer(ones, ones) 

    for i in range(max_iter): 
        grad = np.dot(sigma, w) + (w.sum() - 1) * ones 
        d = np.linalg.solve(H, -grad) 
        w_new = w + d
        w_new = np.maximum(w_new, 0) 

        if np.linalg.norm(w_new - w) < tol:
            w = w_new
            break
        w = w_new

    return w / w.sum() 

def max_sharpe(mu, sigma, risk_free_rate=0.0):
    """Maximise le ratio de Sharpe (par algorthime SLSQP)."""
    n = len(mu)
    
    # Minimisation de l'opposé du Sharpe
    def negative_sharpe(w):
        port_ret = np.dot(w, mu)
        port_var = np.dot(w.T, np.dot(sigma, w))
        port_std = np.sqrt(port_var)

        if port_std < 1e-8:
            return 0.0
            
        return -(port_ret - risk_free_rate) / port_std

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    min_w = config.MAX_SHORT_WEIGHT if config.ALLOW_SHORT_SELLING else 0.0
    max_w = config.MAX_WEIGHT
    bounds = tuple((min_w, max_w) for _ in range(n))
    
    init_guess = np.ones(n) / n
    
    result = minimize(negative_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x