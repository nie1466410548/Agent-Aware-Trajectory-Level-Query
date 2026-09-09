import pandas as pd
import numpy as np

# Analyze interviewer background alignment impact
# Query interview data with job departments and get outcome
int_align_sql = """
SELECT ie.application_id, ie.interviewer_name, ie.job_title, 
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation, ie.interviewer_is_hiring_manager,
       ae.status as app_status, ae.job_parent_departments as app_job_depts
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.job_parent_departments IS NOT NULL
"""
int_df = db.frame(db.query(int_align_sql))
print(f"Total interview records with dept data: {len(int_df)}")
print(int_df.head(10).to_string())

# Check if interviewer name appears in hiring_managers field
# Or if the job_parent_departments of the interviewer align with the application
# Let's get a sample of the data
print("\nUnique overall_recommendation values:", int_df['overall_recommendation'].unique())

# Normalize recommendation
def normalize_rec(r):
    if r is None:
        return 'Unknown'
    r = str(r).lower()
    if r in ['strong_yes', 'strong yes', 'yes']:
        return 'Positive'
    elif r in ['strong_no', 'strong no', 'no']:
        return 'Negative'
    elif r == 'maybe':
        return 'Maybe'
    return 'Other'

int_df['rec_norm'] = int_df['overall_recommendation'].apply(normalize_rec)
print("\nRecommendation distribution:")
print(int_df['rec_norm'].value_counts())

# Since we can't easily match interviewer names to departments,
# let's look at the relationship between interview type and outcomes
# Different interview types may have different levels of alignment

# Let's also check if there's a relationship between interview duration and positive outcome
int_dur_sql = """
SELECT ie.overall_recommendation, ie.duration_interview_minutes,
       ie.interview_name, ie.job_parent_departments,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.duration_interview_minutes IS NOT NULL
"""
dur_df = db.frame(db.query(int_dur_sql))
dur_df['rec_norm'] = dur_df['overall_recommendation'].apply(normalize_rec)
print("\nDuration by recommendation:")
print(dur_df.groupby('rec_norm')['duration_interview_minutes'].describe())

# Final Interview has highest positive rate (47.5%) and longest duration (67 min)
# Technical Interview: 45.3% positive, 64 min
# Panel Interview: 44.3% positive, 62 min
# Behavioral Interview: 43.2% positive, 65 min

# Let's analyze the retention rate at each stage
# From the current_job_stage distribution, we can see the pipeline

# Stage-wise retention analysis
stage_sql = """
SELECT current_job_stage,
  COUNT(*) as total,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
  SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
  SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
  SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY 
  CASE current_job_stage
    WHEN 'Application Review' THEN 1
    WHEN 'Phone Screen' THEN 2
    WHEN 'Technical Interview' THEN 3
    WHEN 'Panel Interview' THEN 4
    WHEN 'Final Interview' THEN 5
    WHEN 'Offer' THEN 6
    ELSE 7
  END
"""
stage_df = db.frame(db.query(stage_sql))
stage_df['total'] = stage_df['total'].astype(int)
stage_df['hired'] = stage_df['hired'].astype(int)
stage_df['rejected'] = stage_df['rejected'].astype(int)
stage_df['withdrawn'] = stage_df['withdrawn'].astype(int)
stage_df['active'] = stage_df['active'].astype(int)
stage_df['retention_rate'] = (stage_df['hired'] + stage_df['active']) / stage_df['total'] * 100
stage_df['dropoff_rate'] = (stage_df['rejected'] + stage_df['withdrawn']) / stage_df['total'] * 100
print("\nStage-wise Retention Analysis:")
print(stage_df.to_string())

# Scorecard average rating by interview type
sc_type_sql = """
SELECT scd.interview_name,
  AVG(scd.rating) as avg_rating,
  COUNT(*) as cnt,
  ROUND(SUM(CASE WHEN scd.rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as high_score_pct
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.interview_name IS NOT NULL
GROUP BY scd.interview_name
ORDER BY avg_rating DESC
"""
sc_type_df = db.frame(db.query(sc_type_sql))
print("\nScorecard Ratings by Interview Type:")
print(sc_type_df.to_string())

# Hired rate by interview type for candidates who went through that type
hire_by_int_type_sql = """
SELECT ie.interview_name,
  COUNT(DISTINCT ie.application_id) as candidates,
  SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) as hired,
  ROUND(100.0 * SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) / COUNT(DISTINCT ie.application_id), 1) as hire_rate
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
GROUP BY ie.interview_name
ORDER BY hire_rate DESC
"""
hire_by_int_df = db.frame(db.query(hire_by_int_type_sql))
print("\nHire Rate by Interview Type:")
print(hire_by_int_df.to_string())

print("\n\n=== BACKGROUND ALIGNMENT ANALYSIS COMPLETE ===")