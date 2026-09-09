
SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat,
  a.candidate_gender, a.candidate_race, a.education_level, a.years_of_experience,
  a.skill_count, a.university_tier, a.stage_hired
FROM greenhouse__application_enhanced a
