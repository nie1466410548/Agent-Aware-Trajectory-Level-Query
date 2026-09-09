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
d2020_6 = d2020[d2020['age_num']>=6].copy()

# ========== 1. NATIONAL DISTRIBUTION ==========
print("========== NATIONAL EDUCATION ATTAINMENT ==========")
for yr, df, sub in [(2000,d2000,d2000),(2010,d2010,d2010),(2020,d2020,d2020_6)]:
    tot = sub['Population Aged 6 and Over - Total' if yr!=2020 else 'Population Aged 3 and Over - Total'].sum()
    print(f"\n{yr} (pop 6+ = {tot:,})")
    if yr==2000:
        cats = ['Never Attended School - Total','Literacy Class - Total','Primary School - Total',
                'Junior High School - Total','Senior High School - Total','Vocational School - Total',
                'Junior College - Total','Undergraduate - Total','Postgraduate - Total']
        labs = ['Never','Literacy','Primary','Junior high','Senior high','Vocational','Junior college','Undergraduate','Postgraduate']
    elif yr==2010:
        cats = ['Never Attended School - Total','Primary School - Total','Junior High School - Total',
                'Senior High School - Total','Junior College - Total','Undergraduate - Total','Postgraduate - Total']
        labs = ['Never','Primary','Junior high','Senior high','Junior college','Undergraduate','Postgraduate']
    else:
        cats = ['ever Attended School - Total','Primary School - Total','Junior High School - Total',
                'Senior High School - Total','Junior College - Total','Undergraduate - Total',
                "Master's Degree - Total",'Doctoral Degree - Total']
        labs = ['Never','Primary','Junior high','Senior high','Junior college','Undergraduate',"Master's",'Doctoral']
    for c,l in zip(cats,labs):
        v = sub[c].sum()
        print(f"  {l:20s}: {v:>10,} ({100*v/tot:.2f}%)")

# ========== 2. GENDER BREAKDOWN ==========
print("\n\n========== GENDER BREAKDOWN ==========")
for yr, df, sub in [(2000,d2000,d2000),(2010,d2010,d2010),(2020,d2020,d2020_6)]:
    tot_col = 'Population Aged 3 and Over - Total' if yr==2020 else 'Population Aged 6 and Over - Total'
    male_col = 'Population Aged 3 and Over - Male' if yr==2020 else 'Population Aged 6 and Over - Male'
    female_col = 'Population Aged 3 and Over - Female' if yr==2020 else 'Population Aged 6 and Over - Female'
    tot = sub[tot_col].sum()
    male_tot = sub[male_col].sum()
    female_tot = sub[female_col].sum()
    print(f"\n{yr} - Male: {male_tot:,} ({100*male_tot/tot:.2f}%), Female: {female_tot:,} ({100*female_tot/tot:.2f}%)")
    if yr==2000:
        # Female columns (no leading space issue)
        fem_cats = {'Never attended': 'Never Attended School - Female',
                    'Primary': 'Primary School - Female',
                    'Junior high': 'Junior High School - Female',
                    'Senior high': 'Senior High School - Female',
                    'Vocational': 'Vocational School - Female',
                    'Junior college': 'Junior College - Female',  # has \xa0 but we cleaned
                    'Undergraduate': 'Undergraduate - Female',
                    'Postgraduate': 'Postgraduate - Female'}
        # Total columns
        tot_cats = {'Never attended': 'Never Attended School - Total',
                    'Primary': 'Primary School - Total',
                    'Junior high': 'Junior High School - Total',
                    'Senior high': 'Senior High School - Total',
                    'Vocational': 'Vocational School - Total',
                    'Junior college': 'Junior College - Total',
                    'Undergraduate': 'Undergraduate - Total',
                    'Postgraduate': 'Postgraduate - Total'}
    elif yr==2010:
        fem_cats = {'Never attended': 'Never Attended School - Female',
                    'Primary': 'Primary School - Female',
                    'Junior high': 'Junior High School - Female',
                    'Senior high': 'Senior High School - Female',
                    'Junior college': 'Junior College - Female',  # has \xa0 but cleaned
                    'Undergraduate': 'Undergraduate - Female',
                    'Postgraduate': 'Postgraduate - Female'}
        tot_cats = {'Never attended': 'Never Attended School - Total',
                    'Primary': 'Primary School - Total',
                    'Junior high': 'Junior High School - Total',
                    'Senior high': 'Senior High School - Total',
                    'Junior college': 'Junior College - Total',
                    'Undergraduate': 'Undergraduate - Total',
                    'Postgraduate': 'Postgraduate - Total'}
    else:
        fem_cats = {'Never attended': 'Never Attended School - Female',
                    'Primary': 'Primary School - Female',
                    'Junior high': 'Junior High School - Female',
                    'Senior high': 'Senior High School - Female',
                    'Junior college': 'Junior College - Female',
                    'Undergraduate': 'Undergraduate - Female',
                    "Master's": "Master's Degree - Female",
                    'Doctoral': 'Doctoral Degree - Female'}
        tot_cats = {'Never attended': 'ever Attended School - Total',
                    'Primary': 'Primary School - Total',
                    'Junior high': 'Junior High School - Total',
                    'Senior high': 'Senior High School - Total',
                    'Junior college': 'Junior College - Total',
                    'Undergraduate': 'Undergraduate - Total',
                    "Master's": "Master's Degree - Total",
                    'Doctoral': 'Doctoral Degree - Total'}
    for lab in fem_cats:
        fv = sub[fem_cats[lab]].sum()
        tv = sub[tot_cats[lab]].sum()
        mv = tv - fv
        fpct = 100*fv/tv if tv>0 else 0
        mpct = 100*mv/tv if tv>0 else 0
        print(f"  {lab:20s}: Male {mv:>10,} ({mpct:.1f}%), Female {fv:>10,} ({fpct:.1f}%)")

