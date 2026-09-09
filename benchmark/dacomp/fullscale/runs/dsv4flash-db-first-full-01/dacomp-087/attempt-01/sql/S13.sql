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
)
SELECT rc.owner_id,
  rc.num_customers,
  rc.total_annual_revenue,
  rc.total_contacts,
  rg.distinct_states,
  rg.distinct_cities,
  rc.num_customers * 0.3 AS term1,
  (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 AS term2,
  CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
       ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END AS term3,
  (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS term4,
  rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
  CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
       ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
  (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
FROM rep_cust rc
JOIN rep_geo rg ON rc.owner_id = rg.owner_id
ORDER BY workload_score DESC
LIMIT 20