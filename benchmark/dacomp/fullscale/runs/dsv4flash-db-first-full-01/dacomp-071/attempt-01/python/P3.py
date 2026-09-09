import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, valid_from, valid_ending_at, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from
"""))

# order stages by stage_id
df = df.sort_values(['opportunity_id','valid_from','stage_id']).reset_index(drop=True)
# does the opportunity have a later record after this row?
df['has_later'] = df.groupby('opportunity_id').cumcount() < (df.groupby('opportunity_id)')['opportunity_id'].transform('count')-1) if False else None

# simpler: within each opportunity, rows are ordered; has_next = not last row
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

pass_like = df['archive_reason'].isin(['Advanced to next stage','Qualified','Proceeding','Hired'])
cross = pd.crosstab(df['has_next'], pass_like)
print("has_next vs pass-like reason:")
print(cross)

# Check rows where has_next is True but reason not pass-like
mismatch1 = df[(df['has_next']) & (~pass_like)]
print("\nrows with a later stage but non-pass reason:", len(mismatch1))
print(mismatch1['archive_reason'].value_counts().head(10))
# and rows where has_next False but pass-like reason (last stage with pass reason) - likely in-progress or hired
mismatch2 = df[(~df['has_next']) & (pass_like)]
print("\nrows last-stage but pass-like reason:", len(mismatch2))
print(mismatch2['archive_reason'].value_counts().head(10))
