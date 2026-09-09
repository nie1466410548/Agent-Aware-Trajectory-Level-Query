SELECT
  MIN(__a20) AS "mn_study",
  MAX(__a21) AS "mx_study",
  (
    1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
  ) AS "avg_study",
  MIN(__a23) AS "mn_sm",
  MAX(__a24) AS "mx_sm",
  (
    1.0 * SUM(__a25_sum) / NULLIF(SUM(__a25_n), 0)
  ) AS "avg_sm",
  MIN(__a26) AS "mn_att",
  MAX(__a27) AS "mx_att",
  (
    1.0 * SUM(__a28_sum) / NULLIF(SUM(__a28_n), 0)
  ) AS "avg_att",
  MIN(__a29) AS "mn_sleep",
  MAX(__a30) AS "mx_sleep",
  (
    1.0 * SUM(__a31_sum) / NULLIF(SUM(__a31_n), 0)
  ) AS "avg_sleep",
  MIN(__a32) AS "mn_ex",
  MAX(__a33) AS "mx_ex",
  (
    1.0 * SUM(__a34_sum) / NULLIF(SUM(__a34_n), 0)
  ) AS "avg_ex",
  MIN(__a35) AS "mn_age",
  MAX(__a36) AS "mx_age",
  (
    1.0 * SUM(__a37_sum) / NULLIF(SUM(__a37_n), 0)
  ) AS "avg_age"
FROM temp."reuse_020_c2";
