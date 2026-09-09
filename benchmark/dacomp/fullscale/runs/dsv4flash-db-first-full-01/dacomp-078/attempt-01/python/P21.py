import pandas as pd, numpy as np

df = pd.read_csv('/work/account_final_model.csv')

# Rebuild ground truth (value_score composite) and retrain multi-dim model on full data for coefficients
def pct_rank(s):
    return s.rank(pct=True)

# Verify value_score was saved correctly
print('value_score stats:', df['value_score'].describe().round(3).to_dict())
print('high_value rate:', df['high_value'].mean().round(3))

# Feature importance: retrain multi-dim logistic regression on standardized full data
multi_feats = ['count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    'avg_nps_rating', 'browser_diversity', 'os_diversity',
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events']

def standardize(X):
    mu = X.mean(axis=0); sd = X.std(axis=0) + 1e-8
    return (X - mu) / sd, mu, sd

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))

def logreg_fit(X, y, lr=0.3, iters=5000, l2=0.01):
    n, d = X.shape
    w = np.zeros(d); b = 0.0
    for i in range(iters):
        z = X @ w + b
        p = sigmoid(z)
        grad_w = (X.T @ (p - y)) / n + l2 * w
        grad_b = (p - y).mean()
        w -= lr * grad_w; b -= lr * grad_b
    return w, b

X = df[multi_feats].values.astype(float)
y = df['high_value'].values
Xs, mu, sd = standardize(X)
w, b = logreg_fit(Xs, y)
coef = pd.DataFrame({'feature': multi_feats, 'coef': w, 'abs_coef': np.abs(w)}).sort_values('abs_coef', ascending=False)
print('\nFeature importance (logistic regression coefficients):')
print(coef.to_string(index=False))
coef.to_csv('/work/feature_importance.csv', index=False)

# Profile comparison: high-value vs non-high-value accounts
print('\nProfile comparison (mean by group):')
profile_cols = ['count_associated_visitors', 'count_active_days', 'count_active_months',
                'sum_minutes', 'sum_events', 'average_daily_minutes', 'average_daily_events',
                'avg_nps_rating', 'active_visitor_ratio', 'feature_click_ratio', 'browser_diversity']
prof = df.groupby('high_value')[profile_cols].mean().T
print(prof.round(2).to_string())
prof.round(2).to_csv('/work/profile_comparison.csv')
print('\nsaved')