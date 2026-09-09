import numpy as np
import pandas as pd

tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']

# 1. Health score distribution per tier
dist = ov_df.groupby('organization_size_category')['organization_health_score'].agg(
    n='count', mean='mean', median='median', std='std', min='min', max='max',
    q25=lambda x: x.quantile(0.25), q75=lambda x: x.quantile(0.75))
print("=== Health score distribution per tier ===")
print(dist.round(2))
print()

# 2. Performance category composition per tier
comp = ov_df.groupby(['organization_size_category','performance_category']).size().unstack(fill_value=0)
comp_pct = comp.div(comp.sum(axis=1), axis=0) * 100
print("=== Performance category composition (% of orgs per tier) ===")
print(comp_pct.round(1))
print()
print(comp)

# 3. Management ratio stats per tier
mr = ov_df.groupby('organization_size_category')['management_ratio'].agg(['count','mean','std','min','max'])
print("=== Management ratio stats per tier ===")
print(mr.round(3))