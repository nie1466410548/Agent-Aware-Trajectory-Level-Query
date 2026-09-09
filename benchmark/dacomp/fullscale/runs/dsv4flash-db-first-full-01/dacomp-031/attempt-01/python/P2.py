import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

# ===== Figure 1: Attrition Rate by Tenure Band =====
res = db.query("""
SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         WHEN YearsAtCompany > 20 THEN '20+ years'
       END AS tenure_band,
       COUNT(*) AS total,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)
""")
df_band = db.frame(res)
print(df_band)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: Employee count
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
bars1 = axes[0].bar(df_band['tenure_band'], df_band['total'], color=colors, alpha=0.8)
axes[0].set_title('Employee Count by Tenure Band', fontsize=14)
axes[0].set_xlabel('Tenure Band')
axes[0].set_ylabel('Number of Employees')
for bar, val in zip(bars1, df_band['total']):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+10, str(val), ha='center', fontsize=11)

# Right: Attrition rate
bars2 = axes[1].bar(df_band['tenure_band'], df_band['attrition_rate'], color=colors, alpha=0.8)
axes[1].set_title('Attrition Rate by Tenure Band', fontsize=14)
axes[1].set_xlabel('Tenure Band')
axes[1].set_ylabel('Attrition Rate (%)')
for bar, val in zip(bars2, df_band['attrition_rate']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val}%', ha='center', fontsize=11)
axes[1].axhline(y=16.08, color='red', linestyle='--', alpha=0.6, label=f'Overall Avg: 16.08%')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/fig1_tenure_bands.png', dpi=150)
plt.close()

# ===== Figure 2: Long-term vs Short-term Comparison =====
res2 = db.query("""
SELECT CASE WHEN YearsAtCompany >= 10 THEN '10+ Years' ELSE '<10 Years' END AS group_name,
       ROUND(AVG(MonthlyIncome),0) AS avg_income,
       ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
       ROUND(AVG(JobLevel),2) AS avg_job_level,
       ROUND(AVG(StockOptionLevel),2) AS avg_stock,
       ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
       ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
       ROUND(100.0*SUM(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_overtime,
       ROUND(100.0*SUM(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_no_stock,
       COUNT(*) AS cnt
FROM sheet1
GROUP BY group_name
ORDER BY group_name DESC
""")
df_lt = db.frame(res2)
print(df_lt)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

metrics = [
    ('avg_income', 'Avg Monthly Income ($)', '#2c3e50'),
    ('avg_years_since_promo', 'Avg Years Since Last Promotion', '#e74c3c'),
    ('avg_job_level', 'Avg Job Level (1-5)', '#3498db'),
    ('pct_overtime', 'Employees Working Overtime (%)', '#e67e22'),
    ('pct_no_stock', 'No Stock Options (%)', '#9b59b6'),
    ('avg_jobsat', 'Avg Job Satisfaction (1-4)', '#27ae60')
]

for idx, (metric, label, color) in enumerate(metrics):
    row, col = divmod(idx, 3)
    ax = axes[row, col]
    bars = ax.bar(df_lt['group_name'], df_lt[metric], color=[color, color], alpha=0.7)
    for bar, val in zip(bars, df_lt[metric]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.02, 
                f'{val}', ha='center', fontsize=11, fontweight='bold')
    ax.set_title(label, fontsize=12)
    ax.set_ylabel(label)
    ax.set_xlabel('')

plt.suptitle('Long-term (10+ years) vs Short-term Employees: Key Metrics', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/work/fig2_longterm_comparison.png', dpi=150)
plt.close()

# ===== Figure 3: Income Progression by Tenure Band =====
res3 = db.query("""
SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         ELSE '20+ years'
       END AS tenure_band,
       ROUND(AVG(MonthlyIncome),0) AS avg_income,
       ROUND(AVG(JobLevel),2) AS avg_job_level,
       ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
       ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)
""")
df_inc = db.frame(res3)

fig, ax1 = plt.subplots(figsize=(10, 6))

x = np.arange(len(df_inc['tenure_band']))
width = 0.35

bars1 = ax1.bar(x - width/2, df_inc['avg_income'], width, label='Avg Monthly Income ($)', color='#3498db', alpha=0.8)
ax1.set_ylabel('Avg Monthly Income ($)', fontsize=12)
ax1.set_xlabel('Tenure Band', fontsize=12)

ax2 = ax1.twinx()
bars2 = ax2.bar(x + width/2, df_inc['avg_years_since_promo'], width, label='Avg Years Since Last Promotion', color='#e74c3c', alpha=0.8)
ax2.set_ylabel('Avg Years Since Last Promotion', fontsize=12)

ax1.set_xticks(x)
ax1.set_xticklabels(df_inc['tenure_band'])

# Add value labels
for bar in bars1:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100, f'${bar.get_height():.0f}', ha='center', fontsize=9)
for bar in bars2:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, f'{bar.get_height():.1f}', ha='center', fontsize=9)

fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.95))
plt.title('Income and Promotion Gap by Tenure Band', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig3_income_promotion.png', dpi=150)
plt.close()

# ===== Figure 4: Attrition Drivers - Overtime & Stock Options =====
res4 = db.query("""
SELECT OverTime, StockOptionLevel, 
       COUNT(*) AS cnt,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_rate
FROM sheet1
GROUP BY OverTime, StockOptionLevel
ORDER BY OverTime, StockOptionLevel
""")
df_driver = db.frame(res4)
print(df_driver)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Overtime impact
ot_data = df_driver.groupby('OverTime')['attrition_rate'].mean().reset_index()
ot_data['OverTime'] = ot_data['OverTime'].map({'No': 'No Overtime', 'Yes': 'Overtime'})
bars = axes[0].bar(ot_data['OverTime'], ot_data['attrition_rate'], 
                   color=['#2ecc71', '#e74c3c'], alpha=0.8, width=0.5)
for bar, val in zip(bars, ot_data['attrition_rate']):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}%', ha='center', fontsize=13, fontweight='bold')
axes[0].set_title('Attrition Rate by Overtime Status', fontsize=14)
axes[0].set_ylabel('Attrition Rate (%)')
axes[0].set_ylim(0, 55)

# Stock option impact
so_data = df_driver.groupby('StockOptionLevel')['attrition_rate'].mean().reset_index()
so_data['StockOptionLevel'] = so_data['StockOptionLevel'].astype(int)
bars = axes[1].bar(so_data['StockOptionLevel'], so_data['attrition_rate'], 
                   color=['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6'], alpha=0.8, width=0.6)
for bar, val in zip(bars, so_data['attrition_rate']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
axes[1].set_title('Attrition Rate by Stock Option Level', fontsize=14)
axes[1].set_xlabel('Stock Option Level (0=none, 4=highest)')
axes[1].set_ylabel('Attrition Rate (%)')
axes[1].set_ylim(0, 25)

plt.tight_layout()
plt.savefig('/work/fig4_attrition_drivers.png', dpi=150)
plt.close()

print("All figures saved.")