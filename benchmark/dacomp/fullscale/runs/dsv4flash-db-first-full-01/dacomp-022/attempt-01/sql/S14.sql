SELECT 
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 2) as overall_completion_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) / COUNT(*), 2) as driver_cancel_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) as customer_cancel_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" IN ('Incomplete','No Driver Found') THEN 1 ELSE 0 END) / COUNT(*), 2) as other_loss_rate
FROM sheet1