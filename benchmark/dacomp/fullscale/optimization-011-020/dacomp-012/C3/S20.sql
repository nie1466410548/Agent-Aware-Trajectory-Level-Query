SELECT
  ROUND(
    (
      1.0 * SUM(__a20_sum) / NULLIF(SUM(__a20_n), 0)
    ) - (
      1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
    ) * (
      1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
    ),
    4
  ) AS "carat_price_cov",
  ROUND(
    (
      (
        1.0 * SUM(__a20_sum) / NULLIF(SUM(__a20_n), 0)
      ) - (
        1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
      ) * (
        1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
      )
    ) / (
      SQRT(
        (
          1.0 * SUM(__a21_sum) / NULLIF(SUM(__a21_n), 0)
        ) - (
          1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
        ) * (
          1.0 * SUM(__a16_sum) / NULLIF(SUM(__a16_n), 0)
        )
      ) * SQRT(
        (
          1.0 * SUM(__a22_sum) / NULLIF(SUM(__a22_n), 0)
        ) - (
          1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
        ) * (
          1.0 * SUM(__a13_sum) / NULLIF(SUM(__a13_n), 0)
        )
      )
    ),
    4
  ) AS "corr_carat_price"
FROM temp."reuse_012_c3";
