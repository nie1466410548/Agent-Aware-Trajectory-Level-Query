
import numpy as np, pandas as pd

# Pull company metrics (revenue, input, profit margin, concentration) via logged db query
metrics_sql = """
WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
cust_conc AS (
  SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share
  FROM cust c JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON c.code = t.code
  GROUP BY c.code
),
supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
supp_conc AS (
  SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share
  FROM supp s JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON s.code = t.code
  GROUP BY s.code
)
SELECT ci."Enterprise Code" AS code, ci."Company Name", ci."Credit Rating" AS rating, ci."Defaulted" AS defaulted,
       COALESCE(rev.total_revenue, 0) AS total_revenue,
       COALESCE(inp.total_input, 0) AS total_input,
       COALESCE(cust_conc.top1_buyer_share, 0) AS top1_buyer,
       COALESCE(supp_conc.top1_supplier_share, 0) AS top1_supplier
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
LEFT JOIN cust_conc ON ci."Enterprise Code" = cust_conc.code
LEFT JOIN supp_conc ON ci."Enterprise Code" = supp_conc.code
"""
res = db.query(metrics_sql)
df = db.frame(res)

# Yearly revenue for CV (profit stability)
yr_sql = """
SELECT "Enterprise Code" AS code, strftime('%Y', "Invoice Date") AS yr, SUM("Amount Including Tax") AS rev
FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice'
GROUP BY "Enterprise Code", yr
"""
yr = db.frame(db.query(yr_sql))
df_y = yr.merge(df[['code']], on='code')
st = df_y.groupby('code')['rev'].agg(['mean','std','count']).rename(columns={'count':'n_years'})
st['cv'] = st['std']/st['mean'].replace(0, np.nan)
st = st.replace([np.inf, -np.inf], np.nan)
df = df.merge(st[['n_years','cv']], left_on='code', right_index=True, how='left')

df['profit'] = df['total_revenue'] - df['total_input']
df['margin'] = np.where(df['total_revenue']>0, df['profit']/df['total_revenue'], 0)
df['defaulted_flag'] = (df['defaulted']=='Yes').astype(int)
df.to_csv('/work/company_metrics.csv', index=False)
print(df.shape)
print(df.groupby('rating')[['defaulted_flag','total_revenue','margin','top1_buyer','top1_supplier','cv']].agg(['mean','median']))
