import numpy as np
from numba import njit, prange
from financial_indicators import portfolio_variance, turnover, portfolio_moments

@njit
def evaluate_portfolio_fitness1(weights, mu, sigma, prev_weights, returns_history, 
                                risk_aversion, skewness_pref, kurtosis_aversion, turnover_aversion):
    expected_return = np.dot(weights, mu)
    risk = portfolio_variance(weights, sigma)
    sk, kt = portfolio_moments(weights, returns_history)
    weights_variation = turnover(weights, prev_weights)
    
    return (expected_return 
            - (risk_aversion * risk) 
            + (skewness_pref * sk) 
            - (kurtosis_aversion * kt) 
            - (turnover_aversion * weights_variation))

@njit(parallel=False)
def evaluate_population(population, mu, sigma, prev_weights, returns_history,
                        risk_aversion, skewness_pref, kurtosis_aversion, turnover_aversion):
    n_pop = population.shape[0]
    scores = np.empty(n_pop)
    
    for i in prange(n_pop): 
        scores[i] = evaluate_portfolio_fitness1(
            population[i], mu, sigma, prev_weights, returns_history,
            risk_aversion, skewness_pref, kurtosis_aversion, turnover_aversion
        )
    return scores