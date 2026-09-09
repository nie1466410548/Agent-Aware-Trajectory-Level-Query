import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/company_metrics.csv')

# Fill NaN CV with median
cv_med = df['cv'].median()
df['cv'] = df['cv'].fillna(cv_med)
df['n_years'] = df['n_years'].fillna(1)

# ---- RISK SCORING ----
rating_map = {'A':1,'B':2,'C':3,'D':4}
df['rating_score'] = df['rating'].map(rating_map)

df['log_revenue'] = np.log1p(df['total_revenue'])

def norm_inv(x):
    mn, mx = x.min(), x.max()
    if mx == mn: return np.zeros(len(x))
    return (x - mn) / (mx - mn)

def norm_dir(x):
    mn, mx = x.min(), x.max()
    if mx == mn: return np.zeros(len(x))
    return (mx - x) / (mx - mn)

risk_rating = norm_inv(df['rating_score'].values)
risk_revenue = norm_dir(df['log_revenue'].values)
risk_margin = norm_dir(df['margin'].values)
risk_stability = norm_dir(df['cv'].values)
risk_downstream = norm_inv(df['top1_buyer'].values)
risk_upstream = norm_inv(df['top1_supplier'].values)

weights = {'rating':0.30,'revenue':0.20,'margin':0.15,'stability':0.15,'downstream':0.10,'upstream':0.10}
df['risk_score'] = (weights['rating']*risk_rating + weights['revenue']*risk_revenue +
                    weights['margin']*risk_margin + weights['stability']*risk_stability +
                    weights['downstream']*risk_downstream + weights['upstream']*risk_upstream)

print("Risk score by default status:")
print(df.groupby('defaulted')['risk_score'].describe())

# Risk tiers - use qcut but convert to string to avoid categorical issues
df['risk_tier'] = pd.qcut(df['risk_score'], q=5, labels=['Very Low','Low','Medium','High','Very High'])
df['risk_tier'] = df['risk_tier'].astype(str)

print("\nRisk tiers:")
print(df.groupby('risk_tier')['risk_score'].agg(['count','min','max']))

# ---- CREDIT ALLOCATION ----
total_credit = 100_000_000
df['credit_weight'] = (1 - df['risk_score']) * np.log1p(df['total_revenue'])
df['credit_weight'] = df['credit_weight'].clip(lower=0.01)
total_w = df['credit_weight'].sum()
df['credit_limit'] = total_credit * df['credit_weight'] / total_w

print("\nCredit allocation by rating:")
print(df.groupby('rating')['credit_limit'].agg(['sum','mean','count']))
print("\nTotal allocated:", df['credit_limit'].sum())

# ---- INTEREST RATE DESIGN ----
res = db.query('SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"')
churn = db.frame(res)

churn_cols = {'A':'Credit Rating A Customer Churn Rate','B':'Credit Rating B Customer Churn Rate','C':'Credit Rating C Customer Churn Rate'}

for r in ['A','B','C']:
    churn[f'exp_ret_{r}'] = churn['Annual Loan Interest Rate'] * (1 - churn[churn_cols[r]])

print("\nOptimal interest rates by rating:")
best_rates = {}
for r in ['A','B','C']:
    idx = churn[f'exp_ret_{r}'].idxmax()
    best_rates[r] = churn.loc[idx, 'Annual Loan Interest Rate']
    print(f"  Rating {r}: rate={best_rates[r]:.4f}, expected_return={churn.loc[idx, f'exp_ret_{r}']:.4f}, churn={churn.loc[idx, churn_cols[r]]:.4f}")

# Assign base rates
df['base_rate'] = 0.0
for r in ['A','B','C']:
    df.loc[df['rating']==r, 'base_rate'] = best_rates[r]
df.loc[df['rating']=='D', 'base_rate'] = 0.15

# Risk tier adjustment (within rating)
tier_adj = {'Very Low':0.0, 'Low':0.005, 'Medium':0.01, 'High':0.015, 'Very High':0.02}
df['rate_adjust'] = df['risk_tier'].map(tier_adj)
df['interest_rate'] = df['base_rate'] + df['rate_adjust']
df['interest_rate'] = df['interest_rate'].clip(upper=0.15)

print("\nInterest rates by tier:")
print(df.groupby('risk_tier')['interest_rate'].agg(['mean','min','max']))

# ---- VISUALIZATION ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Risk score by rating
for r in ['A','B','C','D']:
    sns.kdeplot(df[df['rating']==r]['risk_score'], label=f'Rating {r}', ax=axes[0,0])
axes[0,0].set_title('Risk Score Distribution by Credit Rating')
axes[0,0].set_xlabel('Risk Score')
axes[0,0].legend()

# 2. Credit limit by rating
colors = {'A':'green','B':'blue','C':'orange','D':'red'}
for r in ['A','B','C','D']:
    sub = df[df['rating']==r]
    axes[0,1].hist(sub['credit_limit']/1e4, alpha=0.6, label=f'Rating {r} (n={len(sub)})', color=colors[r], bins=15)
axes[0,1].set_title('Credit Limit Distribution by Rating')
axes[0,1].set_xlabel('Credit Limit (10K RMB)')
axes[0,1].set_ylabel('Count')
axes[0,1].legend()

# 3. Expected return vs rate
for r, col in churn_cols.items():
    axes[1,0].plot(churn['Annual Loan Interest Rate'], churn[f'exp_ret_{r}'], 
                   marker='o', label=f'Rating {r}', linewidth=2)
axes[1,0].set_title('Expected Return Rate vs Interest Rate')
axes[1,0].set_xlabel('Annual Loan Interest Rate')
axes[1,0].set_ylabel('Expected Return Rate')
axes[1,0].legend()
axes[1,0].grid(True, alpha=0.3)

# 4. Total credit by rating
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
print("Figure saved successfully")

# Save final plan
df.to_csv('/work/final_allocation.csv', index=False)
print("\nFinal plan summary:")
print(df.groupby(['rating','risk_tier']).agg(
    n=('code','count'),
    total_credit=('credit_limit','sum'),
    avg_credit=('credit_limit','mean'),
    avg_rate=('interest_rate','mean')
).round(2))