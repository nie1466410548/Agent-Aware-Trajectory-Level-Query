-- Browsing behavior metrics by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS browsing_events,
  ROUND(AVG(b."Time on Page"),1) AS avg_time_on_page,
  ROUND(AVG(b."View Count"),1) AS avg_view_count,
  ROUND(AVG(b."Scroll Distance"),1) AS avg_scroll,
  ROUND(AVG(b."Zoom Count"),1) AS avg_zoom_count,
  ROUND(AVG(b."Time on Detail Page"),1) AS avg_detail_time,
  ROUND(AVG(b."Time on Review Page"),1) AS avg_review_time,
  ROUND(SUM(b."Product Link Share Count")*1.0/COUNT(*),3) AS avg_share_per_view,
  ROUND(AVG(b."Has Swiped" = 'Yes')*100,1) AS swiped_pct,
  ROUND(AVG(b."Has Zoomed" = 'Yes')*100,1) AS zoomed_pct,
  ROUND(AVG(b."Viewed Specifications" = 'Yes')*100,1) AS specs_pct
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group