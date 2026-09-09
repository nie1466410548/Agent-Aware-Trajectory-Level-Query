SELECT 
  email_domain,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_ltv,
  SUM(total_count_completed_surveys) AS total_ltv
FROM qualtrics__contact
GROUP BY email_domain
ORDER BY avg_ltv DESC