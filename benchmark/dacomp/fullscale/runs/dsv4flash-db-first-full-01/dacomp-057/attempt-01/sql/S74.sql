SELECT account_id, advertising_channel_type, advertising_channel_subtype, campaign_lifecycle_stage, customer_maturity_stage,
       account_maturity_stage, strategic_customer_segment,
       COUNT(*) AS n_rows,
       ROUND(AVG(customer_acquisition_cost),2) AS avg_cac,
       ROUND(AVG(ltv_cac_ratio),2) AS avg_ltv_cac,
       ROUND(AVG(acquisition_sophistication_score),1) AS avg_soph,
       ROUND(AVG(cac_efficiency_percentile),1) AS avg_eff,
       ROUND(AVG(channel_diversity_count),1) AS avg_chdiv,
       SUM(retention_risk) AS retention_risk_cnt,
       SUM(scale_opportunity) AS scale_opp_cnt,
       SUM(high_cac_alert) AS high_cac_cnt,
       SUM(negative_roi_alert) AS neg_roi_cnt
FROM google_ads__customer_acquisition_analysis
WHERE (account_id = 'ACC_FIN_001' AND advertising_channel_type = 'SHOPPING')
   OR (account_id = 'ACC_ECOM_002' AND advertising_channel_type = 'VIDEO' AND advertising_channel_subtype = 'YOUTUBE_SEARCH')
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype, campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment
ORDER BY account_id, advertising_channel_type, campaign_lifecycle_stage