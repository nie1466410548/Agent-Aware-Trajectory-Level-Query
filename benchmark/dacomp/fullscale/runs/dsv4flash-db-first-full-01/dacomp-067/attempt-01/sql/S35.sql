SELECT MAX(has_interviewed_w_hiring_manager) as max_hm, 
       MIN(has_interviewed_w_hiring_manager) as min_hm,
       SUM(has_interviewed_w_hiring_manager) as sum_hm
FROM greenhouse__application_enhanced