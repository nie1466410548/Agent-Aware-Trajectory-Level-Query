import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_pickle('/work/df_final.pkl')

# FIGURE A: Deviation distribution
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red' if abs(d) > 0.15 else 'steelblue' for d in df['deviation']]
ax.bar(range(len(df)), sorted(df['deviation']), color=['red' if abs(d) > 0.15 else 'steelblue' for d in sorted(df['deviation'])])
ax.axhline(0.15, color='k', linestyle='--', alpha=0.7, label='+0.15 threshold')
ax.axhline(-0.15, color='k', linestyle='--', alpha=0.7)
ax.axhline(0, color='gray', linewidth=0.8)
ax.set_xlabel('Customer (sorted by deviation)', fontsize=12)
ax.set_ylabel('Deviation from Segment Avg Retention', fontsize=12)
ax.set_title('Retention Probability Deviations from Segment Averages (n=149 records)', fontsize=13)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor='red', label='Anomaly (>0.15)'), Patch(facecolor='steelblue', label='Within range')], loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/deviation_distribution.png', dpi=150)
plt.close()

# FIGURE B: Retention by segment with band
fig, ax = plt.subplots(figsize=(10, 6))
seg_order = ['Basic','Growing','Standard','High Value','Premium']
for seg in seg_order:
    sub = df[df['profitability_segment']==seg]
    ax.scatter(np.full(len(sub), seg), sub['retention_probability'], 
               c=['red' if abs(d)>0.15 else 'steelblue' for d in sub['deviation']],
               s=55, alpha=0.7, edgecolors='k', linewidth=0.4)
    avg = sub['avg_retention'].iloc[0]
    ax.plot([seg], [avg], 'D', color='black', markersize=10, label='Segment avg' if seg==seg_order[0] else None)
    ax.errorbar(seg, avg, yerr=0.15, fmt='none', ecolor='orange', linewidth=2, capsize=5, alpha=0.9)
ax.set_ylabel('Retention Probability', fontsize=12)
ax.set_xlabel('Profitability Segment', fontsize=12)
ax.set_title('Retention Probability by Segment (red=anomaly, black diamond=segment avg, orange bar=±0.15 band)', fontsize=12)
ax.legend(loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/retention_by_segment.png', dpi=150)
plt.close()

# FIGURE C: Seasonal concentration vs retention in anomaly-prone segments
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
seg_mask = df['profitability_segment'].isin(['High Value','Standard','Basic'])
for ax, xcol, xlabel, title in [
    (axes[0], 'seasonal_max_share', 'Max Quarterly Share', 'Seasonal Concentration vs Retention'),
    (axes[1], 'seasonal_entropy', 'Seasonal Entropy', 'Seasonal Balance vs Retention')]:
    for seg in ['High Value','Standard','Basic']:
        sub = df[(df['profitability_segment']==seg) & seg_mask]
        ax.scatter(sub[xcol], sub['retention_probability'], alpha=0.6, s=50, label=seg, edgecolors='k', linewidth=0.3)
    # trend line
    z = np.polyfit(df.loc[seg_mask, xcol].fillna(0), df.loc[seg_mask, 'retention_probability'], 1)
    xr = np.linspace(df.loc[seg_mask, xcol].fillna(0).min(), df.loc[seg_mask, xcol].fillna(0).max(), 50)
    ax.plot(xr, np.polyval(z, xr), 'k--', alpha=0.6, label='Trend')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel('Retention Probability', fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/seasonal_retention_link.png', dpi=150)
plt.close()

# FIGURE D: tx_ratio effect in high revenue band
fig, ax = plt.subplots(figsize=(9, 6))
high_rev = df[df['total_revenue'] > 799.5]
ax.scatter(high_rev['tx_ratio'], high_rev['retention_probability'],
           c=['red' if abs(d)>0.15 else 'steelblue' for d in high_rev['deviation']],
           s=80, alpha=0.8, edgecolors='k', linewidth=0.4)
ax.axvline(0.454, color='orange', linestyle='--', linewidth=2, label='tx_ratio=0.454 (tree split)')
ax.set_xlabel('Transaction Consistency Ratio (transaction_count / expected)', fontsize=12)
ax.set_ylabel('Retention Probability', fontsize=12)
ax.set_title('High-Revenue Customers (>$800): Consistency Ratio vs Retention', fontsize=12)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/tx_ratio_effect.png', dpi=150)
plt.close()

# Final summary stats for report
print("=== FINAL SUMMARY STATS ===")
print(f"Total records: {len(df)}, unique customers: {df['customer_id'].nunique()}")
print(f"Anomaly records: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.1f}%), unique anomaly customers: {df[df['is_anomaly']==1]['customer_id'].nunique()}")
print("\nAnomaly composition by segment:")
print(df.groupby('profitability_segment')['is_anomaly'].agg(['count','sum','mean']).round(3))
print("\nPositive vs negative anomaly:")
print(df[df['is_anomaly']==1].groupby('is_above_avg').size())
print("\nQ4-heavy share among anomalies:")
print(df.groupby('is_anomaly')['seasonal_preference'].value_counts(normalize=True).round(3))

print("\nAll figures ready.")