import pandas as pd, numpy as np

df = pd.read_csv('/work/account_scored.csv')

# Let's try different thresholds for the 2D model vs ground truth
# The task says 68% accuracy with 2D model. Let's see what definition gives ~68%
for hv_pct in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
    hv_thresh = df['value_score'].quantile(1 - hv_pct)
    df['hv'] = (df['value_score'] >= hv_thresh).astype(int)
    
    # Old model: simple average of duration and frequency percentile ranks
    # Use the same proportion (top hv_pct) for old model prediction
    old_thresh = df['old_score'].quantile(1 - hv_pct)
    df['old_pred'] = (df['old_score'] >= old_thresh).astype(int)
    
    acc = (df['old_pred'] == df['hv']).mean()
    prec = df[(df['old_pred']==1)&(df['hv']==1)].shape[0] / max(df['old_pred'].sum(), 1)
    rec = df[(df['old_pred']==1)&(df['hv']==1)].shape[0] / max(df['hv'].sum(), 1)
    f1 = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0
    print(f'High-value top {hv_pct*100:.0f}%: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}')

print('\n--- Trying different ground truth definitions ---')
# Try: high-value = top 20% by sum_minutes only (purely value-based)
df['hv_eng'] = (df['sum_minutes'] >= df['sum_minutes'].quantile(0.80)).astype(int)
for hv_pct in [0.2]:
    old_thresh = df['old_score'].quantile(1 - hv_pct)
    df['old_pred'] = (df['old_score'] >= old_thresh).astype(int)
    acc = (df['old_pred'] == df['hv_eng']).mean()
    prec = df[(df['old_pred']==1)&(df['hv_eng']==1)].shape[0] / max(df['old_pred'].sum(), 1)
    rec = df[(df['old_pred']==1)&(df['hv_eng']==1)].shape[0] / max(df['hv_eng'].sum(), 1)
    print(f'Ground truth=top20% sum_minutes: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}')

# Try: high-value = top 20% by a score that excludes duration/frequency (NPS + adoption + breadth + diversity)
df['val2'] = (dim['satisfaction']*0.3 + dim['adoption']*0.3 + dim['breadth']*0.2 + dim['diversity']*0.2)
hv_thresh2 = df['val2'].quantile(0.80)
df['hv2'] = (df['val2'] >= hv_thresh2).astype(int)
# Old model predicts same proportion
old_thresh = df['old_score'].quantile(0.80)
df['old_pred'] = (df['old_score'] >= old_thresh).astype(int)
acc = (df['old_pred'] == df['hv2']).mean()
print(f'Ground truth=non-engagement composite: Acc={acc:.4f}')

# Try: 68% when using the raw score (not percentile-matched)? 
# Maybe the "existing model" uses a fixed threshold like old_score > 0.5
for t in [0.3, 0.4, 0.5, 0.6, 0.7]:
    df['old_pred'] = (df['old_score'] >= t).astype(int)
    # Ground truth = value_score > 0.5 (median)
    df['hv'] = (df['value_score'] >= 0.5).astype(int)
    acc = (df['old_pred'] == df['hv']).mean()
    print(f'Fixed threshold t={t}: old_pred_rate={df["old_pred"].mean():.3f}, hv_rate={df["hv"].mean():.3f}, Acc={acc:.4f}')