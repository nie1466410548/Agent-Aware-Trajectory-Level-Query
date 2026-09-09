-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_020_c2" AS
SELECT "Mental health score" AS __g0, "Gender" AS __g1, "Part-time job" AS __g2, "Diet quality" AS __g3, "Parents' education level" AS __g4, "Internet quality" AS __g5, "Extracurricular activity participation" AS __g6, COUNT(*) AS __a0, MIN("Mental health score") AS __a1, MAX("Mental health score") AS __a2, SUM("Mental health score") AS __a3_sum, COUNT("Mental health score") AS __a3_n, MIN("Exam score") AS __a4, MAX("Exam score") AS __a5, SUM("Exam score") AS __a6_sum, COUNT("Exam score") AS __a6_n, SUM("Exam score" * "Exam score") AS __a7_sum, COUNT("Exam score" * "Exam score") AS __a7_n, SUM(CASE WHEN "Age" IS NULL THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Daily study time" IS NULL THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN "Social media usage time" IS NULL THEN 1 ELSE 0 END) AS __a10, SUM(CASE WHEN "Attendance rate" IS NULL THEN 1 ELSE 0 END) AS __a11, SUM(CASE WHEN "Sleep duration" IS NULL THEN 1 ELSE 0 END) AS __a12, SUM(CASE WHEN "Exercise frequency" IS NULL THEN 1 ELSE 0 END) AS __a13, SUM(CASE WHEN "Mental health score" IS NULL THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN "Exam score" IS NULL THEN 1 ELSE 0 END) AS __a15, SUM(CASE WHEN "Part-time job" IS NULL THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN "Gender" IS NULL THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN "Internet quality" IS NULL THEN 1 ELSE 0 END) AS __a18, SUM(CASE WHEN "Diet quality" IS NULL THEN 1 ELSE 0 END) AS __a19, MIN("Daily study time") AS __a20, MAX("Daily study time") AS __a21, SUM("Daily study time") AS __a22_sum, COUNT("Daily study time") AS __a22_n, MIN("Social media usage time") AS __a23, MAX("Social media usage time") AS __a24, SUM("Social media usage time") AS __a25_sum, COUNT("Social media usage time") AS __a25_n, MIN("Attendance rate") AS __a26, MAX("Attendance rate") AS __a27, SUM("Attendance rate") AS __a28_sum, COUNT("Attendance rate") AS __a28_n, MIN("Sleep duration") AS __a29, MAX("Sleep duration") AS __a30, SUM("Sleep duration") AS __a31_sum, COUNT("Sleep duration") AS __a31_n, MIN("Exercise frequency") AS __a32, MAX("Exercise frequency") AS __a33, SUM("Exercise frequency") AS __a34_sum, COUNT("Exercise frequency") AS __a34_n, MIN("Age") AS __a35, MAX("Age") AS __a36, SUM("Age") AS __a37_sum, COUNT("Age") AS __a37_n FROM "sheet1"  GROUP BY "Mental health score", "Gender", "Part-time job", "Diet quality", "Parents' education level", "Internet quality", "Extracurricular activity participation";

-- S4
SELECT
  SUM(__a0) AS "total_rows"
FROM temp."reuse_020_c2";

-- S7
SELECT
  __g0 AS "mh",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 3) AS "avg_exam",
  ROUND(
    (
      1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
    ) - (
      1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
    ) * (
      1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
    ),
    3
  ) AS "var_exam"
FROM temp."reuse_020_c2"
GROUP BY
  __g0
ORDER BY
  mh;

-- S9
SELECT
  __g1 AS "Gender",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g1;

-- S10
SELECT
  __g2 AS "Part-time job",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g2;

-- S11
SELECT
  __g3 AS "Diet quality",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g3;

-- S12
SELECT
  __g4 AS "Parents' education level",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g4;

-- S13
SELECT
  __g5 AS "Internet quality",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g5;

-- S14
SELECT
  __g6 AS "Extracurricular activity participation",
  SUM(__a0) AS "n"
FROM temp."reuse_020_c2"
GROUP BY
  __g6;

-- S15
SELECT
  SUM(__a8) AS "age_null",
  SUM(__a9) AS "study_null",
  SUM(__a10) AS "sm_null",
  SUM(__a11) AS "att_null",
  SUM(__a12) AS "sleep_null",
  SUM(__a13) AS "ex_null",
  SUM(__a14) AS "mh_null",
  SUM(__a15) AS "exam_null",
  SUM(__a16) AS "pt_null",
  SUM(__a17) AS "gender_null",
  SUM(__a18) AS "iq_null",
  SUM(__a19) AS "diet_null"
FROM temp."reuse_020_c2";

DROP TABLE temp."reuse_020_c2";
