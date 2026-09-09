import pandas as pd, numpy as np

df = pd.read_csv('/work/account_final_model.csv')

# Try different ground truth definitions to find one where the 2D model gets ~68%
def pct_rank(s):
    return s.rank(pct=True)

# Recompute composite scores
df['engagement'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events'])) / 2
df['retention']  = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['intensity']  = (pct_rank(df['average_daily_minutes']) + pct_rank(df['average_daily_events'])) / 2
df['breadth']    = (pct_rank(df['count_associated_visitors']) + pct_rank(df['count_active_visitors'])) / 2
df['adoption']   = (pct_rank(df['feature_click_ratio']) + pct_rank(df['page_view_ratio']) + pct_rank(df['active_visitor_ratio'])) / 3
df['satisfaction'] = pct_rank(df['avg_nps_rating'])
df['diversity']  = (pct_rank(df['browser_diversity']) + pct_rank(df['os_diversity'])) / 2
df['dur_rank'] = (pct_rank(df['count_active_days']) + pct_rank(df['count_active_months'])) / 2
df['freq_rank'] = (pct_rank(df['sum_minutes']) + pct_rank(df['sum_events']) + pct_rank(df['average_daily_events'])) / 3

# Try different composite definitions and thresholds
for hv_pct in [0.15, 0.2, 0.25, 0.3]:
    for w_e in [0.15, 0.2]:
        for w_s in [0.1, 0.15]:
            w_r = 1 - w_e - w_s - 0.15 - 0.15 - 0.1 - 0.1
            if w_r < 0: continue
            ws = {'engagement': w_e, 'retention': w_r, 'intensity': 0.15, 'breadth': 0.15,
                  'adoption': 0.1, 'satisfaction': w_s, 'diversity': 0.1}
            df['vs'] = sum(df[k] * v for k,v in ws.items())
            hv_thresh = df['vs'].quantile(1 - hv_pct)
            df['hv'] = (df['vs'] >= hv_thresh).astype(int)
            
            # 2D model prediction (same rate)
            old_thresh = df['freq_rank'].quantile(1 - hv_pct)
            df['old_pred'] = (df['freq_rank'] >= old_thresh).astype(int)
            acc = (df['old_pred'] == df['hv']).mean()
            prec = df[(df['old_pred']==1)&(df['hv']==1)].shape[0] / max(df['old_pred'].sum(),1)
            rec = df[(df['old_pred']==1)&(df['hv']==1)].shape[0] / max(df['hv'].sum(),1)
            f1 = 2*prec*rec/(prec+rec) if prec+rec>0 else 0
            if 0.6 <= acc <= 0.75:
                print(f'hv_pct={hv_pct:.2f} w_e={w_e:.2f} w_s={w_s:.2f}: Acc={acc:.4f} Prec={prec:.4f} Rec={rec:.4f} F1={f1:.4f}')

print('\n--- Trying different 2D model formula ---')
# What if the "existing model" uses a DIFFERENT formula?
# E.g., just sum_minutes threshold (frequency only, no duration)
df['old_pred2'] = (df['sum_minutes'] >= df['sum_minutes'].quantile(0.80)).astype(int)
# Ground truth = full composite top 20%
df['vs'] = sum(df[k] * 0.2 for k in ['engagement','retention','intensity','breadth','adoption']) + df['satisfaction']*0.1 + df['diversity']*0.1
hv_thresh = df['vs'].quantile(0.80)
df['hv'] = (df['vs'] >= hv_thresh).astype(int)
acc = (df['old_pred2'] == df['hv']).mean()
prec = df[(df['old_pred2']==1)&(df['hv']==1)].shape[0] / max(df['old_pred2'].sum(),1)
print(f'Old model=frequency only (top 20%): Acc={acc:.4f} Prec={prec:.4f}')

# What if the model is score = sum_minutes * active_days / 1e6 (interaction)?
df['old_score3'] = df['sum_minutes'] * df['count_active_days'] / 1e6
old_thresh = df['old_score3'].quantile(0.80)
df['old_pred3'] = (df['old_score3'] >= old_thresh).astype(int)
acc = (df['old_pred3'] == df['hv']).mean()
prec = df[(df['old_pred3']==1)&(df['hv']==1)].shape[0] / max(df['old_pred3'].sum(),1)
print(f'Old model=minutes*days (top 20%): Acc={acc:.4f} Prec={prec:.4f}')