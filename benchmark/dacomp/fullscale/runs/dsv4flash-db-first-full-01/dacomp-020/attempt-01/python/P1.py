
import json, numpy as np, pandas as pd
from scipy import stats

# Load all rows from the archived result
rows = []
with open('results/S3.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))

cols = ["Student ID","Age","Gender","Daily study time","Social media usage time","Part-time job",
        "Attendance rate","Sleep duration","Diet quality","Exercise frequency","Parents' education level",
        "Internet quality","Mental health score","Extracurricular activity participation","Exam score"]
df = pd.DataFrame(rows, columns=cols)
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
