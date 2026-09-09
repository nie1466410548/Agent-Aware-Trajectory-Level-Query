SELECT
  ROUND(AVG(forecasted_outflows),2) AS avg_fc_outflow,
  ROUND(AVG(forecasted_inflows),2) AS avg_fc_inflow,
  ROUND(AVG(forecasted_net_cash_flow),2) AS avg_fc_net,
  ROUND(SUM(forecasted_outflows),2) AS sum_fc_outflow,
  ROUND(SUM(forecasted_inflows),2) AS sum_fc_inflow,
  ROUND(SUM(forecasted_net_cash_flow),2) AS sum_fc_net
FROM quickbooks__cashflow_forecast