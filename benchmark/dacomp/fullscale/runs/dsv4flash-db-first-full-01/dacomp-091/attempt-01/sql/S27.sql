WITH vendor_share AS (
  SELECT 0.2318 AS outflow_share
),
baseline AS (
  SELECT
    forecast_month,
    forecast_year,
    forecast_month_num,
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    cash_flow_health_score,
    liquidity_risk_level,
    -- Vendor portion of outflow
    forecasted_outflows * outflow_share AS vendor_outflow,
    -- 30% reduction on vendor portion
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    -- Adjusted outflow
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    -- Adjusted net cash flow
    forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) AS adjusted_net_cash_flow,
    -- Monthly deficit ratio (baseline)
    CASE WHEN forecasted_net_cash_flow < 0 THEN -forecasted_net_cash_flow / NULLIF(forecasted_inflows, 0) ELSE 0 END AS baseline_lri,
    -- Monthly deficit ratio (adjusted)
    CASE WHEN forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) < 0
      THEN -(forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30)) / NULLIF(forecasted_inflows, 0)
      ELSE 0 END AS adjusted_lri
  FROM quickbooks__cashflow_forecast, vendor_share
)
SELECT
  forecast_month,
  forecast_year,
  forecast_month_num,
  ROUND(forecasted_inflows,2) AS forecasted_inflows,
  ROUND(forecasted_outflows,2) AS forecasted_outflows,
  ROUND(vendor_outflow,2) AS vendor_outflow,
  ROUND(vendor_reduction,2) AS vendor_reduction_30pct,
  ROUND(adjusted_outflow,2) AS adjusted_outflow,
  ROUND(forecasted_net_cash_flow,2) AS baseline_net,
  ROUND(adjusted_net_cash_flow,2) AS adjusted_net,
  ROUND(baseline_lri,6) AS baseline_lri_monthly,
  ROUND(adjusted_lri,6) AS adjusted_lri_monthly,
  liquidity_risk_level,
  cash_flow_health_score
FROM baseline
ORDER BY forecast_month