SELECT 
  risk_group,
  ROUND(AVG(total_invoice_amount),2) AS avg_total_invoice_amt,
  ROUND(AVG(monthly_revenue_avg),2) AS avg_monthly_rev,
  ROUND(AVG(revenue_current_year),2) AS avg_rev_cy,
  ROUND(AVG(revenue_prev_year),2) AS avg_rev_py,
  ROUND(AVG(revenue_growth_yoy_pct),2) AS avg_growth_yoy,
  ROUND(AVG(total_payments),2) AS avg_payments,
  ROUND(AVG(total_quantity_purchased),2) AS avg_qty,
  ROUND(AVG(unique_products_purchased),2) AS avg_products,
  ROUND(AVG(payment_timeliness_score),2) AS avg_timeliness
FROM (
  SELECT *, CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
)
GROUP BY risk_group