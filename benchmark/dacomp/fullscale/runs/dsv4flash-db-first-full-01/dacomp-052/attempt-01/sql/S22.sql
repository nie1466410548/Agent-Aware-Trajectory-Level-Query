WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT team_strengths, COUNT(*) AS n
FROM target GROUP BY team_strengths ORDER BY n DESC