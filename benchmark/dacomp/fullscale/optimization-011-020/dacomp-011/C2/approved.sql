-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_011_c2" AS
SELECT "Parents' education level" AS __g0, gender AS __g1, "Diet quality" AS __g2, "Internet quality" AS __g3, "Extracurricular activity participation" AS __g4, CASE WHEN "Daily study time" < 2 THEN '<2h' WHEN "Daily study time" < 4 THEN '2-4h' WHEN "Daily study time" < 6 THEN '4-6h' ELSE '6h+' END AS __g5, CASE WHEN "Mental health score" <= 3 THEN 'Low (0-3)' WHEN "Mental health score" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END AS __g6, CASE WHEN "Attendance rate" < 70 THEN '<70%' WHEN "Attendance rate" < 85 THEN '70-85%' WHEN "Attendance rate" < 95 THEN '85-95%' ELSE '95%+' END AS __g7, "Part-time job" AS __g8, CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS __g9, COUNT(*) AS __a0, SUM("Exam score") AS __a1_sum, COUNT("Exam score") AS __a1_n, MIN("Exam score") AS __a2, MAX("Exam score") AS __a3, SUM("Daily study time") AS __a4_sum, COUNT("Daily study time") AS __a4_n, SUM("Social media usage time") AS __a5_sum, COUNT("Social media usage time") AS __a5_n, SUM("Attendance rate") AS __a6_sum, COUNT("Attendance rate") AS __a6_n, SUM("Sleep duration") AS __a7_sum, COUNT("Sleep duration") AS __a7_n, SUM("Exercise frequency") AS __a8_sum, COUNT("Exercise frequency") AS __a8_n, SUM("Mental health score") AS __a9_sum, COUNT("Mental health score") AS __a9_n, SUM("Exam score" * "Exam score") AS __a10, SUM("Exam score") AS __a11 FROM "sheet1"  GROUP BY "Parents' education level", gender, "Diet quality", "Internet quality", "Extracurricular activity participation", CASE WHEN "Daily study time" < 2 THEN '<2h' WHEN "Daily study time" < 4 THEN '2-4h' WHEN "Daily study time" < 6 THEN '4-6h' ELSE '6h+' END, CASE WHEN "Mental health score" <= 3 THEN 'Low (0-3)' WHEN "Mental health score" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END, CASE WHEN "Attendance rate" < 70 THEN '<70%' WHEN "Attendance rate" < 85 THEN '70-85%' WHEN "Attendance rate" < 95 THEN '85-95%' ELSE '95%+' END, "Part-time job", CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END;

-- S3
SELECT
  SUM(__a0) AS "total_rows"
FROM temp."reuse_011_c2";

-- S4
SELECT
  __g0 AS "parent_edu",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND(MIN(__a2), 2) AS "min_exam",
  ROUND(MAX(__a3), 2) AS "max_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0
ORDER BY
  avg_exam DESC;

-- S6
SELECT
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND(MIN(__a2), 2) AS "min_exam",
  ROUND(MAX(__a3), 2) AS "max_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study",
  ROUND((
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ), 2) AS "avg_social",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 2) AS "avg_attendance",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 2) AS "avg_sleep",
  ROUND((
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ), 2) AS "avg_exercise",
  ROUND((
    1.0 * SUM(__a9_sum) / NULLIF(SUM(__a9_n), 0)
  ), 2) AS "avg_mh"
FROM temp."reuse_011_c2";

-- S8
SELECT
  __g0 AS "parent_edu",
  __g1 AS "Gender",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  SUM(__a0) AS "n"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g1
ORDER BY
  parent_edu,
  __g1;

-- S9
SELECT
  __g0 AS "parent_edu",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study",
  ROUND((
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ), 2) AS "avg_social",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 2) AS "avg_attendance",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 2) AS "avg_sleep",
  ROUND((
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ), 2) AS "avg_exercise",
  ROUND((
    1.0 * SUM(__a9_sum) / NULLIF(SUM(__a9_n), 0)
  ), 2) AS "avg_mh"
FROM temp."reuse_011_c2"
GROUP BY
  __g0
ORDER BY
  parent_edu;

-- S13
SELECT
  __g0 AS "parent_edu",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    SUM(__a10) - SUM(__a11) * SUM(__a11) / SUM(__a0)
  ) / (
    SUM(__a0) - 1
  ), 2) AS "var_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0
ORDER BY
  parent_edu;

-- S15
SELECT
  __g2 AS "val",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g2
ORDER BY
  avg_exam DESC;

-- S16
SELECT
  __g3 AS "val",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g3
ORDER BY
  avg_exam DESC;

-- S17
SELECT
  __g4 AS "val",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g4
ORDER BY
  avg_exam DESC;

-- S18
SELECT
  __g1 AS "val",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g1
ORDER BY
  avg_exam DESC;

-- S19
SELECT
  __g5 AS "study_cat",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ), 2) AS "avg_social",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 2) AS "avg_attendance",
  ROUND((
    1.0 * SUM(__a9_sum) / NULLIF(SUM(__a9_n), 0)
  ), 2) AS "avg_mh"
FROM temp."reuse_011_c2"
GROUP BY
  __g5
ORDER BY
  avg_exam DESC;

-- S20
SELECT
  __g6 AS "mh_cat",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study"
FROM temp."reuse_011_c2"
GROUP BY
  __g6
ORDER BY
  avg_exam DESC;

-- S21
SELECT
  __g7 AS "attendance_cat",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study"
FROM temp."reuse_011_c2"
GROUP BY
  __g7
ORDER BY
  avg_exam DESC;

-- S22
SELECT
  __g0 AS "parent_edu",
  __g5 AS "study_cat",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g5
ORDER BY
  parent_edu,
  study_cat;

-- S23
SELECT
  __g0 AS "parent_edu",
  __g8 AS "pt_job",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g8
ORDER BY
  parent_edu,
  pt_job;

-- S24
SELECT
  __g0 AS "parent_edu",
  __g2 AS "diet",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g0,
  __g2
ORDER BY
  parent_edu,
  diet;

-- S29
SELECT
  __g9 AS "parent_edu",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam",
  ROUND((
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ), 2) AS "avg_study",
  ROUND((
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ), 2) AS "avg_social",
  ROUND((
    1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)
  ), 2) AS "avg_att",
  ROUND((
    1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)
  ), 2) AS "avg_sleep",
  ROUND((
    1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)
  ), 2) AS "avg_ex",
  ROUND((
    1.0 * SUM(__a9_sum) / NULLIF(SUM(__a9_n), 0)
  ), 2) AS "avg_mh"
FROM temp."reuse_011_c2"
GROUP BY
  __g9
ORDER BY
  avg_exam DESC;

-- S30
SELECT
  __g9 AS "parent_edu",
  __g2 AS "diet",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 2) AS "avg_exam"
FROM temp."reuse_011_c2"
GROUP BY
  __g9,
  __g2
ORDER BY
  parent_edu,
  diet;

DROP TABLE temp."reuse_011_c2";
