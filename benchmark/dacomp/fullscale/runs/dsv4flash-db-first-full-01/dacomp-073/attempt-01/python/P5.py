import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Get all data
postings = db.frame(db.query("SELECT * FROM lever__posting_enhanced"))
requisitions = db.frame(db.query("SELECT * FROM lever__requisition_enhanced"))

# ===== STEP 1: Monthly Posting Counts per Department =====
postings['ym'] = postings['created_at'].str[:7]
monthly = postings.groupby(['categories_department', 'ym']).size().unstack(fill_value=0)
print("Monthly Posting Counts per Department:")
print(monthly)

# ===== STEP 2: MoM Growth Rates =====
departments = ['Engineering', 'Finance', 'HR', 'Marketing', 'Operations', 'Sales']
months = ['2025-05', '2025-06', '2025-07']

mom_growth = {}
for dept in departments:
    growth_rates = []
    for i in range(1, len(months)):
        prev = monthly.loc[dept, months[i-1]]
        curr = monthly.loc[dept, months[i]]
        if prev > 0:
            growth = (curr - prev) / prev
            growth_rates.append(growth)
    avg_growth = np.mean(growth_rates) if growth_rates else 0
    mom_growth[dept] = {
        'may': monthly.loc[dept, '2025-05'],
        'jun': monthly.loc[dept, '2025-06'],
        'jul': monthly.loc[dept, '2025-07'],
        'jun_mom': growth_rates[0] if len(growth_rates) > 0 else 0,
        'jul_mom': growth_rates[1] if len(growth_rates) > 1 else 0,
        'avg_mom': avg_growth,
        'latest_mom': growth_rates[-1] if growth_rates else 0
    }

print("\n\nMoM Growth Rates:")
print(f"{'Department':<15} {'May':<8} {'Jun':<8} {'Jul':<8} {'Jun MoM':<10} {'Jul MoM':<10} {'Avg MoM':<10}")
print("="*75)
for dept, data in mom_growth.items():
    print(f"{dept:<15} {data['may']:<8} {data['jun']:<8} {data['jul']:<8} {data['jun_mom']*100:<10.1f}% {data['jul_mom']*100:<10.1f}% {data['avg_mom']*100:<10.1f}%")

# ===== STEP 3: Current Active Postings =====
active = postings[postings['state'].isin(['published', 'pending'])]
active_counts = active.groupby('categories_department').size()
print("\n\nCurrent Active Postings (Published + Pending):")
print(active_counts)

# Active HMs per department
active_hms = active.groupby('categories_department')['posting_hiring_manager_name'].nunique()
all_hms = postings.groupby('categories_department')['posting_hiring_manager_name'].nunique()

print("\nDistinct Hiring Managers per Department:")
print(pd.DataFrame({'all_hms': all_hms, 'active_hms': active_hms}))

# ===== STEP 4: Identify High-Growth Teams =====
# Criteria: avg MoM > 15% AND active postings > 10
high_growth = {}
for dept in departments:
    avg_mom = mom_growth[dept]['avg_mom']
    active_cnt = active_counts.get(dept, 0)
    is_high = avg_mom > 0.15 and active_cnt > 10
    high_growth[dept] = {
        'avg_mom': avg_mom,
        'active_postings': active_cnt,
        'is_high_growth': is_high
    }
    print(f"{dept}: avg_mom={avg_mom*100:.1f}%, active={active_cnt}, high_growth={is_high}")

# ===== STEP 5: Hiring Pressure Index =====
# Using count_open_opportunities as "pending roles" (open opportunities/candidates to process)
# This represents the hiring workload each team faces
open_opp = active.groupby('categories_department')['count_open_opportunities'].sum()
print("\n\nOpen Opportunities per Department:")
print(open_opp)

# Pressure Index = open_opportunities / hiring_managers
pressure_index = {}
for dept in departments:
    opp = open_opp.get(dept, 0)
    hm = active_hms.get(dept, 1)  # use active HMs
    pi = opp / hm
    pressure_index[dept] = {
        'open_opp': opp,
        'hiring_managers': hm,
        'pressure_index': pi
    }
    print(f"{dept}: open_opp={opp:.0f}, HMs={hm}, PI={pi:.2f}")

