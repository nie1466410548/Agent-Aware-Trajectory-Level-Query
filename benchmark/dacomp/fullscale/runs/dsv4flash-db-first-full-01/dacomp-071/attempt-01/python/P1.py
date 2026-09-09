import pandas as pd

df = db.frame(db.query("""
SELECT stage_id, stage, archive_reason, COUNT(*) as cnt
FROM lever__opportunity_stage_history
GROUP BY stage_id, stage, archive_reason
ORDER BY stage_id, cnt DESC
"""))

# Pivot to see reason distribution per stage
pv = df.pivot_table(index='archive_reason', columns='stage', values='cnt', aggfunc='sum', fill_value=0)
print("Full archive_reason list:")
print(df.groupby('archive_reason')['cnt'].sum().sort_values(ascending=False))
print("\nCross-tab stage x reason:")
print(pv)
