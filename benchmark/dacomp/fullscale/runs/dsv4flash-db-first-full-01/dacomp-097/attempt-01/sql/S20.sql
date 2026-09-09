SELECT arr_bucket, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
      ELSE 'unknown'
    END AS arr_bucket
  FROM intercom__company_enhanced
) GROUP BY arr_bucket
ORDER BY cnt DESC