SELECT Patents_info, filing_date, grant_date, cpc
FROM publicationinfo
WHERE Patents_info LIKE '%DE-%'
