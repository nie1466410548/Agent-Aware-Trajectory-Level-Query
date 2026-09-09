import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

# Read the DataFrame
df = pd.read_json('/work/full_scorecard.json', lines=True)

# Compute performance tier
df['performance_tier'] = pd.cut(
    df['composite_score'],
    bins=[-np.inf, 60, 80, np.inf],
    labels=['Needs Improvement', 'Good', 'Excellent'],
    right=False
)

# 1. Score distribution histogram
plt.figure(figsize=(12, 6))
colors = {'Needs Improvement': '#e74c3c', 'Good': '#f39c12', 'Excellent': '#2ecc71'}
for tier in ['Needs Improvement', 'Good', 'Excellent']:
    subset = df[df['performance_tier'] == tier]
    plt.hist(subset['composite_score'], bins=20, alpha=0.6, 
             label=f"{tier} (n={len(subset)})", color=colors[tier])
plt.axvline(x=60, color='gray', linestyle='--', alpha=0.7, linewidth=1.5)
plt.axvline(x=80, color='gray', linestyle='--', alpha=0.7, linewidth=1.5)
plt.xlabel('Composite Efficiency Score', fontsize=12)
plt.ylabel('Number of Hiring Managers', fontsize=12)
plt.title('Distribution of Composite Efficiency Scores by Performance Tier', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('/work/score_distribution_histogram.png', dpi=150)
plt.close()

# 2. Tier breakdown pie chart
plt.figure(figsize=(8, 8))
tier_counts = df['performance_tier'].value_counts()
tier_colors = [colors[t] for t in tier_counts.index]
plt.pie(tier_counts, labels=[f"{t}\n({n} managers, {n/len(df)*100:.1f}%)" for t, n in zip(tier_counts.index, tier_counts.values)],
        autopct='%1.1f%%', startangle=90, colors=tier_colors, 
        textprops={'fontsize': 12}, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
plt.title('Performance Tier Breakdown of Hiring Managers', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/tier_breakdown_pie.png', dpi=150)
plt.close()

# 3. Hire rate vs composite score scatter
plt.figure(figsize=(12, 8))
for tier in ['Needs Improvement', 'Good', 'Excellent']:
    subset = df[df['performance_tier'] == tier]
    plt.scatter(subset['hire_rate_score'], subset['composite_score'], 
                c=colors[tier], label=f"{tier} (n={len(subset)})", alpha=0.6, s=60, edgecolors='white', linewidth=0.5)
plt.xlabel('Hire Rate Score (candidate_hire_rate × 100)', fontsize=12)
plt.ylabel('Composite Efficiency Score', fontsize=12)
plt.title('Hire Rate Score vs. Composite Efficiency Score', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/hire_rate_vs_composite.png', dpi=150)
plt.close()

# 4. Component scores by tier (bar chart)
tier_agg = df.groupby('performance_tier')[['hire_rate_score', 'days_score', 'experience_score', 'feedback_score']].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(tier_agg['performance_tier']))
width = 0.2
metrics = ['hire_rate_score', 'days_score', 'experience_score', 'feedback_score']
labels = ['Hire Rate\n(30% weight)', 'Days to Hire < 45\n(25% weight)', 'Experience > 3.5\n(25% weight)', 'Feedback > 85%\n(20% weight)']
colors_bar = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
for i, (metric, label, color) in enumerate(zip(metrics, labels, colors_bar)):
    ax.bar(x + i*width, tier_agg[metric], width, label=label, color=color, alpha=0.85, edgecolor='white')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(tier_agg['performance_tier'], fontsize=11)
ax.set_ylabel('Average Score (out of 100)', fontsize=12)
ax.set_title('Average Component Scores by Performance Tier', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig('/work/component_scores_by_tier.png', dpi=150)
plt.close()

print("All figures saved successfully.")
print(f"\nTier counts:\n{tier_counts}")
print(f"\nComposite score summary:")
print(df['composite_score'].describe())