WITH vendor_share AS (SELECT 0.2318 AS outflow_share),
m AS (
  SELECT
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    CASE WHEN forecasted_net_cash_flow < 0 THEN -forecasted_net_cash_flow / NULLIF(forecasted_inflows,0) ELSE 0 END AS baseline_lri,
    CASE WHEN forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) < 0
      THEN -(forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30)) / NULLIF(forecasted_inflows,0) ELSE 0 END AS adjusted_lri
  FROM quickbooks__cashflow_forecast, vendor_share
)
SELECT
  ROUND(SUM(forecasted_outflows),2) AS total_baseline_outflow,
  ROUND(SUM(adjusted_outflow),2) AS total_adjusted_outflow,
  ROUND(SUM(vendor_reduction),2) AS total_vendor_reduction,
  ROUND(100.0*SUM(vendor_reduction)/SUM(forecasted_outflows),2) AS pct_outflow_reduction,
  ROUND(SUM(forecasted_inflows) - SUM(forecasted_outflows),2) AS baseline_net_18m,
  ROUND(SUM(forecasted_inflows) - SUM(adjusted_outflow),2) AS adjusted_net_18m,
  ROUND(AVG(baseline_lri),6) AS baseline_lri_avg,
  ROUND(AVG(adjusted_lri),6) AS adjusted_lri_avg,
  ROUND(AVG(baseline_lri)-AVG(adjusted_lri),6) AS lri_change
FROM m