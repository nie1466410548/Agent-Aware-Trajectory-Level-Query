# Gender breakdown
def gender_dist(df, yr):
    sub = df if yr!=2020 else df[df['age_num']>=6].copy()
    tot_col = 'Population Aged 3 and Over - Total' if yr==2020 else 'Population Aged 6 and Over - Total'
    male_col = 'Population Aged 3 and Over - Male' if yr==2020 else 'Population Aged 6 and Over - Male'
    female_col = 'Population Aged 3 and Over - Female' if yr==2020 else 'Population Aged 6 and Over - Female'
    tot = sub[tot_col].sum()
    male_tot = sub[male_col].sum()
    female_tot = sub[female_col].sum()
    
    print(f"===== {yr} Gender =====")
    print(f"Total: {tot:,}; Male: {male_tot:,} ({100*male_tot/tot:.2f}%); Female: {female_tot:,} ({100*female_tot/tot:.2f}%)")
    print()
    
    if yr==2000:
        cats = ['Never Attended School - Total','Never Attended School - Female','Literacy Class - Total',
                'Primary School - Total','Primary School - Female',
                'Junior High School - Total','Junior High School - Female',
                'Senior High School - Total','Senior High School - Female',
                'Vocational School - Total','Vocational School - Female',
                'Junior College - Total','Junior College - Female',
                'Undergraduate - Total','Undergraduate - Female',
                'Postgraduate - Total','Postgraduate - Female']
        labels = ['Never','Never(F)','Literacy','Primary','Primary(F)',
                  'Junior high','Junior high(F)','Senior high','Senior high(F)',
                  'Vocational','Vocational(F)','Junior college','Junior college(F)',
                  'Undergraduate','Undergraduate(F)','Postgraduate','Postgraduate(F)']
    elif yr==2010:
        cats = ['Never Attended School - Total','Never Attended School - Female',
                'Primary School - Total','Primary School - Female',
                'Junior High School - Total','Junior High School - Female',
                'Senior High School - Total','Senior High School - Female',
                'Junior College - Total','Junior College - Female',
                'Undergraduate - Total','Undergraduate - Female',
                'Postgraduate - Total','Postgraduate - Female']
        labels = ['Never','Never(F)','Primary','Primary(F)',
                  'Junior high','Junior high(F)','Senior high','Senior high(F)',
                  'Junior college','Junior college(F)','Undergraduate','Undergraduate(F)',
                  'Postgraduate','Postgraduate(F)']
    else:
        cats = ['ever Attended School - Total','Never Attended School - Female',
                'Primary School - Total','Primary School - Female',
                'Junior High School - Total','Junior High School - Female',
                'Senior High School - Total','Senior High School - Female',
                'Junior College - Total','Junior College - Female',
                'Undergraduate - Total','Undergraduate - Female',
                "Master's Degree - Total","Master's Degree - Female",
                'Doctoral Degree - Total','Doctoral Degree - Female']
        labels = ['Never','Never(F)','Primary','Primary(F)',
                  'Junior high','Junior high(F)','Senior high','Senior high(F)',
                  'Junior college','Junior college(F)','Undergraduate','Undergraduate(F)',
                  "Master's","Master's(F)",'Doctoral','Doctoral(F)']
    
    for c,l in zip(cats,labels):
        v = sub[c].sum()
        if '(F)' in l:
            pct = 100*v/sub[cats[labels.index(l.replace('(F)',''))]].sum() if sub[cats[labels.index(l.replace('(F)',''))]].sum()>0 else 0
            print(f"  {l:20s}: {v:>10,}  ({pct:.1f}% of total)")
        else:
            print(f"  {l:20s}: {v:>10,}  ({100*v/tot:.2f}%)")

gender_dist(d2000,2000)
gender_dist(d2010,2010)
gender_dist(d2020,2020)