import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_json('/work/promo_full.json', orient='records')

for cat in ['Meat', 'Snack Food', 'Daily Delivery/Refrigerated', 'Fruits/Vegetables', 'Daily Chemical Products']:
    sub = df[df['cat_name'] == cat]
    r_dd_sales, _ = stats.pearsonr(sub['discount_depth'], sub['sale_count'])
    r_dd_price, _ = stats.pearsonr(sub['discount_depth'], sub['promotion_price'])
    r_price_sales, _ = stats.pearsonr(sub['promotion_price'], sub['sale_count'])
    # Partial correlation: discount depth vs sales controlling for price
    from scipy.stats import pearsonr
    def partial_corr(x, y, z):
        rx = pearsonr(x, z)[0]; ry = pearsonr(y, z)[0]; rxy = pearsonr(x, y)[0]
        return (rxy - rx*ry) / np.sqrt((1-rx**2)*(1-ry**2))
    pc = partial_corr(sub['discount_depth'], sub['sale_count'], sub['promotion_price'])
    print(f"{cat}: n={len(sub)}, r(dd,sales)={r_dd_sales:.3f}, r(dd,price)={r_dd_price:.3f}, r(price,sales)={r_price_sales:.3f}, partial r(dd,sales|price)={pc:.3f}")

# Also check avg promo price by discount bin for Meat vs Snack
for cat in ['Meat', 'Snack Food']:
    sub = df[df['cat_name'] == cat].copy()
    sub['dd_bin'] = pd.cut(sub['discount_depth'], bins=[0,0.2,0.3,0.4,1.0], labels=['<20%','20-30%','30-40%','>40%'])
    print(f"\n{cat} avg promo price by bin:")
    print(sub.groupby('dd_bin', observed=True)['promotion_price'].agg(['mean','count']).round(1))