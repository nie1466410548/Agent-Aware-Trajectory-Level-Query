import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Figure 1: National education distribution over time (broad categories)
fig, axes = plt.subplots(1, 3, figsize=(18, 7), sharey=True)

years = [2000, 2010, 2020]
# Comparable categories: No schooling, Primary, Junior high, Senior high+, Higher education
# 2000: No school = never+literacy, Senior high+ = senior+vocational, Higher = jcollege+undergrad+postgrad
# 2010/2020: No school = never, Senior high = senior, Higher = jcollege+undergrad+postgrad

data = {
    2000: {'No schooling': 110.4, 'Primary': 441.6, 'Junior high': 422.4, 'Senior high+': 138.3, 'Higher education': 44.0},
    2010: {'No schooling': 62.1, 'Primary': 357.2, 'Junior high': 518.2, 'Senior high': 186.6, 'Higher education': 118.4},
    2020: {'No schooling': 41.5, 'Primary': 347.4, 'Junior high': 487.1, 'Senior high': 212.2, 'Higher education': 217.2}
}

# Convert to percentages
pop = {2000: 1156.7, 2010: 1242.5, 2020: 1315.3}
cats = ['No schooling', 'Primary', 'Junior high', 'Senior high', 'Higher education']
# For 2000, senior high+ maps to senior high category
colors = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']

for i, yr in enumerate(years):
    ax = axes[i]
    vals = data[yr]
    # Map 2000 senior high+ to senior high category
    if yr == 2000:
        d = [vals['No schooling'], vals['Primary'], vals['Junior high'], vals['Senior high+'], vals['Higher education']]
    else:
        d = [vals['No schooling'], vals['Primary'], vals['Junior high'], vals['Senior high'], vals['Higher education']]
    d_pct = [100*v/pop[yr] for v in d]
    
    bars = ax.barh(cats, d_pct, color=colors)
    for bar, v, absv in zip(bars, d_pct, d):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{v:.1f}%\n({absv:.1f}M)', ha='left', va='center', fontsize=9)
    ax.set_xlim(0, 55)
    ax.set_title(f'{yr}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Percentage of population 6+ (%)')
    if i == 0:
        ax.set_ylabel('Education level')

plt.suptitle('China Education Attainment Distribution (2000 → 2020)', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/work/fig1_national_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 2: Gender gap - female share of each education level
fig, ax = plt.subplots(figsize=(12, 7))
gendata = {
    2000: {'Never': 71.7, 'Primary': 50.9, 'Junior high': 43.6, 'Senior high': 39.8, 'Vocational': 49.1, 'Junior college': 40.2, 'Undergraduate': 34.9, 'Postgraduate': 30.2},
    2010: {'Never': 71.8, 'Primary': 52.9, 'Junior high': 46.2, 'Senior high': 44.3, 'Junior college': 46.3, 'Undergraduate': 44.7, 'Postgraduate': 43.2},
    2020: {'Never': 74.2, 'Primary': 52.9, 'Junior high': 45.9, 'Senior high': 44.9, 'Junior college': 47.7, 'Undergraduate': 49.4, "Master's": 50.2, 'Doctoral': 39.4}
}
# Use comparable categories
cats2 = ['Never', 'Primary', 'Junior high', 'Senior high', 'Junior college', 'Undergraduate', 'Postgraduate']
x = np.arange(len(cats2))
width = 0.25
bars1 = ax.bar(x - width, [gendata[2000].get(c, 0) for c in cats2], width, label='2000', color='#1f77b4')
bars2 = ax.bar(x, [gendata[2010].get(c, 0) for c in cats2], width, label='2010', color='#ff7f0e')
bars3 = ax.bar(x + width, [gendata[2020].get(c, 0) for c in cats2], width, label='2020', color='#2ca02c')
ax.axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='50% (gender parity)')
ax.set_xticks(x)
ax.set_xticklabels(cats2)
ax.set_ylabel('Female share (%)')
ax.set_title('Female Share of Education Attainment by Level (2000-2020)', fontsize=16, fontweight='bold')
ax.legend()
ax.set_ylim(0, 85)
for bar in bars1+bars2+bars3:
    h = bar.get_height()
    if h > 0:
        ax.text(bar.get_x()+bar.get_width()/2, h+1, f'{h:.1f}%', ha='center', va='bottom', fontsize=8, rotation=90)
