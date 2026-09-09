
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load per-product sales + repurchase data (products with >=5 customers)
res = db.query("""
WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code" AS product, s.total_sales, s.n_transactions,
       ps.n_customers, ps.repeat_customers,
       1.0 * ps.repeat_customers / NULLIF(ps.n_customers,0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
""")
df = db.frame(res)
print("Products (>=5 customers):", len(df))
print(df[['product','total_sales','n_transactions','n_customers','repeat_customers','repurchase_rate']].head())

# Correlation between repurchase rate and total sales
for col in ['total_sales', 'n_transactions', 'n_customers']:
    r_p, p_p = stats.pearsonr(df[col], df['repurchase_rate'])
    r_s, p_s = stats.spearmanr(df[col], df['repurchase_rate'])
    print(f"{col} vs repurchase_rate: Pearson r={r_p:.4f} (p={p_p:.2e}), Spearman rho={r_s:.4f} (p={p_s:.2e})")

# Log-scaled correlation too (sales are highly skewed)
df['log_sales'] = np.log10(df['total_sales'].clip(lower=1e-6))
r_p, p_p = stats.pearsonr(df['log_sales'], df['repurchase_rate'])
r_s, p_s = stats.spearmanr(df['log_sales'], df['repurchase_rate'])
print(f"log10(total_sales) vs repurchase_rate: Pearson r={r_p:.4f} (p={p_p:.2e}), Spearman rho={r_s:.4f} (p={p_s:.2e})")
