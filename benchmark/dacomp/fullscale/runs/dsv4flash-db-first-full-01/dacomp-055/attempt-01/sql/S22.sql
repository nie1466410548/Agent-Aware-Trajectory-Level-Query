SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email, investment_priority_score, acquisition_cost, customer_lifetime_value, product_adoption_rate, support_resolution_efficiency, total_sales_amount_via_c
FROM (
  SELECT v.marketo_lead_id, v.stripe_customer_id, v.zendesk_user_id, v.primary_email, v.investment_priority_score, v.acquisition_cost, v.customer_lifetime_value, v.product_adoption_rate, v.support_resolution_efficiency
  FROM customer360__customer_value_analysis v
  WHERE v.marketo_lead_id IN (8915, 6947, 8230)
) 
LIMIT 20