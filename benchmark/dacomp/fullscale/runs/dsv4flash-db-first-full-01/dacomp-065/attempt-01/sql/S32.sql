WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT i.application_id, i.interview_id, i.technical_score, i.problem_solving_score,
       i.communication_score, i.culture_fit_score, i.leadership_score,
       i.overall_recommendation, i.job_stage, i.interviewer_gender,
       i.interviewer_level, i.interviewer_experience_years, i.interviewer_company_tenure,
       i.interview_time_of_day, i.interview_day_of_week, i.interview_season,
       i.candidate_gender, i.candidate_race, i.candidate_disability_status, i.candidate_veteran_status,
       i.interview_duration_minutes, i.interviewer_is_hiring_manager,
       i.follow_up_questions_count, i.interviewer_satisfaction,
       cat.company_cat
FROM greenhouse__interview_enhanced i
JOIN cat ON cat.application_id = i.application_id
WHERE i.technical_score IS NOT NULL
ORDER BY i.application_id, i.interview_id