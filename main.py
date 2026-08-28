from classic_optimization import max_sharpe
import numpy as np
import os
import pandas as pd
import yfinance as yf
from tqdm import tqdm
import matplotlib.pyplot as plt
import textwrap
import config
from market_data import get_market_estimators
from genetic_algorithm import crossover, mutation, repair, fitness
from classic_optimization import newton_raphson_variance, max_sharpe
from numba import njit

@njit
def evolve_population(population, mu, cov_matrix, prev_weights, returns_history_np, 
                       generations, pop_size, elitism_count, mutation_rate, min_weight, max_weight,
                       risk_av, skew_pref, kurt_av, turn_av):
    
    # Évolution de la population
    best_global_solution = population[0].copy()
    best_global_score = -np.inf

    for gen in range(generations):
        scores = fitness.evaluate_population(
            population, mu, cov_matrix, prev_weights, returns_history_np,
            risk_av, skew_pref, kurt_av, turn_av
        )

        # Ordonner la population suivant leurs scores de fitness croissant
        ranking = np.argsort(scores)[::-1]
        population = population[ranking]

        if scores[ranking[0]] > best_global_score:
            best_global_score = scores[ranking[0]]
            best_global_solution = population[0].copy()

        next_population = np.empty_like(population)

        # Conservation des meilleurs individus
        for i in range(elitism_count):
            next_population[i] = population[i].copy()

        # Génération des enfants
        nb_children = pop_size - elitism_count
        
        # Sélection par tournoi
        p1_indices = np.empty(nb_children, dtype=np.int32)
        p2_indices = np.empty(nb_children, dtype=np.int32)
        tournament_size = 3
        
        for i in range(nb_children):
            t1 = np.random.randint(0, pop_size, tournament_size)
            p1_indices[i] = np.min(t1)
            t2 = np.random.randint(0, pop_size, tournament_size)
            p2_indices[i] = np.min(t2)

        idx = elitism_count
        for p1_idx, p2_idx in zip(p1_indices, p2_indices):
            child = crossover.blx_alpha_crossover(population[p1_idx], population[p2_idx])
            child = mutation.bump_mutation(child, mutation_rate, min_weight, max_weight)
            child = repair.repair_chromosome(child, min_weight, max_weight)
            next_population[idx] = child
            idx += 1

        population = next_population

    return best_global_solution

def genetic_algorithm(price_history, prev_weights):
    # Estimation des paramètres de marché
    mu, cov_matrix, returns_history = get_market_estimators(price_history, 
                                                            config.LOOKBACK_WINDOW, config.SHORT_WINDOW) 
    returns_history_np = returns_history.values 
    nb_assets = len(mu)

    if prev_weights is None:
        prev_weights = np.ones(nb_assets) / nb_assets

    effective_min_weight = config.MAX_SHORT_WEIGHT if config.ALLOW_SHORT_SELLING else 0.0

    # Initialisation et réparation de la population
    population = np.random.uniform(effective_min_weight, config.MAX_WEIGHT, (config.POPULATION_SIZE, nb_assets))
    for i in range(config.POPULATION_SIZE):
        population[i] = repair.repair_chromosome(population[i], effective_min_weight, config.MAX_WEIGHT)

    best_global_solution = evolve_population(
        population, mu, cov_matrix, prev_weights, returns_history_np,
        config.GENERATIONS, config.POPULATION_SIZE, config.ELITISM_COUNT, 
        config.MUTATION_RATE, effective_min_weight, config.MAX_WEIGHT,
        config.RISK_AVERSION, config.SKEWNESS_PREFERENCE, config.KURTOSIS_AVERSION, config.TURNOVER_AVERSION
    )
    return best_global_solution

