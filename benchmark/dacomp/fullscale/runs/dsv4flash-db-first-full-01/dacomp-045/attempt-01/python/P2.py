import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick

# Style settings
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

# ========== 1. Favorites Category Comparison ==========
fav_hv = {"Clothing, Shoes & Hats":37,"Sports & Outdoors":36,"Home & Living":31,"Food & Beverages":29,"beauty & skincare":27,"Home Appliances":25,"Digital 3C":20}
fav_reg = {"Clothing, Shoes & Hats":19,"Food & Beverages":17,"Home Appliances":17,"Sports & Outdoors":17,"Digital 3C":16,"beauty & skincare":14,"Home & Living":13}
cats = sorted(set(fav_hv) | set(fav_reg))
hv_pct = [fav_hv.get(c,0)/sum(fav_hv.values())*100 for c in cats]
reg_pct = [fav_reg.get(c,0)/sum(fav_reg.values())*100 for c in cats]

fig, ax = plt.subplots(figsize=(14,6))
x = np.arange(len(cats))
w = 0.35
bars1 = ax.bar(x-w/2, hv_pct, w, label='High-Value (Diamond/Platinum)', color='#2E86AB', alpha=0.85)
bars2 = ax.bar(x+w/2, reg_pct, w, label='Regular', color='#A23B72', alpha=0.85)
ax.set_ylabel('Percentage of Favorites (%)', fontweight='bold')
ax.set_title('Favorite Category Preferences: High-Value vs Regular Users', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([c.replace(' & ','\n') for c in cats], fontsize=9)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/fav_categories.png', dpi=150)
plt.close()
print("Saved fav_categories.png")

# ========== 2. Browsing Category Comparison ==========
br_hv = {"Clothing, Shoes & Hats":40,"Sports & Outdoors":37,"Home & Living":36,"Home Appliances":34,"Food & Beverages":32,"beauty & skincare":31,"Digital 3C":23}
br_reg = {"Food & Beverages":22,"Clothing, Shoes & Hats":21,"Sports & Outdoors":20,"beauty & skincare":19,"Home Appliances":18,"Digital 3C":17,"Home & Living":15}
cats2 = sorted(set(br_hv) | set(br_reg))
hv_pct2 = [br_hv.get(c,0)/sum(br_hv.values())*100 for c in cats2]
reg_pct2 = [br_reg.get(c,0)/sum(br_reg.values())*100 for c in cats2]

fig, ax = plt.subplots(figsize=(14,6))
x = np.arange(len(cats2))
bars1 = ax.bar(x-w/2, hv_pct2, w, label='High-Value (Diamond/Platinum)', color='#2E86AB', alpha=0.85)
bars2 = ax.bar(x+w/2, reg_pct2, w, label='Regular', color='#A23B72', alpha=0.85)
ax.set_ylabel('Percentage of Browsing Views (%)', fontweight='bold')
ax.set_title('Browsing Category Preferences: High-Value vs Regular Users', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([c.replace(' & ','\n') for c in cats2], fontsize=9)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/br_categories.png', dpi=150)
plt.close()
print("Saved br_categories.png")

# ========== 3. Search Category Comparison ==========
kw_cat = {
 "Bluetooth speaker":"Digital 3C","Wireless Mouse":"Digital 3C","Mechanical keyboard":"Digital 3C",
 "Apple phone":"Digital 3C","Huawei laptop":"Digital 3C","Coffee machine":"Home Appliances",
 "air fryer":"Home Appliances","down jacket":"Clothing, Shoes & Hats","Children's schoolbag":"Clothing, Shoes & Hats",
 "hiking backpack":"Sports & Outdoors","sneakers":"Sports & Outdoors","Fitness equipment":"Sports & Outdoors",
 "toothbrush":"beauty & skincare"}
sh_hv = {"toothbrush":24,"Apple phone":21,"Coffee machine":21,"Bluetooth speaker":19,"Children's schoolbag":18,"Wireless Mouse":18,"Mechanical keyboard":16,"hiking backpack":16,"air fryer":15,"down jacket":14,"Huawei laptop":13,"sneakers":11,"Fitness equipment":10}
sh_reg = {"sneakers":14,"Bluetooth speaker":13,"Wireless Mouse":12,"down jacket":12,"Children's schoolbag":9,"toothbrush":9,"Coffee machine":8,"Mechanical keyboard":8,"Apple phone":7,"Fitness equipment":7,"air fryer":7,"hiking backpack":6,"Huawei laptop":5}
def to_cat(d):
    out={}
    for k,v in d.items():
        c=kw_cat.get(k,"Other")
        out[c]=out.get(c,0)+v
    return out
sc_hv=to_cat(sh_hv); sc_reg=to_cat(sh_reg)
cats3=sorted(set(sc_hv)|set(sc_reg))
hv_pct3=[sc_hv.get(c,0)/sum(sc_hv.values())*100 for c in cats3]
reg_pct3=[sc_reg.get(c,0)/sum(sc_reg.values())*100 for c in cats3]

fig, ax = plt.subplots(figsize=(10,6))
x = np.arange(len(cats3))
bars1 = ax.bar(x-w/2, hv_pct3, w, label='High-Value (Diamond/Platinum)', color='#2E86AB', alpha=0.85)
bars2 = ax.bar(x+w/2, reg_pct3, w, label='Regular', color='#A23B72', alpha=0.85)
ax.set_ylabel('Percentage of Searches (%)', fontweight='bold')
ax.set_title('Search Category Preferences (Keyword-Mapped): High-Value vs Regular Users', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(cats3, fontsize=9)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/search_categories.png', dpi=150)
plt.close()
print("Saved search_categories.png")

# ========== 4. Favorite Brands Comparison ==========
fb_hv = {"Haier Smart Home Co., Ltd.":46,"BYD Co., Ltd.":40,"Tsingtao Brewery Co., Ltd.":35,"Xizang Nuodikang Pharmaceutical Co., Ltd.":34,"Kweichow Moutai Co., Ltd.":29,"Yunnan Baiyao Group Co., Ltd.":21}
fb_reg = {"Haier Smart Home Co., Ltd.":25,"Kweichow Moutai Co., Ltd.":22,"BYD Co., Ltd.":18,"Tsingtao Brewery Co., Ltd.":17,"Yunnan Baiyao Group Co., Ltd.":17,"Xizang Nuodikang Pharmaceutical Co., Ltd.":14}
brands = sorted(set(fb_hv)|set(fb_reg))
hv_pct4 = [fb_hv.get(b,0)/sum(fb_hv.values())*100 for b in brands]
reg_pct4 = [fb_reg.get(b,0)/sum(fb_reg.values())*100 for b in brands]
short_brands = [b.split(' Co., Ltd.')[0] for b in brands]

fig, ax = plt.subplots(figsize=(14,6))
x = np.arange(len(brands))
bars1 = ax.bar(x-w/2, hv_pct4, w, label='High-Value (Diamond/Platinum)', color='#2E86AB', alpha=0.85)
bars2 = ax.bar(x+w/2, reg_pct4, w, label='Regular', color='#A23B72', alpha=0.85)
ax.set_ylabel('Percentage of Favorites (%)', fontweight='bold')
ax.set_title('Favorite Brand Preferences: High-Value vs Regular Users', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(short_brands, fontsize=9, rotation=15)
ax.legend()
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/fav_brands.png', dpi=150)
plt.close()
print("Saved fav_brands.png")

# ========== 5. Search Hour Distribution ==========
# Data from S21
# High-Value: hour->count
hv_hours = {0:9,1:10,2:8,3:15,4:7,5:6,6:7,7:8,8:7,9:9,10:9,11:8,12:9,13:6,14:7,15:15,16:12,17:9,18:5,19:10,20:6,21:7,22:13,23:14}
reg_hours = {0:9,1:4,2:7,3:4,4:6,5:2,6:7,7:4,8:4,9:4,10:5,11:3,12:5,13:3,14:6,15:3,16:6,17:4,18:8,19:4,20:4,21:8,22:4,23:3}
gold_hours = {0:11,1:6,2:4,3:4,4:2,5:8,6:5,7:6,8:10,9:2,10:5,11:3,12:4,13:4,15:1,17:6,18:3,19:4,20:3,21:6,22:8,23:13}

hours = list(range(24))
hv_vals = [hv_hours.get(h,0)/sum(hv_hours.values())*100 for h in hours]
reg_vals = [reg_hours.get(h,0)/sum(reg_hours.values())*100 for h in hours]
gold_vals = [gold_hours.get(h,0)/sum(gold_hours.values())*100 for h in hours]

fig, ax = plt.subplots(figsize=(14,6))
ax.plot(hours, hv_vals, 'o-', color='#2E86AB', linewidth=2, markersize=6, label='High-Value (Diamond/Platinum)')
ax.plot(hours, reg_vals, 's-', color='#A23B72', linewidth=2, markersize=6, label='Regular')
ax.plot(hours, gold_vals, '^-', color='#F18F01', linewidth=2, markersize=5, label='Gold (Intermediate)')
ax.set_xlabel('Hour of Day', fontweight='bold')
ax.set_ylabel('Percentage of Searches (%)', fontweight='bold')
ax.set_title('Search Active Time Distribution: High-Value vs Regular Users', fontweight='bold')
ax.set_xticks(range(0,24,2))
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/search_hour_dist.png', dpi=150)
plt.close()
print("Saved search_hour_dist.png")

# ========== 6. Compute statistics ==========
hv_avg_hour = sum(h*hv_hours.get(h,0) for h in hours)/sum(hv_hours.values())
reg_avg_hour = sum(h*reg_hours.get(h,0) for h in hours)/sum(reg_hours.values())
print(f"High-Value average search hour: {hv_avg_hour:.2f}")
print(f"Regular average search hour: {reg_avg_hour:.2f}")

# Peak hours (top 3)
hv_sorted = sorted(hv_hours.items(), key=lambda x:-x[1])
reg_sorted = sorted(reg_hours.items(), key=lambda x:-x[1])
print(f"High-Value peak hours: {hv_sorted[:5]}")
print(f"Regular peak hours: {reg_sorted[:5]}")

# Day of week analysis
hv_dow = {0:34,1:30,2:32,3:24,4:26,5:34,6:36}
reg_dow = {0:18,1:19,2:16,3:17,4:15,5:18,6:14}
days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
hv_dow_pct = [hv_dow[i]/sum(hv_dow.values())*100 for i in range(7)]
reg_dow_pct = [reg_dow[i]/sum(reg_dow.values())*100 for i in range(7)]

fig, ax = plt.subplots(figsize=(10,6))
x = np.arange(7)
bars1 = ax.bar(x-w/2, hv_dow_pct, w, label='High-Value', color='#2E86AB', alpha=0.85)
bars2 = ax.bar(x+w/2, reg_dow_pct, w, label='Regular', color='#A23B72', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(days)
ax.set_ylabel('Percentage of Searches (%)', fontweight='bold')
ax.set_title('Search Activity by Day of Week: High-Value vs Regular Users', fontweight='bold')
ax.legend()
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f'{bar.get_height():.1f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('/work/search_dow.png', dpi=150)
plt.close()
print("Saved search_dow.png")

# Comparison of search behavior metrics
print("\n=== Search Behavior Metrics Comparison ===")
print("Metric | High-Value | Regular")
print(f"Avg Input Duration | 15.0 | 15.8")
print(f"Avg Viewed Results | 28.4 | 32.4")
print(f"Avg Clicked Results | 14.4 | 16.6")
print(f"Avg Conversion Rate | 0.483 | 0.484")
print(f"Autocomplete Use | 54.6% | 54.7%")

print("\n=== Browsing Behavior Metrics Comparison ===")
print("Metric | High-Value | Regular")
print(f"Avg Time on Page | 304.4 | 301.4")
print(f"Avg Scroll Distance | 580.1 | 577.2")
print(f"Avg Zoom Count | 2.9 | 2.6")
print(f"Avg Detail Page Time | 249.5 | 266.8")
print(f"Avg Review Page Time | 150.9 | 145.7")
print(f"Swiped % | 53.6% | 50.0%")
print(f"Zoomed % | 53.2% | 49.2%")
print(f"Specs Viewed % | 53.6% | 49.2%")
print(f"Avg Share/View | 24.1 | 25.5")

print("\nAll plots saved.")