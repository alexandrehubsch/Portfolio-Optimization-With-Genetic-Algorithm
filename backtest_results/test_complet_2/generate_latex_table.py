#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le code LaTeX d'une longtable depuis le CSV des résultats de backtest.
Usage : python generate_latex_table.py resultats.csv [sortie.tex]
"""

import csv
import sys
import unicodedata

# Échappement LaTeX

ACCENT_MAP = {
    '\u00e9': r"\'e", '\u00e8': r'\`e', '\u00ea': r'\^e', '\u00eb': r'\"e',
    '\u00e0': r'\`a', '\u00e2': r'\^a', '\u00ee': r'\^i', '\u00ef': r'\"i',
    '\u00f4': r'\^o', '\u00f9': r'\`u', '\u00fb': r'\^u', '\u00fc': r'\"u',
    '\u00e7': r'\c{c}', '\u00c9': r"\'E", '\u00c8': r'\`E', '\u00c0': r'\`A',
    '\u00c7': r'\c{C}', '\u2013': '--', '\u2014': '---',
    '\u2019': "'", '\u2018': "'", '\u00a0': '~',
}

def latex_escape(s):
    if not isinstance(s, str):
        s = str(s)
    s = s.replace('\\', r'\textbackslash{}')
    for c, r in [('&',r'\&'), ('%',r'\%'), ('#',r'\#'), ('$',r'\$'),
                 ('{',r'\{'), ('}',r'\}'), ('_',r'\_')]:
        s = s.replace(c, r)
    for c, r in ACCENT_MAP.items():
        s = s.replace(c, r)
    return s

def clean_scenario(name):
    """FR_Bull_2015_2019  ->  FR Bull 2015 2019"""
    return name.replace('_', ' ')

def model_info(model):
    """Formate le nom du modèle pour LaTeX."""
    m = model.strip()
    ml = m.lower()
    if 'g' in ml and ('n' in ml) and ('tique' in ml or 'netique' in ml):
        return r'\textbf{A.G.}'
    elif 'variance' in ml or 'var' in ml:
        return r'Min.\,Var.'
    elif 'sharpe' in ml:
        return r'Max.\,Sh.'
    else:
        return latex_escape(m)

def fmt(val, dec=2):
    """Formate le nombre pour LaTeX."""
    try:
        f_val = float(val)
        res = f'{f_val:.{dec}f}'
        return res.replace('-', r'$-$')
    except:
        return '---'

# Lecture CSV

def read_csv_robust(path):
    for enc in ('utf-8-sig', 'utf-8', 'latin-1', 'cp1252'):
        try:
            with open(path, newline='', encoding=enc) as f:
                reader = csv.DictReader(f)
                raw_fields = reader.fieldnames
                if raw_fields is None:
                    continue
                clean_fields = [n.strip().lstrip('\ufeff') for n in raw_fields]
                reader.fieldnames = clean_fields
                rows = list(reader)
            print(f"  Encodage detecte : {enc}", file=sys.stderr)
            return rows, clean_fields
        except (UnicodeDecodeError, Exception) as e:
            continue
    print("ERREUR : impossible de lire le CSV.", file=sys.stderr)
    sys.exit(1)

COL_ALIASES = {
    'scenario':  ['Sc\u00e9nario', 'Scenario', 'scenario', 'SCENARIO'],
    'modele':    ['Mod\u00e8le', 'Modele', 'modele', 'Mod\xe8le'],
    'periode':   ['P\u00e9riode', 'Periode', 'periode', 'P\xe9riode'],
    'nb_actifs': ['Nb Actifs', 'NbActifs', 'nb_actifs'],
    'mode':      ['Mode', 'mode'],
    'rdt_tot':   ['Rendement Total (%)', 'Rendement Total'],
    'rdt_ann':   ['Rendement Annualis\u00e9 (%)', 'Rendement Annualise (%)', 'Rendement Annualise'],
    'vol_ann':   ['Volatilit\u00e9 Ann. (%)', 'Volatilite Ann. (%)', 'Volatilite Ann.'],
    'sharpe':    ['Ratio de Sharpe', 'Sharpe'],
    'sortino':   ['Ratio Sortino', 'Sortino'],
    'maxdd':     ['Perte Maximale (%)', 'Perte Maximale', 'Max DD'],
    'turnover':  ['Turnover Moyen', 'Turnover'],
}

def find_col(row, key):
    for alias in COL_ALIASES.get(key, [key]):
        if alias in row:
            return row[alias]
        for k in row:
            if unicodedata.normalize('NFC', k) == unicodedata.normalize('NFC', alias):
                return row[k]
    return ''

# Génération LaTeX

NCOLS = 11

# Colonnes dynamiques auto-ajustables
COL_FMT = r'p{2.6cm} l c c r r r r r r r'

def header_rows():
    h1 = (r'Sc\'enario & Mod\`ele & P\'er. & N & '
          r'Rdt Tot. & Rdt Ann. & Vol. & '
          r'Sharpe & Sortino & Max DD & Turnover moyen \\')
    h2 = (r' & & & & '
          r'(\%) & (\%) & (\%) & '
          r' & & (\%) & \\')
    return h1 + '\n' + h2

def generate(csv_path):
    rows, fields = read_csv_robust(csv_path)
    print(f"  {len(rows)} lignes lues.", file=sys.stderr)

    lines = []
    lines += [
        '% PACKAGES REQUIS dans le preambule :\n',
        '%   \\usepackage{longtable, booktabs, array, microtype}\n',
        '%   \\usepackage[utf8]{inputenc}\n',
        '% INCLUSION : \\input{table_generee.tex}\n\n',
        r'\begingroup' + '\n',
        r'\scriptsize' + '\n',
        r'\setlength{\tabcolsep}{4pt}' + '\n',            # Espacement horizontal
        r'\renewcommand{\arraystretch}{1.35}' + '\n',     # Espacement vertical
        r'\setlength{\LTcapwidth}{\linewidth}' + '\n',
        r'\begin{longtable}{' + COL_FMT + '}\n\n',
        r"\caption{R\'esultats complets des backtests -- A.G. vs mod\`eles de r\'ef\'erence (Configuration 2)}" + '\n',
        r'\label{tab:resultats_complets_conf2} \\' + '\n\n',
        r'\toprule' + '\n',
        header_rows() + '\n',
        r'\midrule' + '\n',
        r'\endfirsthead' + '\n\n',
        r'\multicolumn{' + str(NCOLS) + r'}{c}{\textit{(suite de la page pr\'ec\'edente)}} \\[4pt]' + '\n',
        r'\toprule' + '\n',
        header_rows() + '\n',
        r'\midrule' + '\n',
        r'\endhead' + '\n\n',
        r'\midrule' + '\n',
        r'\multicolumn{' + str(NCOLS) + r'}{r}{\textit{Suite page suivante\ldots}} \\' + '\n',
        r'\endfoot' + '\n\n',
        r'\bottomrule' + '\n',
        r'\addlinespace[1ex]' + '\n',
        (r'\multicolumn{' + str(NCOLS) + r'}{l}{\tiny\textit{'
         r"A.G. : Algorithme G\'en\'etique \quad|\quad "
         r'Min.\,Var. : Minimisation Variance \quad|\quad '
         r'Max.\,Sh. : Maximum Sharpe'
         r'}} \\[-0.5ex]' + '\n'),
        (r'\multicolumn{' + str(NCOLS) + r'}{l}{\tiny\textit{'
         r'N : nb actifs \quad|\quad '
         r'Turnover moyen : Turnover \quad|\quad '
         r'L/O : Long-Only \quad|\quad '
         r'L/S : Long/Short'
         r'}} \\' + '\n'),
        r'\endlastfoot' + '\n\n',
    ]

    prev_scenario = None
    for row in rows:
        scenario_raw = find_col(row, 'scenario')
        modele_raw   = find_col(row, 'modele')
        periode_raw  = find_col(row, 'periode')
        nb_actifs    = find_col(row, 'nb_actifs')
        mode_raw     = find_col(row, 'mode')
        rdt_tot      = find_col(row, 'rdt_tot')
        rdt_ann      = find_col(row, 'rdt_ann')
        vol_ann      = find_col(row, 'vol_ann')
        sharpe       = find_col(row, 'sharpe')
        sortino      = find_col(row, 'sortino')
        maxdd        = find_col(row, 'maxdd')
        turnover     = find_col(row, 'turnover')

        # Séparateur entre scénarios
        if prev_scenario is not None and scenario_raw != prev_scenario:
            lines.append(r'\midrule' + '\n')

        abbrev = model_info(modele_raw)
        scenario_tex = clean_scenario(scenario_raw)
        periode_tex  = periode_raw.replace('\u2013','--').replace('\u2014','--').replace('–','--')

        # Affichage du scénario sur la première ligne
        display_scenario = scenario_tex if scenario_raw != prev_scenario else ''

        lines.append(
            f'{display_scenario} & {abbrev} & {periode_tex} & {nb_actifs} & '
            f'{fmt(rdt_tot,1)} & {fmt(rdt_ann,2)} & {fmt(vol_ann,2)} & '
            f'{fmt(sharpe,3)} & {fmt(sortino,3)} & {fmt(maxdd,2)} & {fmt(turnover,3)} \\\\\n'
        )
        prev_scenario = scenario_raw

    lines += [
        r'\end{longtable}' + '\n',
        r'\endgroup' + '\n',
    ]
    return ''.join(lines)

# Main

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python generate_latex_table.py resultats.csv [sortie.tex]', file=sys.stderr)
        sys.exit(1)

    result = generate(sys.argv[1])

    if len(sys.argv) >= 3:
        out = sys.argv[2]
        with open(out, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'Fichier ecrit : {out}', file=sys.stderr)
    else:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        print(result)