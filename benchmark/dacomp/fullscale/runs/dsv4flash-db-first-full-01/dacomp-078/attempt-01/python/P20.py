import pandas as pd, numpy as np

trend = pd.read_csv('/work/monthly_trends.csv')
trend['month_num'] = trend['month'].str.slice(5,7).astype(int)

# For accounts with >=5 months, evaluate a momentum-based rule:
# Signal = ratio of last observed month to previous month in the training window (first 3 months)
# Outcome = average value in the next 3 months (months 4-6) relative to training average
print('Per-account trajectory evaluation (train=first 3 months, test=next 3):')
for acc, g in trend.groupby('account_id'):
    g = g.sort_values('month_num').reset_index(drop=True)
    if len(g) < 6:
        continue
    train = g.iloc[:3]
    test = g.iloc[3:6]
    m1, m2, m3 = train['month_minutes'].values
    train_avg = train['month_minutes'].mean()
    test_avg = test['month_minutes'].mean()
    mom_ratio = m3 / max(m2, 1e-9)
    growth_ratio = test_avg / max(train_avg, 1e-9)
    # Label outcomes
    if growth_ratio > 1.1: outcome = 'GROW'
    elif growth_ratio < 0.7: outcome = 'DECLINE'
    else: outcome = 'STABLE'
    print(f'{acc}: m1={m1:9.0f} m2={m2:9.0f} m3={m3:9.0f} | momentum m3/m2={mom_ratio:.2f} | '
          f'train_avg={train_avg:8.0f} test_avg={test_avg:8.0f} ratio={growth_ratio:.2f} -> {outcome}')

# Correlation between momentum (m3/m2) and future growth ratio
rows = []
for acc, g in trend.groupby('account_id'):
    g = g.sort_values('month_num').reset_index(drop=True)
    if len(g) < 6: continue
    train = g.iloc[:3]; test = g.iloc[3:6]
    m1, m2, m3 = train['month_minutes'].values
    mom = m3 / max(m2, 1e-9)
    growth = test['month_minutes'].mean() / max(train['month_minutes'].mean(), 1e-9)
    rows.append((mom, growth))
rdf = pd.DataFrame(rows, columns=['momentum', 'future_growth'])
print('\nMomentum vs future growth correlation:', rdf['momentum'].corr(rdf['future_growth']).round(3))
print(rdf.to_string(index=False))