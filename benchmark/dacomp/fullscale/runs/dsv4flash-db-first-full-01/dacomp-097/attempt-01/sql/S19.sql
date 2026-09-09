SELECT seat_bucket, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
      WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
      WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
      WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
      WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
      ELSE 'unknown'
    END AS seat_bucket
  FROM intercom__company_enhanced
) GROUP BY seat_bucket
ORDER BY cnt DESC