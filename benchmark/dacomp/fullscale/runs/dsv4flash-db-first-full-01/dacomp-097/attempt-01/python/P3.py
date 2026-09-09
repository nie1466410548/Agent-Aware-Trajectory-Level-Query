import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load ARR bucket metrics
arr_metrics = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS bot_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  co.arr_bucket,
  AVG(agg.num_convs) AS avg_convs_per_company,
  AVG(agg.avg_resp_delay) AS avg_resp_delay,
  AVG(agg.avg_duration) AS avg_duration,
  AVG(agg.bot_ratio) AS avg_bot_ratio_pct
FROM agg
JOIN company_dim co ON agg.company_name = co.company_name
GROUP BY co.arr_bucket
ORDER BY co.arr_bucket
"""))

seat_metrics = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS bot_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  co.seat_bucket,
  AVG(agg.num_convs) AS avg_convs_per_company,
  AVG(agg.avg_resp_delay) AS avg_resp_delay,
  AVG(agg.avg_duration) AS avg_duration,
  AVG(agg.bot_ratio) AS avg_bot_ratio_pct
FROM agg
JOIN company_dim co ON agg.company_name = co.company_name
GROUP BY co.seat_bucket
ORDER BY co.seat_bucket
"""))

print("ARR Bucket Metrics:")
print(arr_metrics)
print("\nSeat Bucket Metrics:")
print(seat_metrics)

# Retention by ARR and seat
arr_ret = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.arr_bucket,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention,
  AVG(cm.contacts_active_7d) AS avg_active_7d,
  AVG(cm.contacts_active_30d) AS avg_active_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.arr_bucket
ORDER BY cd.arr_bucket
"""))

seat_ret = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.seat_bucket,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention,
  AVG(cm.contacts_active_7d) AS avg_active_7d,
  AVG(cm.contacts_active_30d) AS avg_active_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.seat_bucket
ORDER BY cd.seat_bucket
"""))

# Plot: ARR bucket analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

arr_order = ['<30k', '30k_65k', '65k_110k', '110k_200k', '200k_plus']
arr_ret['arr_bucket'] = pd.Categorical(arr_ret['arr_bucket'], categories=arr_order, ordered=True)
arr_ret = arr_ret.sort_values('arr_bucket')

# Left: Retention by ARR
x = np.arange(len(arr_ret))
w = 0.35
axes[0].bar(x - w/2, arr_ret['weekly_retention']*100, w, label='Weekly', color='steelblue', alpha=0.85)
axes[0].bar(x + w/2, arr_ret['monthly_retention']*100, w, label='Monthly', color='lightcoral', alpha=0.85)
axes[0].set_xticks(x)
axes[0].set_xticklabels(arr_ret['arr_bucket'], rotation=30)
axes[0].set_title('Retention Rate by ARR Bucket')
axes[0].set_ylabel('%')
axes[0].legend()
for i in range(len(arr_ret)):
    axes[0].text(i - w/2, arr_ret['weekly_retention'].iloc[i]*100 + 0.5, f"{arr_ret['weekly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)
    axes[0].text(i + w/2, arr_ret['monthly_retention'].iloc[i]*100 + 0.5, f"{arr_ret['monthly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)

# Right: Active contacts by ARR
axes[1].bar(x, arr_ret['avg_active_7d'], alpha=0.7, label='Active 7d', color='cornflowerblue')
axes[1].bar(x, arr_ret['avg_active_30d'], alpha=0.5, label='Active 30d', color='salmon')
axes[1].set_xticks(x)
axes[1].set_xticklabels(arr_ret['arr_bucket'], rotation=30)
axes[1].set_title('Avg Active Contacts by ARR Bucket')
axes[1].set_ylabel('Count')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/arr_analysis.png', dpi=120)
plt.close()

# Plot: Seat bucket analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
seat_order = ['under_60', '60_129', '130_259', '260_419', '420_plus']
seat_ret['seat_bucket'] = pd.Categorical(seat_ret['seat_bucket'], categories=seat_order, ordered=True)
seat_ret = seat_ret.sort_values('seat_bucket')

x = np.arange(len(seat_ret))
w = 0.35
axes[0].bar(x - w/2, seat_ret['weekly_retention']*100, w, label='Weekly', color='steelblue', alpha=0.85)
axes[0].bar(x + w/2, seat_ret['monthly_retention']*100, w, label='Monthly', color='lightcoral', alpha=0.85)
axes[0].set_xticks(x)
axes[0].set_xticklabels(seat_ret['seat_bucket'], rotation=30)
axes[0].set_title('Retention Rate by Seat Bucket')
axes[0].set_ylabel('%')
axes[0].legend()
for i in range(len(seat_ret)):
    axes[0].text(i - w/2, seat_ret['weekly_retention'].iloc[i]*100 + 0.5, f"{seat_ret['weekly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)
    axes[0].text(i + w/2, seat_ret['monthly_retention'].iloc[i]*100 + 0.5, f"{seat_ret['monthly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)

axes[1].bar(x, seat_ret['avg_active_7d'], alpha=0.7, label='Active 7d', color='cornflowerblue')
axes[1].bar(x, seat_ret['avg_active_30d'], alpha=0.5, label='Active 30d', color='salmon')
axes[1].set_xticks(x)
axes[1].set_xticklabels(seat_ret['seat_bucket'], rotation=30)
axes[1].set_title('Avg Active Contacts by Seat Bucket')
axes[1].set_ylabel('Count')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/seat_analysis.png', dpi=120)
plt.close()

print("Done with ARR and seat analysis figures.")