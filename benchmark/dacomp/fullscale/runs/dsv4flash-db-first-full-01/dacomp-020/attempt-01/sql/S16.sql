SELECT 
  MIN("Daily study time") as mn_study, MAX("Daily study time") as mx_study, AVG("Daily study time") as avg_study,
  MIN("Social media usage time") as mn_sm, MAX("Social media usage time") as mx_sm, AVG("Social media usage time") as avg_sm,
  MIN("Attendance rate") as mn_att, MAX("Attendance rate") as mx_att, AVG("Attendance rate") as avg_att,
  MIN("Sleep duration") as mn_sleep, MAX("Sleep duration") as mx_sleep, AVG("Sleep duration") as avg_sleep,
  MIN("Exercise frequency") as mn_ex, MAX("Exercise frequency") as mx_ex, AVG("Exercise frequency") as avg_ex,
  MIN("Age") as mn_age, MAX("Age") as mx_age, AVG("Age") as avg_age
FROM sheet1