import pandas as pd, numpy as np

df = pd.read_csv('/work/full_state_analysis.csv')

all_states = db.frame(db.query("SELECT state_name AS state FROM state_economic_data"))
missing = set(all_states['state']) - set(df['state'])
print("States missing from customer-based analysis:", sorted(missing))

# States with 0 reps
print("\nStates with n_reps=0:")
print(df[df['n_reps']==0][['state','n_reps','n_customers','CAC','investment_efficiency_score']].to_string())

print("\nStates with 0 customers (CAC NaN):")
print(df[df['CAC'].isna()][['state','n_customers','n_reps','investment_efficiency_score']].to_string())

# Correlation check of components
print("\nCorrelation of normalized components with final score:")
comps = ['n_CAC','n_avg_rev','n_med_rev','n_penetration','n_eff','n_conc','n_comp','n_return']
print(df[comps + ['investment_efficiency_score']].corr()['investment_efficiency_score'].sort_values(ascending=False).to_string())

# Full top 20
print("\nFull top-20 ranked states:")
print(df[['rank','state','investment_efficiency_score','CAC','avg_revenue','median_revenue','market_penetration','sales_efficiency','industry_concentration','competition_intensity_score','investment_return_score']].head(20).round(2).to_string())
