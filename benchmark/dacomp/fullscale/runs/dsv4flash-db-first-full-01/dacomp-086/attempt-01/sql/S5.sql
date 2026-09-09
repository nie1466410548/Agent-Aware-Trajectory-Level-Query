SELECT 
  COUNT(*) AS n,
  MIN(days_since_last_activity) AS min_days, MAX(days_since_last_activity) AS max_days,
  MIN(total_activities_30d) AS min_act30, MAX(total_activities_30d) AS max_act30,
  MIN(total_contacts) AS min_tc, MAX(total_contacts) AS max_tc,
  MIN(contacts_with_email) AS min_ce, MAX(contacts_with_email) AS max_ce,
  MIN(annual_revenue) AS min_rev, MAX(annual_revenue) AS max_rev,
  MIN(total_won_amount) AS min_won, MAX(total_won_amount) AS max_won,
  MIN(number_of_employees) AS min_emp, MAX(number_of_employees) AS max_emp,
  MIN(current_pipeline_amount) AS min_pipe, MAX(current_pipeline_amount) AS max_pipe
FROM salesforce__customer_360_view