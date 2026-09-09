
WITH cat AS (
  SELECT DISTINCT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
  SUM(CASE WHEN a.stage_application_review=1 THEN 1 ELSE 0 END) AS app_review,
  SUM(CASE WHEN a.stage_phone_screen=1 THEN 1 ELSE 0 END) AS phone_screen,
  SUM(CASE WHEN a.stage_technical_interview=1 THEN 1 ELSE 0 END) AS tech_int,
  SUM(CASE WHEN a.stage_panel_interview=1 THEN 1 ELSE 0 END) AS panel,
  SUM(CASE WHEN a.stage_final_interview=1 THEN 1 ELSE 0 END) AS final_int,
  SUM(CASE WHEN a.stage_offer=1 THEN 1 ELSE 0 END) AS offer,
  SUM(CASE WHEN a.stage_hired=1 THEN 1 ELSE 0 END) AS hired
FROM (SELECT DISTINCT application_id, stage_application_review, stage_phone_screen, stage_technical_interview,
      stage_panel_interview, stage_final_interview, stage_offer, stage_hired
      FROM greenhouse__application_enhanced) a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_application_review = 1
GROUP BY cat.company_cat
ORDER BY hired DESC
