-- Distribution of account_source
SELECT account_source, COUNT(*) AS n FROM salesforce__account_daily_history WHERE type='Customer' GROUP BY account_source ORDER BY n DESC