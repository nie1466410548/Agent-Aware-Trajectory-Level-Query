SELECT account_size_segment, industry_normalized, COUNT(*) AS cnt, AVG(annual_revenue) AS avg_rev, AVG(number_of_employees) AS avg_emp, AVG(total_contacts) AS avg_contacts
FROM salesforce__customer_360_view
WHERE annual_revenue IS NOT NULL
GROUP BY account_size_segment, industry_normalized
ORDER BY account_size_segment, cnt DESC