# ===== STEP 6: Project 2 Months Forward =====
# Future pressure = current pressure * (1 + avg_mom_growth)^2
future_pressure = {}
shortage_teams = []
additional_resources = {}

for dept in departments:
    curr_pi = pressure_index[dept]['pressure_index']
    curr_opp = pressure_index[dept]['open_opp']
    hm = pressure_index[dept]['hiring_managers']
    avg_mom = mom_growth[dept]['avg_mom']
    
    # Projected pending roles in 2 months
    projected_opp = curr_opp * (1 + avg_mom) ** 2
    projected_pi = projected_opp / hm
    
    # Capacity: each HM handles max 6 postings
    # Additional resources needed = (projected opp - 6 * HMs) / 6
    capacity = 6
    needed = max(0, (projected_opp - capacity * hm) / capacity)
    
    future_pressure[dept] = {
        'current_pi': curr_pi,
        'projected_opp': projected_opp,
        'projected_pi': projected_pi,
        'will_shortage': projected_pi > 8,
        'additional_resources': needed
    }
    
    print(f"\n{dept}:")
    print(f"  Current PI: {curr_pi:.2f}")
    print(f"  Projected Open Opp in 2 months: {projected_opp:.0f}")
    print(f"  Projected PI: {projected_pi:.2f}")
    print(f"  Shortage risk (PI>8): {projected_pi > 8}")
    if projected_pi > 8:
        print(f"  Additional HMs needed: {needed:.1f}")
        shortage_teams.append(dept)
        additional_resources[dept] = needed

print(f"\n\nTeams facing resource shortage: {shortage_teams}")
for dept, res in additional_resources.items():
    print(f"  {dept}: {res:.1f} additional HMs needed")

# ===== VISUALIZATION =====
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Monthly posting trends
ax = axes[0, 0]
for dept in departments:
    vals = [mom_growth[dept]['may'], mom_growth[dept]['jun'], mom_growth[dept]['jul']]
    ax.plot(['May', 'Jun', 'Jul'], vals, marker='o', label=dept)
ax.set_title('Monthly Posting Counts per Department')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Postings')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

# 2. MoM growth rates
ax = axes[0, 1]
dept_names = departments
avg_moms = [mom_growth[d]['avg_mom']*100 for d in departments]
colors = ['green' if v > 15 else 'red' for v in avg_moms]
bars = ax.bar(dept_names, avg_moms, color=colors)
ax.axhline(y=15, color='red', linestyle='--', label='15% threshold')
ax.set_title('Average MoM Growth Rate (%)')
ax.set_ylabel('Growth Rate (%)')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# 3. Active postings
ax = axes[0, 2]
act_vals = [active_counts.get(d, 0) for d in departments]
ax.bar(dept_names, act_vals, color='steelblue')
ax.axhline(y=10, color='red', linestyle='--', label='10 threshold')
ax.set_title('Current Active Postings per Department')
ax.set_ylabel('Active Postings')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# 4. Pressure Index (current)
ax = axes[1, 0]
curr_pis = [pressure_index[d]['pressure_index'] for d in departments]
ax.bar(dept_names, curr_pis, color='coral')
ax.axhline(y=8, color='red', linestyle='--', label='Shortage threshold (8)')
ax.set_title('Current Hiring Pressure Index')
ax.set_ylabel('Pressure Index (Open Opp / HMs)')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# 5. Projected Pressure Index
ax = axes[1, 1]
proj_pis = [future_pressure[d]['projected_pi'] for d in departments]
colors2 = ['red' if v > 8 else 'steelblue' for v in proj_pis]
ax.bar(dept_names, proj_pis, color=colors2)
ax.axhline(y=8, color='red', linestyle='--', label='Shortage threshold (8)')
ax.set_title('Projected Pressure Index (2 months)')
ax.set_ylabel('Projected Pressure Index')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# 6. Additional resources needed
ax = axes[1, 2]
add_res = [future_pressure[d]['additional_resources'] for d in departments]
colors3 = ['red' if r > 0 else 'green' for r in add_res]
ax.bar(dept_names, add_res, color=colors3)
ax.set_title('Additional Hiring Managers Needed')
ax.set_ylabel('Additional HMs')
ax.axhline(y=0, color='black', linestyle='-')
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/hiring_analysis.png', dpi=150)
plt.close()
print("\n\nChart saved to /work/hiring_analysis.png")