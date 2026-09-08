import json, pandas as pd
R = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-006/pilot-01/results/"
sc_prod = pd.DataFrame(json.load(open(R+"91c3b0c7572b44eb898eca77acc81baf.json")))
p2 = sc_prod.pivot_table(index="month", columns="product", values="profit", aggfunc="sum").fillna(0).sort_index()
share = (p2.sum()/p2.sum().sum()*100).sort_values(ascending=False)
print("Product share of SC annual profit (%):")
print(share.round(1).to_string())
print("\nOffice furniture monthly profit:")
print(p2["Office furniture"].round(0).to_string())
print("\nKitchen Appliances monthly profit:")
print(p2["Kitchen Appliances"].round(0).to_string())
