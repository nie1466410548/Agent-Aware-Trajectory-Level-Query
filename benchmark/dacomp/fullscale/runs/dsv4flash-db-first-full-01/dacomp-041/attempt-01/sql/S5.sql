SELECT COUNT(*) as total_halls, 
       AVG("Daily Visitor Count") as avg_visitor, 
       MAX("Daily Visitor Count") as max_visitor, 
       MIN("Daily Visitor Count") as min_visitor
FROM gallery_information