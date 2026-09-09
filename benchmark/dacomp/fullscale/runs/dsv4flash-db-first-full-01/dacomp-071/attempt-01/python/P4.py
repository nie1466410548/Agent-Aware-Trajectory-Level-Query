import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, valid_from, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from
"""))
df['row_num'] = df.groupby('opportunity_id').cumcount()
df['n_rows'] = df.groupby('opportunity_id')['opportunity_id'].transform('count')

# Show a few opportunities with 4+ rows to see reason patterns
multi = df[df['n_rows'] >= 4].head(20)
print(multi.to_string())
