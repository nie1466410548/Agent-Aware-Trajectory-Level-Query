
WITH per_sub AS (
  SELECT subsidiary_id, dashboard_date,
         ROW_NUMBER() OVER (PARTITION BY subsidiary_id ORDER BY dashboard_date) AS period_idx,
         cash_flow_risk_level, weighted_average_days_outstanding, overdue_percentage
  FROM netsuite2_financial_dashboard
),
rev AS (
  SELECT subsidiary_id, accounting_period_ending, SUM(converted_amount) AS revenue
  FROM netsuite2_income_statement WHERE account_type_name='Revenue' GROUP BY 1,2
),
exp AS (
  SELECT subsidiary_id, accounting_period_ending, SUM(converted_amount) AS expense
  FROM netsuite2_income_statement WHERE account_type_name='Expense' GROUP BY 1,2
),
joined AS (
  SELECT d.subsidiary_id, d.dashboard_date, d.period_idx, d.cash_flow_risk_level,
         d.weighted_average_days_outstanding, d.overdue_percentage,
         r.revenue, e.expense
  FROM per_sub d
  LEFT JOIN rev r ON r.subsidiary_id=d.subsidiary_id AND r.accounting_period_ending=d.dashboard_date
  LEFT JOIN exp e ON e.subsidiary_id=d.subsidiary_id AND e.accounting_period_ending=d.dashboard_date
)
SELECT subsidiary_id, dashboard_date, period_idx, cash_flow_risk_level,
       weighted_average_days_outstanding, overdue_percentage, revenue, expense,
       LAG(revenue) OVER w AS prev_revenue,
       LAG(expense) OVER w AS prev_expense,
       LAG(overdue_percentage) OVER w AS prev_overdue,
       LAG(overdue_percentage,2) OVER w AS prev2_overdue
FROM joined
WINDOW w AS (PARTITION BY subsidiary_id ORDER BY dashboard_date)
ORDER BY subsidiary_id, period_idx
