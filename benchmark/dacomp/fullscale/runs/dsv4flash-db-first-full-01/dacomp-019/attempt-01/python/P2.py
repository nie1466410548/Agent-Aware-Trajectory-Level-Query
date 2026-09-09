import pandas as pd
import numpy as np
from datetime import datetime

# Load the archived query result (Imported + Joint-venture, 264 rows)
df = pd.read_json('/results/S29.rows.jsonl', lines=True)
print(df.shape)
print(df.columns.tolist())
print(df['origin'].value_counts())
print(df['inv_status'].value_counts())
print(df['alert_status'].value_counts())
print(df.dtypes)
