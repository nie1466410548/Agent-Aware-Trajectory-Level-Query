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
SELECT person_id, campaign_id, campaign_name, campaign_subject_line, send_at, open_rate, click_rate,
       count_received_email, count_opened_email, count_clicked_email, net_revenue_touch,
       active_retention_rate_week, active_retention_rate_month, person_email_open_rate,
       dow, hour, day_part, time_half, theme, holiday, hol_diff
FROM (
  SELECT t2.*,
         h.d AS holiday,
         CAST(julianday(substr(t2.send_at,1,10)) - julianday(h.d) AS INTEGER) AS hol_diff,
         ROW_NUMBER() OVER (PARTITION BY t2.person_id, t2.campaign_id ORDER BY ABS(julianday(substr(t2.send_at,1,10)) - julianday(h.d)), julianday(h.d)) AS rn
  FROM t t2
  CROSS JOIN holidays h
) WHERE rn = 1
ORDER BY send_at