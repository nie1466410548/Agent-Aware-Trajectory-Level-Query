import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Campaign performance by age group - from SQL query S54
campaign_data = pd.DataFrame([
    # <25
    ["<25","Brand-Day Special Offer",4,1.35,0.6,2.13,0.273,293.0,100.0],
    ["<25","Spend-and-Save Promotion",6,17.3,0.63,2.5,0.453,334.5,83.3],
    ["<25","Double-11 Mega Sale",8,25.4,0.89,2.7,0.444,313.0,62.5],
    ["<25","Group-buy Coupon Grab",6,30.0,1.07,2.08,0.373,272.5,83.3],
    ["<25","Flash Sale (limited-time)",6,27.0,0.72,2.45,0.267,281.0,83.3],
    ["<25","Year-End Clearance",5,26.2,0.93,2.52,0.38,381.0,80.0],
    ["<25","Holiday Treat",5,22.8,1.0,1.68,0.44,289.0,80.0],
    ["<25","Points Doubling",4,22.0,0.9,1.7,0.208,340.0,75.0],
    ["<25","New-Year Red Packet",4,22.0,0.9,2.25,0.35,274.0,75.0],
    ["<25","Members Only",4,22.0,0.9,2.37,0.35,250.0,75.0],
    # 25-35
    ["25-35","Spend-and-Save Promotion",12,22.3,0.97,2.03,0.437,328.4,91.7],
    ["25-35","Double-11 Mega Sale",12,27.1,1.57,2.1,0.376,301.7,58.3],
    ["25-35","Brand-Day Special Offer",8,15.4,0.65,1.48,0.343,339.5,87.5],
    ["25-35","Year-End Clearance",7,22.9,1.34,2.89,0.47,284.6,100.0],
    ["25-35","New-Year Red Packet",6,30.0,1.18,2.92,0.2,409.2,50.0],
    ["25-35","Group-buy Coupon Grab",6,20.5,0.71,2.92,0.208,339.0,66.7],
    ["25-35","Flash Sale (limited-time)",6,20.7,0.63,2.73,0.435,291.5,66.7],
    ["25-35","Holiday Treat",5,32.0,1.13,4.22,0.444,275.4,60.0],
    ["25-35","Points Doubling",4,17.0,0.78,1.75,0.315,317.0,75.0],
    ["25-35","Members Only",3,21.7,1.01,2.8,0.573,305.0,100.0],
    # 36-50
    ["36-50","Members Only",13,26.5,1.08,2.49,0.254,358.1,92.3],
    ["36-50","Spend-and-Save Promotion",12,22.8,0.87,2.8,0.408,296.3,91.7],
    ["36-50","Flash Sale (limited-time)",11,27.1,0.92,2.81,0.327,303.7,90.9],
    ["36-50","Double-11 Mega Sale",11,23.5,1.1,2.85,0.439,252.0,90.9],
    ["36-50","Group-buy Coupon Grab",11,19.5,0.67,2.58,0.37,305.5,81.8],
    ["36-50","Year-End Clearance",9,26.2,1.0,2.84,0.384,282.0,77.8],
    ["36-50","New-Year Red Packet",9,26.7,1.0,3.17,0.417,312.7,100.0],
    ["36-50","Brand-Day Special Offer",9,23.0,0.82,2.07,0.4,230.0,88.9],
    ["36-50","Holiday Treat",8,28.5,1.26,2.07,0.445,288.8,87.5],
    ["36-50","Points Doubling",8,24.0,1.0,2.2,0.339,280.0,87.5],
    # 50+
    ["50+","Brand-Day Special Offer",14,20.9,0.72,2.32,0.447,301.1,85.7],
    ["50+","Double-11 Mega Sale",14,23.1,0.93,2.56,0.432,315.9,78.6],
    ["50+","Points Doubling",15,24.1,1.01,2.97,0.33,264.4,80.0],
    ["50+","Holiday Treat",10,28.3,1.1,2.37,0.539,293.3,90.0],
    ["50+","Group-buy Coupon Grab",15,24.1,1.01,2.51,0.431,255.0,66.7],
    ["50+","Spend-and-Save Promotion",14,28.8,0.99,2.64,0.393,310.0,78.6],
    ["50+","Flash Sale (limited-time)",12,25.7,1.0,2.88,0.274,291.0,91.7],
    ["50+","Year-End Clearance",7,27.1,0.99,2.06,0.357,298.0,71.4],
    ["50+","New-Year Red Packet",7,25.7,0.92,2.44,0.4,280.0,71.4],
    ["50+","Members Only",7,26.3,0.96,2.17,0.41,298.0,85.7],
], columns=["Age group","Event Name","interactions","avg_shares","share_rate_pct","avg_rating","avg_conv","avg_dwell","used_pct"])

# Figure 3: Heatmap of avg feedback rating per campaign per age group
campaign_rating = campaign_data.pivot_table(index="Event Name", columns="Age group", values="avg_rating", aggfunc="mean")
campaign_rating = campaign_rating[["<25","25-35","36-50","50+"]]

fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(campaign_rating.values, cmap="RdYlGn", vmin=1, vmax=4.5)
ax.set_xticks(range(len(campaign_rating.columns)))
ax.set_xticklabels(campaign_rating.columns)
ax.set_yticks(range(len(campaign_rating.index)))
ax.set_yticklabels(campaign_rating.index)
plt.setp(ax.get_xticklabels(), rotation=0)

for i in range(len(campaign_rating.index)):
    for j in range(len(campaign_rating.columns)):
        val = campaign_rating.values[i][j]
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="black", fontsize=8)

