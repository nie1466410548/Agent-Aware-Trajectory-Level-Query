SELECT COUNT(*) as total_readings, COUNT(DISTINCT "Environmental Reading ID") as distinct_readings,
       COUNT(DISTINCT "Display Case Reference") as distinct_cases
FROM environmental_monitoring_data