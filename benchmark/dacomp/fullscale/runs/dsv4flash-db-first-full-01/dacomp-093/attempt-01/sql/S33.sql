SELECT
  (SELECT COUNT(*) FROM klaviyo__persons) AS n_persons,
  (SELECT ROUND(SUM(count_received_email),0) FROM klaviyo__persons) AS sum_person_received,
  (SELECT ROUND(AVG(count_received_email),0) FROM klaviyo__campaigns) AS avg_campaign_received,
  (SELECT COUNT(*) FROM klaviyo__campaigns) AS n_campaigns,
  (SELECT ROUND(SUM(count_opened_email),0) FROM klaviyo__persons) AS sum_person_opened,
  (SELECT ROUND(AVG(count_opened_email),0) FROM klaviyo__campaigns) AS avg_campaign_opened