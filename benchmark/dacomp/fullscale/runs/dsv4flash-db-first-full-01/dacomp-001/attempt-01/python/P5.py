import pandas as pd, numpy as np

df = pd.read_csv('/work/final_allocation.csv')

# Revised plan: deny credit to D-rated (all defaulted)
df_rev = df[df['rating'] != 'D'].copy()

# Re-allocate 100M among A/B/C using same weights
total_credit = 100_000_000
w = df_rev['credit_weight'].sum()
df_rev['credit_limit'] = total_credit * df_rev['credit_weight'] / w

# Recompute rates: same base rates + tier adjustments
df_rev['interest_rate'] = df_rev['base_rate'] + df_rev['rate_adjust']
df_rev['interest_rate'] = df_rev['interest_rate'].clip(upper=0.15)

res = db.query('SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"')
churn = db.frame(res)

def get_churn(rate, rating):
    col = {'A':'Credit Rating A Customer Churn Rate','B':'Credit Rating B Customer Churn Rate','C':'Credit Rating C Customer Churn Rate'}[rating]
    rates = churn['Annual Loan Interest Rate'].values
    churns = churn[col].values
    idx = np.argmin(np.abs(rates - rate))
    return float(churns[idx])

df_rev['churn_rate'] = df_rev.apply(lambda r: get_churn(r['interest_rate'], r['rating']), axis=1)
df_rev['expected_income'] = df_rev['credit_limit'] * df_rev['interest_rate'] * (1 - df_rev['churn_rate'])
df_rev['expected_loss'] = df_rev['credit_limit'] * df_rev['defaulted_flag']

total_income = df_rev['expected_income'].sum()
total_loss = df_rev['expected_loss'].sum()
net = total_income - total_loss

print("=== REVISED PORTFOLIO (A/B/C only) ===")
print(f"Total credit: {df_rev['credit_limit'].sum():,.0f}")
print(f"Expected income: {total_income:,.0f}")
print(f"Expected loss: {total_loss:,.0f}")
print(f"Net expected return: {net:,.0f}")
print(f"Net return rate: {net/total_credit*100:.2f}%")

print("\n=== By Rating ===")
for r in ['A','B','C']:
    sub = df_rev[df_rev['rating']==r]
    print(f"Rating {r}: credit={sub['credit_limit'].sum():,.0f}, income={sub['expected_income'].sum():,.0f}, "
          f"loss={sub['expected_loss'].sum():,.0f}, avg_rate={sub['interest_rate'].mean()*100:.2f}%, n={len(sub)}")

print("\n=== By Risk Tier ===")
tier_sum = df_rev.groupby('risk_tier').agg(
    credit=('credit_limit','sum'), income=('expected_income','sum'),
    avg_rate=('interest_rate','mean'), n=('code','count')).round(0)
print(tier_sum)

df_rev.to_csv('/work/revised_plan.csv', index=False)

# Also compute: credit limit as % of revenue (leverage ratio check)
df_rev['limit_to_revenue'] = df_rev['credit_limit'] / df_rev['total_revenue'].replace(0, np.nan)
print("\nCredit limit / annual revenue ratio by rating:")
print(df_rev.groupby('rating')['limit_to_revenue'].agg(['mean','median','max']).round(4))