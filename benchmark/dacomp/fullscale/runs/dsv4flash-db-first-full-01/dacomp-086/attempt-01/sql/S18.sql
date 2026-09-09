SELECT industry_normalized, account_size_segment, 
       COUNT(*) AS n,
       ROUND(AVG(health_score), 1) AS avg_hs,
       ROUND(MIN(health_score), 1) AS min_hs,
       ROUND(MAX(health_score), 1) AS max_hs
FROM (
  WITH scores AS (
    SELECT 
      account_id, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, total_contacts, contacts_with_email,
      days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *, ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores
)
GROUP BY industry_normalized, account_size_segment
ORDER BY industry_normalized, account_size_segment