import pandas as pd
import numpy as np

result = db.query("SELECT * FROM sheet1 WHERE EmpID IN (SELECT EmpID FROM sheet1 GROUP BY EmpID HAVING COUNT(*)>1) ORDER BY EmpID")
dup = db.frame(result)
print(dup[['EmpID','Department','JobRole','Attrition','MonthlyIncome','JobLevel','Age']].sort_values('EmpID').to_string())
print(f"\nRows: {len(dup)}")