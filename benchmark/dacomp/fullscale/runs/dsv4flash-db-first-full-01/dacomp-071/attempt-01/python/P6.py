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
m1 = df[(df['has_next']) & (~pass_like)]
print("Inconsistent (non-pass reason but later stage) rows by stage:")
print(m1.groupby('stage')['archive_reason'].value_counts().to_string())

# Show a couple of examples
print("\nExample inconsistent opportunities:")
ex = m1['opportunity_id'].unique()[:5]
print(df[df['opportunity_id'].isin(ex)].to_string())
