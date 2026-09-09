SELECT 
  is_xm_directory_contact, is_research_core_contact,
  COUNT(*) AS n,
  AVG(total_count_completed_surveys) AS avg_ltv,
  SUM(total_count_completed_surveys) AS total_ltv
FROM qualtrics__contact
GROUP BY is_xm_directory_contact, is_research_core_contact