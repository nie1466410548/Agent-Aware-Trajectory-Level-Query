
import numpy as np
import pandas as pd
from scipy import stats

# ---- Favorites category contingency ----
fav_hv = {"Clothing, Shoes & Hats":37,"Sports & Outdoors":36,"Home & Living":31,"Food & Beverages":29,"beauty & skincare":27,"Home Appliances":25,"Digital 3C":20}
fav_reg = {"Clothing, Shoes & Hats":19,"Food & Beverages":17,"Home Appliances":17,"Sports & Outdoors":17,"Digital 3C":16,"beauty & skincare":14,"Home & Living":13}
cats = sorted(set(fav_hv) | set(fav_reg))
cont = np.array([[fav_hv.get(c,0) for c in cats],[fav_reg.get(c,0) for c in cats]])
chi2, p, dof, _ = stats.chi2_contingency(cont)
print("=== Favorites Category chi-square ===")
print(f"chi2={chi2:.2f}, dof={dof}, p={p:.4f}")
print("HV shares:", [f"{c}:{fav_hv.get(c,0)/sum(fav_hv.values()):.3f}" for c in cats])
print("Reg shares:", [f"{c}:{fav_reg.get(c,0)/sum(fav_reg.values()):.3f}" for c in cats])

# ---- Browsing category contingency ----
br_hv = {"Clothing, Shoes & Hats":40,"Sports & Outdoors":37,"Home & Living":36,"Home Appliances":34,"Food & Beverages":32,"beauty & skincare":31,"Digital 3C":23}
br_reg = {"Food & Beverages":22,"Clothing, Shoes & Hats":21,"Sports & Outdoors":20,"beauty & skincare":19,"Home Appliances":18,"Digital 3C":17,"Home & Living":15}
cats2 = sorted(set(br_hv) | set(br_reg))
cont2 = np.array([[br_hv.get(c,0) for c in cats2],[br_reg.get(c,0) for c in cats2]])
chi2b, pb, dofb, _ = stats.chi2_contingency(cont2)
print("\n=== Browsing Category chi-square ===")
print(f"chi2={chi2b:.2f}, dof={dofb}, p={pb:.4f}")
print("HV shares:", [f"{c}:{br_hv.get(c,0)/sum(br_hv.values()):.3f}" for c in cats2])
print("Reg shares:", [f"{c}:{br_reg.get(c,0)/sum(br_reg.values()):.3f}" for c in cats2])

# ---- Search keyword mapped to categories ----
# keyword -> category mapping
kw_cat = {
 "Bluetooth speaker":"Digital 3C","Wireless Mouse":"Digital 3C","Mechanical keyboard":"Digital 3C",
 "Apple phone":"Digital 3C","Huawei laptop":"Digital 3C","Coffee machine":"Home Appliances",
 "air fryer":"Home Appliances","down jacket":"Clothing, Shoes & Hats","Children's schoolbag":"Clothing, Shoes & Hats",
 "hiking backpack":"Sports & Outdoors","sneakers":"Sports & Outdoors","Fitness equipment":"Sports & Outdoors",
 "toothbrush":"beauty & skincare"}
sh_hv = {"toothbrush":24,"Apple phone":21,"Coffee machine":21,"Bluetooth speaker":19,"Children's schoolbag":18,"Wireless Mouse":18,"Mechanical keyboard":16,"hiking backpack":16,"air fryer":15,"down jacket":14,"Huawei laptop":13,"sneakers":11,"Fitness equipment":10}
sh_reg = {"sneakers":14,"Bluetooth speaker":13,"Wireless Mouse":12,"down jacket":12,"Children's schoolbag":9,"toothbrush":9,"Coffee machine":8,"Mechanical keyboard":8,"Apple phone":7,"Fitness equipment":7,"air fryer":7,"hiking backpack":6,"Huawei laptop":5}
def to_cat_counts(d):
    out = {}
    for k,v in d.items():
        c = kw_cat.get(k, "Other")
        out[c] = out.get(c,0)+v
    return out
sc_hv = to_cat_counts(sh_hv); sc_reg = to_cat_counts(sh_reg)
cats3 = sorted(set(sc_hv)|set(sc_reg))
cont3 = np.array([[sc_hv.get(c,0) for c in cats3],[sc_reg.get(c,0) for c in cats3]])
chi2s, ps, dofs, _ = stats.chi2_contingency(cont3)
print("\n=== Search Category chi-square ===")
print(f"chi2={chi2s:.2f}, dof={dofs}, p={ps:.4f}")
print("HV shares:", [f"{c}:{sc_hv.get(c,0)/sum(sc_hv.values()):.3f}" for c in cats3])
print("Reg shares:", [f"{c}:{sc_reg.get(c,0)/sum(sc_reg.values()):.3f}" for c in cats3])

# ---- Favorites brand contingency ----
fb_hv = {"Haier Smart Home Co., Ltd.":46,"BYD Co., Ltd.":40,"Tsingtao Brewery Co., Ltd.":35,"Xizang Nuodikang Pharmaceutical Co., Ltd.":34,"Kweichow Moutai Co., Ltd.":29,"Yunnan Baiyao Group Co., Ltd.":21}
fb_reg = {"Haier Smart Home Co., Ltd.":25,"Kweichow Moutai Co., Ltd.":22,"BYD Co., Ltd.":18,"Tsingtao Brewery Co., Ltd.":17,"Yunnan Baiyao Group Co., Ltd.":17,"Xizang Nuodikang Pharmaceutical Co., Ltd.":14}
brands = sorted(set(fb_hv)|set(fb_reg))
cont4 = np.array([[fb_hv.get(b,0) for b in brands],[fb_reg.get(b,0) for b in brands]])
chi2f, pf, doff, _ = stats.chi2_contingency(cont4)
print("\n=== Favorites Brand chi-square ===")
print(f"chi2={chi2f:.2f}, dof={doff}, p={pf:.4f}")
print("HV shares:", [f"{b}:{fb_hv.get(b,0)/sum(fb_hv.values()):.3f}" for b in brands])
print("Reg shares:", [f"{b}:{fb_reg.get(b,0)/sum(fb_reg.values()):.3f}" for b in brands])

# Save key structures for plotting
np.save('/work/fav_cats.npy', {'hv':fav_hv,'reg':fav_reg,'cats':cats})
np.save('/work/br_cats.npy', {'hv':br_hv,'reg':br_reg,'cats':cats2})
np.save('/work/sc_cats.npy', {'hv':sc_hv,'reg':sc_reg,'cats':cats3})
np.save('/work/fb_brands.npy', {'hv':fb_hv,'reg':fb_reg,'brands':brands})
print("\nDone saving")
