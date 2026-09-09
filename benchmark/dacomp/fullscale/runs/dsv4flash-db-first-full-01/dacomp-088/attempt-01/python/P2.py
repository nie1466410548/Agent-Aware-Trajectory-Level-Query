import pandas as pd, numpy as np

# Re-read saved data
cust = pd.read_csv('/work/state_customer_metrics.csv')

# Merge with opp data
merged = cust.merge(opp, on='state', how='left').merge(reps, on='state', how='left').merge(eco, on='state', how='left')

# Handle missing values
merged['n_reps'] = merged['n_reps'].fillna(0)
merged['n_opps'] = merged['n_opps'].fillna(0)
merged['won_opps'] = merged['won_opps'].fillna(0)
merged['avg_won_amount'] = merged['avg_won_amount'].fillna(0)
merged['avg_won_prob'] = merged['avg_won_prob'].fillna(50)
merged['avg_won_cycle_days'] = merged['avg_won_cycle_days'].fillna(200)
merged['avg_probability'] = merged['avg_probability'].fillna(50)
merged['avg_cycle_days'] = merged['avg_cycle_days'].fillna(200)

# 1. CAC = (n_reps * 150000) / n_customers
merged['CAC'] = (merged['n_reps'] * 150000) / merged['n_customers'].replace(0, np.nan)

# 2. Average Customer Value (mean and median already computed)
# 3. Market Penetration Rate = n_customers / (population / 10000)
merged['market_penetration'] = merged['n_customers'] / (merged['population'] / 10000)

# 4. Sales Efficiency = avg_won_amount / avg_won_cycle_days * (avg_won_prob/100)
merged['sales_efficiency'] = (merged['avg_won_amount'] / merged['avg_won_cycle_days'].replace(0, np.nan)) * (merged['avg_won_prob'] / 100)

# 5. Industry Concentration already computed
# 6. Competition Intensity Assessment Model
# Based on: average win probability, average deal size, sales cycle length
# Normalize components first
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# Features for competition intensity: low win prob -> high competition, large deal size -> high competition, long cycle -> high competition
comp_features = merged[['avg_probability', 'avg_won_amount', 'avg_cycle_days']].fillna(merged[['avg_probability', 'avg_won_amount', 'avg_cycle_days']].median())
# Invert win probability (low win prob = high competition intensity)
comp_features['inv_win_prob'] = 100 - comp_features['avg_probability']
comp_features_scaled = scaler.fit_transform(comp_features[['inv_win_prob', 'avg_won_amount', 'avg_cycle_days']])
comp_features_scaled = pd.DataFrame(comp_features_scaled, columns=['win_prob_score', 'deal_size_score', 'cycle_score'])
merged['competition_intensity_score'] = (comp_features_scaled['win_prob_score'] * 0.35 + 
                                          comp_features_scaled['deal_size_score'] * 0.35 + 
                                          comp_features_scaled['cycle_score'] * 0.30) * 100

# 7. Investment Return Prediction Algorithm
# Incorporate: state GDP, population density, primary industry types, market maturity, business friendliness
# GDP per capita as proxy for economic strength
merged['population_density'] = merged['population'] / merged['population'].mean()  # relative density

# Score primary industry alignment with our customer base
our_top_industries = ['Technology', 'Manufacturing', 'Financial Services', 'Energy', 'Healthcare']
def industry_alignment(primary):
    if primary in our_top_industries:
        return 1.0
    return 0.5

merged['industry_alignment'] = merged['primary_industry'].apply(industry_alignment)

# Normalize economic indicators
eco_features = merged[['gdp_per_capita', 'market_maturity_score', 'business_friendly_index', 'competition_intensity']].fillna(0)
eco_scaled = scaler.fit_transform(eco_features)
eco_scaled = pd.DataFrame(eco_scaled, columns=['gdp_score', 'maturity_score', 'biz_friendly_score', 'comp_intensity'])
merged['investment_return_score'] = (
    eco_scaled['gdp_score'] * 0.25 +
    eco_scaled['maturity_score'] * 0.15 +
    eco_scaled['biz_friendly_score'] * 0.20 +
    merged['industry_alignment'] * 0.15 +
    (1 - eco_scaled['comp_intensity']) * 0.25
) * 100

# 8. Investment Efficiency Score (composite)
# Normalize all metric components
eff_features = merged[['CAC', 'avg_revenue', 'median_revenue', 'market_penetration', 
                       'sales_efficiency', 'industry_concentration', 'competition_intensity_score',
                       'investment_return_score']].fillna(0)

# For CAC, lower is better -> invert
eff_features_scaled = pd.DataFrame()
for col in eff_features.columns:
    vals = eff_features[col].fillna(0).values.reshape(-1, 1)
    scaled = scaler.fit_transform(vals).flatten()
    eff_features_scaled[col] = scaled

# Invert CAC (lower CAC = better)
eff_features_scaled['CAC'] = 1 - eff_features_scaled['CAC']

merged['investment_efficiency_score'] = (
    eff_features_scaled['CAC'] * 0.15 +
    eff_features_scaled['avg_revenue'] * 0.10 +
    eff_features_scaled['median_revenue'] * 0.10 +
    eff_features_scaled['market_penetration'] * 0.15 +
    eff_features_scaled['sales_efficiency'] * 0.15 +
    eff_features_scaled['industry_concentration'] * 0.05 +
    eff_features_scaled['competition_intensity_score'] * 0.10 +
    eff_features_scaled['investment_return_score'] * 0.20
) * 100

# Rank
merged = merged.sort_values('investment_efficiency_score', ascending=False)
merged['rank'] = range(1, len(merged)+1)

# Save
merged.to_csv('/work/full_state_analysis.csv', index=False)
print(merged[['state', 'rank', 'investment_efficiency_score', 'CAC', 'avg_revenue', 'median_revenue', 
              'market_penetration', 'sales_efficiency', 'industry_concentration',
              'competition_intensity_score', 'investment_return_score']].head(20).to_string())

print("\n\n=== Top 10 States for Investment ===")
print(merged[['state', 'rank', 'investment_efficiency_score']].head(10).to_string())
print("\n\n=== Bottom 10 States ===")
print(merged[['state', 'rank', 'investment_efficiency_score']].tail(10).to_string())