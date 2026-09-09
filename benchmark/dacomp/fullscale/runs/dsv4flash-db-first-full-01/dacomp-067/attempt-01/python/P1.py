import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os

# Load data from database using Python
# First, let's get the channel performance data
# Channel data from talent_pipeline_simplified
channels_sql = """
SELECT source_name, source_type, total_applications, unique_candidates, 
       total_hires, applications_with_interviews, avg_process_days,
       hire_rate, interview_rate, interview_to_hire_rate, efficiency_score
FROM greenhouse__talent_pipeline_simplified
ORDER BY source_name
"""
channels_result = db.query(channels_sql)
channels_df = db.frame(channels_result)
print("Channel data:")
print(channels_df.to_string())

# Department-level data from application_enhanced
dept_sql = """
SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept_group,
  COUNT(*) as applications,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
  AVG(count_interviews) as avg_interviews
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept_group
ORDER BY hires DESC
"""
dept_result = db.query(dept_sql)
dept_df = db.frame(dept_result)
print("\nDepartment data:")
print(dept_df.to_string())

# Source-specific hire data
source_hire_sql = """
SELECT sourced_from,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  COUNT(*) as applications,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
GROUP BY sourced_from
ORDER BY hires DESC
"""
source_hire_result = db.query(source_hire_sql)
source_hire_df = db.frame(source_hire_result)
print("\nSource hire data:")
print(source_hire_df.to_string())

# Interview recommendation analysis
interview_sql = """
SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 'Positive'
    WHEN lower(overall_recommendation) IN ('strong_no','no','maybe') THEN 'Non-Positive'
    ELSE 'Other'
  END as rec_group,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_group
"""
interview_result = db.query(interview_sql)
interview_df = db.frame(interview_result)
print("\nInterview recommendation data:")
print(interview_df.to_string())

# Interviewer satisfaction - by interview type
int_type_sql = """
SELECT interview_name,
  COUNT(*) as total,
  ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as positive_pct,
  AVG(duration_interview_minutes) as avg_duration
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY interview_name
ORDER BY total DESC
"""
int_type_result = db.query(int_type_sql)
int_type_df = db.frame(int_type_result)
print("\nInterview type data:")
print(int_type_df.to_string())

# Scorecard ratings by attribute
scorecard_sql = """
SELECT attribute_name, 
  COUNT(*) as cnt,
  AVG(rating) as avg_rating
FROM greenhouse__interview_scorecard_detail
WHERE attribute_name IS NOT NULL AND rating IS NOT NULL
GROUP BY attribute_name
ORDER BY avg_rating DESC
"""
scorecard_result = db.query(scorecard_sql)
scorecard_df = db.frame(scorecard_result)
print("\nScorecard data:")
print(scorecard_df.to_string())

# Diversity metrics
div_result = db.query("SELECT * FROM greenhouse__diversity_metrics")
div_df = db.frame(div_result)
print("\nDiversity metrics:")
print(div_df.to_string())

print("\n\n=== DATA ANALYSIS COMPLETE ===")