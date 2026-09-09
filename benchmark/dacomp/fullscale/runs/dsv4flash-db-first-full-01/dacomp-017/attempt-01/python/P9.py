import pandas as pd
import numpy as np
import json

result = db.query("""
SELECT "Product", "Quantity", Sales, profit, "Discount", "Shipping Cost"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
""")
rows = db.rows(result)
hf = pd.DataFrame(rows, columns=['Product', 'Quantity', 'Sales', 'profit', 'Discount', 'Shipping Cost'])
hf['Quantity'] = pd.to_numeric(hf['Quantity'])
hf['Discount'] = pd.to_numeric(hf['Discount'])

# Check how profit relates to Sales, Quantity, Discount
hf['margin'] = hf['profit'] / hf['Sales']
hf['sales_per_qty'] = hf['Sales'] / hf['Quantity']
hf['discount'] = hf['Discount']

# Group by product and quantity: check profit patterns
print("=== Sofa Covers: profit vs discount, quantity ===")
sc = hf[hf['Product'] == 'Sofa Covers'].groupby(['Quantity', 'discount']).agg(
    profit=('profit', 'first'), sales=('Sales', 'first'), margin=('margin', 'first')).reset_index()
print(sc.head(15))

# Hypothesis: profit = Sales * (base - discount * k) where base,k depend on product and quantity?
# Check within product+quantity, does profit vary with discount linearly?
print("\n=== Check margin vs discount for each product/qty ===")
for (prod, qty), g in hf.groupby(['Product', 'Quantity']):
    if len(g) < 3:
        continue
    # unique discounts and margins
    u = g.groupby('discount')['margin'].mean().sort_index()
    if len(u) >= 3:
        slopes = np.polyfit(u.index, u.values, 1)
        if abs(slopes[0]) > 0.001:
            print(f"{prod}, qty={qty}: margin_by_discount={u.round(4).to_dict()}, slope={slopes[0]:.3f}")

print("\n=== For Beds & Umbrellas, does margin depend on discount? ===")
for prod in ['Beds', 'Umbrellas']:
    g = hf[hf['Product'] == prod]
    u = g.groupby(['Quantity', 'discount'])['margin'].mean().reset_index()
    print(prod)
    print(u.round(4).head(15))

# Overall: try profit = Sales * (a0 + a1*qty + a2*discount)
import numpy as np
X = hf[['Quantity', 'discount']].values
y = hf['margin'].values
# Linear regression with product dummies
import statsmodels.api as sm
X_dum = pd.get_dummies(hf['Product'], prefix='P', drop_first=True).astype(float)
X_full = pd.concat([hf[['Quantity', 'discount']], X_dum], axis=1)
X_full = sm.add_constant(X_full)
model = sm.OLS(hf['margin'], X_full).fit()
print("\n=== OLS: margin ~ Quantity + Discount + Product dummies ===")
print(model.params.round(4))
print("R2:", round(model.rsquared, 4))