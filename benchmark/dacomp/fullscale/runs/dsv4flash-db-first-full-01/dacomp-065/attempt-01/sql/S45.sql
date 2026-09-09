WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(*) AS n_apps,
       SUM(a.stage_offer) AS reached_offer,
       SUM(a.stage_hired) AS hired,
       AVG(CAST(a.stage_offer AS FLOAT)) AS offer_rate,
       AVG(CAST(a.stage_hired AS FLOAT)) AS hire_rate
FROM greenhouse__application_enhanced a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_technical_interview = 1
GROUP BY cat.company_cat
ORDER BY offer_rate DESC