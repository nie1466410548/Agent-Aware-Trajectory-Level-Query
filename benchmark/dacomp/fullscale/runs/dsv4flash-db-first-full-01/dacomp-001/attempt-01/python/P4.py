import pandas as pd, numpy as np

df = pd.read_csv('/work/final_allocation.csv')

# Map churn rates by rating and interest rate
# For each company, find the churn rate corresponding to their assigned interest rate
res = db.query('SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"')
churn = db.frame(res)

def get_churn(rate, rating):
    """Find churn rate for given interest rate and rating"""
    if rating == 'D':
        return 1.0  # D-rated all default, so churn = 100% (they'll default anyway)
    col = {'A':'Credit Rating A Customer Churn Rate','B':'Credit Rating B Customer Churn Rate','C':'Credit Rating C Customer Churn Rate'}[rating]
    # Find the closest rate in the table
    rates = churn['Annual Loan Interest Rate'].values
    churns = churn[col].values
    # Exact match
    idx = np.argmin(np.abs(rates - rate))
    return float(churns[idx])

df['churn_rate'] = df.apply(lambda r: get_churn(r['interest_rate'], r['rating']), axis=1)
df['expected_interest_income'] = df['credit_limit'] * df['interest_rate'] * (1 - df['churn_rate'])
df['expected_loss'] = df['credit_limit'] * df['defaulted_flag']  # if defaulted, loss = full credit

# Expected portfolio income
total_income = df['expected_interest_income'].sum()
total_loss = df['expected_loss'].sum()
net_expected = total_income - total_loss

print("=== Portfolio Expected Performance ===")
print(f"Total credit allocated: {df['credit_limit'].sum():,.0f} RMB")
print(f"Expected interest income: {total_income:,.0f} RMB")
print(f"Expected loss (defaults): {total_loss:,.0f} RMB")
print(f"Net expected return: {net_expected:,.0f} RMB")
print(f"Expected return rate: {net_expected/df['credit_limit'].sum()*100:.2f}%")

# By rating
print("\n=== By Rating ===")
for r in ['A','B','C','D']:
    sub = df[df['rating']==r]
    print(f"\nRating {r}:")
    print(f"  Total credit: {sub['credit_limit'].sum():,.0f}")
    print(f"  Expected income: {sub['expected_interest_income'].sum():,.0f}")
    print(f"  Expected loss: {sub['expected_loss'].sum():,.0f}")
    print(f"  Avg interest rate: {sub['interest_rate'].mean()*100:.2f}%")
    print(f"  Avg churn rate: {sub['churn_rate'].mean()*100:.2f}%")

# Expected return by risk tier
print("\n=== By Risk Tier ===")
for t in ['Very Low','Low','Medium','High','Very High']:
    sub = df[df['risk_tier']==t]
    print(f"\n{t}:")
    print(f"  Total credit: {sub['credit_limit'].sum():,.0f}")
    print(f"  Expected income: {sub['expected_interest_income'].sum():,.0f}")
    print(f"  Avg rate: {sub['interest_rate'].mean()*100:.2f}%")