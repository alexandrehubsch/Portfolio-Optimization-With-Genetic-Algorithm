import matplotlib.pyplot as plt

# Style graphique minimaliste

PALETTE = {
    "GA":      "#2563EB",
    "MV":      "#F59E0B",
    "MS":      "#EF4444",
    "CAC":     "#6B7280",
    "zero":    "#D1D5DB",
    "bg":      "#FFFFFF",
    "grid":    "#F3F4F6",
    "text":    "#111827",
    "subtext": "#6B7280",
}

ASSET_COLORS = [
    "#2563EB", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6",
    "#EC4899", "#14B8A6", "#F97316", "#6366F1", "#84CC16",
    "#06B6D4", "#A855F7", "#F43F5E", "#22C55E", "#EAB308",
    "#3B82F6", "#E11D48", "#059669", "#D97706", "#7C3AED",
    "#0EA5E9", "#D946EF", "#65A30D", "#EA580C", "#7E22CE",
    "#0284C7", "#BE185D", "#4D7C0F", "#C2410C", "#6D28D9",
    "#0369A1", "#9D174D", "#3F6212", "#9A3412", "#5B21B6",
    "#075985", "#831843", "#365314", "#7C2D12", "#4C1D95",
]


def apply_minimal_style():
    plt.rcParams.update({
        "figure.facecolor":      PALETTE["bg"],
        "axes.facecolor":        PALETTE["bg"],
        "axes.edgecolor":        PALETTE["grid"],
        "axes.linewidth":        0.6,
        "axes.spines.top":       False,
        "axes.spines.right":     False,
        "axes.spines.left":      False,
        "axes.spines.bottom":    True,
        "axes.grid":             True,
        "axes.grid.axis":        "y",
        "grid.color":            PALETTE["grid"],
        "grid.linewidth":        0.8,
        "xtick.color":           PALETTE["subtext"],
        "ytick.color":           PALETTE["subtext"],
        "xtick.labelsize":       8,
        "ytick.labelsize":       8,
        "xtick.major.size":      0,
        "ytick.major.size":      0,
        "text.color":            PALETTE["text"],
        "font.family":           "sans-serif",
        "font.size":             9,
        "legend.frameon":        False,
        "legend.fontsize":       8,
        "figure.dpi":            150,
    })


# Univers d'actifs - France et Europe

FR_BLUE_CHIPS   = ['MC.PA', 'TTE.PA', 'AI.PA', 'SAN.PA', 'OR.PA', 'BNP.PA', 'DG.PA', 'CS.PA', 'CAP.PA']
FR_FINANCE      = ['BNP.PA', 'CS.PA', 'GLE.PA', 'ACA.PA', 'SGO.PA']
FR_ENERGIE      = ['TTE.PA', 'ENGI.PA', 'VIE.PA']
FR_TECH         = ['CAP.PA', 'ATO.PA', 'DSY.PA']
FR_LARGE_CAP    = ['MC.PA', 'TTE.PA', 'AI.PA', 'SAN.PA', 'OR.PA', 'BNP.PA', 'DG.PA', 'CS.PA',
                   'CAP.PA', 'GLE.PA', 'ACA.PA', 'ENGI.PA', 'VIE.PA', 'ATO.PA', 'DSY.PA']

EU_MIXED        = ['ASML.AS', 'SAP.DE', 'NOVO-B.CO', 'NESN.SW', 'ROG.SW']
EU_FINANCE      = ['SAN.MC', 'BBVA.MC', 'ISP.MI', 'DBK.DE', 'INGA.AS']
EU_INDUSTRIAL   = ['SIE.DE', 'ABB.ST', 'SGRO.L', 'RR.L', 'AIR.PA']
EU_HEALTHCARE   = ['NOVO-B.CO', 'ROG.SW', 'AZN.L', 'NVO', 'SAN.PA']
EU_BROAD        = ['ASML.AS', 'SAP.DE', 'NOVO-B.CO', 'NESN.SW', 'ROG.SW',
                   'SAN.MC', 'BBVA.MC', 'DBK.DE', 'INGA.AS', 'AIR.PA',
                   'SIE.DE', 'AZN.L', 'OR.PA', 'MC.PA', 'TTE.PA']

# Univers d'actifs - États-Unis

