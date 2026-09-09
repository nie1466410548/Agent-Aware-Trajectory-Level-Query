import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load all data
rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nNull counts:\n{df.isnull().sum()}")
print(f"\nExam score basic stats:\n{df['Exam score'].describe()}")
print(f"\nParent education value counts:\n{df['Parents education level'].value_counts()}")