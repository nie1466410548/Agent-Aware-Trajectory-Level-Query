import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load ranked data
with open('/results/S27.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
df = pd.DataFrame(rows)
df.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
              'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']

# Load salary data
with open('/results/S29.rows.jsonl') as f:
    rows2 = [json.loads(l) for l in f]
df_sal = pd.DataFrame(rows2)
df_sal.columns = ['Employee ID','Employee','Base Salary','Company Accommodation']

# Merge
df = df.merge(df_sal, on=['Employee ID','Employee'], how='left')
print("Merged shape:", df.shape)
print(df[['Employee','Base Salary']].head())

# Define top performers (top 10 by composite score)
df['is_top10'] = df['rank'] <= 10
df['is_top20'] = df['rank'] <= 20

# Group metrics
metrics = ['Age','tenure_months','total_eff_hours','total_units','avg_units','avg_pass_rate','Base Salary','days']

print("\n=== Top 10 vs Rest ===")
for m in metrics:
    top = df.loc[df.is_top10, m].dropna()
    rest = df.loc[~df.is_top10, m].dropna()
    t_stat, p_val = stats.ttest_ind(top, rest, equal_var=False)
    print(f"{m:20s}: Top10 mean={top.mean():.2f}, Rest mean={rest.mean():.2f}, t={t_stat:.3f}, p={p_val:.4f}")

print("\n=== Top 20 vs Rest ===")
for m in metrics:
    top = df.loc[df.is_top20, m].dropna()
    rest = df.loc[~df.is_top20, m].dropna()
    t_stat, p_val = stats.ttest_ind(top, rest, equal_var=False)
    print(f"{m:20s}: Top20 mean={top.mean():.2f}, Rest mean={rest.mean():.2f}, t={t_stat:.3f}, p={p_val:.4f}")

# Gender distribution in top vs bottom
print("\n=== Gender in Top 10 ===")
print(df[df.is_top10]['Gender'].value_counts())
print("\n=== Gender in Top 20 ===")
print(df[df.is_top20]['Gender'].value_counts())

# Education distribution
print("\n=== Education in Top 10 ===")
print(df[df.is_top10]['Education Level'].value_counts())
print("\n=== Education in Top 20 ===")
print(df[df.is_top20]['Education Level'].value_counts())

# Team distribution
print("\n=== Team in Top 10 ===")
print(df[df.is_top10]['Team'].value_counts())
print("\n=== Team in Top 20 ===")
print(df[df.is_top20]['Team'].value_counts())

# Correlation analysis
print("\n=== Correlation with composite_score ===")
corr = df[metrics + ['composite_score']].corr()['composite_score'].sort_values(ascending=False)
print(corr)

# Create visualizations
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 1. Top 10 composition by Education
ax = axes[0,0]
top10 = df[df.is_top10]
edu_order = top10['Education Level'].value_counts()
edu_order.plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Top 10 by Education Level')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)

# 2. Top 10 composition by Age
ax = axes[0,1]
df['is_top_flag'] = df['is_top10'].map({True:'Top 10', False:'Rest'})
sns.boxplot(x='is_top_flag', y='Age', data=df, ax=ax, palette='Set2')
ax.set_title('Age Distribution: Top 10 vs Rest')

# 3. Top 10 by Team
ax = axes[0,2]
team_counts = top10['Team'].value_counts()
team_counts.plot(kind='bar', ax=ax, color='coral')
ax.set_title('Top 10 by Team')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)

# 4. Gender composition
ax = axes[1,0]
gender_counts = df.groupby(['is_top10','Gender']).size().unstack(fill_value=0)
gender_counts.T.plot(kind='bar', ax=ax, color=['steelblue','lightcoral'])
ax.set_title('Gender Distribution: Top 10 vs Rest')
ax.set_ylabel('Count')
ax.legend(['Rest','Top 10'])
ax.tick_params(axis='x', rotation=0)

