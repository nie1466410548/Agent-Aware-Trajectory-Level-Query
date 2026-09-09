SELECT postings_per_hm, COUNT(*) as num_managers
FROM (
  SELECT posting_hiring_manager_name, COUNT(*) as postings_per_hm
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name
)
GROUP BY postings_per_hm
ORDER BY postings_per_hm DESC
LIMIT 15