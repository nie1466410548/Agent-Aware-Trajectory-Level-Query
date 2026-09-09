import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_json('/work/promo_data.json', orient='records')

# Per-category analysis
cats = df['cat_name'].value_counts().index
results = []
for cat in cats:
    sub = df[df['cat_name'] == cat].copy()
    n = len(sub)
    total_sales = int(sub['sale_count'].sum())
    avg_sales = sub['sale_count'].mean()
    med_sales = sub['sale_count'].median()
    avg_dd = sub['discount_depth'].mean()
    std_dd = sub['discount_depth'].std()
    
    # Correlation
    r_p, p_p = stats.pearsonr(sub['discount_depth'], sub['sale_count'])
    r_s, p_s = stats.spearmanr(sub['discount_depth'], sub['sale_count'])
    
    # Linear regression: sales ~ discount_depth
    slope, intercept, r_val, p_val, stderr = stats.linregress(sub['discount_depth'], sub['sale_count'])
    
    # Sales per discount point (elasticity proxy)
    results.append({
        'category': cat,
        'n_promos': n,
        'total_sales': total_sales,
        'avg_sales': round(avg_sales, 2),
        'med_sales': med_sales,
        'avg_dd': round(avg_dd, 4),
        'std_dd': round(std_dd, 4),
        'pearson_r': round(r_p, 4),
        'pearson_p': p_p,
        'spearman_r': round(r_s, 4),
        'spearman_p': p_s,
        'reg_slope': round(slope, 4),
        'reg_intercept': round(intercept, 2),
        'reg_r2': round(r_val**2, 4)
    })

res_df = pd.DataFrame(results)
res_df = res_df.sort_values('total_sales', ascending=False)
print(res_df.to_string())
res_df.to_csv('/work/category_results.csv', index=False)
print("\nSaved.")