SELECT inv_group, management_priority, COUNT(*) n
FROM (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS inv_group
  FROM asana__project_analytics
)
WHERE inv_group IN ('HHLV','HH_HV','LHHV','LH_LV')
GROUP BY inv_group, management_priority
ORDER BY inv_group, management_priority