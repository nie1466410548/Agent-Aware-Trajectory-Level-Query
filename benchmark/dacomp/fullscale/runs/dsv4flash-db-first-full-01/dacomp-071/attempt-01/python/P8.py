import pandas as pd
df = db.frame(db.query("""
SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
"""))
df['stage_num'] = df['stage_id'].str.extract(r'(\d+)').astype(int)
opp_max = df.groupby('opportunity_id')['stage_num'].max().reset_index()
opp_max.columns = ['opportunity_id', 'max_stage_num']

# Check Hired stage opportunities
hired_opps = df[df['stage'] == 'Hired']['opportunity_id'].unique()
print("Hired opps max_stage_num:")
print(opp_max[opp_max['opportunity_id'].isin(hired_opps)].head(10))
print("Count:", len(hired_opps))
print()
# Check if max_stage_num == 10 for these
print("All hired opps have max_stage_num=10?", 
      (opp_max[opp_max['opportunity_id'].isin(hired_opps)]['max_stage_num'] == 10).all())

# Debug the full computation
df2 = df.merge(opp_max, on='opportunity_id')
hired_grp = df2[df2['stage'] == 'Hired']
print("\nHired stage group size:", len(hired_grp))
terminal_hired = hired_grp[hired_grp['max_stage_num'] == 10]
print("Terminal at Hired:", len(terminal_hired))
print("archive_reason values:", terminal_hired['archive_reason'].value_counts().to_dict())