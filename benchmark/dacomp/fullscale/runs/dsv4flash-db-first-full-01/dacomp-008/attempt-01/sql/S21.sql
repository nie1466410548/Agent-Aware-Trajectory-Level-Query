SELECT
  ROUND((SUM(dev * team) - SUM(dev)*SUM(team)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(team*team) - SUM(team)*SUM(team)/COUNT(*))), 0), 4) as corr_dev_team,
  ROUND((SUM(dev * sat) - SUM(dev)*SUM(sat)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(sat*sat) - SUM(sat)*SUM(sat)/COUNT(*))), 0), 4) as corr_dev_sat,
  ROUND((SUM(dev * budget) - SUM(dev)*SUM(budget)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(budget*budget) - SUM(budget)*SUM(budget)/COUNT(*))), 0), 4) as corr_dev_budget
FROM (
  SELECT 
    "Budget Amount" - "Actual Cost" as dev,
    "Team Size" as team,
    "Customer Satisfaction" as sat,
    "Budget Amount" as budget
  FROM sheet1
  WHERE "Project Status" = 'Completed'
)