import pandas as pd, numpy as np

trend = pd.read_csv('/work/monthly_trends.csv')
trend['month_num'] = trend['month'].str.slice(5,7).astype(int)

# For accounts with >= 6 months of data, test a simple trend model:
# Fit linear trend on first 3 months -> predict months 4-6 (and beyond)
accounts_6plus = trend.groupby('account_id').filter(lambda g: len(g) >= 6)
print('Accounts with >=6 months:', accounts_6plus['account_id'].nunique())

def linfit(x, y):
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    return coef  # [slope, intercept]

rows_out = []
for acc, g in trend.groupby('account_id'):
    if len(g) < 5:
        continue
    g = g.sort_values('month_num').reset_index(drop=True)
    train = g.iloc[:3]   # first 3 months
    test = g.iloc[3:]    # next 3-6 months
    x_tr = train['month_num'].values
    y_tr = np.log1p(train['month_minutes'].values)
    slope, intercept = linfit(x_tr, y_tr)
    # Predict all future months
    x_test = test['month_num'].values
    pred_log = slope * x_test + intercept
    pred_val = np.expm1(pred_log)
    actual_val = test['month_minutes'].values
    # Trend direction: compare average of first 3 months vs last 3 available
    train_avg = g['month_minutes'].iloc[:3].mean()
    test_avg = g['month_minutes'].iloc[3:6].mean()
    actual_direction = 'declining' if test_avg < train_avg * 0.7 else ('growing' if test_avg > train_avg * 1.3 else 'stable')
    pred_direction = 'declining' if slope < -0.1 else ('growing' if slope > 0.1 else 'stable')
    corr = np.corrcoef(np.log1p(actual_val), pred_val)[0,1] if len(actual_val)>2 else np.nan
    mape = np.mean(np.abs(np.log1p(actual_val) - pred_log))  # log error
    rows_out.append(dict(account_id=acc, slope=slope, intercept=intercept,
                         train_avg=train_avg, future_avg=test_avg,
                         actual_direction=actual_direction, pred_direction=pred_direction,
                         log_mae=mape))
    
res = pd.DataFrame(rows_out)
print(res.to_string(index=False))
res.to_csv('/work/trend_model_results.csv', index=False)
print('\nsaved')