# ========== 3. AGE GROUP BREAKDOWN ==========
print("\n\n========== AGE GROUP BREAKDOWN ==========")
def age_group(yr, df, sub):
    tot_col = 'Population Aged 3 and Over - Total' if yr==2020 else 'Population Aged 6 and Over - Total'
    tot = sub[tot_col].sum()
    bins = [0,14,19,24,34,44,54,64,200]
    if yr==2000:
        labs = ['6-14','15-19','20-24','25-34','35-44','45-54','55-64','65+']
    else:
        labs = ['6-14','15-19','20-24','25-34','35-44','45-54','55-64','65+']
    # For 2020, use 6-14 first
    if yr==2020:
        sub['age_bin'] = pd.cut(sub['age_num'], bins=bins, labels=labs, right=True)
    else:
        sub['age_bin'] = pd.cut(sub['age_num'], bins=bins, labels=labs, right=True)
    print(f"\n{yr} Age group higher education (junior college+)")
    for lb in labs:
        grp = sub[sub['age_bin']==lb]
        if len(grp)==0:
            continue
        gtot = grp[tot_col].sum()
        if yr==2000:
            higher = grp['Junior College - Total'].sum() + grp['Undergraduate - Total'].sum() + grp['Postgraduate - Total'].sum()
            no_school = grp['Never Attended School - Total'].sum() + grp['Literacy Class - Total'].sum()
        elif yr==2010:
            higher = grp['Junior College - Total'].sum() + grp['Undergraduate - Total'].sum() + grp['Postgraduate - Total'].sum()
            no_school = grp['Never Attended School - Total'].sum()
        else:
            higher = grp['Junior College - Total'].sum() + grp['Undergraduate - Total'].sum() + grp["Master's Degree - Total"].sum() + grp['Doctoral Degree - Total'].sum()
            no_school = grp['ever Attended School - Total'].sum()
        print(f"  {lb:8s}: pop={gtot:>10,}, higher edu={higher:>10,} ({100*higher/gtot:.1f}%), no schooling={no_school:>10,} ({100*no_school/gtot:.1f}%)")

age_group(2000, d2000, d2000)
age_group(2010, d2010, d2010)
age_group(2020, d2020, d2020_6)

# ========== 4. URBAN/TOWN/RURAL ==========
print("\n\n========== URBAN/TOWN/RURAL EDUCATION ==========")
# Load sub-region tables
d2000_urb = load("2000_cn_pop_6_up_age_sex_eduurb")
d2000_twn = load("2000_cn_twn_pop_6_up_age_sex_ed")
d2000_vil = load("2000cnpop6upagesexeduvillage")
d2010_city = load("2010_cn_city_pop_6_up_age_sex_e")
d2010_town = load("2010_cn_town_pop6up_agesexedu")
d2010_rural = load("2010_cn_rural_6_up_age_sex_edu")
d2020_city = load("2020_cn_city_pop_3_up_age_sex_e")
d2020_town = load("2020_cn_town_pop_3up_agesexedu")
d2020_rural = load("2020_cn_rural_pop_3up_agesexed")

for yr, regions in [(2000,[('Urban',d2000_urb),('Town',d2000_twn),('Village',d2000_vil)]),
                    (2010,[('City',d2010_city),('Town',d2010_town),('Rural',d2010_rural)]),
                    (2020,[('City',d2020_city),('Town',d2020_town),('Rural',d2020_rural)])]:
    print(f"\n{yr}:")
    for rname, rdf in regions:
        if yr==2020:
            rsub = rdf[rdf['age_num']>=6].copy()
            tot = rsub['Population Aged 3 and Over - Total'].sum()
            never = rsub['ever Attended School - Total'].sum()
            primary = rsub['Primary School - Total'].sum()
            junior = rsub['Junior High School - Total'].sum()
            senior = rsub['Senior High School - Total'].sum()
            jcollege = rsub['Junior College - Total'].sum()
            undergrad = rsub['Undergraduate - Total'].sum()
            postgrad = rsub["Master's Degree - Total"].sum() + rsub['Doctoral Degree - Total'].sum()
        else:
            rsub = rdf
            tot = rsub['Population Aged 6 and Over - Total'].sum()
            never = rsub['Never Attended School - Total'].sum()
            primary = rsub['Primary School - Total'].sum()
            junior = rsub['Junior High School - Total'].sum()
            senior = rsub['Senior High School - Total'].sum()
            if yr==2000:
                jcollege = rsub['Junior College - Total'].sum()
                undergrad = rsub['Undergraduate - Total'].sum()
                postgrad = rsub['Postgraduate - Total'].sum()
            else:
                jcollege = rsub['Junior College - Total'].sum()
                undergrad = rsub['Undergraduate - Total'].sum()
                postgrad = rsub['Postgraduate - Total'].sum()
        higher = jcollege + undergrad + postgrad
        print(f"  {rname:10s}: pop={tot:>10,}, never={never:>10,}({100*never/tot:.1f}%), primary={primary:>10,}({100*primary/tot:.1f}%), junior={junior:>10,}({100*junior/tot:.1f}%), senior={senior:>10,}({100*senior/tot:.1f}%), higher={higher:>10,}({100*higher/tot:.1f}%)")

print("\n\nDone!")