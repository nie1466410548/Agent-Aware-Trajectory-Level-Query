
WITH cat AS (
  SELECT application_id, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  WHERE i.technical_score IS NOT NULL
  GROUP BY i.application_id
)
SELECT * FROM app_agg
