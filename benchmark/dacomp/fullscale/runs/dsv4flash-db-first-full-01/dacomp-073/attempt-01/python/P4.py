import pandas as pd
postings = db.frame(db.query("SELECT categories_department, state, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department, state ORDER BY categories_department, state"))
pivot = postings.pivot(index='categories_department', columns='state', values='cnt').fillna(0).astype(int)
pivot['total'] = pivot.sum(axis=1)
print(pivot)