US_MEGA_TECH    = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA']
US_FINANCE      = ['JPM', 'BAC', 'GS', 'MS', 'BRK-B']
US_SANTE        = ['JNJ', 'PFE', 'MRK', 'ABBV', 'UNH']
US_ENERGIE      = ['XOM', 'CVX', 'COP', 'SLB', 'EOG']
US_CONSO        = ['PG', 'KO', 'PEP', 'WMT', 'COST']
US_DIVERSIFIED  = ['AAPL', 'MSFT', 'JPM', 'JNJ', 'XOM', 'BRK-B', 'PG', 'KO']
US_INDUSTRIE    = ['HON', 'GE', 'MMM', 'CAT', 'DE']
US_TELECOM      = ['T', 'VZ', 'TMUS', 'CMCSA']
US_IMMOBILIER   = ['AMT', 'PLD', 'SPG', 'EQIX', 'O']
US_MATERIALS    = ['LIN', 'APD', 'ECL', 'NEM', 'FCX']
US_LARGE_BLEND  = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA',
                   'JPM', 'BAC', 'JNJ', 'PFE', 'XOM', 'CVX',
                   'PG', 'KO', 'WMT', 'BRK-B', 'HON', 'CAT']
US_SMALL_CAP    = ['IWM', 'VBR', 'SLYV', 'IJR', 'VBK']  # via ETFs small-cap

# Univers d'actifs - Marchés émergents et Asie

EM_BROAD        = ['EEM', 'VWO', 'IEMG', 'GXC', 'EWZ']
EM_ASIA         = ['EWJ', 'EWY', 'EWT', 'MCHI', 'INDA']
EM_LATAM        = ['EWZ', 'EWW', 'ECH', 'EPU', 'GXG']
EM_EMEA         = ['EZA', 'TUR', 'EPOL', 'EGPT', 'KSA']
ASIA_PACIFIC    = ['EWJ', 'EWY', 'EWT', 'EWA', 'EWH', 'EWS', 'THD', 'EPHE']
CHINA_FOCUS     = ['MCHI', 'GXC', 'FXI', 'KWEB', 'CQQQ']
INDIA_FOCUS     = ['INDA', 'INDY', 'EPI', 'PIN']

# Univers d'actifs - ETF

ETF_US          = ['SPY', 'QQQ', 'IWM', 'DIA']
ETF_INTL        = ['EFA', 'EEM', 'VGK', 'EWJ']
ETF_SECTORS     = ['XLK', 'XLF', 'XLE', 'XLV', 'XLY', 'XLP']
ETF_BONDS       = ['TLT', 'IEF', 'SHY', 'HYG', 'EMB']
ETF_REAL_ASSETS = ['GLD', 'SLV', 'USO', 'VNQ', 'PDBC']
ETF_BROAD_MKT   = ['SPY', 'QQQ', 'IWM', 'DIA', 'EFA', 'EEM', 'VGK',
                   'EWJ', 'GLD', 'TLT', 'IEF', 'HYG']
ETF_THEMATIC    = ['ARKK', 'ARKG', 'ARKW', 'CLOU', 'BOTZ', 'ROBO']
ETF_ESG         = ['ESGU', 'ESGV', 'SUSL', 'CRBN', 'MOTE']
ETF_LEVERAGE    = ['SSO', 'QLD', 'TQQQ', 'UPRO', 'UDOW']  # 2x/3x — volatilité extrême
ETF_INVERSE     = ['SH', 'PSQ', 'DOG', 'RWM', 'SDS']      # inverses — utiles en bear

# Univers d'actifs - Matières premières

COMMODITIES_BROAD  = ['GLD', 'SLV', 'USO', 'UNG', 'PDBC', 'CORN', 'WEAT', 'SOYB']
COMMODITIES_METALS = ['GLD', 'SLV', 'PPLT', 'PALL', 'DBP', 'GDX', 'GDXJ']
COMMODITIES_ENERGY = ['USO', 'UNG', 'BNO', 'AMLP', 'XLE', 'XOP', 'OIH']
REAL_ASSETS        = ['GLD', 'SLV', 'USO', 'VNQ', 'PDBC', 'REET', 'WPC', 'O']
INFLATION_HEDGE    = ['TIP', 'SCHP', 'GLD', 'VNQ', 'USO', 'PDBC', 'CORN', 'BCI']

# Univers d'actifs - Cryptomonnaies

CRYPTO_MAJORS   = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
CRYPTO_LARGE    = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD', 'AVAX-USD', 'DOT-USD']
CRYPTO_DEFI     = ['ETH-USD', 'LINK-USD', 'UNI-USD', 'AAVE-USD', 'MKR-USD', 'CRV-USD']
CRYPTO_BROAD    = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'XRP-USD',
                   'AVAX-USD', 'DOT-USD', 'MATIC-USD', 'LINK-USD', 'ADA-USD']

