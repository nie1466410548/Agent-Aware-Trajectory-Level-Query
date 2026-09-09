# Build national distribution table
def national_dist(df, year, ages='6plus'):
    sub = df if ages=='3plus' else df[df['age_num']>=6].copy()
    tot = sub['Population Aged 6 and Over - Total' if 'Population Aged 6 and Over - Total' in sub.columns else 'Population Aged 3 and Over - Total'].sum()
    levels = {}
    levels['Never attended'] = sub['Never Attended School - Total'].sum() if 'Never Attended School - Total' in sub.columns else sub['ever Attended School - Total'].sum()
    if year==2000:
        levels['Literacy class'] = sub['Literacy Class - Total'].sum()
    levels['Primary'] = sub['Primary School - Total'].sum()
    levels['Junior high'] = sub['Junior High School - Total'].sum()
    if year==2000:
        levels['Senior high + Voc'] = sub['Senior High School - Total'].sum() + sub['Vocational School - Total'].sum()
    else:
        levels['Senior high'] = sub['Senior High School - Total'].sum()
    levels['Junior college'] = sub['Junior College - Total'].sum()
    levels['Undergraduate'] = sub['Undergraduate - Total'].sum()
    if year==2000:
        levels['Postgraduate'] = sub['Postgraduate - Total'].sum()
    elif year==2010:
        levels['Postgraduate'] = sub['Postgraduate - Total'].sum()
    else:
        levels['Postgraduate'] = sub["Master's Degree - Total"].sum() + sub['Doctoral Degree - Total'].sum()
    return tot, levels

dist = {}
for yr, df in [(2000,d2000),(2010,d2010),(2020,d2020)]:
    tot, levels = national_dist(df, yr)
    dist[yr] = (tot, levels)
    print(f"===== {yr} (pop 6+ = {tot:,}) =====")
    for k,v in levels.items():
        print(f"  {k}: {v:>15,}  ({100*v/tot:.2f}%)")

# Save for later
import json
json.dump({str(k):{'tot':v[0],'levels':v[1]} for k,v in dist.items()}, open('/work/dist_national.json','w'))