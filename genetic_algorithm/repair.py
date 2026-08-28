import numpy as np
from numba import njit

@njit
def repair_chromosome(weights, min_weight, max_weight):
    n = len(weights)
    
    if min_weight >= 0.0:
        # Mode Long-Only
        if n * min_weight > 1.0 or n * max_weight < 1.0:
            return np.ones(n) / n
            
        for i in range(n):
            if weights[i] < min_weight: weights[i] = min_weight
            elif weights[i] > max_weight: weights[i] = max_weight
                
        for _ in range(5):
            current_sum = np.sum(weights)
            diff = 1.0 - current_sum
            
            if abs(diff) < 1e-7:
                break
                
            total_room = 0.0
            if diff > 0:
                for i in range(n): total_room += max_weight - weights[i]
            else:
                for i in range(n): total_room += weights[i] - min_weight
                    
            if total_room < 1e-8:
                break
                
            for i in range(n):
                if diff > 0:
                    adj = diff * ((max_weight - weights[i]) / total_room)
                else:
                    adj = diff * ((weights[i] - min_weight) / total_room)
                
                weights[i] += adj
                
                if weights[i] < min_weight: weights[i] = min_weight
                elif weights[i] > max_weight: weights[i] = max_weight

        return weights
    else:
        # Mode Long/Short (sum(|w_i|) = 1)
        limit = max(abs(min_weight), abs(max_weight))
        if n * limit < 1.0:
            return np.ones(n) / n
            
        for i in range(n):
            if weights[i] < min_weight:
                weights[i] = min_weight
            elif weights[i] > max_weight:
                weights[i] = max_weight

        for _ in range(10):
            gross_exposure = 0.0
            for i in range(n):
                gross_exposure += abs(weights[i])

            if gross_exposure < 1e-10:
                return np.ones(n) / n

            scale = 1.0 / gross_exposure
            for i in range(n):
                weights[i] *= scale

            clipped = False
            for i in range(n):
                if weights[i] < min_weight:
                    weights[i] = min_weight
                    clipped = True
                elif weights[i] > max_weight:
                    weights[i] = max_weight
                    clipped = True

            if not clipped:
                break

        return weights