# Portefeuilles diversifiés (10-35 actifs)


MIX_FR_US           = ['MC.PA', 'TTE.PA', 'OR.PA', 'BNP.PA', 'AAPL', 'MSFT', 'JPM', 'JNJ']
MIX_FR_ETF          = ['MC.PA', 'TTE.PA', 'AI.PA', 'SAN.PA', 'SPY', 'GLD', 'TLT']
MIX_ACTIONS_OR      = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'GLD', 'SLV']
MIX_ACTIONS_BONDS   = ['SPY', 'QQQ', 'EFA', 'TLT', 'IEF', 'HYG']
MIX_60_40           = ['SPY', 'QQQ', 'EFA', 'EEM', 'TLT', 'IEF', 'GLD', 'SHY']
MIX_ALL_ASSET       = ['SPY', 'EFA', 'EEM', 'TLT', 'GLD', 'USO', 'VNQ', 'BTC-USD']
MIX_FR_CRYPTO       = ['MC.PA', 'TTE.PA', 'OR.PA', 'SAN.PA', 'BTC-USD', 'ETH-USD']
MIX_EU_US           = ['ASML.AS', 'SAP.DE', 'NESN.SW', 'AAPL', 'MSFT', 'GOOGL', 'JPM', 'JNJ']
MIX_DEFENSIVE       = ['JNJ', 'PG', 'KO', 'PEP', 'WMT', 'TLT', 'GLD', 'SHY']
MIX_OFFENSIF        = ['NVDA', 'TSLA', 'META', 'AMZN', 'BTC-USD', 'ETH-USD', 'SOL-USD']
MIX_SECTEURS_US     = ['XLK', 'XLF', 'XLE', 'XLV', 'XLY', 'XLP', 'SPY']
MIX_FR_EU           = ['MC.PA', 'TTE.PA', 'OR.PA', 'BNP.PA', 'ASML.AS', 'SAP.DE', 'NOVO-B.CO', 'NESN.SW']


MIX_GLOBAL_15 = [
    'SPY', 'EFA', 'EEM', 'EWJ', 'VGK',
    'TLT', 'IEF', 'HYG', 'EMB', 'GLD',
    'USO', 'VNQ', 'BTC-USD', 'AAPL', 'MSFT'
]

MIX_GLOBAL_20 = [
    'SPY', 'QQQ', 'EFA', 'EEM', 'EWJ',
    'VGK', 'TLT', 'IEF', 'SHY', 'HYG',
    'EMB', 'GLD', 'SLV', 'USO', 'VNQ',
    'BTC-USD', 'ETH-USD', 'AAPL', 'MSFT', 'JPM'
]

MIX_RISK_PARITY_20 = [
    'SPY', 'EFA', 'EEM', 'TLT', 'IEF',
    'SHY', 'HYG', 'EMB', 'GLD', 'SLV',
    'USO', 'VNQ', 'PDBC', 'CORN', 'WEAT',
    'BTC-USD', 'ETH-USD', 'XLP', 'XLV', 'XLU'
]

MIX_ENDOWMENT_20 = [
    'SPY', 'EFA', 'EEM', 'QQQ', 'IWM',
    'VGK', 'EWJ', 'VNQ', 'REET', 'GLD',
    'TLT', 'IEF', 'HYG', 'EMB', 'TIP',
    'USO', 'PDBC', 'BTC-USD', 'AAPL', 'MSFT'
]


MIX_WORLD_25 = [
    'SPY', 'QQQ', 'IWM', 'EFA', 'EEM',
    'EWJ', 'EWY', 'MCHI', 'EWZ', 'VGK',
    'ASML.AS', 'NESN.SW', 'SAP.DE', 'TLT', 'IEF',
    'HYG', 'EMB', 'GLD', 'SLV', 'USO',
    'VNQ', 'BTC-USD', 'ETH-USD', 'AAPL', 'MSFT'
]

MIX_WORLD_30 = [
    'SPY', 'QQQ', 'IWM', 'DIA', 'EFA',
    'EEM', 'EWJ', 'EWY', 'EWT', 'MCHI',
    'EWZ', 'VGK', 'ASML.AS', 'NESN.SW', 'TLT',
    'IEF', 'SHY', 'HYG', 'EMB', 'TIP',
    'GLD', 'SLV', 'USO', 'VNQ', 'PDBC',
    'BTC-USD', 'ETH-USD', 'AAPL', 'MSFT', 'GOOGL'
]

