
  SELECT customer360_id, COUNT(*) cnt FROM customer360__address 
  WHERE source_system='marketo' GROUP BY customer360_id ORDER BY cnt DESC LIMIT 10
