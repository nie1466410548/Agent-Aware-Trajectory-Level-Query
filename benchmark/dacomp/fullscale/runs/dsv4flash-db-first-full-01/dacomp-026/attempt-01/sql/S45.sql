SELECT 
  "Route Optimization Status", COUNT(*) AS cnt,
  ROUND(AVG("Delivery Success Rate"),1) AS avg_success,
  ROUND(AVG("Average Delivery Time"),1) AS avg_time
FROM transportation1 tr JOIN disaster_events de ON de."Disaster Event ID" = tr."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
GROUP BY "Route Optimization Status"