SELECT COUNT(*) AS total,
  COUNT(DISTINCT account_id || '|' || substr(date_day,1,10) || '|' || advertising_channel_type || '|' || advertising_channel_subtype || '|' || customer_maturity_stage || '|' || campaign_lifecycle_stage || '|' || strategic_customer_segment || '|' || account_maturity_stage) AS full_key
FROM google_ads__customer_acquisition_analysis