MIX_ULTRA_DIV_35 = [
    'SPY', 'QQQ', 'IWM', 'DIA', 'EFA',
    'EEM', 'EWJ', 'EWY', 'EWT', 'MCHI',
    'INDA', 'EWZ', 'EWW', 'EZA', 'VGK',
    'ASML.AS', 'SAP.DE', 'NESN.SW', 'TLT', 'IEF',
    'SHY', 'HYG', 'EMB', 'TIP', 'GLD',
    'SLV', 'USO', 'UNG', 'VNQ', 'PDBC',
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'AAPL', 'MSFT'
]


MIX_TECH_THEMATIC  = ['QQQ', 'ARKK', 'BOTZ', 'CLOU', 'NVDA', 'TSLA', 'MSFT', 'AAPL', 'GOOGL', 'META']
MIX_GREEN_ENERGY   = ['ICLN', 'QCLN', 'TAN', 'FAN', 'ENPH', 'SEDG', 'PLUG', 'FSLR', 'BEP', 'NEE']
MIX_HEALTHCARE_GL  = ['XLV', 'IHI', 'IBB', 'ARKG', 'JNJ', 'UNH', 'ABBV', 'PFE', 'NOVO-B.CO', 'AZN.L']
MIX_REAL_ASSETS_EX = ['GLD', 'SLV', 'PPLT', 'USO', 'UNG', 'VNQ', 'REET', 'PDBC', 'CORN', 'WEAT', 'BCI', 'TIP']
MIX_CRYPTO_ETF     = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'BNB-USD', 'LINK-USD',
                      'ADA-USD', 'DOT-USD', 'AVAX-USD', 'MATIC-USD', 'XRP-USD']


MIX_CRISIS_PROOF = ['GLD', 'TLT', 'SHY', 'TIP', 'VNQ', 'XLV', 'XLP', 'XLU', 'SH', 'PSQ']
MIX_STAGFLATION  = ['GLD', 'SLV', 'USO', 'UNG', 'TIP', 'PDBC', 'VNQ', 'XLE', 'CVX', 'XOM']


MIX_LEVERAGE_2X  = ['SSO', 'QLD', 'UGL', 'UCO', 'ROM', 'UYG', 'RXL', 'AGQ']
MIX_MOMENTUM_US  = ['AAPL', 'MSFT', 'NVDA', 'META', 'GOOGL', 'AMZN', 'TSLA', 'AMD', 'CRM', 'NFLX']


# Scenarios de test

