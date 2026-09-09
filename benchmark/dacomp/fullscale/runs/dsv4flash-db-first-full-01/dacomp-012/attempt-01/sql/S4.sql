SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN "Carat (diamond weight)" IS NULL THEN 1 ELSE 0 END) AS null_carat,
  SUM(CASE WHEN "Cut (quality)" IS NULL THEN 1 ELSE 0 END) AS null_cut,
  SUM(CASE WHEN "Color" IS NULL THEN 1 ELSE 0 END) AS null_color,
  SUM(CASE WHEN "Clarity" IS NULL THEN 1 ELSE 0 END) AS null_clarity,
  SUM(CASE WHEN "Depth percentage" IS NULL THEN 1 ELSE 0 END) AS null_depth,
  SUM(CASE WHEN "Table percentage" IS NULL THEN 1 ELSE 0 END) AS null_table,
  SUM(CASE WHEN "X-axis length (mm)" IS NULL THEN 1 ELSE 0 END) AS null_x,
  SUM(CASE WHEN "Y-axis width (mm)" IS NULL THEN 1 ELSE 0 END) AS null_y,
  SUM(CASE WHEN "Z-axis depth (mm)" IS NULL THEN 1 ELSE 0 END) AS null_z,
  SUM(CASE WHEN "Price (USD)" IS NULL THEN 1 ELSE 0 END) AS null_price
FROM sheet1