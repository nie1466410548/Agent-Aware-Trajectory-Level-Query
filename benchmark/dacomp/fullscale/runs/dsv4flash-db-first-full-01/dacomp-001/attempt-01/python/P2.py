import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/company_metrics.csv')

# Fill NaN CV (single-year companies) with median
cv_median = df['cv'].median()
df['cv'].fillna(cv_median, inplace=True)
df['n_years'].fillna(1, inplace=True)

# ---- RISK SCORING MODEL ----
# Base risk from credit rating (ordinal encoding)
rating_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
df['rating_score'] = df['rating'].map(rating_map)

# Revenue capacity: log revenue (higher = better, so inverse)
# Companies with more revenue can handle larger loans
df['log_revenue'] = np.log1p(df['total_revenue'])

# Profit margin (higher = better)
# Profit stability: lower CV = more stable = better
# Concentration: higher top1_buyer or top1_supplier = higher dependency risk

# Normalize each factor to [0,1] range
def norm_inv(x):  # higher x = worse
    mn, mx = x.min(), x.max()
    if mx == mn: return np.zeros_like(x)
    return (x - mn) / (mx - mn)

def norm_dir(x):  # higher x = better
    mn, mx = x.min(), x.max()
    if mx == mn: return np.zeros_like(x)
    return (mx - x) / (mx - mn)

# Risk factors (higher = more risk)
risk_rating = norm_inv(df['rating_score'])      # 1-4 normalized
risk_revenue = norm_dir(df['log_revenue'])       # low revenue = high risk
risk_margin = norm_dir(df['margin'])             # low margin = high risk
risk_stability = norm_dir(df['cv'])              # high CV = high risk (normalized inversely)
risk_downstream = norm_inv(df['top1_buyer'])     # high buyer concentration = high risk
risk_upstream = norm_inv(df['top1_supplier'])    # high supplier concentration = high risk

# Composite risk score (weighted sum)
weights = {
    'rating': 0.30,
    'revenue': 0.20,
    'margin': 0.15,
    'stability': 0.15,
    'downstream': 0.10,
    'upstream': 0.10
}

df['risk_score'] = (weights['rating'] * risk_rating +
                    weights['revenue'] * risk_revenue +
                    weights['margin'] * risk_margin +
                    weights['stability'] * risk_stability +
                    weights['downstream'] * risk_downstream +
                    weights['upstream'] * risk_upstream)

# Check: defaulted companies should have higher risk scores
print("Defaulted vs non-defaulted risk scores:")
print(df.groupby('defaulted')['risk_score'].describe())

# --- RISK TIERS ---
# Use score quantiles to create tiers
df['risk_tier'] = pd.qcut(df['risk_score'], q=5, labels=['Very Low','Low','Medium','High','Very High'])
print("\nRisk tiers distribution:")
print(df.groupby('risk_tier', observed=False).agg({
    'code': 'count', 'rating': lambda x: x.value_counts().index[0], 
    'defaulted_flag': 'sum', 'total_revenue': 'sum'
}))

# ---- CREDIT ALLOCATION PLAN ----
# Total credit: 100,000,000 RMB
total_credit = 100_000_000

# Credit limit proportional to (1 - risk_score) * base_amount
# But also consider revenue capacity
df['credit_weight'] = (1 - df['risk_score']) * np.log1p(df['total_revenue'])
# Ensure minimum positive weight
df['credit_weight'] = df['credit_weight'].clip(lower=0.01)

total_weight = df['credit_weight'].sum()
df['credit_limit'] = total_credit * df['credit_weight'] / total_weight

print("\nCredit allocation by risk tier:")
print(df.groupby('risk_tier', observed=False)['credit_limit'].agg(['sum','mean','count']))

# ---- INTEREST RATE DESIGN ----
# Load churn rates
res2 = db.query('SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"')
churn = db.frame(res2)
churn_cols = {
    'A': 'Credit Rating A Customer Churn Rate',
    'B': 'Credit Rating B Customer Churn Rate',
    'C': 'Credit Rating C Customer Churn Rate'
}