def run_backtest(tickers, start_date, end_date, global_data=None, cac_data=None, plot=True, verbose=True):
    if global_data is not None and cac_data is not None:
        data = global_data.loc[start_date:end_date, tickers].copy()
        cac40_data = cac_data.loc[start_date:end_date].copy()
    else:
        if verbose:
            print(f"\n Téléchargement des données pour {len(tickers)} actifs...")
        data = yf.download(tickers, start=start_date, end=end_date, progress=verbose)['Close']
        cac40_data = yf.download('^FCHI', start=start_date, end=end_date, progress=verbose)['Close']
    
    # Nettoyage et complétion des prix
    data = data.ffill().bfill() 
    data = data.dropna(axis=1, thresh=len(data) * 0.8) 
    data = data.ffill() 

    cac40_data = cac40_data.ffill().bfill()
    cac40_returns = cac40_data.pct_change().dropna()

    valid_tickers = list(data.columns)
    if len(valid_tickers) < 2:
        raise ValueError(f"Pas assez d'actifs valides ({len(valid_tickers)}). L'optimisation nécessite au moins 2 actifs.")
    
    tickers = valid_tickers

    if len(tickers) == 0:
        raise ValueError("Aucun actif n'a d'historique complet sur cette période.")
        
    if len(data) <= config.LOOKBACK_WINDOW:
        raise ValueError(f"La période de backtest doit être plus longue que {config.LOOKBACK_WINDOW} jours.")

    portfolio_value_ga, portfolio_value_mv, portfolio_value_ms, cac40_value = 100, 100, 100, 100
    
    portfolio_values_ga, portfolio_values_mv, portfolio_values_ms, cac40_values, dates = [], [], [], [], []
    history_weights_ga, history_weights_mv, history_weights_ms = [], [], []
    
    prev_weights_ga, prev_weights_mv, prev_weights_ms = None, None, None

    start_idx = config.LOOKBACK_WINDOW
    
    iterable = range(start_idx, len(data), config.REBALANCE_FREQ)
    if verbose:
        iterable = tqdm(iterable, desc="Backtest en cours")
    
    for i in iterable: 
        price_history = data.iloc[:i]
        
        # Optimisations (GA, Min Var, Max Sharpe)
        mu, cov_matrix, _ = get_market_estimators(price_history, config.LOOKBACK_WINDOW, config.SHORT_WINDOW)
        
        weights_ga = genetic_algorithm(price_history, prev_weights_ga)
        weights_mv = newton_raphson_variance(cov_matrix) 
        weights_ms = max_sharpe(mu, cov_matrix)

        # Frais de transaction
        if prev_weights_ga is not None:
            portfolio_value_ga *= (1 - (np.sum(np.abs(weights_ga - prev_weights_ga)) * config.TRANSACTION_FEE))
            portfolio_value_mv *= (1 - (np.sum(np.abs(weights_mv - prev_weights_mv)) * config.TRANSACTION_FEE))
            portfolio_value_ms *= (1 - (np.sum(np.abs(weights_ms - prev_weights_ms)) * config.TRANSACTION_FEE))

        prices_evolution = data.iloc[i-1:min(i + config.REBALANCE_FREQ, len(data))]
        
        # Calcul des rendements du segment
        daily_returns = prices_evolution.pct_change().fillna(0.0).iloc[1:]
        
        if len(daily_returns) == 0:
            continue
        
        ret_vals = daily_returns.values
        
        port_vals_ga = portfolio_value_ga * np.cumprod(1 + (ret_vals @ weights_ga))
        port_vals_mv = portfolio_value_mv * np.cumprod(1 + (ret_vals @ weights_mv))
        port_vals_ms = portfolio_value_ms * np.cumprod(1 + (ret_vals @ weights_ms))
        
        cac_rets_segment = cac40_returns.reindex(daily_returns.index).fillna(0.0)
        if isinstance(cac_rets_segment, pd.DataFrame):
            cac_rets_segment = cac_rets_segment.iloc[:, 0]
        cac_vals = cac40_value * np.cumprod(1 + cac_rets_segment.values)
        
        portfolio_values_ga.extend(port_vals_ga)
        portfolio_values_mv.extend(port_vals_mv)
        portfolio_values_ms.extend(port_vals_ms)
        cac40_values.extend(cac_vals)
        dates.extend(daily_returns.index)
        
        segment_length = len(daily_returns)
        history_weights_ga.extend([weights_ga] * segment_length)
        history_weights_mv.extend([weights_mv] * segment_length)
        history_weights_ms.extend([weights_ms] * segment_length)
        
        portfolio_value_ga = port_vals_ga[-1]
        portfolio_value_mv = port_vals_mv[-1]
        portfolio_value_ms = port_vals_ms[-1]
        cac40_value = cac_vals[-1]
            
        prev_weights_ga, prev_weights_mv, prev_weights_ms = weights_ga, weights_mv, weights_ms
        
    # Assemblage des résultats
    results_df = pd.DataFrame(index=dates, data={
        'GA_Portfolio': portfolio_values_ga,
        'MV_Portfolio': portfolio_values_mv,
        'MS_Portfolio': portfolio_values_ms,
        'CAC40': cac40_values
    })
    
    df_w_ga = pd.DataFrame(history_weights_ga, index=dates, columns=tickers)
    df_w_mv = pd.DataFrame(history_weights_mv, index=dates, columns=tickers)
    df_w_ms = pd.DataFrame(history_weights_ms, index=dates, columns=tickers)
    
    # Graphiques
    if plot:
        plt.rcParams.update({"text.usetex": False, "font.family": "serif"})
        nb_days = len(results_df)
        def calc_returns(series):
            tot_ret = (series.iloc[-1] / series.iloc[0] - 1) * 100
            ann_ret = ((1 + tot_ret/100)**(252/nb_days) - 1) * 100
            return tot_ret, ann_ret
        
        tot_ga, ann_ga = calc_returns(results_df['GA_Portfolio'])
        tot_mv, ann_mv = calc_returns(results_df['MV_Portfolio'])
        tot_ms, ann_ms = calc_returns(results_df['MS_Portfolio'])
        tot_cac, ann_cac = calc_returns(results_df['CAC40'])

        tickers_str = ", ".join(tickers)
        wrapped_tickers = textwrap.fill(tickers_str, width=85)

        fig, axes = plt.subplots(4, 1, figsize=(14, 16), gridspec_kw={'height_ratios': [3, 1, 1, 1]}, sharex=True)
        fig.suptitle(f'Backtest et Comparaison des Performances', fontsize=15, y=0.97)
        
        axes[0].plot(results_df.index, results_df['GA_Portfolio'], label=f'GA ({tot_ga:.1f}%)', color='b', linewidth=1.5)
        axes[0].plot(results_df.index, results_df['MV_Portfolio'], label=f'Min Var ({tot_mv:.1f}%)', color='orange', linewidth=1.5, alpha=0.8)
        axes[0].plot(results_df.index, results_df['MS_Portfolio'], label=f'Max Sharpe ({tot_ms:.1f}%)', color='red', linewidth=1.5, alpha=0.8)
        axes[0].plot(results_df.index, results_df['CAC40'], label=f'CAC 40 ({tot_cac:.1f}%)', color='green', linewidth=1.5, linestyle=':')
        axes[0].axhline(100, color='gray', linestyle='--', linewidth=1)
        axes[0].legend(loc='upper left')
        axes[0].grid(True, alpha=0.3)

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        pos_weights = df_w_ga.clip(lower=0)
        neg_weights = df_w_ga.clip(upper=0)
        
        axes[1].stackplot(pos_weights.index, pos_weights.T, labels=pos_weights.columns, colors=colors[:len(tickers)], alpha=0.8)
        axes[1].stackplot(neg_weights.index, neg_weights.T, colors=colors[:len(tickers)], alpha=0.8)
        axes[1].axhline(0, color='black', linewidth=1, linestyle='--')
        axes[1].set_title('Allocation d\'actifs - Algorithme Génétique')
        
        axes[2].stackplot(df_w_mv.index, df_w_mv.T, labels=df_w_mv.columns, alpha=0.8)
        axes[2].set_title('Allocation d\'actifs - Minimisation Variance')

        axes[3].stackplot(df_w_ms.index, df_w_ms.T, labels=df_w_ms.columns, alpha=0.8)
        axes[3].set_title('Allocation d\'actifs - Maximisation Sharpe')
        
        handles, labels = axes[3].get_legend_handles_labels()
        fig.legend(handles, labels, loc='center left', title="Actifs", bbox_to_anchor=(0.91, 0.5))
        plt.tight_layout(rect=[0, 0.02, 0.90, 0.95], h_pad=2.0)
        
        os.makedirs("figure", exist_ok=True)
        plt.savefig(f"figure/backtest_complet_{start_date}_au_{end_date}.png", dpi=300)
        plt.show()

    return results_df, df_w_ga, df_w_mv, df_w_ms

if __name__ == "__main__":
    run_backtest(config.ASSETS, start_date=config.START_DATE, end_date=config.END_DATE)