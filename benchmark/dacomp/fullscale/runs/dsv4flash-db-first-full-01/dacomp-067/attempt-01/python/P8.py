import pandas as pd
import numpy as np

# ========== INTERVIEWER SATISFACTION SCORE ANALYSIS ==========

# Method 1: Average rating per scorecard (not per attribute)
sc_avg_sql = """
SELECT scorecard_id, 
       AVG(rating) as avg_scorecard_rating,
       MAX(rating) as max_rating,
       MIN(rating) as min_rating,
       overall_recommendation
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY scorecard_id
"""
sc_avg_df = db.frame(db.query(sc_avg_sql))
print(f"Scorecards with ratings: {len(sc_avg_df)}")
print(f"Average scorecard rating: {sc_avg_df['avg_scorecard_rating'].mean():.2f}")
print(f"Distribution of avg scorecard ratings:")
print(sc_avg_df['avg_scorecard_rating'].describe())

# Method 2: Map overall_recommendation to numeric
rec_map = {
    'strong_no': 1, 'Strong No': 1, 'strong_yes': 5, 'Strong Yes': 5,
    'no': 2, 'No': 2, 'yes': 4, 'Yes': 4, 'Maybe': 3, 'maybe': 3
}
sc_avg_df['rec_score'] = sc_avg_df['overall_recommendation'].map(rec_map)
print(f"\nAverage recommendation score (mapped): {sc_avg_df['rec_score'].mean():.2f}")

# Method 3: Average rating per candidate (application)
app_avg_sql = """
SELECT scd.application_id,
       AVG(scd.rating) as avg_candidate_rating,
       COUNT(scd.scorecard_id) as num_scorecards
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
GROUP BY scd.application_id
"""
app_avg_df = db.frame(db.query(app_avg_sql))
print(f"\nApplications with scorecard ratings: {len(app_avg_df)}")
print(f"Average rating per application: {app_avg_df['avg_candidate_rating'].mean():.2f}")
print(f"Distribution:")
print(app_avg_df['avg_candidate_rating'].describe())

# Method 4: Average rating per interview (from interview_enhanced)
# Maybe the interviewer satisfaction is the average rating across all attributes
# Let's check the overall average
all_ratings_sql = "SELECT AVG(rating) as avg_all FROM greenhouse__interview_scorecard_detail WHERE rating IS NOT NULL"
all_ratings_df = db.frame(db.query(all_ratings_sql))
print(f"\nOverall average rating across all scorecard attributes: {all_ratings_df['avg_all'].iloc[0]:.2f}")

# Method 5: Check if there's a different score in candidate_summary
cs_sql = "SELECT AVG(avg_interview_score) as avg FROM greenhouse__candidate_summary WHERE avg_interview_score IS NOT NULL"
cs_df = db.frame(db.query(cs_sql))
print(f"\nAverage interview score from candidate_summary: {cs_df['avg'].iloc[0]:.2f}")

# Method 6: Check job_enhanced for avg_job_rating
je_sql = "SELECT AVG(avg_job_rating) as avg FROM greenhouse__job_enhanced WHERE avg_job_rating IS NOT NULL"
je_df = db.frame(db.query(je_sql))
print(f"\nAverage job rating from job_enhanced: {je_df['avg'].iloc[0]:.2f}")

# Let's also check the distribution of scorecard ratings more carefully
rating_dist_sql = """
SELECT rating, COUNT(*) as cnt
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating
"""
rating_dist_df = db.frame(db.query(rating_dist_sql))
print("\nRating distribution:")
print(rating_dist_df.to_string())

# The average of 2.70 is well below 4.0
# Let's see if there's a "satisfaction" metric we can compute
# Maybe the overall_recommendation mapped to numeric gives us a better measure
rec_scores_sql = """
SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes', 'strong yes') THEN 5
    WHEN lower(overall_recommendation) IN ('yes') THEN 4
    WHEN lower(overall_recommendation) IN ('maybe') THEN 3
    WHEN lower(overall_recommendation) IN ('no') THEN 2
    WHEN lower(overall_recommendation) IN ('strong_no', 'strong no') THEN 1
    ELSE NULL
  END as rec_score,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_score
ORDER BY rec_score
"""
rec_scores_df = db.frame(db.query(rec_scores_sql))
print("\nRecommendation score distribution:")
print(rec_scores_df.to_string())
weighted_avg = (rec_scores_df['rec_score'] * rec_scores_df['cnt']).sum() / rec_scores_df['cnt'].sum()
print(f"Weighted average recommendation score: {weighted_avg:.2f}")

# So the interviewer satisfaction is around 2.70-3.30 depending on metric
# This is below 4.0. The task says "maintaining above 4.0" - maybe it's already >4.0
# Let me think about what "interviewer satisfaction" could mean
# Perhaps it's the percentage of positive recommendations?
pos_pct = 4353 / (4353 + 4369 + 937) * 100
print(f"\nPositive recommendation rate: {pos_pct:.1f}%")
# Or maybe it's computed differently

print("\n\n=== SATISFACTION ANALYSIS COMPLETE ===")