ax.set_title("Campaign Feedback Rating by Age Group")
fig.colorbar(im, ax=ax, label="Avg Rating")
plt.tight_layout()
plt.savefig("fig3_campaign_rating_heatmap.png", dpi=150)
plt.close()
print("fig3 saved")

# Figure 4: Browsing preferences by age group
browsing = pd.DataFrame([
    ["<25","Apparel",10],["<25","Beauty & Makeup",11],["<25","Digital Products",10],["<25","Home Appliances",12],["<25","None",13],
    ["25-35","Apparel",14],["25-35","Beauty & Makeup",18],["25-35","Digital Products",11],["25-35","Home Appliances",15],["25-35","None",11],
    ["36-50","Apparel",26],["36-50","Beauty & Makeup",20],["36-50","Digital Products",22],["36-50","Home Appliances",16],["36-50","None",22],
    ["50+","Apparel",16],["50+","Beauty & Makeup",27],["50+","Digital Products",17],["50+","Home Appliances",24],["50+","None",22],
], columns=["Age group","Browsing Preference","count"])

browsing_pivot = browsing.pivot_table(index="Browsing Preference", columns="Age group", values="count", aggfunc="sum", fill_value=0)
browsing_pivot = browsing_pivot[["<25","25-35","36-50","50+"]]

fig, ax = plt.subplots(figsize=(9, 5))
browsing_pct = browsing_pivot.div(browsing_pivot.sum(axis=0), axis=1) * 100
bottom = np.zeros(4)
colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00"]
for idx, (pref, row) in enumerate(browsing_pct.iterrows()):
    vals = row.values
    ax.bar(row.index, vals, bottom=bottom, color=colors[idx % len(colors)], label=pref, edgecolor='black')
    bottom += vals
ax.set_ylabel("Percentage (%)")
ax.set_title("Browsing Preferences by Age Group")
ax.legend(loc='upper right', fontsize=7)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig("fig4_browsing_preferences.png", dpi=150)
plt.close()
print("fig4 saved")

# Figure 5: At-risk analysis by gender and membership
# Gender data from SQL
gender_data = pd.DataFrame([
    ["<25","Female",27,18,66.7],["<25","Male",29,17,58.6],
    ["25-35","Female",40,25,62.5],["25-35","Male",29,12,41.4],
    ["36-50","Female",54,31,57.4],["36-50","Male",52,21,40.4],
    ["50+","Female",45,19,42.2],["50+","Male",61,31,50.8]
], columns=["Age group","Gender","total","at_risk","at_risk_pct"])

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

# Gender churn risk
ax = axes[0]
groups = ["<25","25-35","36-50","50+"]
x = np.arange(len(groups))
w = 0.35
for i, g in enumerate(["Female","Male"]):
    subset = gender_data[gender_data["Gender"]==g].set_index("Age group").reindex(groups)
    ax.bar(x + i*w, subset["at_risk_pct"], w, label=g, color=["#e78ac3","#8da0cb"][i], edgecolor='black')
ax.set_xticks(x + w/2)
ax.set_xticklabels(groups)
ax.set_ylabel("Churn risk rate (%)")
ax.set_title("Churn risk by gender and age group")
ax.legend()
ax.grid(axis='y', alpha=0.3)

# Membership data
membership = pd.DataFrame([
    ["<25","Diamond",9,5,55.6],["<25","Gold",11,6,54.5],["<25","Platinum",12,7,58.3],["<25","Regular",24,17,70.8],
    ["25-35","Diamond",16,6,37.5],["25-35","Gold",18,11,61.1],["25-35","Platinum",13,5,38.5],["25-35","Regular",22,15,68.2],
    ["36-50","Diamond",27,11,40.7],["36-50","Gold",33,15,45.5],["36-50","Platinum",20,11,55.0],["36-50","Regular",26,15,57.7],
    ["50+","Diamond",31,14,45.2],["50+","Gold",22,9,40.9],["50+","Platinum",26,12,46.2],["50+","Regular",27,15,55.6]
], columns=["Age group","Membership","total","at_risk","at_risk_pct"])

ax = axes[1]
mems = ["Regular","Gold","Platinum","Diamond"]
colors_m = ["#d73027","#fc8d59","#fee08b","#91bfdb"]
x = np.arange(len(groups))
w = 0.2
for i, m in enumerate(mems):
    subset = membership[membership["Membership"]==m].set_index("Age group").reindex(groups)
    ax.bar(x + i*w, subset["at_risk_pct"], w, label=m, color=colors_m[i], edgecolor='black')
ax.set_xticks(x + 1.5*w)
ax.set_xticklabels(groups)
ax.set_ylabel("Churn risk rate (%)")
ax.set_title("Churn risk by membership level and age group")
ax.legend(fontsize=7)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("fig5_churn_by_gender_membership.png", dpi=150)
plt.close()
print("fig5 saved")

# Figure 6: Cart checkout rate by age group
cart = pd.DataFrame([
    ["<25",42,21,37.5,1.38,2.76],
    ["25-35",54,24,34.8,1.5,3.11],
    ["36-50",88,35,33.0,1.41,3.03],
    ["50+",85,47,44.3,1.48,2.82]
], columns=["Age group","carts","checked_out","checkout_pct","avg_mods","avg_qty"])

fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(cart["Age group"], cart["checkout_pct"], color="#7570b3", edgecolor='black')
for b, v in zip(bars, cart["checkout_pct"]):
    ax.text(b.get_x()+b.get_width()/2, v+0.6, f"{v:.1f}%", ha='center', fontsize=9)
ax.set_ylabel("Checkout rate (%)")
ax.set_title("Shopping cart checkout rate by age group")
ax.set_ylim(0, 55)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("fig6_cart_checkout.png", dpi=150)
plt.close()
print("fig6 saved")