SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'clinical_info'
ORDER BY ordinal_position;

