import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

col = "Parents' education level"

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# ============ Figure 1: Boxplot of Exam Scores by Parents' Education Level ============
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1a: Parents' Education
order = ['High School', 'Bachelor', 'Master']
data_plot = df[df[col].isin(order)].copy()
sns.boxplot(x=col, y='Exam score', data=data_plot, order=order, ax=axes[0,0], palette='Set2')
axes[0,0].set_title('Exam Score by Parents\' Education Level', fontsize=12)
axes[0,0].set_xlabel('Parents\' Education Level')
axes[0,0].set_ylabel('Exam Score')

# 1b: Study Time (categorized)
df['study_cat'] = pd.cut(df['Daily study time'], bins=[0,2,4,6,24], labels=['<2h','2-4h','4-6h','6h+'])
sns.boxplot(x='study_cat', y='Exam score', data=df, ax=axes[0,1], palette='Set2',
            order=['<2h','2-4h','4-6h','6h+'])
axes[0,1].set_title('Exam Score by Daily Study Time', fontsize=12)
axes[0,1].set_xlabel('Daily Study Time')

# 1c: Mental Health
df['mh_cat'] = pd.cut(df['Mental health score'], bins=[-1,3,6,10], labels=['Low (0-3)','Medium (4-6)','High (7-10)'])
sns.boxplot(x='mh_cat', y='Exam score', data=df, ax=axes[0,2], palette='Set2',
            order=['Low (0-3)','Medium (4-6)','High (7-10)'])
axes[0,2].set_title('Exam Score by Mental Health Score', fontsize=12)
axes[0,2].set_xlabel('Mental Health Score')

# 1d: Social Media Usage (categorized)
df['social_cat'] = pd.cut(df['Social media usage time'], bins=[0,1,3,5,10], labels=['<1h','1-3h','3-5h','5h+'])
sns.boxplot(x='social_cat', y='Exam score', data=df, ax=axes[1,0], palette='Set2',
            order=['<1h','1-3h','3-5h','5h+'])
axes[1,0].set_title('Exam Score by Social Media Usage', fontsize=12)
axes[1,0].set_xlabel('Social Media Usage Time')

# 1e: Sleep Duration (categorized)
df['sleep_cat'] = pd.cut(df['Sleep duration'], bins=[0,5,7,9,12], labels=['<5h','5-7h','7-9h','9h+'])
sns.boxplot(x='sleep_cat', y='Exam score', data=df, ax=axes[1,1], palette='Set2',
            order=['<5h','5-7h','7-9h','9h+'])
axes[1,1].set_title('Exam Score by Sleep Duration', fontsize=12)
axes[1,1].set_xlabel('Sleep Duration')

# 1f: Exercise Frequency (categorized)
df['ex_cat'] = pd.cut(df['Exercise frequency'], bins=[-1,1,3,5,7], labels=['0-1','2-3','4-5','6-7'])
sns.boxplot(x='ex_cat', y='Exam score', data=df, ax=axes[1,2], palette='Set2',
            order=['0-1','2-3','4-5','6-7'])
axes[1,2].set_title('Exam Score by Exercise Frequency (days/week)', fontsize=12)
axes[1,2].set_xlabel('Exercise Frequency')

plt.tight_layout()
plt.savefig('/work/figure1_factors_boxplots.png', dpi=150)
plt.close()
print("Figure 1 saved")

# ============ Figure 2: Scatter plot of strongest predictors ============
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 2a: Study time
sns.scatterplot(x='Daily study time', y='Exam score', data=df, alpha=0.5, ax=axes[0])
# Add regression line
sns.regplot(x='Daily study time', y='Exam score', data=df, scatter=False, ax=axes[0], color='red')
axes[0].set_title(f'Daily Study Time vs Exam Score (r=0.825)', fontsize=12)

# 2b: Mental health
sns.scatterplot(x='Mental health score', y='Exam score', data=df, alpha=0.5, ax=axes[1])
sns.regplot(x='Mental health score', y='Exam score', data=df, scatter=False, ax=axes[1], color='red')
axes[1].set_title(f'Mental Health Score vs Exam Score (r=0.326)', fontsize=12)

# 2c: Social media usage
sns.scatterplot(x='Social media usage time', y='Exam score', data=df, alpha=0.5, ax=axes[2])
sns.regplot(x='Social media usage time', y='Exam score', data=df, scatter=False, ax=axes[2], color='red')
axes[2].set_title(f'Social Media Usage vs Exam Score (r=-0.214)', fontsize=12)

plt.tight_layout()
plt.savefig('/work/figure2_scatter_correlations.png', dpi=150)
plt.close()
print("Figure 2 saved")

# ============ Figure 3: Standardized coefficients bar chart ============
fig, ax = plt.subplots(figsize=(10, 6))

features = ['Daily study time', 'Mental health score', 'Exercise frequency', 
            'Social media usage time', 'Sleep duration', 'Diet quality (Good)',
            'Parents education (Master)', 'Internet quality (Good)', 'Age',
            'Parents education (Bachelor)', 'Diet quality (Poor)', 'Internet quality (Poor)',
            'Part-time job (Yes)', 'Gender (Other)', 'Extracurricular (Yes)',
            'Attendance rate', 'Gender (Male)']
coefs = [0.8254, 0.3113, 0.1749, -0.1328, 0.1318, -0.0282, -0.0204, -0.0193, 
         -0.0110, -0.0071, -0.0050, 0.0050, 0.0041, -0.0030, -0.0025, -0.0019, -0.0001]
colors = ['#2ecc71' if c > 0 else '#e74c3c' for c in coefs]

bars = ax.barh(range(len(features)), coefs, color=colors)
ax.set_yticks(range(len(features)))
ax.set_yticklabels(features)
ax.set_xlabel('Standardized Coefficient (Beta Weight)')
ax.set_title('Relative Importance of Factors on Exam Score\n(Multiple Regression, R²=0.855)')
ax.axvline(0, color='black', linewidth=0.5)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/work/figure3_standardized_coefficients.png', dpi=150)
plt.close()
print("Figure 3 saved")