SELECT MIN(first_event_on) AS min_first, MAX(last_event_on) AS max_last,
  MIN(last_visit) AS min_last_visit, MAX(last_visit) AS max_last_visit,
  MIN(first_visit_at) AS min_first_visit, MAX(last_updated_at) AS max_updated
FROM pendo__visitor