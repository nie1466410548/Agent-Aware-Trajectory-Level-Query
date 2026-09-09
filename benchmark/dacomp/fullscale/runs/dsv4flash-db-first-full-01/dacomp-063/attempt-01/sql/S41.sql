SELECT performance_tier, COUNT(*) as cnt, AVG(overall_performance_score) as avg_perf, AVG(resolution_rate_percentage) as avg_res_rate
FROM jira__team_performance_dashboard
GROUP BY performance_tier