import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df = df.sort_values(['opportunity_id','stage_id']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

pass_like = df['archive_reason'].isin(['Advanced to next stage','Qualified','Proceeding','Hired'])
cross = pd.crosstab(df['has_next'], pass_like)
print("has_next (by stage order) vs pass-like reason:")
print(cross)

# rows with has_next True but non-pass reason
m1 = df[(df['has_next']) & (~pass_like)]
print("\nrows with later stage in order but non-pass reason:", len(m1))
print(m1['archive_reason'].value_counts().head())

# last-stage rows (terminal) with pass-like reason
m2 = df[(~df['has_next']) & (pass_like)]
print("\nterminal rows with pass-like reason:", len(m2))
print(m2['archive_reason'].value_counts())

# Check terminal rows by stage
print("\nTerminal stage distribution:")
print(df[~df['has_next']]['stage'].value_counts())
