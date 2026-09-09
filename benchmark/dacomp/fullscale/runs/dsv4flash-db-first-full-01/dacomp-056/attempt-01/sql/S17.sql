SELECT MIN(portfolio_contribution_pct) AS min_pct,
       MAX(portfolio_contribution_pct) AS max_pct,
       AVG(portfolio_contribution_pct) AS avg_pct
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL