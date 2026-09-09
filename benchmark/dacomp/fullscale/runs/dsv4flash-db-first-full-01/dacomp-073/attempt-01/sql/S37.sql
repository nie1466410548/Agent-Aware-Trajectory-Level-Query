WITH monthly AS (
  SELECT categories_department,
         substr(created_at, 1, 7) as ym,
         COUNT(*) as cnt
  FROM lever__posting_enhanced
  WHERE substr(created_at, 1, 7) IS NOT NULL
  GROUP BY categories_department, substr(created_at, 1, 7)
),
mom_growth AS (
  SELECT categories_department, ym, cnt,
         LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) as prev_cnt,
         CASE WHEN LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) > 0
              THEN 1.0*(cnt - LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)) / LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)
              ELSE NULL END as mom_growth
  FROM monthly
)
SELECT categories_department,
       AVG(mom_growth) as avg_mom_growth,
       SUM(CASE WHEN ym = '2025-07' THEN cnt ELSE 0 END) as latest_month_cnt
FROM mom_growth
WHERE ym IN ('2025-06', '2025-07')
  AND mom_growth IS NOT NULL
GROUP BY categories_department
ORDER BY categories_department