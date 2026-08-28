import numpy as np
from numba import njit

@njit
def blx_alpha_crossover(p1, p2, alpha=0.5):
    """Croisement BLX-alpha."""
    n = len(p1)
    child = np.empty(n)
    for i in range(n):
        x_min = min(p1[i], p2[i])
        x_max = max(p1[i], p2[i])
        diff = x_max - x_min
        low = x_min - alpha * diff
        high = x_max + alpha * diff
        child[i] = np.random.uniform(low, high)
    return child

@njit
def basic_crossover(p1, p2, alpha=0.5):
    return alpha * p1 + (1 - alpha) * p2