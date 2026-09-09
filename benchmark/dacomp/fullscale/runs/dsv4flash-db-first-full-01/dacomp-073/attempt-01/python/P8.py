import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===== DATA LOADING =====
postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
requisitions = db.frame(db.query("SELECT * FROM lever__requisition_enhanced"))

# ===== 1. MONTHLY POSTING TRENDS =====
postings['ym'] = postings['created_at'].str[:7]
monthly = postings.groupby(['categories_department', 'ym']).size().unstack(fill_value=0)

# ===== 2. MoM GROWTH RATES =====
departments = ['Engineering', 'Finance', 'HR', 'Marketing', 'Operations', 'Sales']
months = ['2025-05', '2025-06', '2025-07']

growth_data = {}
for dept in departments:
    may = monthly.loc[dept, '2025-05']
    jun = monthly.loc[dept, '2025-06']
    jul = monthly.loc[dept, '2025-07']
    jun_mom = (jun - may) / may if may > 0 else 0
    jul_mom = (jul - jun) / jun if jun > 0 else 0
    avg_mom = (jun_mom + jul_mom) / 2
    growth_data[dept] = {'may': may, 'jun': jun, 'jul': jul, 'jun_mom': jun_mom, 'jul_mom': jul_mom, 'avg_mom': avg_mom}

# ===== 3. ACTIVE POSTINGS & HIRING MANAGERS =====
active = postings[postings['state'].isin(['published', 'pending'])]
active_counts = active.groupby('categories_department').size()
active_hms = active.groupby('categories_department')['posting_hiring_manager_name'].nunique()
all_hms = postings.groupby('categories_department')['posting_hiring_manager_name'].nunique()

# ===== 4. HIGH-GROWTH TEAMS =====
# Criteria: avg MoM > 15% AND active postings > 10
high_growth_depts = []
for dept in departments:
    if growth_data[dept]['avg_mom'] > 0.15 and active_counts.get(dept, 0) > 10:
        high_growth_depts.append(dept)

print(f"High-growth teams (avg MoM > 15%, active > 10): {high_growth_depts}")

# ===== 5. HIRING PRESSURE INDEX =====
# Using count_open_opportunities as "pending roles" - this represents the number of 
# open candidate opportunities (applications) that hiring managers need to process
# Index = open_opportunities / hiring_managers

pressure_current = {}
for dept in high_growth_depts:
    open_opp = active[active['categories_department'] == dept]['count_open_opportunities'].sum()
    hm = active_hms.get(dept, 1)
    pressure_current[dept] = {'open_opp': open_opp, 'hms': hm, 'pi': open_opp / hm}

print("\nCurrent Hiring Pressure Index (Open Opp / Active HMs):")
for dept, data in pressure_current.items():
    print(f"  {dept}: {data['open_opp']:.0f} open opp / {data['hms']} HMs = {data['pi']:.2f}")

# ===== 6. PROJECT 2 MONTHS FORWARD =====
# Projected pending roles = current * (1 + avg_mom)^2
# Projected PI = projected / current HMs
# Shortage if projected PI > 8
# Additional resources = max(0, (projected - 6 * HMs) / 6)

shortage_teams = []
resources_needed = {}
pressure_projected = {}

for dept in high_growth_depts:
    curr_opp = pressure_current[dept]['open_opp']
    curr_hm = pressure_current[dept]['hms']
    avg_mom = growth_data[dept]['avg_mom']
    
    proj_opp = curr_opp * (1 + avg_mom) ** 2
    proj_pi = proj_opp / curr_hm
    
    # Additional resources needed if projected pressure > 8
    # Each HM handles max 6 postings worth of work
    add_hm = max(0, (proj_opp - 6 * curr_hm) / 6)
    
    pressure_projected[dept] = {'proj_opp': proj_opp, 'proj_pi': proj_pi, 'add_hm': add_hm}
    
    if proj_pi > 8:
        shortage_teams.append(dept)
        resources_needed[dept] = add_hm
    
    print(f"\n{dept}:")
    print(f"  Current: {curr_opp:.0f} opp, {curr_hm} HMs, PI={pressure_current[dept]['pi']:.2f}")
    print(f"  Projected (2mo): {proj_opp:.0f} opp, PI={proj_pi:.2f}")
    print(f"  Shortage risk: {'YES' if proj_pi > 8 else 'NO'}")
    if proj_pi > 8:
        print(f"  Additional HMs needed: {add_hm:.1f}")

print(f"\n\nTeams facing resource shortage: {shortage_teams}")

# ===== 7. VISUALIZATIONS =====
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Monthly posting trends
ax = axes[0, 0]
for dept in departments:
    vals = [growth_data[dept]['may'], growth_data[dept]['jun'], growth_data[dept]['jul']]
    ax.plot(['May', 'Jun', 'Jul'], vals, marker='o', linewidth=2, label=dept)
