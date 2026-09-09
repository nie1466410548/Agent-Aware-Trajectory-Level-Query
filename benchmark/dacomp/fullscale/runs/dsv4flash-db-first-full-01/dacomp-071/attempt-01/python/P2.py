import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, valid_from, valid_ending_at, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from
"""))
print("rows:", len(df))
print("unique opportunities:", df['opportunity_id'].nunique())
print("duplicate (opp, stage) combos (i.e., >1 record same opp+stage):", 
      (df.groupby(['opportunity_id','stage_id']).size() > 1).sum())

# check if archive_reason is consistent across a given opportunity's rows
g = df.groupby('opportunity_id')['archive_reason'].nunique()
print("opportunities with >1 distinct archive_reason among their rows:", (g > 1).sum())
print("opportunities with exactly 1 archive_reason:", (g == 1).sum())

# count of stage rows per opportunity
h = df.groupby('opportunity_id').size()
print("\nrows per opportunity describe:")
print(h.describe())
print("\nmax rows:", h.max())