plt.tight_layout()
plt.savefig('/work/fig2_gender_gap.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 3: Age cohort - higher education rates
fig, ax = plt.subplots(figsize=(12, 7))
age_cats = ['6-14', '15-19', '20-24', '25-34', '35-44', '45-54', '55-64', '65+']
age_higher = {
    2000: [0.0, 3.4, 8.6, 6.1, 4.8, 3.0, 3.1, 1.5],
    2010: [0.0, 8.2, 25.3, 17.9, 9.1, 6.1, 3.6, 3.2],
    2020: [0.0, 21.6, 51.9, 35.8, 23.0, 10.0, 6.1, 3.6]
}
age_noschool = {
    2000: [2.7, 1.0, 1.7, 2.6, 4.5, 11.0, 25.6, 55.0],
    2010: [2.1, 0.5, 0.5, 0.9, 1.7, 3.4, 9.1, 28.1],
    2020: [0.5, 0.2, 0.3, 0.4, 0.8, 1.8, 3.9, 14.2]
}

x = np.arange(len(age_cats))
width = 0.25
ax.bar(x - width, age_higher[2000], width, label='2000', color='#1f77b4')
ax.bar(x, age_higher[2010], width, label='2010', color='#ff7f0e')
ax.bar(x + width, age_higher[2020], width, label='2020', color='#2ca02c')
ax.set_xticks(x)
ax.set_xticklabels(age_cats)
ax.set_ylabel('Higher education rate (%)')
ax.set_title('Higher Education (Junior College+) Rate by Age Group', fontsize=16, fontweight='bold')
ax.legend()
for i, (v2000, v2010, v2020) in enumerate(zip(age_higher[2000], age_higher[2010], age_higher[2020])):
    if v2000 > 0:
        ax.text(i - width, v2000 + 0.5, f'{v2000:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
    if v2010 > 0:
        ax.text(i, v2010 + 0.5, f'{v2010:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
    if v2020 > 0:
        ax.text(i + width, v2020 + 0.5, f'{v2020:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
plt.tight_layout()
plt.savefig('/work/fig3_age_higher_edu.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 4: Urban/Rural comparison
fig, axes = plt.subplots(1, 3, figsize=(18, 7), sharey=True)
reg_years = [(2000, [('Urban', 11.7), ('Town', 5.0), ('Village', 0.5)]),
             (2010, [('City', 21.5), ('Town', 9.3), ('Rural', 2.1)]),
             (2020, [('City', 28.2), ('Town', 14.0), ('Rural', 4.9)])]

for i, (yr, regs) in enumerate(reg_years):
    ax = axes[i]
    names = [r[0] for r in regs]
    vals = [r[1] for r in regs]
    colors_reg = ['#1f77b4', '#ff7f0e', '#2ca02c']
    bars = ax.barh(names, vals, color=colors_reg)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, f'{v:.1f}%', ha='left', va='center', fontsize=12)
    ax.set_title(f'{yr}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Higher education rate (%)')
    ax.set_xlim(0, 35)
    if i == 0:
        ax.set_ylabel('Region')

plt.suptitle('Higher Education Rate by Urban/Rural Classification', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/work/fig4_urban_rural.png', dpi=150, bbox_inches='tight')
plt.close()

# Figure 5: No schooling rate decline by age group
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(age_cats))
width = 0.25
ax.bar(x - width, age_noschool[2000], width, label='2000', color='#1f77b4')
ax.bar(x, age_noschool[2010], width, label='2010', color='#ff7f0e')
ax.bar(x + width, age_noschool[2020], width, label='2020', color='#2ca02c')
ax.set_xticks(x)
ax.set_xticklabels(age_cats)
ax.set_ylabel('No schooling rate (%)')
ax.set_title('No Schooling Rate by Age Group (2000-2020)', fontsize=16, fontweight='bold')
ax.legend()
for i, (v2000, v2010, v2020) in enumerate(zip(age_noschool[2000], age_noschool[2010], age_noschool[2020])):
    if v2000 > 0:
        ax.text(i - width, v2000 + 0.5, f'{v2000:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
    if v2010 > 0:
        ax.text(i, v2010 + 0.5, f'{v2010:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
    if v2020 > 0:
        ax.text(i + width, v2020 + 0.5, f'{v2020:.1f}', ha='center', va='bottom', fontsize=7, rotation=90)
plt.tight_layout()
plt.savefig('/work/fig5_noschooling_age.png', dpi=150, bbox_inches='tight')
plt.close()

print("All figures saved successfully!")