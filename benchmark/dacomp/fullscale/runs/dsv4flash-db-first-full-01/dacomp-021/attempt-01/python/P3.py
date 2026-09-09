import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Reload daily data
daily = pd.read_csv('/work/daily_stats.csv')
daily['date'] = pd.to_datetime(daily['date_key'])
daily['cancel_pct'] = 100*daily['cancellations']/daily['bookings']
daily['nodriver_pct'] = 100*daily['no_driver']/daily['bookings']
daily['incomplete_pct'] = 100*daily['incomplete']/daily['bookings']
daily['weekday'] = daily['date'].dt.dayofweek
daily['month'] = daily['date'].dt.month
daily['is_weekend'] = daily['weekday'].isin([5,6])

# Monthly aggregation
monthly = daily.groupby('month').agg(
    bookings=('bookings','sum'),
    cancel_pct=('cancel_pct','mean'),
    no_driver_pct=('nodriver_pct','mean'),
    incomplete_pct=('incomplete_pct','mean'),
    cost_per_km=('cost_per_km','mean')
).round(2)
print("Monthly aggregation:")
print(monthly.to_string())

# Figure 5: Booking volume vs cost-per-km scatter (daily)
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#e74c3c' if w else '#3498db' for w in daily['is_weekend']]
sc = ax.scatter(daily['bookings'], daily['cost_per_km'], alpha=0.5, c=colors, s=20, edgecolors='none')
ax.set_xlabel('Daily bookings'); ax.set_ylabel('Avg cost per km (₹)')
ax.set_title('Daily booking volume vs per-km cost (red=weekend)')
# Add trend line
m, b = np.polyfit(daily['bookings'], daily['cost_per_km'], 1)
ax.plot(daily['bookings'], m*daily['bookings']+b, color='gray', lw=1, ls='--')
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('/work/fig5_volume_vs_cost.png', dpi=130); plt.close(fig)

# Figure 6: Monthly trend
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.bar(monthly.index, monthly['bookings'], color='#3498db', alpha=0.7, label='Monthly bookings')
ax2 = ax1.twinx()
ax2.plot(monthly.index, monthly['cost_per_km'], marker='o', color='#e74c3c', lw=2, label='Avg cost per km')
ax2.plot(monthly.index, monthly['cancel_pct'], marker='s', color='green', lw=2, label='Cancellation rate %')
ax1.set_xlabel('Month'); ax1.set_ylabel('Bookings'); ax2.set_ylabel('Cost/km / Cancel %')
ax1.set_title('Monthly trends in volume, price, and cancellation')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')
fig.tight_layout(); fig.savefig('/work/fig6_monthly_trends.png', dpi=130); plt.close(fig)

# Figure 7: Hour-of-day by weekday heatmap
# Query hour x weekday data
hwd_sql = """
WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT dow, hour, COUNT(*) AS bookings,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS cost_per_km
FROM parsed
GROUP BY dow, hour
ORDER BY dow, hour
"""
resh = db.query(hwd_sql)
hwd = db.frame(resh)
hwd_pivot = hwd.pivot_table(index='hour', columns='dow', values='bookings', aggfunc='first')
hwd_pivot.columns = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(hwd_pivot.values, cmap='YlOrRd', aspect='auto')
ax.set_xticks(range(7)); ax.set_xticklabels(['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
ax.set_yticks(range(24)); ax.set_yticklabels(range(24))
ax.set_xlabel('Day of week'); ax.set_ylabel('Hour of day')
ax.set_title('Hour × Day-of-week booking volume heatmap')
for i in range(24):
    for j in range(7):
        val = hwd_pivot.values[i,j]
        ax.text(j, i, str(int(val)), ha='center', va='center', fontsize=5.5, color='black' if val<5000 else 'white')
fig.tight_layout(); fig.savefig('/work/fig7_heatmap_weekday_hour.png', dpi=130); plt.close(fig)

# Cost per km heatmap
cpk_pivot = hwd.pivot_table(index='hour', columns='dow', values='cost_per_km', aggfunc='first')
cpk_pivot.columns = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
fig, ax = plt.subplots(figsize=(11, 6))
im = ax.imshow(cpk_pivot.values, cmap='viridis', aspect='auto')
ax.set_xticks(range(7)); ax.set_xticklabels(['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])
ax.set_yticks(range(24)); ax.set_yticklabels(range(24))
ax.set_xlabel('Day of week'); ax.set_ylabel('Hour of day')
ax.set_title('Hour × Day-of-week average cost per km (₹)')
for i in range(24):
    for j in range(7):
        val = cpk_pivot.values[i,j]
        if not np.isnan(val):
            ax.text(j, i, '%.0f'%val, ha='center', va='center', fontsize=5.5, color='white' if val>35 else 'black')
fig.tight_layout(); fig.savefig('/work/fig8_heatmap_cost_km.png', dpi=130); plt.close(fig)

# Figure 9: Cancellation type breakdown by hour
cancel_sql = """
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS total,
  SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END) AS cust_cancel,
  SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END) AS drv_cancel
FROM parsed
GROUP BY hour
ORDER BY hour
"""
rc = db.query(cancel_sql)
cancel_df = db.frame(rc)
cancel_df['cust_pct'] = 100*cancel_df['cust_cancel']/cancel_df['total']
cancel_df['drv_pct'] = 100*cancel_df['drv_cancel']/cancel_df['total']

fig, ax = plt.subplots(figsize=(10, 4.2))
ax.bar(cancel_df['hour']-0.15, cancel_df['cust_pct'], width=0.3, color='#3498db', label='Customer cancelled')
ax.bar(cancel_df['hour']+0.15, cancel_df['drv_pct'], width=0.3, color='#e74c3c', label='Driver cancelled')
ax.set_xticks(range(0,24)); ax.set_xlabel('Hour of day'); ax.set_ylabel('Cancellation rate (%)')
ax.set_title('Customer vs Driver cancellation rates by hour')
ax.legend(); ax.grid(alpha=0.3, axis='y')
fig.tight_layout(); fig.savefig('/work/fig9_cancel_by_type.png', dpi=130); plt.close(fig)

print("All figures created.")