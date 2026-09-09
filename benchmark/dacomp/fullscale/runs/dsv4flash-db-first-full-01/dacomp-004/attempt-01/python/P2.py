import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Figure 1: Monthly performance of top products ---
top_products = ['DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045']
res = db.query("""
SELECT "Sales Month" AS month, "Product Code" AS product, SUM("Sales Amount") AS sales_amount
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY product, month
""")
df_monthly = db.frame(res)
df_monthly['month_str'] = df_monthly['month'].astype(str)
df_monthly['month_ym'] = pd.to_datetime(df_monthly['month_str'], format='%Y%m')

fig, ax = plt.subplots(figsize=(10, 5))
for prod in top_products:
    prod_data = df_monthly[df_monthly['product'] == prod]
    ax.plot(prod_data['month_ym'], prod_data['sales_amount'], marker='o', label=prod)
    # Annotate the peak month
    peak = prod_data.loc[prod_data['sales_amount'].idxmax()]
    ax.annotate(f"Peak: {peak['month_ym'].strftime('%Y-%m')} = {peak['sales_amount']:.0f}",
                xy=(peak['month_ym'], peak['sales_amount']),
                xytext=(10, 10), textcoords='offset points', fontsize=8)
ax.set_xlabel('Month')
ax.set_ylabel('Sales Amount')
ax.set_title('Monthly Sales Performance of Top Products')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('/work/top_products_monthly.png', dpi=150)
plt.close()
print("Saved top_products_monthly.png")

# --- Figure 2: Scatter plot of repurchase rate vs total sales (all products with >=5 customers) ---
res2 = db.query("""
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
  SELECT "Product Code", SUM("Sales Amount") AS total_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s.total_sales, 1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
""")
df2 = db.frame(res2)

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(df2['total_sales'], df2['repurchase_rate'], alpha=0.3, s=5, c='steelblue')

# Log scale for x
ax.set_xscale('log')
ax.set_xlabel('Total Sales Amount (log scale)')
ax.set_ylabel('Customer Repurchase Rate')
ax.set_title('Repurchase Rate vs Total Sales Amount\n(All products with ≥5 customers)')

# Linear regression line on log-x
x_log = np.log10(df2['total_sales'].clip(lower=1e-6))
y = df2['repurchase_rate']
slope, intercept, r_val, p_val, std_err = stats.linregress(x_log, y)
x_line = np.logspace(np.log10(df2['total_sales'].min()), np.log10(df2['total_sales'].max()), 100)
ax.plot(x_line, intercept + slope * np.log10(x_line), 'r--', lw=1.5,
        label=f'Linear fit (r²={r_val**2:.3f}, p={p_val:.2e})')
ax.legend()
plt.tight_layout()
plt.savefig('/work/repurchase_vs_sales_scatter.png', dpi=150)
plt.close()
print("Saved repurchase_vs_sales_scatter.png")

# --- Figure 3: Bar chart of repurchase rates for top products ---
prod_data = [
    ('DW-1001040125', 'Jan 2015 top', 0.1346, 5948.88),
    ('DW-2316020016', 'Feb 2015 top', 0.0, 5600.0),
    ('DW-1203130446', 'Mar 2015 top', 0.2643, 7384.83),
    ('DW-1518040045', 'Apr 2015 top', 0.0588, 1400.30)
]
labels = [f"{p[0]}\n({p[1]})" for p in prod_data]
rates = [p[2] for p in prod_data]
sales = [p[3] for p in prod_data]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
bars1 = ax1.bar(range(len(labels)), rates, color=colors, edgecolor='gray')
ax1.set_xticks(range(len(labels)))
ax1.set_xticklabels(labels, fontsize=8)
ax1.set_ylabel('Customer Repurchase Rate')
ax1.set_title('Repurchase Rate of Top Products')
for bar, rate in zip(bars1, rates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{rate:.2%}', ha='center', fontsize=9)

bars2 = ax2.bar(range(len(labels)), sales, color=colors, edgecolor='gray')
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, fontsize=8)
ax2.set_ylabel('Total Sales Amount')
ax2.set_title('Total Sales (All Months) of Top Products')
for bar, s in zip(bars2, sales):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'${s:.0f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/work/top_products_repurchase_vs_sales.png', dpi=150)
plt.close()
print("Saved top_products_repurchase_vs_sales.png")

print("All figures saved.")