SELECT DISTINCT campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment,
       COUNT(*) AS n_rows
FROM google_ads__customer_acquisition_analysis
GROUP BY campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment
ORDER BY n_rows DESC
LIMIT 30