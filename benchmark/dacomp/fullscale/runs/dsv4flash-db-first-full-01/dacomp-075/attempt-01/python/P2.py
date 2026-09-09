import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/focus_group_vendors.csv')

# ==========================================
# MULTI-DIMENSIONAL RESILIENCE FRAMEWORK
# ==========================================

# Helper: Min-Max normalization (0-100, higher = better)
def normalize_minmax(col, higher_is_better=True):
    c = df[col].values
    c_min, c_max = np.min(c), np.max(c)
    if c_max == c_min:
        return np.ones(len(c)) * 50
    if higher_is_better:
        return (c - c_min) / (c_max - c_min) * 100
    else:
        return (c_max - c) / (c_max - c_min) * 100

# ---------- Dimension 1: Financial Resilience ----------
# Components: payment delay (lower better), overdue % (lower better), 
# financial health score (higher better), payables/expenses ratio (lower better)
# avg_payment_delay - lower is better (fewer delays)
# overdue_payment_percentage - lower is better
# financial_health_score - higher is better

df['financial_delay_score'] = normalize_minmax('avg_payment_delay', higher_is_better=False)
df['financial_overdue_score'] = normalize_minmax('overdue_payment_percentage', higher_is_better=False)
df['financial_health_score_norm'] = normalize_minmax('financial_health_score', higher_is_better=True)

df['financial_resilience'] = (
    0.30 * df['financial_delay_score'] + 
    0.35 * df['financial_overdue_score'] + 
    0.35 * df['financial_health_score_norm']
)

# ---------- Dimension 2: Operational Resilience ----------
# Components: quality_score (higher better), cybersecurity_score (higher better), 
# innovation_capability_score (higher better)
df['quality_score_norm'] = normalize_minmax('quality_score', higher_is_better=True)
df['cybersecurity_score_norm'] = normalize_minmax('cybersecurity_score', higher_is_better=True)
df['innovation_score_norm'] = normalize_minmax('innovation_capability_score', higher_is_better=True)

df['operational_resilience'] = (
    0.35 * df['quality_score_norm'] + 
    0.35 * df['cybersecurity_score_norm'] + 
    0.30 * df['innovation_score_norm']
)

# ---------- Dimension 3: Market Resilience ----------
# Components: market_volatility_index (lower better), alternative_suppliers_count (higher better),
# price_volatility_coefficient (lower better), switching_cost_estimate (lower better)
df['market_volatility_score'] = normalize_minmax('market_volatility_index', higher_is_better=False)
df['alt_suppliers_score'] = normalize_minmax('alternative_suppliers_count', higher_is_better=True)
df['price_volatility_score'] = normalize_minmax('price_volatility_coefficient', higher_is_better=False)
df['switching_cost_score'] = normalize_minmax('switching_cost_estimate', higher_is_better=False)

df['market_resilience'] = (
    0.30 * df['market_volatility_score'] + 
    0.30 * df['alt_suppliers_score'] + 
    0.20 * df['price_volatility_score'] + 
    0.20 * df['switching_cost_score']
)

# ---------- Dimension 4: Strategic Resilience ----------
# Components: geographic distribution (diversity), contract expiry risk, environmental rating
# For geographic region - categorical, create a diversity score
# For contract expiry - days until expiry (higher better)
# For environmental_rating - ordinal mapping

# Parse contract expiry dates
df['contract_expiry_date'] = pd.to_datetime(df['contract_expiry_date'])
df['analysis_date'] = pd.to_datetime(df['analysis_date'])
df['days_until_contract_expiry'] = (df['contract_expiry_date'] - df['analysis_date']).dt.days

# Environmental rating mapping
env_map = {'A+': 100, 'A': 85, 'B+': 70, 'B': 60, 'B-': 50, 'C+': 40, 'C': 30, 'D': 20, 'F': 0}
df['env_score'] = df['environmental_rating'].map(env_map).fillna(30)

# Relationship stability mapping
stab_map = {'Mature': 100, 'Stable': 80, 'Developing': 50, 'Unstable': 20, 'Very New': 10}
df['stability_score'] = df['relationship_stability'].map(stab_map).fillna(50)

# Contract type diversity (strategic partnership = good diversification)
df['contract_type_score'] = np.where(df['contract_type'] == 'Strategic Partnership', 100,
                            np.where(df['contract_type'] == 'Preferred Vendor', 70,
                            np.where(df['contract_type'] == 'Annual contract with performance metrics', 50, 30)))

# Geographic region distribution risk
region_map = {'Global': 100, 'Northeast': 60, 'West Coast': 60, 'Southeast': 60, 
              'Southwest': 60, 'Central US': 60, 'Midwest': 60}
df['geo_score'] = df['geographic_region'].map(region_map).fillvalue(50) if hasattr(df['geographic_region'].map(region_map), 'fillvalue') else df['geographic_region'].map(region_map).fillna(50)

# Days until contract expiry - more days = better (less risk of sudden expiry)
df['contract_expiry_score'] = normalize_minmax('days_until_contract_expiry', higher_is_better=True)
# Days since last transaction - more recent = better
df['recency_score'] = normalize_minmax('days_since_last_transaction', higher_is_better=False)

# Relationship days - longer = more stable
df['relationship_days_score'] = normalize_minmax('vendor_relationship_days', higher_is_better=True)

df['strategic_resilience'] = (
    0.20 * df['geo_score'] + 
    0.20 * df['contract_expiry_score'] + 
    0.15 * df['env_score'] + 
    0.15 * df['stability_score'] + 
    0.15 * df['recency_score'] + 
    0.15 * df['relationship_days_score']
)

# ==========================================
# OVERALL RESILIENCE SCORE
# ==========================================
df['overall_resilience'] = (
    0.25 * df['financial_resilience'] + 
    0.25 * df['operational_resilience'] + 
    0.25 * df['market_resilience'] + 
    0.25 * df['strategic_resilience']
)

# ==========================================
# CLASSIFICATION
# ==========================================
def classify_resilience(score):
    if score >= 70: return 'High Resilience'
    elif score >= 50: return 'Medium Resilience'
    elif score >= 30: return 'Low Resilience'
    else: return 'Critical Risk'

df['resilience_class'] = df['overall_resilience'].apply(classify_resilience)

print("=== RESILIENCE SCORES SUMMARY ===")
print(f"Financial Resilience: Mean={df['financial_resilience'].mean():.1f}, SD={df['financial_resilience'].std():.1f}, Range=[{df['financial_resilience'].min():.1f}, {df['financial_resilience'].max():.1f}]")
print(f"Operational Resilience: Mean={df['operational_resilience'].mean():.1f}, SD={df['operational_resilience'].std():.1f}, Range=[{df['operational_resilience'].min():.1f}, {df['operational_resilience'].max():.1f}]")
print(f"Market Resilience: Mean={df['market_resilience'].mean():.1f}, SD={df['market_resilience'].std():.1f}, Range=[{df['market_resilience'].min():.1f}, {df['market_resilience'].max():.1f}]")
print(f"Strategic Resilience: Mean={df['strategic_resilience'].mean():.1f}, SD={df['strategic_resilience'].std():.1f}, Range=[{df['strategic_resilience'].min():.1f}, {df['strategic_resilience'].max():.1f}]")
print(f"Overall Resilience: Mean={df['overall_resilience'].mean():.1f}, SD={df['overall_resilience'].std():.1f}, Range=[{df['overall_resilience'].min():.1f}, {df['overall_resilience'].max():.1f}]")

print("\n=== RESILIENCE CLASS DISTRIBUTION ===")
print(df['resilience_class'].value_counts())

# Save scores
df.to_csv('/work/focus_group_with_scores.csv', index=False)
print("\nSaved scored data")

# Identify top 10 key vendors by spend
top_vendors = df.nlargest(10, 'total_vendor_spend')
print("\n=== TOP 10 VENDORS BY SPEND ===")
for _, r in top_vendors.iterrows():
    print(f"{r['vendor_name']:40s} | Spend=${r['total_vendor_spend']:>10,.0f} | Fin={r['financial_resilience']:.0f} | Ops={r['operational_resilience']:.0f} | Mkt={r['market_resilience']:.0f} | Strat={r['strategic_resilience']:.0f} | Overall={r['overall_resilience']:.0f} | Class={r['resilience_class']}")