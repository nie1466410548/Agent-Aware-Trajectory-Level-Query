import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
df = df.sort_values(['opportunity_id','stage_num']).reset_index(drop=True)
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')
df['has_next'] = df['row_num'] < df['n_rows'] - 1

proc = df[df['archive_reason'] == 'Proceeding']
print("Proceeding rows:", len(proc))
print(proc.groupby('stage')['opportunity_id'].count().to_string())
print("\nProceeding rows with has_next:", proc['has_next'].value_counts().to_dict())
print("\nProceeding at their terminal stage (last stage reached):")
term_proc = proc[~proc['has_next']]
print(term_proc.groupby('stage').size().to_string())
