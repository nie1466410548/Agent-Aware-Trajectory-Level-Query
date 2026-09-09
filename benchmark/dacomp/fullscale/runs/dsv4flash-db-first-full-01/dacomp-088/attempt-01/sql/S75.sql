
    SELECT industry, COUNT(DISTINCT account_id) AS n
    FROM salesforce__account_daily_history WHERE type='Customer'
    GROUP BY industry ORDER BY n DESC LIMIT 8
