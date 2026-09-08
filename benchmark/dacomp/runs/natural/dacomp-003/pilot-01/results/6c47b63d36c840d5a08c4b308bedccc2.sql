SELECT MIN("Year") AS min_year, MAX("Year") AS max_year, COUNT(*) AS n_rows, COUNT(DISTINCT "Region Code") AS n_regions
FROM sheet1;
