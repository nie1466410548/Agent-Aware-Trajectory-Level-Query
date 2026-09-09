import pandas as pd
import numpy as np
import json

def load(tbl):
    res = db.query(f'SELECT * FROM "{tbl}"')
    df = db.frame(res)
    df.columns = [c.replace('\xa0',' ').strip() for c in df.columns]
    age = df['Age'].astype(str).str.extract(r'(\d+)')[0].astype(float)
    df['age_num'] = age
    for c in df.columns:
        if c not in ('Age','age_num'):
            df[c] = pd.to_numeric(df[c].astype(str).str.strip().replace({'':'0','nan':'0','None':'0'}), errors='coerce').fillna(0).astype(np.int64)
    return df

d2000 = load("2000_cn_pop_6_up_age_sex_edu")
d2010 = load("2010_cn_pop_6_up_age_sex_edu")
d2020 = load("2020_cn_pop_3_up_age_sex_edu")

# National distribution
for yr, df in [(2000,d2000),(2010,d2010),(2020,d2020)]:
    sub = df if yr==2020 else df
    if yr==2020:
        sub = df[df['age_num']>=6].copy()
    tot = sub['Population Aged 6 and Over - Total' if yr!=2020 else 'Population Aged 3 and Over - Total'].sum()
    print(f"===== {yr} (pop 6+ = {tot:,}) =====")
    if yr==2000:
        cats = ['Never Attended School - Total','Literacy Class - Total','Primary School - Total',
                'Junior High School - Total','Senior High School - Total','Vocational School - Total',
                'Junior College - Total','Undergraduate - Total','Postgraduate - Total']
        labels = ['Never attended','Literacy class','Primary','Junior high','Senior high','Vocational','Junior college','Undergraduate','Postgraduate']
    elif yr==2010:
        cats = ['Never Attended School - Total','Primary School - Total','Junior High School - Total',
                'Senior High School - Total','Junior College - Total','Undergraduate - Total','Postgraduate - Total']
        labels = ['Never attended','Primary','Junior high','Senior high','Junior college','Undergraduate','Postgraduate']
    else:
        cats = ['ever Attended School - Total','Primary School - Total','Junior High School - Total',
                'Senior High School - Total','Junior College - Total','Undergraduate - Total',
                "Master's Degree - Total",'Doctoral Degree - Total']
        labels = ['Never attended','Primary','Junior high','Senior high','Junior college','Undergraduate','Master\'s','Doctoral']
    for c,l in zip(cats,labels):
        v = sub[c].sum()
        print(f"  {l:20s}: {v:>12,}  ({100*v/tot:.2f}%)")