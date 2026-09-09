SELECT is_won, COUNT(*) AS n, AVG(amount) AS avg_amount, AVG(probability) AS avg_prob
FROM salesforce__opportunity_enhanced
GROUP BY is_won