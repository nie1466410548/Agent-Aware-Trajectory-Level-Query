SELECT p."Outlet Type",
  ROUND(AVG(e."Annual Budget"), 1) AS avg_annual_budget,
  ROUND(AVG(e."Monthly Allocation"), 1) AS avg_monthly_alloc,
  ROUND(AVG(e."Amount Used"), 1) AS avg_amount_used,
  ROUND(AVG(e."Remaining Amount"), 1) AS avg_remaining,
  ROUND(SUM(e."Amount Used") * 1.0 / NULLIF(SUM(e."Annual Budget"), 0), 4) AS budget_utilization
FROM "point_of_sale_(pos)_information" p
LEFT JOIN expense_allocation_table e ON p."Outlet ID" = e."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_annual_budget DESC