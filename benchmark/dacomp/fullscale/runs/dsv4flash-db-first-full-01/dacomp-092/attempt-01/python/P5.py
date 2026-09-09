import numpy as np
import pandas as pd

# Monthly joined data from query S48
data = [
    ("2024-04", 19.87, 21.42, 80.55, 85.77),
    ("2024-05", 16.31, 16.48, 84.33, 91.20),
    ("2024-06", 9.48, 9.62, 82.93, 84.72),
    ("2024-07", 19.43, 19.06, 84.00, 89.59),
    ("2024-08", 28.68, 28.63, 82.29, 85.04),
    ("2024-09", 33.00, 33.47, 81.49, 85.36),
    ("2024-10", 26.55, 26.93, 82.68, 89.69),
    ("2024-11", 19.46, 18.87, 81.53, 81.53),
    ("2024-12", 7.91, 8.09, 85.27, 91.11),
    ("2025-01", 17.30, 17.67, 84.33, 92.34),
    ("2025-02", 31.66, 32.19, 81.62, 86.18),
    ("2025-03", 31.78, 30.11, 82.44, 87.81),
]

df = pd.DataFrame(data, columns=['month', 'hv_rev_share', 'hv_gp_share', 'health_score', 'collection_rate'])

# Split months into high vs low HV share
df['hv_share_bucket'] = np.where(df['hv_gp_share'] >= 25, 'High HV Share (>=25%)',
                         np.where(df['hv_gp_share'] < 15, 'Low HV Share (<15%)', 'Mid'))

print("=== Differential Impact: High vs Low HV Share Months ===")
for bucket in ['High HV Share (>=25%)', 'Mid', 'Low HV Share (<15%)']:
    sub = df[df['hv_share_bucket'] == bucket]
    if len(sub) > 0:
        print(f"\n{bucket}: n={len(sub)} months")
        print(f"  Avg Business Health Score: {sub['health_score'].mean():.2f}")
        print(f"  Avg Collection Rate: {sub['collection_rate'].mean():.2f}")

high = df[df['hv_gp_share'] >= 25]
low = df[df['hv_gp_share'] < 15]
print("\n=== Mean Comparison ===")
print(f"Health Score: High-share months {high['health_score'].mean():.2f} vs Low-share months {low['health_score'].mean():.2f} "
      f"(diff {low['health_score'].mean() - high['health_score'].mean():.2f})")
print(f"Collection Rate: High-share months {high['collection_rate'].mean():.2f} vs Low-share months {low['collection_rate'].mean():.2f} "
      f"(diff {low['collection_rate'].mean() - high['collection_rate'].mean():.2f})")

# Average HV share over period
print(f"\nAverage HV gross profit share over 12 months: {df['hv_gp_share'].mean():.1f}%")
print(f"Average HV revenue share over 12 months: {df['hv_rev_share'].mean():.1f}%")

# High-vol contribution to gross profit and outstanding balance
print(f"\nHigh-vol customers: 700/2800 (25%) of customers")
print(f"High-vol revenue share: ~21.9% of invoices")
print(f"High-vol outstanding balance share: 22.2%")

# AR structure
print(f"\n=== AR Risk Exposure ===")
print(f"Total AR (all periods): $109.07M")
print(f"  Current (0-30d): 72.2%")
print(f"  Past Due (31-60d): 18.1%")
print(f"  Past Due (61-90d): 7.2%")
print(f"  Long Overdue (90+): 2.5%")
print(f"Total past-due exposure: 27.8% of AR")