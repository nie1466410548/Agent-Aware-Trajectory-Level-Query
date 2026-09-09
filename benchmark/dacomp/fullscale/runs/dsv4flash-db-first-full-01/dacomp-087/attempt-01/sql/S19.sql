WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
workload_scores AS (
  SELECT rc.owner_id,
    rc.num_customers,
    rc.total_annual_revenue,
    rc.total_contacts,
    rg.distinct_states,
    rg.distinct_cities,
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5.0
         ELSE CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) END AS coverage_rate_capped,
    rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
         ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
    (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
  FROM rep_cust rc
  JOIN rep_geo rg ON rc.owner_id = rg.owner_id
),
efficiency_scores AS (
  SELECT spd.owner_id, spd.rep_name, spd.manager_id,
    spd.win_rate_pct / 100.0 AS win_rate,
    spd.avg_deal_size_usd,
    spd.avg_sales_cycle_days,
    spd.close_rate_pct / 100.0 AS opp_conversion_rate,
    spd.win_rate_pct / 100.0 * 0.4 + (spd.avg_deal_size_usd / 100000.0) * 0.3 + 
    (120.0 / NULLIF(spd.avg_sales_cycle_days, 0)) * 0.2 + (spd.close_rate_pct / 100.0) * 0.1 AS efficiency_score
  FROM salesforce__sales_performance_dashboard spd
)
SELECT ws.owner_id, spd.rep_name, spd.manager_id,
  ws.workload_score, es.efficiency_score,
  ws.num_customers, ws.total_annual_revenue, ws.coverage_rate_capped,
  ws.distinct_states, ws.distinct_cities,
  es.win_rate, es.avg_deal_size_usd, es.avg_sales_cycle_days, es.opp_conversion_rate
FROM workload_scores ws
JOIN efficiency_scores es ON ws.owner_id = es.owner_id
JOIN salesforce__sales_performance_dashboard spd ON ws.owner_id = spd.owner_id
ORDER BY ws.workload_score DESC
LIMIT 1000