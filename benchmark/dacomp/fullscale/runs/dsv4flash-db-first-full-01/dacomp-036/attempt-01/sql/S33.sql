SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       COUNT(DISTINCT ip."IP Record ID") AS ip_records,
       COUNT(DISTINCT ip."IP Address") AS distinct_ips,
       COUNT(DISTINCT ip."Province") AS provinces
FROM ip_address_information_table ip
JOIN login_records_table lr ON ip."Login record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY distinct_ips DESC