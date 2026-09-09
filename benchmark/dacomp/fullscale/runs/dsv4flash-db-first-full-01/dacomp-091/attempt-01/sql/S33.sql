
  WITH vendor_share AS (SELECT 0.2318 AS outflow_share)
  SELECT
    forecast_month,
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) AS adjusted_net,
    cash_flow_health_score,
    liquidity_risk_level
  FROM quickbooks__cashflow_forecast, vendor_share
  ORDER BY forecast_month
