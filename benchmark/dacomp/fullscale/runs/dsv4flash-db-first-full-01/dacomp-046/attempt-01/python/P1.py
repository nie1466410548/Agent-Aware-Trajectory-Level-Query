
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# Pull pre-aggregated results
summary = pd.DataFrame([
    {"Age group":"<25","user_count":56,"at_risk_count":35,"churn_risk_pct":62.5,"avg_shares":22.36,"avg_feedback_rating":2.33,"avg_conversion_rate":0.40,"avg_dwell_time":299.96},
    {"Age group":"25-35","user_count":69,"at_risk_count":37,"churn_risk_pct":53.62,"avg_shares":23.13,"avg_feedback_rating":2.46,"avg_conversion_rate":0.38,"avg_dwell_time":319.81},
    {"Age group":"36-50","user_count":106,"at_risk_count":52,"churn_risk_pct":49.06,"avg_shares":25.09,"avg_feedback_rating":2.55,"avg_conversion_rate":0.37,"avg_dwell_time":299.98},
    {"Age group":"50+","user_count":106,"at_risk_count":50,"churn_risk_pct":47.17,"avg_shares":26.02,"avg_feedback_rating":2.49,"avg_conversion_rate":0.39,"avg_dwell_time":303.22},
])
summary = summary.sort_values("Age group").reset_index(drop=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

# 1) Churn risk
ax = axes[0]
bars = ax.bar(summary["Age group"], summary["churn_risk_pct"], color=["#8da0cb","#66c2a5","#fc8d62","#e78ac3"], edgecolor='black')
for b, v in zip(bars, summary["churn_risk_pct"]):
    ax.text(b.get_x()+b.get_width()/2, v+0.6, f"{v:.1f}%", ha='center', fontsize=9)
ax.set_ylabel("Churn risk rate (%)")
ax.set_title("At-risk user share by age group")
ax.set_ylim(0, 75)
ax.grid(axis='y', alpha=0.3)

# 2) Avg shares
ax = axes[1]
bars = ax.bar(summary["Age group"], summary["avg_shares"], color=["#8da0cb","#66c2a5","#fc8d62","#e78ac3"], edgecolor='black')
for b, v in zip(bars, summary["avg_shares"]):
    ax.text(b.get_x()+b.get_width()/2, v+0.3, f"{v:.1f}", ha='center', fontsize=9)
ax.set_ylabel("Avg number of shares")
ax.set_title("Avg shares per campaign interaction")
ax.set_ylim(0, 32)
ax.grid(axis='y', alpha=0.3)

# 3) Feedback rating
ax = axes[2]
bars = ax.bar(summary["Age group"], summary["avg_feedback_rating"], color=["#8da0cb","#66c2a5","#fc8d62","#e78ac3"], edgecolor='black')
for b, v in zip(bars, summary["avg_feedback_rating"]):
    ax.text(b.get_x()+b.get_width()/2, v+0.03, f"{v:.2f}", ha='center', fontsize=9)
ax.set_ylabel("Avg feedback rating (1-5)")
ax.set_title("Avg campaign feedback rating")
ax.set_ylim(0, 3.2)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("work/fig1_age_group_churn_share_rating.png", dpi=150)
plt.close()

# Conversion + dwell time
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
ax = axes[0]
bars = ax.bar(summary["Age group"], summary["avg_conversion_rate"]*100, color="#66a61e", edgecolor='black')
for b, v in zip(bars, summary["avg_conversion_rate"]*100):
    ax.text(b.get_x()+b.get_width()/2, v+0.4, f"{v:.1f}%", ha='center', fontsize=9)
ax.set_ylabel("Avg conversion rate (%)")
ax.set_title("Campaign conversion rate by age group")
ax.set_ylim(0, 50)
ax.grid(axis='y', alpha=0.3)

ax = axes[1]
bars = ax.bar(summary["Age group"], summary["avg_dwell_time"], color="#e6ab02", edgecolor='black')
for b, v in zip(bars, summary["avg_dwell_time"]):
    ax.text(b.get_x()+b.get_width()/2, v+3, f"{v:.0f}s", ha='center', fontsize=9)
ax.set_ylabel("Avg dwell time (seconds)")
ax.set_title("Campaign dwell time by age group")
ax.set_ylim(0, 380)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("work/fig2_age_group_conv_dwell.png", dpi=150)
plt.close()
print("figures 1-2 done")
print(summary.to_string())
