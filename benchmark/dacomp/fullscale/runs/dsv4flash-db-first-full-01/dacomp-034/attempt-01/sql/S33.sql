-- Check attachment_1 and attachment_2 data ranges
SELECT MIN(create_dt) AS m1, MAX(create_dt) AS m2 FROM attachment_1
UNION ALL
SELECT MIN(create_dt), MAX(create_dt) FROM attachment_2