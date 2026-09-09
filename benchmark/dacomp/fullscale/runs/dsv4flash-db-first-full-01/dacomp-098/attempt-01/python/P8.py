import pandas as pd
import numpy as np
import json
from scipy import stats

# Load conversation-level data from the earlier CTE output - re-run the query to get per-conversation data
result = db.query("""
SELECT 
  ce.all_conversation_contacts AS contact_id,
  ce.conversation_id,
  ce.conversation_created_at,
  ce.conversation_initiated_type,
  ce.conversation_subject,
  ce.sla_name,
  ce.sla_status,
  ce.conversation_rating,
  ce.conversation_state,
  ce.all_conversation_tags,
  cm.count_total_parts,
  cm.count_reopens,
  cm.time_to_first_response_minutes,
  CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
  END AS stage,
  CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
  END AS intent
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
""")
conv = db.frame(result)
print(f"Conversations: {len(conv)}")
print(f"Bot first: {(conv['conversation_initiated_type']=='bot_first').sum()}")
print(f"Human first: {(conv['conversation_initiated_type']=='human_first').sum()}")

# ============ Conversation quality metrics ============
print("\n" + "="*70)
print("CONVERSATION-LEVEL QUALITY METRICS BY TYPE")
print("="*70)
for g in ['bot_first','human_first']:
    sub = conv[conv['conversation_initiated_type']==g]
    print(f"\n{g}: n={len(sub)}")
    print(f"  Avg rating:      {sub['conversation_rating'].mean():.3f}")
    print(f"  Avg total parts: {sub['count_total_parts'].mean():.1f}")
    print(f"  Avg reopens:     {sub['count_reopens'].mean():.3f}")
    print(f"  Avg first resp:  {sub['time_to_first_response_minutes'].mean():.1f} min")
    print(f"  SLA met rate:    {(sub['sla_status']=='met').mean()*100:.1f}% (met) / {(sub['sla_status']=='breached').mean()*100:.1f}% breached")
    print(f"  State: {sub['conversation_state'].value_counts().to_dict()}")

# Rating test
rb = conv[conv['conversation_initiated_type']=='bot_first']['conversation_rating'].dropna()
rh = conv[conv['conversation_initiated_type']=='human_first']['conversation_rating'].dropna()
stat, p = stats.mannwhitneyu(rb, rh, alternative='two-sided')
print(f"\n  Rating bot vs human: p={p:.4f}")

# ============ SLA by type ============
print("\n" + "="*70)
print("SLA STATUS DISTRIBUTION BY TYPE")
print("="*70)
print(pd.crosstab(conv['conversation_initiated_type'], conv['sla_status'], normalize='index'))

# ============ Subject distribution ============
print("\n" + "="*70)
print("CONVERSATION SUBJECT BY TYPE")
print("="*70)
print(pd.crosstab(conv['conversation_initiated_type'], conv['conversation_subject'], normalize='index').round(3))

# ============ First-conversation stage distribution by type ============
print("\n" + "="*70)
print("FIRST-CONVERSATION STAGE DISTRIBUTION BY TYPE")
print("="*70)
df = pd.read_csv('/work/contact_funnel.csv')
ct = pd.crosstab(df['first_type'], df['first_stage'], normalize='index')
print(ct.round(3))

print("\n(Counts)")
ct2 = pd.crosstab(df['first_type'], df['first_stage'])
print(ct2)

# ============ Intent distribution in first conversation ============
print("\n" + "="*70)
print("FIRST-CONVERSATION INTENT DISTRIBUTION BY TYPE")
print("="*70)
print(pd.crosstab(df['first_type'], df['intent'], normalize='index').round(3))
print(pd.crosstab(df['first_type'], df['intent']))

# ============ Outcome distribution (max stage) by type ============
print("\n" + "="*70)
print("MAX STAGE REACHED BY TYPE")
print("="*70)
stage_names = {1:'contacted',2:'marketing_qualified',3:'trial_started',4:'demo_booked',5:'trial_activated',6:'proposal_sent',7:'closed_won',8:'expansion_in_flight'}
df['max_stage_name'] = df['max_stage_rank'].map(stage_names)
print(pd.crosstab(df['first_type'], df['max_stage_name'], normalize='index').round(3))
print(pd.crosstab(df['first_type'], df['max_stage_name']))