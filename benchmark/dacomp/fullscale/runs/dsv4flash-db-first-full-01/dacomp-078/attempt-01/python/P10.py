import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/work/account_with_visitor.csv')
print('Shape:', df.shape)
print('Retained rate:', df['retained'].mean().round(4))

# Define feature sets
baseline_features = [
    'count_active_days', 'count_active_months',  # duration
    'sum_minutes', 'sum_events', 'average_daily_minutes', 'average_daily_events'  # frequency
]

multi_dim_features = [
    # Account size & adoption
    'count_associated_visitors', 'count_active_visitors', 'count_page_viewing_visitors',
    'count_feature_clicking_visitors', 'active_visitor_ratio', 'page_view_ratio', 'feature_click_ratio',
    # Duration & frequency (same as baseline)
    'count_active_days', 'count_active_months', 'sum_minutes', 'sum_events',
    'average_daily_minutes', 'average_daily_events',
    'minutes_per_active_day', 'events_per_active_day',
    # Satisfaction
    'avg_nps_rating',
    # Visitor diversity
    'browser_diversity', 'os_diversity',
    # Visitor-level engagement
    'avg_visitor_minutes', 'avg_visitor_events', 'avg_visitor_daily_min',
    'avg_visitor_daily_events', 'avg_visitor_active_days', 'avg_visitor_active_months',
    'total_visitor_minutes', 'total_visitor_events'
]

y = df['retained'].values

# Baseline 2D model (duration + frequency)
baseline_model = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
baseline_scores = cross_val_score(baseline_model, df[baseline_features].values, y, cv=cv, scoring='accuracy')
print(f'Baseline (2D) model accuracy: {baseline_scores.mean():.4f} +/- {baseline_scores.std():.4f}')

# Multi-dimensional model
multi_model = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])
multi_scores = cross_val_score(multi_model, df[multi_dim_features].values, y, cv=cv, scoring='accuracy')
print(f'Multi-dimensional model accuracy: {multi_scores.mean():.4f} +/- {multi_scores.std():.4f}')

# Also compute AUC for both
baseline_auc = cross_val_score(baseline_model, df[baseline_features].values, y, cv=cv, scoring='roc_auc')
multi_auc = cross_val_score(multi_model, df[multi_dim_features].values, y, cv=cv, scoring='roc_auc')
print(f'Baseline AUC: {baseline_auc.mean():.4f}')
print(f'Multi-dim AUC: {multi_auc.mean():.4f}')

# Detailed per-fold CV
for fold, (train_idx, test_idx) in enumerate(cv.split(df[multi_dim_features].values, y)):
    X_train, X_test = df[multi_dim_features].values[train_idx], df[multi_dim_features].values[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    clf = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    clf.fit(X_train_s, y_train)
    y_pred = clf.predict(X_test_s)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, clf.predict_proba(X_test_s)[:, 1])
    print(f'Fold {fold+1}: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}, AUC={auc:.4f}')

# Feature importance (coefficients from the multi-dim model on full data)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[multi_dim_features].values)
clf = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
clf.fit(X_scaled, y)
coef_df = pd.DataFrame({'feature': multi_dim_features, 'coef': clf.coef_[0]})
coef_df['abs_coef'] = coef_df['coef'].abs()
coef_df = coef_df.sort_values('abs_coef', ascending=False)
print('\nTop 15 feature coefficients:')
print(coef_df.head(15).to_string(index=False))