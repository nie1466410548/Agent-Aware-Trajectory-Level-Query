result = db.query("SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department, substr(created_at, 1, 7) ORDER BY categories_department, ym")
df = db.frame(result)
print(df)