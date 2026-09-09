SELECT interview_name, COUNT(*) as cnt,
       AVG(duration_interview_minutes) as avg_duration,
       ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes','strong yes','yes') THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*),0), 1) as positive_pct
FROM greenhouse__interview_enhanced
GROUP BY interview_name
ORDER BY cnt DESC