# Expected revenue = rate * (1 - churn_rate) * loan_amount
# For each rate, compute expected return per unit loan
for r in ['A','B','C']:
    churn[f'expected_return_{r}'] = churn['Annual Loan Interest Rate'] * (1 - churn[churn_cols[r]])

# For D-rated, assume very high risk, use max rate
print("\n--- Optimal interest rate selection ---")
for r in ['A','B','C']:
    best_idx = churn[f'expected_return_{r}'].idxmax()
    best_rate = churn.loc[best_idx, 'Annual Loan Interest Rate']
    best_exp_return = churn.loc[best_idx, f'expected_return_{r}']
    best_churn = churn.loc[best_idx, churn_cols[r]]
    print(f"Rating {r}: optimal rate = {best_rate:.4f}, expected return rate = {best_exp_return:.4f}, churn = {best_churn:.4f}")

# Assign interest rates per company based on rating + risk tier
df['base_rate'] = 0.0
for r in ['A','B','C']:
    best_idx = churn[f'expected_return_{r}'].idxmax()
    best_rate = churn.loc[best_idx, 'Annual Loan Interest Rate']
    df.loc[df['rating']==r, 'base_rate'] = best_rate

# For D-rated, use highest rate (15%)
df.loc[df['rating']=='D', 'base_rate'] = 0.15

# Adjust rate within rating based on risk tier
tier_rate_adjust = {'Very Low': 0.0, 'Low': 0.005, 'Medium': 0.01, 'High': 0.015, 'Very High': 0.02}
df['rate_adjust'] = df['risk_tier'].map(tier_rate_adjust)
df['interest_rate'] = df['base_rate'] + df['rate_adjust']
# Cap rate at 15%
df['interest_rate'] = df['interest_rate'].clip(upper=0.15)

print("\nInterest rates by risk tier:")
print(df.groupby('risk_tier', observed=False)['interest_rate'].agg(['mean','min','max']))

# Save for visualization
df.to_csv('/work/allocation_plan.csv', index=False)

# ---- VISUALIZATION ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Risk score distribution by rating
for a in ['A','B','C','D']:
    sns.kdeplot(df[df['rating']==a]['risk_score'], label=f'Rating {a}', ax=axes[0,0])
axes[0,0].set_title('Risk Score Distribution by Credit Rating')
axes[0,0].set_xlabel('Risk Score')
axes[0,0].legend()

# 2. Credit limit distribution
colors = {'A':'green','B':'blue','C':'orange','D':'red'}
for r in ['A','B','C','D']:
    sub = df[df['rating']==r]
    axes[0,1].hist(sub['credit_limit']/1e4, alpha=0.6, label=f'Rating {r} (n={len(sub)})', color=colors[r], bins=15)
axes[0,1].set_title('Credit Limit Distribution by Rating')
axes[0,1].set_xlabel('Credit Limit (10K RMB)')
axes[0,1].set_ylabel('Count')
axes[0,1].legend()

# 3. Expected return vs interest rate
for r, col in churn_cols.items():
    axes[1,0].plot(churn['Annual Loan Interest Rate'], churn[f'expected_return_{r}'], 
                   marker='o', label=f'Rating {r}', linewidth=2)
axes[1,0].axvline(x=0.04, color='gray', linestyle='--', alpha=0.5)
axes[1,0].set_title('Expected Return Rate vs Interest Rate')
axes[1,0].set_xlabel('Annual Loan Interest Rate')
axes[1,0].set_ylabel('Expected Return Rate')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# 4. Total credit allocation by rating
total_by_rating = df.groupby('rating')['credit_limit'].sum()
axes[1,1].bar(total_by_rating.index, total_by_rating.values/1e4, color=[colors[r] for r in total_by_rating.index])
axes[1,1].set_title(f'Total Credit Allocation (Total: {total_credit/1e4:.0f}万 RMB)')
axes[1,1].set_xlabel('Credit Rating')
axes[1,1].set_ylabel('Total Credit (10K RMB)')
for i, v in enumerate(total_by_rating.values):
    axes[1,1].text(i, v/1e4, f'{v/1e4:.1f}万', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('/work/credit_analysis.png', dpi=150)
plt.close()
print("\nSaved figures to /work/credit_analysis.png")