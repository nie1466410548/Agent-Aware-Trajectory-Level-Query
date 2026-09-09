SELECT 
  (SELECT SUM(clicks) FROM google_ads__ad_group_report) AS ag_clicks,
  (SELECT SUM(clicks) FROM google_ads__keyword_report) AS kw_clicks,
  (SELECT SUM(impressions) FROM google_ads__ad_group_report) AS ag_imp,
  (SELECT SUM(impressions) FROM google_ads__keyword_report) AS kw_imp,
  (SELECT SUM(conversions) FROM google_ads__ad_group_report) AS ag_conv,
  (SELECT SUM(conversions) FROM google_ads__keyword_report) AS kw_conv