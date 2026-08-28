import numpy as np
from numba import njit

@njit
def bump_mutation(weights, mutation_rate, min_weight, max_weight):
    """Perturbation de deux actifs dans les bornes autorisées."""
    if np.random.random() > mutation_rate:
        return weights

    mutated = weights.copy()
    n = len(weights)
    
    i = np.random.randint(0, n)
    j = np.random.randint(0, n)
    while i == j:
        j = np.random.randint(0, n)

    bump = np.random.uniform(0.01, 0.05)
    
    if mutated[i] + bump <= max_weight and mutated[j] - bump >= min_weight:
        mutated[i] += bump
        mutated[j] -= bump

    return mutated