import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/project_data.csv')
dfc = df[df['status']=='Completed']

# Final precision stats for report
print("=== ALL PROJECTS: Summary by Project Type ===")
for pt in ['Software Development', 'Infrastructure', 'Marketing Promotion']:
    g = df[df['Project Type']==pt]['deviation']
    print(f"\n{pt}: n={len(g)}")
    print(f"  Mean={g.mean():.2f}, Median={g.median():.2f}, Std={g.std():.2f}")
    print(f"  P10={g.quantile(0.1):.2f}, P25={g.quantile(0.25):.2f}, P75={g.quantile(0.75):.2f}, P90={g.quantile(0.9):.2f}")
    print(f"  Min={g.min():.2f}, Max={g.max():.2f}")
    print(f"  % positive (under budget): {(g>0).mean()*100:.1f}%")
    print(f"  % negative (over budget): {(g<0).mean()*100:.1f}%")

print("\n=== COMPLETED PROJECTS: Summary by Project Type ===")
for pt in ['Software Development', 'Infrastructure', 'Marketing Promotion']:
    g = dfc[dfc['Project Type']==pt]['deviation']
    print(f"\n{pt}: n={len(g)}")
    print(f"  Mean={g.mean():.2f}, Median={g.median():.2f}, Std={g.std():.2f}")
    print(f"  Min={g.min():.2f}, Max={g.max():.2f}")
    print(f"  % over budget: {(g<0).mean()*100:.1f}%")

print("\n=== OVERALL ===")
print(f"Total projects: {len(df)}")
print(f"Completed: {len(dfc)}")
print(f"All projects - mean deviation: {df['deviation'].mean():.2f}, median: {df['deviation'].median():.2f}")
print(f"Completed - mean deviation: {dfc['deviation'].mean():.2f}, median: {dfc['deviation'].median():.2f}")
print(f"Completed - % over budget: {(dfc['deviation']<0).mean()*100:.1f}%")

# What about the relationship between priority and deviation for completed?
print("\n=== Completed: Deviation by Priority ===")
for p in ['High', 'Medium', 'Low']:
    g = dfc[dfc['Priority']==p]['deviation']
    print(f"{p}: n={len(g)}, mean={g.mean():.2f}, median={g.median():.2f}, over_budget={(g<0).mean()*100:.1f}%")

# Check number of in-progress projects with high deviation
print("\n=== In-Progress projects: deviation distribution ===")
ip = df[df['status']=='In Progress']
print(f"n={len(ip)}, mean={ip['deviation'].mean():.2f}, median={ip['deviation'].median():.2f}")
print(f"mean comp%={ip['comp_num'].mean():.1f}%")
print(f"Expected remaining budget (mean): {ip['budget'].mean() * (100-ip['comp_num'].mean())/100:.2f}")
print(f"Current deviation (mean): {ip['deviation'].mean():.2f}")