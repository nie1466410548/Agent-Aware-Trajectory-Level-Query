SELECT account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage, strategic_customer_segment, acquisition_cohort, COUNT(*) AS cnt
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage, strategic_customer_segment, acquisition_cohort
HAVING cnt > 1
LIMIT 10