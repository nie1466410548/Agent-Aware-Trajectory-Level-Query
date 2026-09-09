import pandas as pd
import numpy as np
import re

# ========== INTERVIEWER BACKGROUND ALIGNMENT ANALYSIS ==========
# Check if interviewer comes from the same department as the job
# Query interview data with relevant fields
align_sql = """
SELECT ie.application_id, ie.interviewer_name, ie.job_title,
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation,
       ie.interview_name,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
LEFT JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL
"""
align_df = db.frame(db.query(align_sql))
print(f"Total aligned-interview records: {len(align_df)}")

# The interviewer's job title may indicate their department
# Let's check if the interviewer's title contains department keywords
# e.g., "Principal Engineer" -> Engineering, "UX Designer" -> Design
def infer_interviewer_dept(title):
    if pd.isna(title):
        return None
    t = title.lower()
    if 'engineer' in t or 'developer' in t or 'architect' in t:
        return 'Engineering'
    elif 'product' in t or 'pm' in t:
        return 'Product'
    elif 'design' in t or 'ux' in t or 'ui' in t:
        return 'Design'
    elif 'marketing' in t or 'growth' in t:
        return 'Marketing'
    elif 'sales' in t or 'account' in t or 'business' in t:
        return 'Sales'
    elif 'customer' in t or 'support' in t:
        return 'Customer'
    elif 'hr' in t or 'people' in t or 'recruit' in t:
        return 'HR'
    elif 'finance' in t or 'account' in t:
        return 'Finance'
    elif 'data' in t or 'analyst' in t:
        return 'Data'
    elif 'manager' in t or 'director' in t or 'lead' in t or 'chief' in t or 'head' in t:
        return 'Management'
    else:
        return 'Other'

align_df['interviewer_dept'] = align_df['job_title'].apply(infer_interviewer_dept)
print("\nInterviewer inferred department distribution:")
print(align_df['interviewer_dept'].value_counts())

# For candidates where we have job parent departments, check alignment
# We'll look at applications where both interviewer dept and job dept are available
job_dept_map = {
    'Engineering': 'Engineering',
    'Product': 'Product',
    'Design': 'Design',
    'Marketing': 'Marketing',
    'Sales': 'Sales'
}

def check_alignment(row):
    iv_dept = row['interviewer_dept']
    if iv_dept not in job_dept_map:
        return None
    if pd.isna(row['job_depts']):
        return None
    # Check if interviewer dept appears in job parent departments
    return 1 if job_dept_map[iv_dept] in str(row['job_depts']) else 0

align_df['aligned'] = align_df.apply(check_alignment, axis=1)
aligned_subset = align_df[align_df['aligned'].notna()].copy()
print(f"\nRecords with alignment info: {len(aligned_subset)}")
print(f"Aligned (same dept): {aligned_subset['aligned'].sum()}")
print(f"Not aligned: {(aligned_subset['aligned']==0).sum()}")

# Normalize recommendation
def norm_rec(r):
    if pd.isna(r):
        return None
    r = str(r).lower()
    if r in ('strong_yes', 'strong yes', 'yes'):
        return 'Positive'
    elif r in ('strong_no', 'strong no', 'no'):
        return 'Negative'
    elif r == 'maybe':
        return 'Maybe'
    return 'Other'

aligned_subset['rec_norm'] = aligned_subset['overall_recommendation'].apply(norm_rec)

# Compare recommendation distribution between aligned and non-aligned
print("\nRecommendation distribution by interviewer-job alignment:")
pivot = pd.crosstab(aligned_subset['aligned'], aligned_subset['rec_norm'], normalize='index') * 100
print(pivot.round(1))
print("\nCounts:")
print(pd.crosstab(aligned_subset['aligned'], aligned_subset['rec_norm']))

# Hired outcome by alignment
print("\nHire outcome by alignment:")
print(pd.crosstab(aligned_subset['aligned'], aligned_subset['app_status'], normalize='index').round(3))

# ========== SCORECARD OUTCOME ANALYSIS ==========
# Relationship between scorecard rating and final outcome
sc_out_sql = """
SELECT scd.scorecard_id, scd.rating, scd.attribute_name,
       scd.overall_recommendation, scd.interview_name, scd.application_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.overall_recommendation IS NOT NULL
"""
sc_out_df = db.frame(db.query(sc_out_sql))
print(f"\nScorecard records: {len(sc_out_df)}")

sc_out_df['rec_norm'] = sc_out_df['overall_recommendation'].apply(norm_rec)
print("\nAvg rating by recommendation:")
print(sc_out_df.groupby('rec_norm')['rating'].mean().round(3))

print("\nAvg rating by final application status:")
print(sc_out_df.groupby('app_status')['rating'].mean().round(3))

# Scorecard rating correlation with hire outcome
print("\nScorecard high-rating (>=4) share by status:")
sc_out_df['high_rating'] = (sc_out_df['rating'] >= 4).astype(int)
print(sc_out_df.groupby('app_status')['high_rating'].mean().round(3))

print("\n\n=== BACKGROUND ALIGNMENT ANALYSIS COMPLETE ===")