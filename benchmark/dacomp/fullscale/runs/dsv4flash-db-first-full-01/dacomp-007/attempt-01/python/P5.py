import pandas as pd
import numpy as np

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)

# Clean comparison R&D vs Sales for job levels 1 and 2
def summarize(sub, factor):
    g = sub.groupby(['Department', factor])['is_attrition'].agg(['count','mean'])
    g['rate'] = (g['mean']*100).round(1)
    return g.reset_index().pivot(index=factor, columns='Department', values='rate'), \
           g.reset_index().pivot(index=factor, columns='Department', values='count')

for lvl in [1,2]:
    sub = df[(df['Department'].isin(['Research & Development','Sales'])) & (df['JobLevel']==lvl)]
    print(f"\n{'='*60}\nJOB LEVEL {lvl} (R&D vs Sales only)\n{'='*60}")
    for f in ['OverTime','MaritalStatus','StockOptionLevel','JobSatisfaction','WorkLifeBalance','BusinessTravel','EnvironmentSatisfaction','JobInvolvement','RelationshipSatisfaction']:
        r, c = summarize(sub, f)
        print(f"\n-- {f} attrition rate % (count) --")
        for idx in r.index:
            rdv = r.loc[idx].get('Research & Development', np.nan)
            slv = r.loc[idx].get('Sales', np.nan)
            rdc = c.loc[idx].get('Research & Development', np.nan)
            slc = c.loc[idx].get('Sales', np.nan)
            print(f"  {idx}: R&D={rdv}% (n={rdc})  Sales={slv}% (n={slc})")