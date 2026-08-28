import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import textwrap
from concurrent.futures import ProcessPoolExecutor
import config
from test_scenarios import *
from main import run_backtest
import yfinance as yf

# Calcul des ratios pour les tableaux de résultats.

def compute_metrics(series, weights_df=None):
    if series is None or len(series) < 5: # Sécurité mini
        return {}

    nb_days = len(series)
    # Calcul des rendements arithmétiques (plus stables pour les métriques de risque)
    daily_returns = series.pct_change().dropna()

    # Filtre erreur yfinance
    # On remplace les rendements > 100% ou < -90% sur une seule journée (souvent des erreurs de données)
    # par 0 pour ne pas fausser la volatilité
    daily_returns = daily_returns.clip(lower=-0.9, upper=1.0)

    tot_ret = (series.iloc[-1] / series.iloc[0] - 1) * 100
    ann_ret = ((1 + tot_ret / 100) ** (252 / nb_days) - 1) * 100
    
    std_dev = daily_returns.std()
    ann_vol = std_dev * np.sqrt(252) * 100

    # Sharpe (gestion de la volatilité nulle)
    rf_daily = (1.02 ** (1 / 252)) - 1
    excess_ret = (daily_returns.mean() - rf_daily) * 252 * 100
    sharpe = excess_ret / ann_vol if ann_vol > 0.001 else 0.0
    rolling_max = series.cummax()
    drawdown = (series - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100
    calmar = ann_ret / abs(max_drawdown) if abs(max_drawdown) > 1e-6 else 0.0
    neg_returns = daily_returns[daily_returns < 0] # Sortino (volatilité à la baisse)
    downside_std = neg_returns.std() * np.sqrt(252) * 100
    sortino = excess_ret / downside_std if downside_std > 0.001 else 0.0

    return {
        "Rendement Total (%)":      round(tot_ret, 2),
        "Rendement Annualisé (%)": round(ann_ret, 2),
        "Volatilité Ann. (%)":      round(ann_vol, 2),
        "Ratio de Sharpe":          round(sharpe, 3),
        "Ratio Sortino":           round(sortino, 3),
        "Perte Maximale (%)":       round(max_drawdown, 2),
        "Ratio Calmar":            round(calmar, 3),
        "VaR 95% (%)":             round(float(np.percentile(daily_returns, 5)) * 100, 3),
        "CVaR 95% (%)":            round(float(daily_returns[daily_returns <= np.percentile(daily_returns, 5)].mean()) * 100, 3),
        "Skewness":                round(float(daily_returns.skew()), 3),
        "Kurtosis":                round(float(daily_returns.kurtosis()), 3),
        "Turnover Moyen":          0.0 if weights_df is None else round(float(weights_df.iloc[::config.REBALANCE_FREQ].diff().abs().sum(axis=1).mean()), 4)
    }


# Génération de graphiques

def save_scenario_chart(label, start, end, mode, results_df, df_w_ga, df_w_mv, df_w_ms, assets):
    plt.style.use('default')
    plt.rcParams.update({
        "text.usetex": False,
        "font.family": "serif",
        "axes.formatter.use_mathtext": True,
        "mathtext.fontset": "stix"
    })

    nb_days = len(results_df)

    def calc_returns(series):
        tot_ret = (series.iloc[-1] / series.iloc[0] - 1) * 100
        ann_ret = ((1 + tot_ret / 100) ** (252 / nb_days) - 1) * 100
        return tot_ret, ann_ret

    tot_ga, ann_ga   = calc_returns(results_df['GA_Portfolio'])
    tot_mv, ann_mv   = calc_returns(results_df['MV_Portfolio'])
    tot_ms, ann_ms   = calc_returns(results_df['MS_Portfolio'])
    tot_cac, ann_cac = calc_returns(results_df['CAC40'])

    tickers_str    = ", ".join(assets)
    wrapped_tickers = textwrap.fill(tickers_str, width=85)

    fig, axes = plt.subplots(4, 1, figsize=(14, 16),
                             gridspec_kw={'height_ratios': [3, 1, 1, 1]},
                             sharex=True)

    fig.suptitle(
        f'{label} ({mode})\nPériode : {start[:4]} – {end[:4]}\nActifs : {wrapped_tickers}',
        fontsize=15, y=0.97
    )

    # Panneau 0 : Performances
    axes[0].plot(results_df.index, results_df['GA_Portfolio'],
                 label=f'GA (Total: {tot_ga:.1f}% | Annuel: {ann_ga:.1f}%)', color='b', linewidth=1.5)
    axes[0].plot(results_df.index, results_df['MV_Portfolio'],
                 label=f'Min Variance (Total: {tot_mv:.1f}% | Annuel: {ann_mv:.1f}%)', color='orange', linewidth=1.5, alpha=0.8)
    axes[0].plot(results_df.index, results_df['MS_Portfolio'],
                 label=f'Max Sharpe (Total: {tot_ms:.1f}% | Annuel: {ann_ms:.1f}%)', color='red', linewidth=1.5, alpha=0.8)
    axes[0].plot(results_df.index, results_df['CAC40'],
                 label=f'CAC 40 (Total: {tot_cac:.1f}% | Annuel: {ann_cac:.1f}%)', color='green', linewidth=1.5, linestyle=':')
    axes[0].axhline(100, color='gray', linestyle='--', linewidth=1)
    axes[0].set_ylabel('Valeur (Base 100)', fontsize=11)
    axes[0].legend(loc='upper left', frameon=True, shadow=True, fontsize=10)
    axes[0].grid(True, alpha=0.3)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    n      = len(assets)

    # Panneau 1 : Allocation GA
    pos_weights = df_w_ga.clip(lower=0)
    neg_weights = df_w_ga.clip(upper=0)
    axes[1].stackplot(pos_weights.index, pos_weights.T, labels=pos_weights.columns, colors=ASSET_COLORS[:n], alpha=0.8)
    axes[1].stackplot(neg_weights.index, neg_weights.T, colors=ASSET_COLORS[:n], alpha=0.8)
    axes[1].axhline(0, color='black', linewidth=1, linestyle='--')
    axes[1].set_title("Allocation d'actifs — Algorithme Génétique", fontsize=11)
    axes[1].set_ylabel('Poids', fontsize=10)
    axes[1].margins(x=0, y=0)

    # Panneau 2 : Min Variance
    axes[2].stackplot(df_w_mv.index, df_w_mv.T, labels=df_w_mv.columns, colors=ASSET_COLORS[:n], alpha=0.8)
    axes[2].set_title("Allocation d'actifs — Minimisation Variance", fontsize=11)
    axes[2].set_ylabel('Poids', fontsize=10)
    axes[2].margins(x=0, y=0)

    # Panneau 3 : Max Sharpe
    axes[3].stackplot(df_w_ms.index, df_w_ms.T, labels=df_w_ms.columns, colors=ASSET_COLORS[:n], alpha=0.8)
    axes[3].set_title("Allocation d'actifs — Maximisation Sharpe", fontsize=11)
    axes[3].set_ylabel('Poids', fontsize=10)
    axes[3].set_xlabel('Date', fontsize=11)
    axes[3].margins(x=0, y=0)

    handles, labels_leg = axes[3].get_legend_handles_labels()
    fig.legend(handles, labels_leg, loc='center left', title="Actifs", bbox_to_anchor=(0.91, 0.5))
    plt.tight_layout(rect=[0, 0.02, 0.90, 0.95], h_pad=2.0)

    os.makedirs("figure", exist_ok=True)
    path = os.path.join("figure", f"{label}.png")
    plt.savefig(path, dpi=300)
    plt.close(fig)


# Exécution du scénario

def process_scenario(label, start, end, assets, allow_short, global_data, cac_data):
    config.ALLOW_SHORT_SELLING = allow_short
    config.MAX_SHORT_WEIGHT    = -0.15 if allow_short else 0.0

    try:

        results_df, df_w_ga, df_w_mv, df_w_ms = run_backtest(
            assets, start_date=start, end_date=end, 
            global_data=global_data, cac_data=cac_data, plot=False, verbose=False
        )
    except Exception as e:
        print(f"[ERREUR] {label} : {e}")
        return []

    mode = "Long/Short" if allow_short else "Long-Only"
    save_scenario_chart(label, start, end, mode, results_df, df_w_ga, df_w_mv, df_w_ms, assets)

    rows = []
    for model_name, series, weights in [
        ("Algorithme Génétique",  results_df["GA_Portfolio"], df_w_ga),
        ("Minimisation Variance", results_df["MV_Portfolio"], df_w_mv),
        ("Maximum Sharpe",        results_df["MS_Portfolio"], df_w_ms),
        ("CAC 40",                results_df["CAC40"],        None),
    ]:
        metrics = compute_metrics(series, weights_df=weights)
        rows.append({
            "Scénario":      label,
            "Période":       f"{start[:4]}–{end[:4]}",
            "Mode":          mode,
            "Nb Actifs":     len(assets),
            "Modèle":        model_name,
            **metrics,
        })

    ann_str = rows[0].get('Rendement Annualisé (%)', '?')
    shr_str = rows[0].get('Ratio de Sharpe', '?')
    dd_str  = rows[0].get('Perte Maximale (%)', '?')
    print(f"[OK] {label} ({mode}) | n={len(assets)} | GA ann.={ann_str}% | Sharpe={shr_str} | DD={dd_str}%")
    return rows

# Rapport de synthèse

def generate_summary_report(summary_df):
    """Génère un rapport texte de synthèse agrégé par modèle et par régime."""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("RAPPORT DE SYNTHÈSE — BACKTESTS DE ROBUSTESSE")
    report_lines.append("=" * 80)

    metrics_cols = [
        "Rendement Annualisé (%)", "Volatilité Ann. (%)", "Ratio de Sharpe","Ratio Sortino", 
        "Perte Maximale (%)", "Ratio Calmar", "VaR 95% (%)", "CVaR 95% (%)", "Turnover Moyen"
    ]

    # Agrégation par modèle
    report_lines.append("\n── PERFORMANCES MÉDIANES PAR MODÈLE ──")
    for col in ["Modèle"]:
        grp = summary_df.reset_index().groupby("Modèle")[metrics_cols].median()
        report_lines.append(grp.to_string())

    # Agrégation par mode (LO vs LS)
    report_lines.append("\n── PERFORMANCES MÉDIANES PAR MODE ──")
    grp_mode = summary_df.reset_index().groupby(["Mode", "Modèle"])[metrics_cols].median()
    report_lines.append(grp_mode.to_string())

    # Top 10 Sharpe
    report_lines.append("\n── TOP 10 SCÉNARIOS PAR RATIO DE SHARPE (Algorithme Génétique) ──")
    ga_df = summary_df.reset_index()
    ga_df = ga_df[ga_df["Modèle"] == "Algorithme Génétique"].sort_values("Ratio de Sharpe", ascending=False)
    report_lines.append(ga_df[["Scénario", "Période", "Mode", "Nb Actifs",
                                "Rendement Annualisé (%)", "Ratio de Sharpe", "Perte Maximale (%)"]].head(10).to_string(index=False))

    # Worst drawdowns
    report_lines.append("\n── TOP 10 PIRES DRAWDOWNS (Algorithme Génétique) ──")
    worst = ga_df.sort_values("Perte Maximale (%)").head(10)
    report_lines.append(worst[["Scénario", "Période", "Mode", "Nb Actifs",
                                "Rendement Annualisé (%)", "Ratio de Sharpe", "Perte Maximale (%)"]].to_string(index=False))

    return "\n".join(report_lines)

# Lancement des tests

def run_all_tests():
    all_results = []
    
    # Tickers uniques de tous les scénarios
    all_assets = set()
    for _, _, _, assets, _ in TEST_SCENARIOS:
        all_assets.update(assets)
    all_assets = list(all_assets)

    print(f"\n[INFO] ⬇️ TÉLÉCHARGEMENT GLOBAL de {len(all_assets)} actifs en cours (2007-2024)...")
    global_data = yf.download(all_assets, start="2007-01-01", end="2024-01-01", progress=False)['Close']
    global_data = global_data.ffill().bfill()
    
    print("[INFO] ⬇️ TÉLÉCHARGEMENT GLOBAL du CAC 40...")
    cac_data = yf.download('^FCHI', start="2007-01-01", end="2024-01-01", progress=False)['Close']
    cac_data = cac_data.ffill().bfill()
    
    print(f"[INFO] Lancement de {len(TEST_SCENARIOS)} scénarios de backtest en parallèle...")

    # Lancement des scénarios en parallèle
    with ProcessPoolExecutor() as executor:
        futures = {

            executor.submit(process_scenario, label, start, end, assets, allow_short, global_data, cac_data): label
            for label, start, end, assets, allow_short in TEST_SCENARIOS
        }
        for future in futures:
            try:
                all_results.extend(future.result())
            except Exception as e:
                print(f"[ERREUR parallèle] {futures[future]} : {e}")

    if not all_results:
        print("Aucun résultat à sauvegarder.")
        return

    summary_df = pd.DataFrame(all_results)
    summary_df.set_index(["Scénario", "Mode", "Modèle"], inplace=True)

    os.makedirs("figure", exist_ok=True)
    csv_path = "figure/resultats_robustesse.csv"
    summary_df.to_csv(csv_path)
    print(f"\n[SAUVEGARDÉ] {csv_path}")


    report = generate_summary_report(summary_df)
    report_path = "figure/rapport_synthese.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[SAUVEGARDÉ] {report_path}")
    print("\n" + report)

if __name__ == "__main__":
    run_all_tests()