TEST_SCENARIOS = [

    # France
    ("FR_Bull_2015_2019",           "2015-01-01", "2019-12-31", FR_BLUE_CHIPS,    False),
    ("FR_Covid_2020_2021",          "2020-01-01", "2021-12-31", FR_BLUE_CHIPS,    False),
    ("FR_Inflation_2022_2023",      "2022-01-01", "2023-12-31", FR_BLUE_CHIPS,    False),
    ("FR_LongTerm_2010_2023",       "2010-01-01", "2023-12-31", FR_BLUE_CHIPS,    False),
    ("FR_GFC_2007_2009",            "2007-01-01", "2009-12-31", FR_BLUE_CHIPS,    False),
    ("FR_PostGFC_2009_2012",        "2009-01-01", "2012-12-31", FR_BLUE_CHIPS,    False),
    ("FR_CriseEuro_2010_2013",      "2010-01-01", "2013-12-31", FR_BLUE_CHIPS,    False),
    ("FR_FullCycle_2007_2023",      "2007-01-01", "2023-12-31", FR_LARGE_CAP,     False),

    # France - Secteurs
    ("FR_Finance_2015_2023",        "2015-01-01", "2023-12-31", FR_FINANCE,       False),
    ("FR_Energie_2015_2023",        "2015-01-01", "2023-12-31", FR_ENERGIE,       False),
    ("FR_Tech_2015_2023",           "2015-01-01", "2023-12-31", FR_TECH,          False),

    # Europe
    ("EU_Mixed_2015_2023",          "2015-01-01", "2023-12-31", EU_MIXED,         False),
    ("EU_Finance_2015_2023",        "2015-01-01", "2023-12-31", EU_FINANCE,       False),
    ("EU_Healthcare_2015_2023",     "2015-01-01", "2023-12-31", EU_HEALTHCARE,    False),
    ("EU_Industrial_2015_2023",     "2015-01-01", "2023-12-31", EU_INDUSTRIAL,    False),
    ("EU_Broad_2015_2023",          "2015-01-01", "2023-12-31", EU_BROAD,         False),
    ("EU_Mixed_Covid",              "2020-01-01", "2021-12-31", EU_MIXED,         False),
    ("EU_Mixed_Bear_2022",          "2022-01-01", "2023-12-31", EU_BROAD,         False),
    ("EU_GFC_2007_2009",            "2007-01-01", "2009-12-31", EU_BROAD,         False),
    ("EU_LongTerm_2010_2023",       "2010-01-01", "2023-12-31", EU_BROAD,         False),

    # États-Unis
    ("US_MegaTech_2015_2023",       "2015-01-01", "2023-12-31", US_MEGA_TECH,     False),
    ("US_Finance_2015_2023",        "2015-01-01", "2023-12-31", US_FINANCE,       False),
    ("US_Sante_2015_2023",          "2015-01-01", "2023-12-31", US_SANTE,         False),
    ("US_Energie_2015_2023",        "2015-01-01", "2023-12-31", US_ENERGIE,       False),
    ("US_Conso_2015_2023",          "2015-01-01", "2023-12-31", US_CONSO,         False),
    ("US_Diversified_2015_2023",    "2015-01-01", "2023-12-31", US_DIVERSIFIED,   False),
    ("US_Industrie_2015_2023",      "2015-01-01", "2023-12-31", US_INDUSTRIE,     False),
    ("US_Immobilier_2015_2023",     "2015-01-01", "2023-12-31", US_IMMOBILIER,    False),
    ("US_Materials_2015_2023",      "2015-01-01", "2023-12-31", US_MATERIALS,     False),
    ("US_LargeBlend_2015_2023",     "2015-01-01", "2023-12-31", US_LARGE_BLEND,   False),
    ("US_MegaTech_Bull",            "2019-01-01", "2021-12-31", US_MEGA_TECH,     False),
    ("US_MegaTech_Bear",            "2022-01-01", "2023-12-31", US_MEGA_TECH,     False),
    ("US_GFC_2007_2009",            "2007-01-01", "2009-12-31", US_DIVERSIFIED,   False),
    ("US_LongTerm_2007_2023",       "2007-01-01", "2023-12-31", US_LARGE_BLEND,   False),
    ("US_Momentum_Bull_2019_2021",  "2019-01-01", "2021-12-31", MIX_MOMENTUM_US,  False),
    ("US_Momentum_Bear_2022_2023",  "2022-01-01", "2023-12-31", MIX_MOMENTUM_US,  False),

    # Émergents et Asie
    ("EM_Broad_2015_2023",          "2015-01-01", "2023-12-31", EM_BROAD,         False),
    ("EM_Asia_2015_2023",           "2015-01-01", "2023-12-31", EM_ASIA,          False),
    ("EM_LatAm_2015_2023",          "2015-01-01", "2023-12-31", EM_LATAM,         False),
    ("Asia_Pacific_2015_2023",      "2015-01-01", "2023-12-31", ASIA_PACIFIC,     False),
    ("China_Focus_2015_2023",       "2015-01-01", "2023-12-31", CHINA_FOCUS,      False),
    ("China_Bear_2021_2023",        "2021-01-01", "2023-12-31", CHINA_FOCUS,      False),
    ("India_Focus_2015_2023",       "2015-01-01", "2023-12-31", INDIA_FOCUS,      False),
    ("EM_Covid_2020_2021",          "2020-01-01", "2021-12-31", EM_BROAD,         False),
    ("EM_Bear_2022_2023",           "2022-01-01", "2023-12-31", EM_BROAD,         False),

    # ETF
    ("ETF_US_Indices_2015_2023",    "2015-01-01", "2023-12-31", ETF_US,           False),
    ("ETF_Intl_2015_2023",          "2015-01-01", "2023-12-31", ETF_INTL,         False),
    ("ETF_Sectors_2015_2023",       "2015-01-01", "2023-12-31", ETF_SECTORS,      False),
    ("ETF_Bonds_2015_2023",         "2015-01-01", "2023-12-31", ETF_BONDS,        False),
    ("ETF_RealAssets_2015_2023",    "2015-01-01", "2023-12-31", ETF_REAL_ASSETS,  False),
    ("ETF_Bonds_Hausse_Taux",       "2022-01-01", "2023-12-31", ETF_BONDS,        False),
    ("ETF_Broad_2015_2023",         "2015-01-01", "2023-12-31", ETF_BROAD_MKT,    False),
    ("ETF_Thematic_2019_2023",      "2019-01-01", "2023-12-31", ETF_THEMATIC,     False),
    ("ETF_Thematic_Bull_2020_2021", "2020-01-01", "2021-12-31", ETF_THEMATIC,     False),
    ("ETF_Thematic_Bear_2022",      "2022-01-01", "2022-12-31", ETF_THEMATIC,     False),

    # Matières premières
    ("Commod_Broad_2015_2023",      "2015-01-01", "2023-12-31", COMMODITIES_BROAD,  False),
    ("Commod_Metals_2015_2023",     "2015-01-01", "2023-12-31", COMMODITIES_METALS, False),
    ("Commod_Energy_2015_2023",     "2015-01-01", "2023-12-31", COMMODITIES_ENERGY, False),
    ("Commod_Energy_Bear_2014_2016","2014-01-01", "2016-12-31", COMMODITIES_ENERGY, False),
    ("Commod_Energy_Bull_2021_2022","2021-01-01", "2022-12-31", COMMODITIES_ENERGY, False),
    ("RealAssets_2015_2023",        "2015-01-01", "2023-12-31", REAL_ASSETS,        False),
    ("InflationHedge_2021_2023",    "2021-01-01", "2023-12-31", INFLATION_HEDGE,    False),

    # Cryptomonnaies
    ("Crypto_Majors_2019_2023",     "2019-01-01", "2023-12-31", CRYPTO_MAJORS,    False),
    ("Crypto_Large_2020_2023",      "2020-01-01", "2023-12-31", CRYPTO_LARGE,     False),
    ("Crypto_Bull_2020_2021",       "2020-01-01", "2021-12-31", CRYPTO_MAJORS,    False),
    ("Crypto_Bear_2022",            "2022-01-01", "2022-12-31", CRYPTO_MAJORS,    False),
    ("Crypto_DeFi_2020_2023",       "2020-01-01", "2023-12-31", CRYPTO_DEFI,      False),
    ("Crypto_Broad_2020_2023",      "2020-01-01", "2023-12-31", CRYPTO_BROAD,     False),
    ("Crypto_Broad_Bear_2022",      "2022-01-01", "2022-12-31", CRYPTO_BROAD,     False),

    # Portefeuilles multi-classes
    ("Mix_FR_US_2015_2023",         "2015-01-01", "2023-12-31", MIX_FR_US,        False),
    ("Mix_FR_ETF_2015_2023",        "2015-01-01", "2023-12-31", MIX_FR_ETF,       False),
    ("Mix_Actions_Or_2015_2023",    "2015-01-01", "2023-12-31", MIX_ACTIONS_OR,   False),
    ("Mix_Actions_Bonds_2015_2023", "2015-01-01", "2023-12-31", MIX_ACTIONS_BONDS,False),
    ("Mix_60_40_2015_2023",         "2015-01-01", "2023-12-31", MIX_60_40,        False),
    ("Mix_AllAsset_2015_2023",      "2015-01-01", "2023-12-31", MIX_ALL_ASSET,    False),
    ("Mix_FR_Crypto_2019_2023",     "2019-01-01", "2023-12-31", MIX_FR_CRYPTO,    False),
    ("Mix_EU_US_2015_2023",         "2015-01-01", "2023-12-31", MIX_EU_US,        False),
    ("Mix_Defensif_2015_2023",      "2015-01-01", "2023-12-31", MIX_DEFENSIVE,    False),
    ("Mix_Offensif_2019_2023",      "2019-01-01", "2023-12-31", MIX_OFFENSIF,     False),
    ("Mix_Secteurs_US_2015_2023",   "2015-01-01", "2023-12-31", MIX_SECTEURS_US,  False),
    ("Mix_FR_EU_2015_2023",         "2015-01-01", "2023-12-31", MIX_FR_EU,        False),
    ("Mix_60_40_Covid",             "2020-01-01", "2021-12-31", MIX_60_40,        False),
    ("Mix_60_40_Inflation",         "2022-01-01", "2023-12-31", MIX_60_40,        False),
    ("Mix_Defensif_Bear",           "2022-01-01", "2023-12-31", MIX_DEFENSIVE,    False),
    ("Mix_Offensif_Bear",           "2022-01-01", "2023-12-31", MIX_OFFENSIF,     False),
    ("Mix_AllAsset_Covid",          "2020-01-01", "2021-12-31", MIX_ALL_ASSET,    False),

    # Portefeuilles 15-20 actifs
    ("Global15_2015_2023",          "2015-01-01", "2023-12-31", MIX_GLOBAL_15,       False),
    ("Global15_Covid",              "2020-01-01", "2021-12-31", MIX_GLOBAL_15,       False),
    ("Global15_Bear_2022",          "2022-01-01", "2023-12-31", MIX_GLOBAL_15,       False),
    ("Global20_2015_2023",          "2015-01-01", "2023-12-31", MIX_GLOBAL_20,       False),
    ("Global20_GFC",                "2007-01-01", "2009-12-31", MIX_GLOBAL_20,       False),
    ("Global20_Covid",              "2020-01-01", "2021-12-31", MIX_GLOBAL_20,       False),
    ("Global20_Bear_2022",          "2022-01-01", "2023-12-31", MIX_GLOBAL_20,       False),
    ("RiskParity20_2015_2023",      "2015-01-01", "2023-12-31", MIX_RISK_PARITY_20,  False),
    ("RiskParity20_Inflation",      "2022-01-01", "2023-12-31", MIX_RISK_PARITY_20,  False),
    ("Endowment20_2015_2023",       "2015-01-01", "2023-12-31", MIX_ENDOWMENT_20,    False),
    ("Endowment20_Covid",           "2020-01-01", "2021-12-31", MIX_ENDOWMENT_20,    False),

    # Portefeuilles 25-35 actifs
    ("World25_2015_2023",           "2015-01-01", "2023-12-31", MIX_WORLD_25,        False),
    ("World25_Covid",               "2020-01-01", "2021-12-31", MIX_WORLD_25,        False),
    ("World25_Bear_2022",           "2022-01-01", "2023-12-31", MIX_WORLD_25,        False),
    ("World30_2015_2023",           "2015-01-01", "2023-12-31", MIX_WORLD_30,        False),
    ("World30_GFC",                 "2007-01-01", "2009-12-31", MIX_WORLD_30,        False),
    ("World30_Covid",               "2020-01-01", "2021-12-31", MIX_WORLD_30,        False),
    ("World30_Bear_2022",           "2022-01-01", "2023-12-31", MIX_WORLD_30,        False),
    ("UltraDiv35_2015_2023",        "2015-01-01", "2023-12-31", MIX_ULTRA_DIV_35,    False),
    ("UltraDiv35_Covid",            "2020-01-01", "2021-12-31", MIX_ULTRA_DIV_35,    False),
    ("UltraDiv35_Bear_2022",        "2022-01-01", "2023-12-31", MIX_ULTRA_DIV_35,    False),
    ("UltraDiv35_FullCycle",        "2015-01-01", "2023-12-31", MIX_ULTRA_DIV_35,    False),

    # Portefeuilles thématiques
    ("TechThematic_2019_2023",      "2019-01-01", "2023-12-31", MIX_TECH_THEMATIC,   False),
    ("TechThematic_Bull_2020_2021", "2020-01-01", "2021-12-31", MIX_TECH_THEMATIC,   False),
    ("TechThematic_Bear_2022",      "2022-01-01", "2022-12-31", MIX_TECH_THEMATIC,   False),
    ("GreenEnergy_2019_2023",       "2019-01-01", "2023-12-31", MIX_GREEN_ENERGY,    False),
    ("GreenEnergy_Bull_2020_2021",  "2020-01-01", "2021-12-31", MIX_GREEN_ENERGY,    False),
    ("GreenEnergy_Bear_2022",       "2022-01-01", "2022-12-31", MIX_GREEN_ENERGY,    False),
    ("Healthcare_Global_2015_2023", "2015-01-01", "2023-12-31", MIX_HEALTHCARE_GL,   False),
    ("RealAssets_Extended_2015_23", "2015-01-01", "2023-12-31", MIX_REAL_ASSETS_EX,  False),
    ("CrisisProof_2007_2023",       "2007-01-01", "2023-12-31", MIX_CRISIS_PROOF,    False),
    ("CrisisProof_GFC",             "2007-01-01", "2009-12-31", MIX_CRISIS_PROOF,    False),
    ("CrisisProof_Covid",           "2020-01-01", "2021-12-31", MIX_CRISIS_PROOF,    False),
    ("Stagflation_2021_2023",       "2021-01-01", "2023-12-31", MIX_STAGFLATION,     False),
    ("CryptoETF_2019_2023",         "2019-01-01", "2023-12-31", MIX_CRYPTO_ETF,      False),

    # LO vs LS
    ("FR_LO_Bull",                  "2015-01-01", "2019-12-31", FR_BLUE_CHIPS,    False),
    ("FR_LS_Bull",                  "2015-01-01", "2019-12-31", FR_BLUE_CHIPS,    True),
    ("FR_LO_Bear",                  "2022-01-01", "2023-12-31", FR_BLUE_CHIPS,    False),
    ("FR_LS_Bear",                  "2022-01-01", "2023-12-31", FR_BLUE_CHIPS,    True),
    ("FR_LO_Covid",                 "2020-01-01", "2021-12-31", FR_BLUE_CHIPS,    False),
    ("FR_LS_Covid",                 "2020-01-01", "2021-12-31", FR_BLUE_CHIPS,    True),
    ("US_LO_Bull",                  "2015-01-01", "2019-12-31", US_DIVERSIFIED,   False),
    ("US_LS_Bull",                  "2015-01-01", "2019-12-31", US_DIVERSIFIED,   True),
    ("US_LO_Bear",                  "2022-01-01", "2023-12-31", US_DIVERSIFIED,   False),
    ("US_LS_Bear",                  "2022-01-01", "2023-12-31", US_DIVERSIFIED,   True),
    ("US_LO_GFC",                   "2007-01-01", "2009-12-31", US_DIVERSIFIED,   False),
    ("US_LS_GFC",                   "2007-01-01", "2009-12-31", US_DIVERSIFIED,   True),
    ("Mix_FR_US_LO_2019_2023",      "2019-01-01", "2023-12-31", MIX_FR_US,        False),
    ("Mix_FR_US_LS_2019_2023",      "2019-01-01", "2023-12-31", MIX_FR_US,        True),
    ("Mix_AllAsset_LO_2019_2023",   "2019-01-01", "2023-12-31", MIX_ALL_ASSET,    False),
    ("Mix_AllAsset_LS_2019_2023",   "2019-01-01", "2023-12-31", MIX_ALL_ASSET,    True),
    ("Global20_LO_2015_2023",       "2015-01-01", "2023-12-31", MIX_GLOBAL_20,    False),
    ("Global20_LS_2015_2023",       "2015-01-01", "2023-12-31", MIX_GLOBAL_20,    True),
    ("World30_LO_2015_2023",        "2015-01-01", "2023-12-31", MIX_WORLD_30,     False),
    ("World30_LS_2015_2023",        "2015-01-01", "2023-12-31", MIX_WORLD_30,     True),
    ("Mix_Offensif_LO_2019_2023",   "2019-01-01", "2023-12-31", MIX_OFFENSIF,     False),
    ("Mix_Offensif_LS_2019_2023",   "2019-01-01", "2023-12-31", MIX_OFFENSIF,     True),
    ("Mix_Defensif_LO_2015_2023",   "2015-01-01", "2023-12-31", MIX_DEFENSIVE,    False),
    ("Mix_Defensif_LS_2015_2023",   "2015-01-01", "2023-12-31", MIX_DEFENSIVE,    True),
    ("Crypto_LO_2020_2023",         "2020-01-01", "2023-12-31", CRYPTO_MAJORS,    False),
    ("Crypto_LS_2020_2023",         "2020-01-01", "2023-12-31", CRYPTO_MAJORS,    True),
    ("UltraDiv35_LO_2015_2023",     "2015-01-01", "2023-12-31", MIX_ULTRA_DIV_35, False),
    ("UltraDiv35_LS_2015_2023",     "2015-01-01", "2023-12-31", MIX_ULTRA_DIV_35, True),

    # Périodes économiques
    ("Global_GFC_2007_2009",        "2007-01-01", "2009-12-31", MIX_GLOBAL_20,       False),
    ("Global_PostGFC_2009_2015",    "2009-01-01", "2015-12-31", MIX_GLOBAL_20,       False),
    ("Global_QE_Era_2012_2018",     "2012-01-01", "2018-12-31", MIX_GLOBAL_20,       False),
    ("Global_PreCovid_2018_2020",   "2018-01-01", "2020-12-31", MIX_GLOBAL_20,       False),
    ("Global_Covid_Recovery",       "2020-03-01", "2021-12-31", MIX_GLOBAL_20,       False),
    ("Global_Tightening_2022_2023", "2022-01-01", "2023-12-31", MIX_GLOBAL_20,       False),
    ("Global_FullCycle_2007_2023",  "2007-01-01", "2023-12-31", MIX_GLOBAL_20,       False),
    ("60_40_GFC",                   "2007-01-01", "2009-12-31", MIX_60_40,           False),
    ("60_40_QE_Era",                "2012-01-01", "2021-12-31", MIX_60_40,           False),
    ("60_40_FullCycle_2007_2023",   "2007-01-01", "2023-12-31", MIX_60_40,           False),
]

