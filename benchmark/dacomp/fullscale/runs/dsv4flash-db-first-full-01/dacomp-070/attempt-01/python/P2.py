import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load region×device monthly data
rows = []
with open('/results/S14.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df_rd = pd.DataFrame(rows)
df_rd['month_dt'] = pd.to_datetime(df_rd['month'] + '-01')
df_rd['month_num'] = (df_rd['month_dt'] - df_rd['month_dt'].min()).dt.days / 30.0
df_rd['conv_rate'] = 100.0 * df_rd['acquisitions'] / df_rd['visitors']
df_rd['cost_per_acq'] = df_rd['visitors'] / df_rd['acquisitions']
df_rd['installs_per_acq'] = df_rd['installs'] / df_rd['acquisitions']
df_rd['update_rate'] = df_rd['updates'] / df_rd['actives'] * 1000

print("Region×Device data shape:", df_rd.shape)
print("Regions:", df_rd['region'].unique())
print("N devices:", df_rd['device'].nunique())
print()

rows = []
with open('/results/S15.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df_rp = pd.DataFrame(rows)
df_rp['month_dt'] = pd.to_datetime(df_rp['month'] + '-01')
df_rp['month_num'] = (df_rp['month_dt'] - df_rp['month_dt'].min()).dt.days / 30.0
print("Region×Package data shape:", df_rp.shape)

rows = []
with open('/results/S13.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df_ts = pd.DataFrame(rows)
df_ts['month_dt'] = pd.to_datetime(df_ts['month'] + '-01')
df_ts['month_num'] = (df_ts['month_dt'] - df_ts['month_dt'].min()).dt.days / 30.0
print("Time series shape:", df_ts.shape)

# Save as CSVs in /work for reuse
df_rd.to_csv('/work/region_device_monthly.csv', index=False)
df_rp.to_csv('/work/region_package_monthly.csv', index=False)
df_ts.to_csv('/work/package_monthly.csv', index=False)

# Check package-level maturity info: use full period wow install growth
print("\nMonthly wow install growth by package (avg over months):")
print(df_ts.groupby('package_name')[['wow_inst','wow_rev','active','rpad','quality','crash']].mean().round(4))