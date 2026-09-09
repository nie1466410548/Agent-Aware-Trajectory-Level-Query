SELECT p.Age, e."Treatment Barriers", e."Patient Reference Number"
FROM encounters e
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
LIMIT 20