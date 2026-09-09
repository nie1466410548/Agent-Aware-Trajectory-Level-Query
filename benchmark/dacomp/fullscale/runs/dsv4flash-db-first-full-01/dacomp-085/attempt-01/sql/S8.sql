SELECT job_value_tier, talent_competition_level, COUNT(*) AS cnt
FROM workday__job_overview
GROUP BY job_value_tier, talent_competition_level
ORDER BY job_value_tier, cnt DESC