# 5. Tenure comparison
ax = axes[1,1]
sns.boxplot(x='is_top_flag', y='tenure_months', data=df, ax=ax, palette='Set2')
ax.set_title('Tenure (months): Top 10 vs Rest')

# 6. Salary comparison
ax = axes[1,2]
sns.boxplot(x='is_top_flag', y='Base Salary', data=df, ax=ax, palette='Set2')
ax.set_title('Base Salary: Top 10 vs Rest')

plt.tight_layout()
plt.savefig('/work/employee_profile_analysis.png', dpi=150)
print("Saved figure 1")

# Second figure: component scores comparison
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))

# Normalized component scores
for comp, name, ax in zip(['total_eff_hours','total_units','avg_pass_rate'],
                           ['Effective Working Hours (total)', 'Units Produced (total)', 'Pass Rate (avg)'],
                           axes2):
    # Min-max normalize
    minv = df[comp].min()
    maxv = df[comp].max()
    df[f'norm_{comp}'] = (df[comp] - minv) / (maxv - minv)
    sns.boxplot(x='is_top_flag', y=f'norm_{comp}', data=df, ax=ax, palette='Set2')
    ax.set_title(f'Normalized {name}')
    ax.set_ylabel('Normalized Score (0-1)')

plt.tight_layout()
plt.savefig('/work/component_scores_comparison.png', dpi=150)
print("Saved figure 2")

# Third figure: scatter plots of key metrics
fig3, axes3 = plt.subplots(1, 3, figsize=(15, 5))

ax = axes3[0]
colors = df['is_top10'].map({True:'red', False:'blue'})
ax.scatter(df['avg_units'], df['avg_pass_rate'], c=colors, alpha=0.6, s=50)
ax.set_xlabel('Avg Units Per Day')
ax.set_ylabel('Avg Pass Rate (%)')
ax.set_title('Units vs Pass Rate\n(Red=Top 10)')
# Add a legend
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Top 10', markerfacecolor='red', markersize=8),
                   Line2D([0], [0], marker='o', color='w', label='Rest', markerfacecolor='blue', markersize=8)]
ax.legend(handles=legend_elements)

ax = axes3[1]
ax.scatter(df['total_eff_hours'], df['total_units'], c=colors, alpha=0.6, s=50)
ax.set_xlabel('Total Effective Working Hours')
ax.set_ylabel('Total Units Produced')
ax.set_title('Eff Hours vs Units\n(Red=Top 10)')
ax.legend(handles=legend_elements)

ax = axes3[2]
ax.scatter(df['Base Salary'], df['composite_score'], c=colors, alpha=0.6, s=50)
ax.set_xlabel('Base Salary')
ax.set_ylabel('Composite Score')
ax.set_title('Salary vs Composite Score\n(Red=Top 10)')
ax.legend(handles=legend_elements)

plt.tight_layout()
plt.savefig('/work/scatter_analysis.png', dpi=150)
print("Saved figure 3")

# Check general stats by gender
print("\n=== Stats by Gender ===")
for col in ['total_eff_hours','total_units','avg_pass_rate','composite_score','Age','tenure_months','Base Salary','avg_units']:
    print(f"\n{col}:")
    print(df.groupby('Gender')[col].describe().round(2))

# Check if all top 10 are female, what's the first male rank
first_male = df[df.Gender=='Male'].sort_values('rank').iloc[0]
print(f"\nFirst male rank: {first_male['rank']}, Employee: {first_male['Employee']}, Score: {first_male['composite_score']:.4f}")

# Check education vs performance
print("\n=== Education Level vs Composite Score ===")
print(df.groupby('Education Level')['composite_score'].describe().round(4))

# Check accommodation
print("\n=== Company Accommodation ===")
print(df['Company Accommodation'].value_counts())
print("\nAccommodation vs Top10:")
print(pd.crosstab(df['is_top10'], df['Company Accommodation']))