-- company_metrics: distribution of registration retention
SELECT 
  AVG(registration_retention_7d) as avg_ret7, AVG(registration_retention_30d) as avg_ret30,
  AVG(contacts_active_7d) as avg_act7, AVG(contacts_active_30d) as avg_act30
FROM intercom__company_metrics