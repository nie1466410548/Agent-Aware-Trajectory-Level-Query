import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score

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
df_rd['update_rate'] = df_rd['updates'] / df_rd['actives'] * 1000  # per 1000 active devices

print("Region×Device data shape:", df_rd.shape)
print("Regions:", df_rd['region'].unique())
print("Devices:", df_rd['device'].unique()[:5], "...")
print()

# Load region×package monthly data with quality/crash
rows = []
with open('/results/S15.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df_rp = pd.DataFrame(rows)
df_rp['month_dt'] = pd.to_datetime(df_rp['month'] + '-01')
df_rp['month_num'] = (df_rp['month_dt'] - df_rp['month_dt'].min()).dt.days / 30.0
print("Region×Package data shape:", df_rp.shape)

# Load package monthly time series
rows = []
with open('/results/S13.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df_ts = pd.DataFrame(rows)
df_ts['month_dt'] = pd.to_datetime(df_ts['month'] + '-01')
df_ts['month_num'] = (df_ts['month_dt'] - df_ts['month_dt'].min()).dt.days / 30.0
print("Time series data shape:", df_ts.shape)

print("\nSample data:")
print(df_rd.head(2))
print(df_rp.head(2))
print(df_ts.head(2))