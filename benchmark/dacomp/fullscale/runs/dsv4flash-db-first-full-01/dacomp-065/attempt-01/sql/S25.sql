WITH cat AS (
  SELECT application_id, candidate_company,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(DISTINCT cat.application_id) AS n_apps,
       COUNT(*) AS n_scorecards,
       AVG(i.technical_score) AS avg_tech,
       AVG(i.problem_solving_score) AS avg_ps,
       AVG(i.communication_score) AS avg_comm,
       AVG(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0 END) AS pos_rec_rate
FROM cat
JOIN greenhouse__interview_enhanced i ON i.application_id = cat.application_id
WHERE i.technical_score IS NOT NULL
GROUP BY cat.company_cat
ORDER BY avg_tech DESC