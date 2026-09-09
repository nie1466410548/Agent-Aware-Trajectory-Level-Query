SELECT COUNT(*) as total_scorecards, 
       SUM(CASE WHEN scorecard_submitted_at IS NOT NULL THEN 1 ELSE 0 END) as submitted,
       ROUND(100.0 * SUM(CASE WHEN scorecard_submitted_at IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) as submission_rate
FROM greenhouse__interview_enhanced