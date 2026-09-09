SELECT MIN(portfolio_contribution_pct) AS min_pct,
       MAX(portfolio_contribution_pct) AS max_pct,
       AVG(portfolio_contribution_pct) AS avg_pct,
       PERCENTILE(portfolio_contribution_pct, 0.5) AS median_pct,
       PERCENTILE(portfolio_contribution_pct, 0.75) AS p75,
       PERCENTILE(portfolio_contribution_pct, 0.90) AS p90,
       PERCENTILE(portfolio_contribution_pct, 0.95) AS p95,
       PERCENTILE(portfolio_contribution_pct, 0.99) AS p99
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL