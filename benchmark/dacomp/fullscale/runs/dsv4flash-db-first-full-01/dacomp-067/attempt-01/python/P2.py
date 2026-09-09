import pandas as pd
import numpy as np
import json

# Analyze stage-level conversion funnel using current_job_stage as a proxy for pipeline position
stage_sql = """
SELECT current_job_stage,
       COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
       SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
       SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY cnt DESC
"""
stage_df = db.frame(db.query(stage_sql))
print("Pipeline by current stage:")
print(stage_df.to_string())

# Applications with interviews vs hired - conversion by channel from application table
conv_sql = """
SELECT sourced_from,
  COUNT(*) as apps,
  SUM(CASE WHEN count_interviews>0 THEN 1 ELSE 0 END) as interviewed,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced
GROUP BY sourced_from
"""
conv_df = db.frame(db.query(conv_sql))
conv_df['app_to_int'] = conv_df['interviewed']/conv_df['apps']*100
conv_df['int_to_hire'] = conv_df['hired']/conv_df['interviewed']*100
conv_df['overall_conv'] = conv_df['hired']/conv_df['apps']*100
print("\nConversion funnel by channel (application-level):")
print(conv_df.to_string())

# Scorecard detail joined with hiring outcome
sc_sql = """
SELECT scd.attribute_name, scd.rating, scd.overall_recommendation,
       scd.interview_name, scd.job_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
LIMIT 1000
"""
sc_df = db.frame(db.query(sc_sql))
print("\nScorecard sample:")
print(sc_df.head().to_string())
print("App status values:", sc_df['app_status'].value_counts().to_dict())

# Gender + race diversity by department
div_dept_sql = """
SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept,
  SUM(CASE WHEN status='hired' AND candidate_gender='Female' THEN 1 ELSE 0 END) as fh,
  SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END) as th_g,
  SUM(CASE WHEN status='hired' AND candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as nwh,
  SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as th_r
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept
ORDER BY th_g DESC
"""
div_dept_df = db.frame(db.query(div_dept_sql))
div_dept_df['female_pct'] = (div_dept_df['fh']/div_dept_df['th_g']*100).round(1)
div_dept_df['nonwhite_pct'] = (div_dept_df['nwh']/div_dept_df['th_r']*100).round(1)
print("\nDiversity by department:")
print(div_dept_df.to_string())

# Save intermediate data
os.makedirs('/work', exist_ok=True) if not os.path.exists('/work') else None