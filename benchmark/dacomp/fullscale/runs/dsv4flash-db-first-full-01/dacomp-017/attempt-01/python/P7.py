import pandas as pd
import numpy as np
import json

result2 = db.query("""
SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows2 = db.rows(result2)
hf = pd.DataFrame(rows2, columns=['yr', 'Product', 'Quantity', 'Sales', 'profit'])
hf['Quantity'] = pd.to_numeric(hf['Quantity'])
print(hf.dtypes)
print(hf['yr'].unique())
print(hf.head())