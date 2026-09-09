SELECT renewal_window, COUNT(*) AS n FROM (
  SELECT *, regexp_replace(all_company_tags, '.*renewal_window=([^|]+).*', '\1') AS renewal_window FROM intercom__company_enhanced
) GROUP BY renewal_window ORDER BY n DESC