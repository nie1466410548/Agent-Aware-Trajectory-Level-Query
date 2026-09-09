
    SELECT primary_state AS state, COUNT(*) AS n_reps
    FROM (
      SELECT owner_id, billing_state AS primary_state
      FROM (
        SELECT owner_id, billing_state, COUNT(*) AS cnt,
               ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
        FROM salesforce__account_daily_history
        WHERE billing_state IS NOT NULL
        GROUP BY owner_id, billing_state
      ) t
      WHERE rn = 1
    ) r
    GROUP BY primary_state
