SELECT c.owner_id, c.account_id, c.account_name, c.annual_revenue, c.billing_state, c.billing_city, c.industry_normalized, c.account_size_segment, c.total_contacts, c.number_of_employees, c.total_opportunities, c.won_opportunities, c.win_rate_percentage
FROM salesforce__customer_360_view c
LIMIT 20