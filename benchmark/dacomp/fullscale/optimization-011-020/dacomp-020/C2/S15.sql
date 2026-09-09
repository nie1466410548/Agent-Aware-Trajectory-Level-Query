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
