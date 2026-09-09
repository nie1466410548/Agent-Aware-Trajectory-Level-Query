import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the full results
df = pd.read_json('/results/S12.rows.jsonl', lines=True)

# Compute performance tier
df['performance_tier'] = pd.cut(
    df['composite_score'],
    bins=[-np.inf, 60, 80, np.inf],
    labels=['Needs Improvement', 'Good', 'Excellent'],
    right=False
)

# Score distribution histogram
plt.figure(figsize=(12, 6))
colors = {'Needs Improvement': '#e74c3c', 'Good': '#f39c12', 'Excellent': '#2ecc71'}
for tier in ['Needs Improvement', 'Good', 'Excellent']:
    subset = df[df['performance_tier'] == tier]
    plt.hist(subset['composite_score'], bins=20, alpha=0.6, 
             label=f"{tier} (n={len(subset)})", color=colors[tier])
plt.axvline(x=60, color='gray', linestyle='--', alpha=0.7, label='Good threshold (60)')
plt.axvline(x=80, color='gray', linestyle='--', alpha=0.7, label='Excellent threshold (80)')
plt.xlabel('Composite Efficiency Score', fontsize=12)
plt.ylabel('Number of Hiring Managers', fontsize=12)
plt.title('Distribution of Composite Efficiency Scores by Performance Tier', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('/work/score_distribution_histogram.png', dpi=150)
plt.close()

# Tier breakdown pie chart
plt.figure(figsize=(8, 8))
tier_counts = df['performance_tier'].value_counts()
tier_colors = [colors[t] for t in tier_counts.index]
plt.pie(tier_counts, labels=[f"{t}\n({n} managers)" for t, n in zip(tier_counts.index, tier_counts.values)],
        autopct='%1.1f%%', startangle=90, colors=tier_colors, textprops={'fontsize': 12})
plt.title('Performance Tier Breakdown of Hiring Managers', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/tier_breakdown_pie.png', dpi=150)
plt.close()

# Scatter: hire rate vs composite score, colored by tier
plt.figure(figsize=(12, 8))
for tier in ['Needs Improvement', 'Good', 'Excellent']:
    subset = df[df['performance_tier'] == tier]
    plt.scatter(subset['hire_rate_score'], subset['composite_score'], 
                c=colors[tier], label=f"{tier} (n={len(subset)})", alpha=0.6, s=50)
plt.xlabel('Hire Rate Score (candidate_hire_rate × 100)', fontsize=12)
plt.ylabel('Composite Efficiency Score', fontsize=12)
plt.title('Hire Rate Score vs. Composite Efficiency Score', fontsize=14)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/hire_rate_vs_composite.png', dpi=150)
plt.close()

# Bar chart: component scores by tier
tier_agg = df.groupby('performance_tier')[['hire_rate_score', 'days_score', 'experience_score', 'feedback_score']].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(tier_agg['performance_tier']))
width = 0.2
metrics = ['hire_rate_score', 'days_score', 'experience_score', 'feedback_score']
labels = ['Hire Rate\n(30% weight)', 'Days to Hire < 45\n(25% weight)', 'Experience > 3.5\n(25% weight)', 'Feedback > 85%\n(20% weight)']
colors_bar = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
for i, (metric, label, color) in enumerate(zip(metrics, labels, colors_bar)):
    ax.bar(x + i*width, tier_agg[metric], width, label=label, color=color, alpha=0.8)
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(tier_agg['performance_tier'], fontsize=11)
ax.set_ylabel('Average Score (out of 100)', fontsize=12)
ax.set_title('Average Component Scores by Performance Tier', fontsize=14)
ax.legend(fontsize=10)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/component_scores_by_tier.png', dpi=150)
plt.close()

print("All figures saved successfully.")
print(f"Tier counts:\n{tier_counts}")
print(f"\nComposite score summary:\n{df['composite_score'].describe()}")