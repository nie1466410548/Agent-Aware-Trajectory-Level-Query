SELECT marketo_lead_id, rfm_score, rfm_segment, rfm_avg_score, recency_score, frequency_score, monetary_score, estimated_customer_ltv, customer_health_score, churn_probability, customer_tier, customer_segment
FROM customer360__customer_value_analysis
WHERE marketo_lead_id = 7116
ORDER BY rfm_score