SELECT
  SUM(__a0) AS "total",
  SUM(__a1) AS "null_carat",
  SUM(__a2) AS "null_cut",
  SUM(__a3) AS "null_color",
  SUM(__a4) AS "null_clarity",
  SUM(__a5) AS "null_depth",
  SUM(__a6) AS "null_table",
  SUM(__a7) AS "null_x",
  SUM(__a8) AS "null_y",
  SUM(__a9) AS "null_z",
  SUM(__a10) AS "null_price"
FROM temp."reuse_012_c3";