ax.set_title('Monthly Posting Creation Counts per Department', fontsize=12, fontweight='bold')
ax.set_xlabel('Month (2025)')
ax.set_ylabel('Number of Postings Created')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

# 2. MoM growth rates
ax = axes[0, 1]
avg_moms = [growth_data[d]['avg_mom']*100 for d in departments]
colors = ['#2ecc71' if v > 15 else '#e74c3c' for v in avg_moms]
bars = ax.bar(departments, avg_moms, color=colors, edgecolor='black', linewidth=0.5)
ax.axhline(y=15, color='#e74c3c', linestyle='--', linewidth=2, label='15% threshold')
for bar, val in zip(bars, avg_moms):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%', 
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Average MoM Growth Rate', fontsize=12, fontweight='bold')
ax.set_ylabel('Growth Rate (%)')
ax.legend()
ax.tick_params(axis='x', rotation=30)

# 3. Current active postings
ax = axes[0, 2]
act_vals = [active_counts.get(d, 0) for d in departments]
bars = ax.bar(departments, act_vals, color='#3498db', edgecolor='black', linewidth=0.5)
ax.axhline(y=10, color='#e74c3c', linestyle='--', linewidth=2, label='10 threshold')
for bar, val in zip(bars, act_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, str(val), 
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Current Active Postings (Published + Pending)', fontsize=12, fontweight='bold')
ax.set_ylabel('Active Postings')
ax.legend()
ax.tick_params(axis='x', rotation=30)

# 4. Current Pressure Index
ax = axes[1, 0]
curr_pis = [pressure_current[d]['pi'] for d in high_growth_depts]
bars = ax.bar(high_growth_depts, curr_pis, color='#e67e22', edgecolor='black', linewidth=0.5)
ax.axhline(y=8, color='#e74c3c', linestyle='--', linewidth=2, label='Shortage threshold (8)')
for bar, val in zip(bars, curr_pis):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{val:.1f}', 
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Current Hiring Pressure Index\n(Open Opp / HMs)', fontsize=12, fontweight='bold')
ax.set_ylabel('Pressure Index')
ax.legend()
ax.tick_params(axis='x', rotation=30)

# 5. Projected Pressure Index
ax = axes[1, 1]
proj_pis = [pressure_projected[d]['proj_pi'] for d in high_growth_depts]
colors2 = ['#e74c3c' if v > 8 else '#2ecc71' for v in proj_pis]
bars = ax.bar(high_growth_depts, proj_pis, color=colors2, edgecolor='black', linewidth=0.5)
ax.axhline(y=8, color='#e74c3c', linestyle='--', linewidth=2, label='Shortage threshold (8)')
for bar, val in zip(bars, proj_pis):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}', 
            ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Projected Pressure Index (2 Months)', fontsize=12, fontweight='bold')
ax.set_ylabel('Projected Pressure Index')
ax.legend()
ax.tick_params(axis='x', rotation=30)

# 6. Additional resources needed
ax = axes[1, 2]
add_res = [pressure_projected[d]['add_hm'] for d in high_growth_depts]
colors3 = ['#e74c3c' if r > 0 else '#2ecc71' for r in add_res]
bars = ax.bar(high_growth_depts, add_res, color=colors3, edgecolor='black', linewidth=0.5)
for bar, val in zip(bars, add_res):
    if val > 0:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Additional Hiring Managers Needed\n(Projected 2 Months)', fontsize=12, fontweight='bold')
ax.set_ylabel('Additional HMs Required')
ax.axhline(y=0, color='black', linewidth=1)
ax.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig('/work/hiring_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nChart saved to /work/hiring_analysis.png")

# ===== 8. SUMMARY TABLE =====
print("\n\n" + "="*80)
print("SUMMARY TABLE")
print("="*80)
print(f"{'Department':<15} {'Avg MoM':<10} {'Active':<10} {'High':<10} {'Curr PI':<10} {'Proj PI':<10} {'Shortage':<10} {'Add HMs':<10}")
print("-"*80)
for dept in departments:
    avg_mom = growth_data[dept]['avg_mom']*100
    act = active_counts.get(dept, 0)
    high = 'YES' if dept in high_growth_depts else 'no'
    if dept in high_growth_depts:
        curr_pi = f"{pressure_current[dept]['pi']:.1f}"
        proj_pi = f"{pressure_projected[dept]['proj_pi']:.1f}"
        short = 'YES' if dept in shortage_teams else 'no'
        add = f"{pressure_projected[dept]['add_hm']:.1f}" if dept in shortage_teams else '0'
    else:
        curr_pi = 'N/A'
        proj_pi = 'N/A'
        short = 'N/A'
        add = 'N/A'
    print(f"{dept:<15} {avg_mom:<10.1f}% {act:<10} {high:<10} {curr_pi:<10} {proj_pi:<10} {short:<10} {add:<10}")