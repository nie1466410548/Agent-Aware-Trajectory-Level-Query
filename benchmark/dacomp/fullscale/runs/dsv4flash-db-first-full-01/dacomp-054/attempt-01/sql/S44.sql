-- Check if customer360_id relates to marketo_lead_id, stripe_customer_id, or zendesk_user_id
-- First, let's see if there's a pattern
SELECT customer360_id, source_system, address_type, priority, rank
FROM customer360__address
WHERE customer360_id = '7eed12549eff566d1179fc92b723bc9c'
ORDER BY source_system, address_type