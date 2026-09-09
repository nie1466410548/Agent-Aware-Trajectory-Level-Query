
import pandas as pd
import numpy as np
from scipy import stats

# Load per-visitor CLV data
clv = db.frame(db.query("""
SELECT c.visitor_id, c.comprehensive_customer_value, c.user_value_score
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id
"""))
clv['comprehensive_customer_value'] = clv['comprehensive_customer_value'].astype(float)

# Load visitor-feature usage
vf = db.frame(db.query("""
SELECT visitor_id, feature_id, sum_clicks, count_active_days, count_click_events, sum_minutes
FROM pendo__visitor_feature
"""))

# Load feature master
feat = db.frame(db.query("""
SELECT feature_id, feature_name, count_visitors, count_accounts, product_area_name, is_core_event, sum_clicks
FROM pendo__feature
"""))
feat['count_visitors'] = feat['count_visitors'].astype(float)

# Build user set per feature
ccv_by_visitor = clv.set_index('visitor_id')['comprehensive_customer_value'].to_dict()
all_visitors = set(clv['visitor_id'])

results = []
for fid, g in vf.groupby('feature_id'):
    users = set(g['visitor_id'])
    nonusers = all_visitors - users
    u_ccv = np.array([ccv_by_visitor[v] for v in users])
    n_ccv = np.array([ccv_by_visitor[v] for v in nonusers])
    tstat, pval = stats.ttest_ind(u_ccv, n_ccv, equal_var=False)
    diff = u_ccv.mean() - n_ccv.mean()
    results.append({
        'feature_id': fid,
        'n_users_tracked': len(users),
        'n_nonusers': len(nonusers),
        'avg_ccv_users': u_ccv.mean(),
        'avg_ccv_nonusers': n_ccv.mean(),
        'ccv_diff': diff,
        't_stat': tstat,
        'p_value': pval
    })

res = pd.DataFrame(results)
res = res.merge(feat, on='feature_id')
res.to_csv('/work/feature_clv_analysis.csv', index=False)
print("Saved. Shape:", res.shape)
print(res.sort_values('ccv_diff', ascending=False).head(15)[['feature_id','feature_name','count_visitors','product_area_name','avg_ccv_users','avg_ccv_nonusers','ccv_diff','p_value','n_users_tracked']].to_string())
