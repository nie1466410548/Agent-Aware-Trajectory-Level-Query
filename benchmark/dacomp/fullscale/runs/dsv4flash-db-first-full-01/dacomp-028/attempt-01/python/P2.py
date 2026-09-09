import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Read the monthly stats
monthly = pd.read_csv('/work/monthly_stats.csv')

# Sort
monthly = monthly.sort_values(['Product Category', 'Market Name', 'Price Type', 'month'])

# Compute MoM growth rate
monthly['prev_avg_price'] = monthly.groupby(['Product Category', 'Market Name', 'Price Type'])['avg_price'].shift(1)
monthly['mom_growth_pct'] = ((monthly['avg_price'] - monthly['prev_avg_price']) / monthly['prev_avg_price']) * 100

print("=== MoM Growth Rates (all) ===")
print(monthly[['month', 'Product Category', 'Market Name', 'Price Type', 'avg_price', 'prev_avg_price', 'mom_growth_pct']].to_string(index=False))

# Focus on Vegetables (most data)
veg = monthly[monthly['Product Category'] == 'Vegetable'].copy()
print("\n\n=== Vegetable MoM Growth Rates ===")
print(veg[['month', 'Market Name', 'Price Type', 'avg_price', 'mom_growth_pct']].to_string(index=False))

# Compute overall average MoM growth per category
overall_monthly = df.groupby(['month', 'Product Category', 'Price Type']).agg(
    avg_price=('Average Price', 'mean'),
    count=('Average Price', 'count')
).reset_index().sort_values(['Product Category', 'Price Type', 'month'])

overall_monthly['prev_avg_price'] = overall_monthly.groupby(['Product Category', 'Price Type'])['avg_price'].shift(1)
overall_monthly['mom_growth_pct'] = ((overall_monthly['avg_price'] - overall_monthly['prev_avg_price']) / overall_monthly['prev_avg_price']) * 100

print("\n\n=== Overall (all markets combined) MoM Growth ===")
print(overall_monthly[['month', 'Product Category', 'Price Type', 'avg_price', 'mom_growth_pct']].to_string(index=False))

# Save for plotting
overall_monthly.to_csv('/work/overall_monthly.csv', index=False)
monthly.to_csv('/work/monthly_with_mom.csv', index=False)