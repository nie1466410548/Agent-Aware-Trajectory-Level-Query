-- Extract segment, seat_bucket, arr_bucket from company tags
SELECT 
  company_id,
  company_name,
  CASE 
    WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
    WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
    WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
    WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
    ELSE 'unknown'
  END AS segment,
  CASE 
    WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
    WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
    WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
    WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
    WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
    ELSE 'unknown'
  END AS seat_bucket,
  CASE 
    WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
    ELSE 'unknown'
  END AS arr_bucket,
  monthly_spend,
  user_count
FROM intercom__company_enhanced
LIMIT 20