import json

def cols(tbl):
    r = db.query(f"SELECT * FROM \"{tbl}\" LIMIT 1")
    # get column names from execution metadata
    execs = r['executions'][0]
    print(tbl)
    for c in execs['columns']:
        print(repr(c))
    print('---')

for t in ["2000_cn_pop_6_up_age_sex_edu","2010_cn_pop_6_up_age_sex_edu","2020_cn_pop_3_up_age_sex_edu"]:
    cols(t)
