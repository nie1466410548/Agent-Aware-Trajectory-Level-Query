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

# Create a decomposition waterfall chart
fig, ax = plt.subplots(figsize=(10, 6))

# Data for decomposition
actual_sales = 20.67
actual_rd = 13.75
rate_effect = 13.28  # from company-standardized
composition_effect = -6.36  # from company-standardized

# Waterfall
categories = ['Sales\nActual Rate', 'Composition\nEffect', 'Rate Effect\n(Within-Level)', 'R&D\nActual Rate']
values = [actual_sales, composition_effect, -(rate_effect), actual_rd]
# Actually, let me think about this more carefully.
# Sales actual = 20.67
# If we remove composition effect (Sales had R&D comp): 20.67 - 6.36 = 14.31? No...
# Let me recompute:

# The decomposition:
# Using company composition as reference:
# Sales standardized = 25.62%
# R&D standardized = 12.35%
# Rate effect = 25.62 - 12.35 = 13.28pp
# Composition effect = Actual diff - Rate effect = 6.92 - 13.28 = -6.36pp

# This means:
# If we equalize composition (to company avg), the gap widens to 13.28pp
# So composition actually masks the true rate difference
# The "rate effect" (within-level attrition differences) is the real driver

# Waterfall showing the decomposition
# Start with Sales actual rate
# Subtract the composition advantage (Sales has better composition)
# Then the remaining is the rate effect
# Followed by R&D actual rate

# Let me build a clean waterfall chart
sales_actual = 20.67
comp_advantage = 6.36  # Sales has composition advantage of 6.36pp
# If Sales had R&D's composition, its rate would be: 20.67 + 6.36 = 27.03
# Then the rate effect: 27.03 - 13.75 = 13.28pp

# So the waterfall:
# Start: Sales actual rate = 20.67%
# Step 1: If Sales had R&D composition (same composition) -> 20.67 + 6.36 = 27.03%
# Step 2: If Sales also had R&D within-level rates -> 27.03 - 13.28 = 13.75%
# End: R&D actual rate = 13.75%

# Build waterfall bars
x_labels = ['1. Sales\nActual Rate', '2. If Sales had\nR&D Composition', '3. If Sales also had\nR&D Within-Level Rates', '4. R&D\nActual Rate']
values = [sales_actual, comp_advantage, -13.28, 0]
running = [sales_actual, sales_actual + comp_advantage, sales_actual + comp_advantage - 13.28, 13.75]

# Draw waterfall
bar_colors = ['#3498db', '#f39c12', '#e74c3c', '#2ecc71']
bar_bottoms = [0, sales_actual, sales_actual + comp_advantage - 13.28, 0]
bar_values = [sales_actual, comp_advantage, 13.28, 13.75]

# Actually, let me use a simpler approach
x = np.arange(len(x_labels))
bar_width = 0.6

# Plot
for i in range(len(x_labels)):
    if i == 0:
        ax.bar(i, running[i], bar_width, color=bar_colors[i], edgecolor='black')
        ax.text(i, running[i]/2, f'{running[i]:.1f}%', ha='center', va='center', fontweight='bold', fontsize=11)
    elif i == len(x_labels)-1:
        ax.bar(i, running[i], bar_width, color=bar_colors[i], edgecolor='black')
        ax.text(i, running[i]/2, f'{running[i]:.1f}%', ha='center', va='center', fontweight='bold', fontsize=11)
    else:
        # This is a step
        ax.bar(i, abs(values[i]), bar_width, bottom=min(running[i-1], running[i]), 
               color=bar_colors[i], edgecolor='black')
        mid = (running[i-1] + running[i])/2
        ax.text(i, mid, f'{abs(values[i]):.1f}pp', ha='center', va='center', fontweight='bold', fontsize=11)

# Connect steps with lines
for i in range(len(x_labels)-1):
    ax.plot([i+0.3, i+1-0.3], [running[i], running[i]], color='gray', linestyle='--', linewidth=0.5)
    ax.plot([i+0.3, i+1-0.3], [running[i+1], running[i+1]], color='gray', linestyle='--', linewidth=0.5)

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=10)
ax.set_ylabel('Attrition Rate (%)', fontsize=12)
ax.set_title('Decomposition of Sales vs R&D Attrition Gap', fontsize=14, fontweight='bold')
ax.set_ylim(0, 32)

# Annotations
ax.annotate(f'Composition Effect:\n+{comp_advantage:.1f}pp\n(Sales has better\njob-level mix)', 
            xy=(1, running[0]+values[1]/2), fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef9e7', edgecolor='#f39c12'))
ax.annotate(f'Rate Effect:\n-{13.28:.1f}pp\n(R&D retains better\nwithin every level)', 
            xy=(2, running[1]-13.28/2), fontsize=9, ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fdedec', edgecolor='#e74c3c'))

plt.tight_layout()
plt.savefig('/work/decomposition.png', dpi=150, bbox_inches='tight')
print("Saved decomposition.png")

# Also create a summary statistics table
print("\n=== SUMMARY STATISTICS ===")
print(f"Department sizes: HR={len(df[df['Department']=='Human Resources'])}, R&D={len(df[df['Department']=='Research & Development'])}, Sales={len(df[df['Department']=='Sales'])}")
print(f"Attrition: HR={df[df['Department']=='Human Resources']['is_attrition'].sum()}, R&D={df[df['Department']=='Research & Development']['is_attrition'].sum()}, Sales={df[df['Department']=='Sales']['is_attrition'].sum()}")
print(f"Attrition rates: HR={df[df['Department']=='Human Resources']['is_attrition'].mean()*100:.2f}%, R&D={df[df['Department']=='Research & Development']['is_attrition'].mean()*100:.2f}%, Sales={df[df['Department']=='Sales']['is_attrition'].mean()*100:.2f}%")

# Key factors summary
print("\n=== KEY FACTORS CONTRIBUTING TO R&D LOWER ATTRITION ===")
print("\nFactor 1: Job Role Composition")
print("R&D has a diverse mix of roles including Research Directors (2.5% attrition),")
print("Managers (5.6%), and Manufacturing Directors (6.8%) with very low attrition.")
print("Sales has Sales Representatives (39.8% attrition) driving up the overall rate.")

print("\nFactor 2: Within-Level Attrition")
print("Across every job level, R&D has lower attrition than Sales.")
print("Level 1: R&D 23.2% vs Sales 41.6%")
print("Level 2: R&D 5.3% vs Sales 15.4%")
print("Level 3: R&D 10.0% vs Sales 21.4%")
print("Level 4: R&D 1.5% vs Sales 11.4%")

print("\nFactor 3: Overtime Impact")
print("Overtime employees in Sales have 38.0% attrition vs 27.2% in R&D")
print("Non-overtime employees: Sales 13.7% vs R&D 8.5%")

print("\nFactor 4: Stock Options")
print("R&D employees more likely to have stock options (StockLevel=0: 42.4% vs 44.2% in Sales)")
print("Within StockLevel=0: R&D 20.5% vs Sales 32.2%")

print("\nFactor 5: Marital Status")
print("Single employees: R&D 21.6% vs Sales 34.4%")
print("R&D has fewer single employees (31.6% vs 34.2% in Sales)")

print("\nFactor 6: Income within Level 1")
print("R&D Level 1 avg income: $2,842 vs Sales Level 1: $2,513")