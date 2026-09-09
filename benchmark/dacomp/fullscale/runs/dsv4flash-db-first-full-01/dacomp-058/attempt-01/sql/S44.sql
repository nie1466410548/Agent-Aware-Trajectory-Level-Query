
SELECT k.* FROM google_ads__keyword_report k
WHERE k.campaign_id IN (105,135,36,184,180,56,69,148,178,27)
ORDER BY k.campaign_id, k.year_quarter
