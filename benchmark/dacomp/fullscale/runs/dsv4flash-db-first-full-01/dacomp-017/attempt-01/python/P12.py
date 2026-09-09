import pandas as pd
import numpy as np
import json

result = db.query("""
SELECT "Product", "Quantity", "Discount", Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' 
  AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
""")
rows = db.rows(result)
hf = pd.DataFrame(rows, columns=['Product', 'Quantity', 'Discount', 'Sales', 'profit'])
hf['Quantity'] = pd.to_numeric(hf['Quantity'])
hf['Discount'] = pd.to_numeric(hf['Discount'])
hf['Margin'] = hf['profit'] / hf['Sales']

# For the majority of products, test margin ~ a + b1*qty + b2*discount with product dummies
X = pd.get_dummies(hf['Product'], drop_first=True).astype(float)
X['Quantity'] = hf['Quantity']
X['Discount'] = hf['Discount']
X['Qty_x_Discount'] = hf['Quantity'] * hf['Discount']
X['const'] = 1.0
y = hf['Margin'].values

A = X.values
coef, res, rank, sv = np.linalg.lstsq(A, y, rcond=None)
pred = A @ coef
ss_res = np.sum((y - pred)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
print(f"R2 of linear model (margin ~ products + qty + discount + qty*discount): {r2:.4f}")

# Focus on the qty*discount interaction coefficient
names = list(X.columns)
qdx_idx = names.index('Qty_x_Discount')
print(f"Coefficient for Qty x Discount: {coef[qdx_idx]:.3f}")
print(f"Coefficient for Quantity: {coef[names.index('Quantity')]:.3f}")
print(f"Coefficient for Discount: {coef[names.index('Discount')]:.3f}")

# Simpler: within each product, regress margin on quantity and discount separately
print("\n=== Per-product regression: margin ~ qty + discount ===")
summary = []
for prod, g in hf.groupby('Product'):
    if g['Discount'].nunique() < 3 or len(g) < 10:
        continue
    Xp = np.column_stack([np.ones(len(g)), g['Quantity'], g['Discount']])
    c, *_ = np.linalg.lstsq(Xp, g['Margin'].values, rcond=None)
    predp = Xp @ c
    r2p = 1 - np.sum((g['Margin'] - predp)**2)/np.sum((g['Margin'] - g['Margin'].mean())**2)
    summary.append({'Product': prod, 'intercept': round(c[0],4), 'qty_coef': round(c[1],4), 'disc_coef': round(c[2],4), 'R2': round(r2p,4)})
    
sdf = pd.DataFrame(summary)
print(sdf.to_string(index=False))

# correlation of margin with quantity overall and within product
print("\nOverall corr(margin, qty):", np.corrcoef(hf['Margin'], hf['Quantity'])[0,1].round(4))
print("Overall corr(margin, qty*discount):", np.corrcoef(hf['Margin'], hf['Quantity']*hf['Discount'])[0,1].round(4))

# Key numbers for report
print("\n=== Summary numbers for report ===")
cat_yr = db.query("""
SELECT "Product Category", substr("Order Date",1,4) AS yr,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
""")
rows_cy = db.rows(cat_yr)
cy = pd.DataFrame(rows_cy, columns=['Category', 'Year', 'Margin'])
swing = cy.groupby('Category')['Margin'].agg(lambda s: s.max() - s.min()).round(4)
print("Category margin swings:")
print(swing)