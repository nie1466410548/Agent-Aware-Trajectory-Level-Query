WITH split AS (
  SELECT company_id, value as tag FROM intercom__company_enhanced, json_each('["' || replace(all_company_tags, ', ', '","') || '"]') WHERE all_company_tags IS NOT NULL AND all_company_tags != ''
)
SELECT tag, COUNT(*) as cnt FROM split GROUP BY tag ORDER BY cnt DESC