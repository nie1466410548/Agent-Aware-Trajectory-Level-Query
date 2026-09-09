SELECT aqr."Environmental monitoring reference", emd."Environmental Reading ID"
FROM air_quality_readings aqr
LEFT JOIN environmental_monitoring_data emd ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
WHERE emd."Environmental Reading ID" IS NULL
LIMIT 5