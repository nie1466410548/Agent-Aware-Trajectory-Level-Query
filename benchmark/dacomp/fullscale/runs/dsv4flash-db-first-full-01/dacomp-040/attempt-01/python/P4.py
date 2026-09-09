import pandas as pd
import numpy as np

def load(tbl):
    res = db.query(f'SELECT * FROM "{tbl}"')
    df = db.frame(res)
    # normalize column names: strip non-breaking and regular spaces at start/end
    df.columns = [c.replace('\xa0',' ').strip() for c in df.columns]
    # age numeric
    age = df['Age'].astype(str).str.extract(r'(\d+)')[0].astype(float)
    # 65+ and 85+ rows
    df['age_num'] = age
    for c in df.columns:
        if c != 'Age' and c != 'age_num':
            df[c] = pd.to_numeric(df[c].astype(str).str.strip().replace({'':'0', 'nan':'0', 'None':'0'}), errors='coerce').fillna(0).astype(np.int64)
    return df

d2000 = load("2000_cn_pop_6_up_age_sex_edu")
d2010 = load("2010_cn_pop_6_up_age_sex_edu")
d2020 = load("2020_cn_pop_3_up_age_sex_edu")

print("2000 total pop:", d2000['Population Aged 6 and Over - Total'].sum())
print("2010 total pop:", d2010['Population Aged 6 and Over - Total'].sum())
print("2020 total pop(3+):", d2020['Population Aged 3 and Over - Total'].sum())
print("2020 total pop(6+):", d2020.loc[d2020['age_num']>=6,'Population Aged 3 and Over - Total'].sum())

# Verify sum of education categories for 2000
cols2000 = ['Never Attended School - Total','Literacy Class - Total','Primary School - Total','Junior High School - Total','Senior High School - Total','Vocational School - Total','Junior College - Total','Undergraduate - Total','Postgraduate - Total']
print("2000 cat sum:", d2000[cols2000].sum().sum(), "vs total:", d2000['Population Aged 6 and Over - Total'].sum())

cols2010 = ['Never Attended School - Total','Primary School - Total','Junior High School - Total','Senior High School - Total','Junior College - Total','Undergraduate - Total','Postgraduate - Total']
print("2010 cat sum:", d2010[cols2010].sum().sum(), "vs total:", d2010['Population Aged 6 and Over - Total'].sum())

cols2020 = ['ever Attended School - Total','Primary School - Total','Junior High School - Total','Senior High School - Total','Junior College - Total','Undergraduate - Total',"Master's Degree - Total",'Doctoral Degree - Total']
sub = d2020[d2020['age_num']>=6]
print("2020 cat sum(6+):", sub[cols2020].sum().sum(), "vs total:", sub['Population Aged 3 and Over - Total'].sum())
# also preschool
print("2020 preschool(6+):", sub['Preschool - Total'].sum())
print("2020 never+preschool+cat(6+):", sub[cols2020].sum().sum()+sub['Preschool - Total'].sum())