SELECT COUNT(*) AS total, SUM(CASE WHEN substr(CreatedDate,1,7)='2023-04' THEN 1 ELSE 0 END) AS apr_created FROM Opportunity
