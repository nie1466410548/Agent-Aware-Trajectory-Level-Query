import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)
df = df.drop_duplicates(subset='EmpID', keep='first')

# Create a heatmap of attrition rates by department and key factors
# Prepare data for the heatmap
factors = ['OverTime', 'MaritalStatus', 'JobLevel', 'StockOptionLevel', 'JobSatisfaction', 
           'WorkLifeBalance', 'BusinessTravel', 'EnvironmentSatisfaction', 'JobInvolvement',
           'RelationshipSatisfaction', 'Gender', 'EducationField']

# Compute overall attrition rate by department for reference
overall = df.groupby('Department')['is_attrition'].mean()*100

# For each factor, compute the attrition rate by department and factor level
heatmap_data = []
factor_categories = []
for factor in factors:
    if factor in ['JobLevel', 'StockOptionLevel', 'JobSatisfaction', 'WorkLifeBalance', 
                  'EnvironmentSatisfaction', 'JobInvolvement', 'RelationshipSatisfaction']:
        # Ordinal - sort by value
        cats = sorted(df[factor].unique())
    else:
        cats = df[factor].unique()
        cats = sorted([c for c in cats if str(c) != 'nan'])
    
    for cat in cats:
        sub = df[df[factor]==cat]
        if len(sub) < 10:
            continue
        rates = sub.groupby('Department')['is_attrition'].mean()*100
        row = {'Factor': f'{factor}={cat}'}
        for dept in ['Human Resources', 'Research & Development', 'Sales']:
            row[dept] = rates.get(dept, np.nan)
        # Also add the difference from overall
        for dept in ['Human Resources', 'Research & Development', 'Sales']:
            row[f'{dept}_diff'] = row[dept] - overall[dept]
        heatmap_data.append(row)

heatmap_df = pd.DataFrame(heatmap_data)

# Create a heatmap showing R&D vs Sales attrition rates by factor
# Filter to factors with enough data
fig, ax = plt.subplots(figsize=(14, max(6, len(heatmap_df)*0.25)))

plot_df = heatmap_df[['Factor', 'Research & Development', 'Sales']].set_index('Factor').dropna()
plot_df = plot_df.sort_values('Sales', ascending=True)

# Color by the difference
colors = ['#e74c3c' if v > 20 else '#f39c12' if v > 15 else '#2ecc71' for v in plot_df['Sales']]
y_pos = range(len(plot_df))

for i, (idx, row) in enumerate(plot_df.iterrows()):
    color = '#e74c3c' if row['Sales'] > 20 else '#f39c12' if row['Sales'] > 15 else '#2ecc71'
    ax.barh(i+0.2, row['Sales'], height=0.3, color=color, alpha=0.7, edgecolor='black')
    color2 = '#e74c3c' if row['Research & Development'] > 20 else '#f39c12' if row['Research & Development'] > 15 else '#2ecc71'
    ax.barh(i-0.2, row['Research & Development'], height=0.3, color=color2, alpha=0.7, edgecolor='black')
    ax.text(row['Sales']+0.5, i+0.2, f"{row['Sales']:.1f}", va='center', fontsize=8)
    ax.text(row['Research & Development']+0.5, i-0.2, f"{row['Research & Development']:.1f}", va='center', fontsize=8)

ax.set_yticks(y_pos)
ax.set_yticklabels(plot_df.index, fontsize=9)
ax.set_xlabel('Attrition Rate (%)')
ax.set_title('Attrition Rate: Sales vs R&D by Factor', fontweight='bold')
ax.axvline(x=overall['Sales'], color='red', linestyle='--', alpha=0.5, label=f"Sales avg={overall['Sales']:.1f}%")
ax.axvline(x=overall['Research & Development'], color='green', linestyle='--', alpha=0.5, label=f"R&D avg={overall['Research & Development']:.1f}%")
ax.legend(fontsize=9)
ax.set_xlim(0, 70)

plt.tight_layout()
plt.savefig('/work/factor_comparison.png', dpi=150, bbox_inches='tight')
print("Saved factor_comparison.png")