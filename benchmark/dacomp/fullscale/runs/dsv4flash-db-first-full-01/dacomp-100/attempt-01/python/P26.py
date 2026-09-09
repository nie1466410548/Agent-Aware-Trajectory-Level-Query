import pandas as pd
import numpy as np
from datetime import timedelta

def compute_auc(y_true, y_score):
    pos = y_score[y_true == 1]
    neg = y_score[y_true == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    n_pos = len(pos); n_neg = len(neg)
    combined = np.concatenate([pos, neg])
    labels = np.concatenate([np.ones(n_pos), np.zeros(n_neg)])
    order = np.argsort(combined)
    sorted_labels = labels[order]
    ranks = np.arange(1, len(combined) + 1)
    pos_ranks = ranks[sorted_labels == 1]
    U = pos_ranks.sum() - n_pos * (n_pos + 1) / 2
    AUC = U / (n_pos * n_neg)
    return AUC

# Company data - get outcome per name from historical cohort
comp = db.frame(db.query("SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced"))

def parse_tags(tags_str):
    d = {}
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            d[k.strip()] = v.strip()
    return d

parsed = pd.DataFrame(comp['all_company_tags'].apply(parse_tags).tolist())
parsed['company_id'] = comp['company_id']
parsed['company_name'] = comp['company_name']
parsed['renewal_date'] = pd.to_datetime(parsed['renewal_date'])

past = parsed[parsed['renewal_window'] == 'within_30_days_past'].copy()
past['is_renewed'] = past['expansion_signal'].map({'Upsell Ready': 1, 'Risk Mitigation': 0})
past = past.dropna(subset=['is_renewed'])
name_outcome = past.groupby('company_name')['is_renewed'].first()

print(f"Names: {len(name_outcome)} total, {name_outcome.sum()} renewed, {(1-name_outcome).sum()} churned")

# Conversation data (full 2023 = pre-renewal year)
conv_enh = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced"))
conv_enh['date'] = pd.to_datetime(conv_enh['conversation_created_at'])

def parse_sentiment(tags_str):
    for pair in tags_str.split('|'):
        if '=' in pair:
            k, v = pair.split('=', 1)
            if k.strip() == 'sentiment':
                return v.strip()
    return None

conv_enh['sentiment'] = conv_enh['all_conversation_tags'].apply(parse_sentiment)
neg_sentiments = ['escalation', 'risk_mitigation', 'cautious_watch', 'executive_focus']
conv_enh['is_negative'] = conv_enh['sentiment'].isin(neg_sentiments)

conv_metrics = db.frame(db.query("SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes FROM intercom__conversation_metrics"))
conv_metrics['resolution_time_min'] = conv_metrics['time_to_last_close_minutes'].fillna(conv_metrics['time_to_first_close_minutes'])
conv_metrics['is_reopened'] = conv_metrics['count_reopens'] > 0

conv_all = conv_enh.merge(conv_metrics, on='conversation_id', how='left')

# Name-level features over full 2023 (pre-renewal period) and 30-day pre-renewal window
name_features = []
for name in name_outcome.index:
    ren_date = past[past['company_name'] == name]['renewal_date'].iloc[0]
    
    # All 2023 conversations
    convs_2023 = conv_all[(conv_all['all_contact_company_names'] == name) & (conv_all['date'].dt.year == 2023)]
    
    # 30-day window before renewal
    win_start = ren_date - timedelta(days=30)
    convs_30d = conv_all[(conv_all['all_contact_company_names'] == name) & 
                         (conv_all['date'] >= win_start) & (conv_all['date'] < ren_date)]
    
    # Last 30 days of 2023 (proxy for 'last 30 days' if renewal window empty)
    convs_dec = conv_all[(conv_all['all_contact_company_names'] == name) & 
                         (conv_all['date'] >= '2023-12-01') & (conv_all['date'] <= '2023-12-31')]
    
    name_features.append({
        'name': name,
        'is_renewed': name_outcome[name],
        'n_conv_2023': len(convs_2023),
        'neg_prop_2023': convs_2023['is_negative'].mean() if len(convs_2023) > 0 else np.nan,
        'res_time_2023': convs_2023['resolution_time_min'].mean() if len(convs_2023) > 0 else np.nan,
        'reopen_prop_2023': convs_2023['is_reopened'].mean() if len(convs_2023) > 0 else np.nan,
        'n_conv_30d': len(convs_30d),
        'neg_prop_30d': convs_30d['is_negative'].mean() if len(convs_30d) > 0 else np.nan,
        'res_time_30d': convs_30d['resolution_time_min'].mean() if len(convs_30d) > 0 else np.nan,
        'reopen_prop_30d': convs_30d['is_reopened'].mean() if len(convs_30d) > 0 else np.nan,
        'n_conv_dec': len(convs_dec),
        'neg_prop_dec': convs_dec['is_negative'].mean() if len(convs_dec) > 0 else np.nan,
        'res_time_dec': convs_dec['resolution_time_min'].mean() if len(convs_dec) > 0 else np.nan,
        'reopen_prop_dec': convs_dec['is_reopened'].mean() if len(convs_dec) > 0 else np.nan,
    })

nf = pd.DataFrame(name_features)
print(f"\nName-level feature table: {len(nf)} rows")
print("\n=== Name-level Comparison: Renewed vs Churned ===")
feats = ['n_conv_2023', 'neg_prop_2023', 'res_time_2023', 'reopen_prop_2023',
         'n_conv_30d', 'neg_prop_30d', 'res_time_30d', 'reopen_prop_30d',
         'n_conv_dec', 'neg_prop_dec', 'res_time_dec', 'reopen_prop_dec']

for feat in feats:
    r = nf[nf['is_renewed'] == 1][feat].dropna()
    c = nf[nf['is_renewed'] == 0][feat].dropna()
    if len(r) > 2 and len(c) > 2:
        auc = compute_auc(nf.dropna(subset=[feat])['is_renewed'].values.astype(int), 
                          nf.dropna(subset=[feat])[feat].values.astype(float))
        print(f"{feat:22s}: Renewed n={len(r)} mean={r.mean():.3f} med={r.median():.3f} | Churned n={len(c)} mean={c.mean():.3f} med={c.median():.3f} | AUC={auc:.3f}")

nf.to_csv('/work/name_level_features.csv', index=False)