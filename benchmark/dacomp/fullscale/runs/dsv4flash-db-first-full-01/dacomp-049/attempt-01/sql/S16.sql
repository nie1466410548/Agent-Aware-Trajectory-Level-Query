SELECT COUNT(*) AS peer_count FROM sheet1
WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%')
  AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')