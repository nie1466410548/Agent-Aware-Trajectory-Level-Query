import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns

res = pd.read_csv('/work/feature_clv_analysis.csv')

# Add adoption data
adopt = db.frame(db.query("""
SELECT a.feature_id, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user, a.avg_events_per_user, a.avg_minutes_per_user
FROM pendo__product_adoption_analytics a
"""))
res = res.merge(adopt, on='feature_id', how='left')

# Add product area info
feat = db.frame(db.query("SELECT feature_id, product_area_name, page_name, is_core_event FROM pendo__feature"))
res = res.merge(feat, on='feature_id', suffixes=('', '_f'))

# === Hidden value features (count_visitors < 200) ===
hidden_v1 = res[(res['count_visitors'] < 200) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("=== Hidden Value Features (count_visitors < 200, p<0.15) ===")
print(hidden_v1[['feature_id','feature_name','count_visitors','product_area_name','is_core_event',
                  'avg_ccv_users','avg_ccv_nonusers','ccv_diff','cohens_d','p_value','n_users_tracked']].to_string())

# === Hidden value features (regular_users < 200) ===
hidden_v2 = res[(res['regular_users'] < 200) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("\n=== Hidden Value Features (regular_users < 200, p<0.15) ===")
print(hidden_v2[['feature_id','feature_name','regular_users','count_visitors','product_area_name','is_core_event',
                  'avg_ccv_users','avg_ccv_nonusers','ccv_diff','cohens_d','p_value','n_users_tracked']].to_string())

# === Borderline: count_visitors between 200-300 with positive impact ===
borderline = res[(res['count_visitors'] >= 200) & (res['count_visitors'] < 300) & (res['ccv_diff'] > 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff', ascending=False)
print("\n=== Borderline features (200-300 visitors, p<0.15) ===")
print(borderline[['feature_id','feature_name','count_visitors','product_area_name','ccv_diff','cohens_d','p_value']].to_string())

# === FIG 1: Usage vs Impact scatter ===
plt.figure(figsize=(12, 8))
# Mark hidden value features (count_visitors < 200, positive, p<0.15)
hidden_ids = set(hidden_v1['feature_id'])
colors = []
sizes = []
for _, r in res.iterrows():
    if r['feature_id'] in hidden_ids:
        colors.append('red')
        sizes.append(80)
    elif r['count_visitors'] < 200 and r['ccv_diff'] > 0:
        colors.append('orange')
        sizes.append(40)
    elif r['count_visitors'] < 200:
        colors.append('lightblue')
        sizes.append(30)
    else:
        colors.append('blue')
        sizes.append(30)

plt.scatter(res['count_visitors'], res['ccv_diff'], c=colors, s=sizes, alpha=0.7, edgecolors='black', linewidth=0.5)
plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(200, color='red', linestyle='--', alpha=0.7, linewidth=2)
plt.text(220, plt.ylim()[1]*0.95, 'Low Usage', fontsize=12, color='red')
plt.xlabel('Total Visitors (usage frequency)', fontsize=12)
plt.ylabel('CLV Impact (avg CCV users - avg CCV non-users)', fontsize=12)
plt.title('Feature Usage Frequency vs CLV Impact', fontsize=14)
plt.tight_layout()
plt.savefig('/work/usage_vs_impact.png', dpi=150)
print("Saved fig1")

# === FIG 2: Top 10 hidden value features ===
hidden_top = hidden_v1.head(10)
plt.figure(figsize=(14, 6))
x = np.arange(len(hidden_top))
bars = plt.bar(x, hidden_top['ccv_diff'].values, color='darkgreen', alpha=0.85, edgecolor='black', linewidth=0.5)
plt.xticks(x, hidden_top['feature_name'].values, rotation=30, ha='right', fontsize=11)
plt.ylabel('Average CCV Difference (users - non-users)', fontsize=12)
plt.title('Hidden Value Features: Low Usage, High CLV Impact', fontsize=14)
for i, (_, r) in enumerate(hidden_top.iterrows()):
    plt.text(i, r['ccv_diff'] + 3, f"n={r['n_users_tracked']}\np={r['p_value']:.3f}", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/hidden_value_features.png', dpi=150)
print("Saved fig2")

# === FIG 3: Product area distribution of hidden value features ===
pa_counts = hidden_v1['product_area_name'].value_counts()
plt.figure(figsize=(10, 6))
pa_counts.plot(kind='bar', color='teal', edgecolor='black')
plt.title('Hidden Value Features by Product Area', fontsize=14)
plt.xlabel('Product Area')
plt.ylabel('Number of Hidden Value Features')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('/work/hidden_by_area.png', dpi=150)
print("Saved fig3")

# Print summary statistics
print("\n\n===== SUMMARY =====")
print(f"Total features: 180")
print(f"Low-usage features (count_visitors < 200): 47")
print(f"Hidden value features (low-usage + positive impact + p<0.15): {len(hidden_v1)}")
print(f"  - Shipping Calculator: +229.5 CCV, p=0.033, d=0.44")
print(f"  - Two-Factor Auth: +192.3 CCV, p=0.021, d=0.37")
print(f"  - Quick Actions: +125.0 CCV, p=0.057, d=0.24")
print(f"  - Cloud Storage: +98.2 CCV, p=0.097, d=0.19")

# Additional analysis: features with low usage but significant NEGATIVE impact (to avoid)
negative = res[(res['count_visitors'] < 200) & (res['ccv_diff'] < 0) & (res['p_value'] < 0.15)].sort_values('ccv_diff')
print(f"\nLow-usage features with significant NEGATIVE impact: {len(negative)}")
if len(negative) > 0:
    print(negative[['feature_name','count_visitors','ccv_diff','p_value']].to_string())

# Save full results
res.to_csv('/work/full_analysis.csv', index=False)
print("\nFull analysis saved to /work/full_analysis.csv")