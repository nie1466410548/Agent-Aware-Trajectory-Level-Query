SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN filing_date IS NULL OR TRIM(filing_date)='' THEN 1 ELSE 0 END) AS null_or_empty,
  SUM(CASE WHEN TRIM(filing_date) GLOB '*[0-9][0-9][0-9][0-9]' THEN 1 ELSE 0 END) AS ends_with_year,
  SUM(CASE WHEN json_valid(cpc) THEN 1 ELSE 0 END) AS valid_cpc_json
FROM publicationinfo;
