import pandas as pd
import datetime

rows = db.query("SELECT _id, \"Main Category\", \"Rank\" FROM sheet1")
df = db.frame(rows)

def decode_ts(oid):
    try:
        ts = int(oid[:8], 16)
        return datetime.datetime.utcfromtimestamp(ts)
    except:
        return None

df['dt'] = df['_id'].apply(decode_ts)
print("Distinct timestamps (months) across dataset:")
print(df['dt'].dt.to_period('M').value_counts().sort_index())

# Check how many periods per main category
df['period'] = df['dt'].dt.to_period('M')
print("\nPeriods per Main Category:")
print(df.groupby(['Main Category','period']).size().unstack(fill_value=0).shape)
print(df.groupby('period')['Main Category'].nunique())