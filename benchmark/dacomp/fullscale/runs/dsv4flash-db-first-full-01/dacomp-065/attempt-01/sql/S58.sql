
WITH cat AS (
  SELECT DISTINCT a.application_id, a.education_level, a.years_of_experience, a.skill_count, a.university_tier,
    CASE
      WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat,
    a.candidate_gender, a.candidate_race
  FROM greenhouse__application_enhanced a
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         cat.candidate_gender, cat.candidate_race,
         AVG(i.technical_score) AS avg_tech
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
