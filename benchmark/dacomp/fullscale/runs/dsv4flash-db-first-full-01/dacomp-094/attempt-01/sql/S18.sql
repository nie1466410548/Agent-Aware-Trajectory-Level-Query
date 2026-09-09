WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT t2.person_id, t2.campaign_id, t2.campaign_name, t2.campaign_subject_line, t2.send_at,
       t2.open_rate, t2.click_rate, t2.count_received_email, t2.count_opened_email, t2.count_clicked_email,
       t2.net_revenue_touch, t2.active_retention_rate_week, t2.active_retention_rate_month,
       t2.person_email_open_rate, t2.dow, t2.hour,
       CASE WHEN t2.dow IN (0,6) THEN 'weekend' ELSE 'weekday' END AS day_part,
       CASE WHEN t2.hour < 12 THEN 'morning' ELSE 'afternoon' END AS time_half,
       CASE WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%launch%' THEN 'new_product_launch'
            WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%offer%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%sale%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%discount%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%deal%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%save%' THEN 'discount'
            WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%story%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%journey%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%behind%' THEN 'storytelling'
            ELSE 'unknown' END AS theme,
       (SELECT MIN(ABS(julianday(substr(t3.send_at,1,10)) - julianday(h.d))) FROM holidays h) AS days_to_holiday,
       (SELECT julianday(substr(t3.send_at,1,10)) - julianday(h.d) FROM holidays h ORDER BY ABS(julianday(substr(t3.send_at,1,10)) - julianday(h.d)) LIMIT 1) AS signed_holiday_diff
FROM t t2
JOIN (SELECT send_at FROM t) t3 ON t3.send_at = t2.send_at