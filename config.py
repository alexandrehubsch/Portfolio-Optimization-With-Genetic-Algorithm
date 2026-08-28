# Algorithme Génétique
POPULATION_SIZE = 1000
GENERATIONS = 3000
MUTATION_RATE = 0.15
ELITISM_COUNT = int(0.05 * POPULATION_SIZE) # 5% d'élitisme

# Paramètres temporels
LOOKBACK_WINDOW = 252          # 1 an de trading
SHORT_WINDOW = 21              # Tendance court terme
REBALANCE_FREQ = 21            # Rééquilibrage mensuel

# Paramètres fitness
RISK_AVERSION = 2            # Réduit le Max Drawdown
SKEWNESS_PREFERENCE = 0.05
KURTOSIS_AVERSION = 0.01       # Pénalise les chutes imprévisibles

# Contraintes
MAX_WEIGHT = 0.25              # Diversification max (25% par actif)
TRANSACTION_FEE = 0.002        # Frais de transaction (0.2%)

# Pénalité pour limiter le turnover
TURNOVER_AVERSION = TRANSACTION_FEE * (252 / REBALANCE_FREQ)

ALLOW_SHORT_SELLING = False    
MAX_SHORT_WEIGHT = -0.15      

# Estimateurs moyenne exponentielle mobile
USE_EMA_ESTIMATOR = True    
EMA_FAST_WINDOW = 40          
EMA_SLOW_WINDOW = 200       

# Pour test unitaire (main.py)
ASSETS   = ['MC.PA', 'TTE.PA', 'AI.PA', 'SAN.PA', 'OR.PA', 'BNP.PA', 'DG.PA', 'CS.PA', 'CAP.PA']
START_DATE = '2015-01-01'
END_DATE = '2019-12-31'