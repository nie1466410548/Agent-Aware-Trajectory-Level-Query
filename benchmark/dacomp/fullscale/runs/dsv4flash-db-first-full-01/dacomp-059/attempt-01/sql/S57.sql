
    SELECT ad_group_id, SUM(conversions_value) AS conv_value, SUM(conversions) AS conv
    FROM google_ads__ad_group_report
    GROUP BY ad_group_id
    HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
