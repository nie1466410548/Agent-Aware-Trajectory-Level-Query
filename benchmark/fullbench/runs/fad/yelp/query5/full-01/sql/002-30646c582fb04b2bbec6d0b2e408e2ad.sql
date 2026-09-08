SELECT business_ref, COUNT(*) c, AVG(rating) ar FROM review GROUP BY business_ref ORDER BY c DESC LIMIT 30
