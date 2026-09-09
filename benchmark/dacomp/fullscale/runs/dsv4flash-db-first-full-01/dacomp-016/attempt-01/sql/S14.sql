-- Count of rows per region-year combination in each table to confirm one row per region per year
SELECT (SELECT COUNT(*) FROM sheet1) AS sheet1_rows,
       (SELECT COUNT(*) FROM economic_indicator_data) AS econ_rows,
       (SELECT COUNT(DISTINCT "Region Name") FROM sheet1) AS regions_sheet,
       (SELECT COUNT(DISTINCT "Region Name") FROM economic_indicator_data) AS regions_econ