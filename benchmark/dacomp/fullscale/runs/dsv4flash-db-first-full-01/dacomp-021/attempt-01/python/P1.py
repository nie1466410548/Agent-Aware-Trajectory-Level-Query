
import json, os, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---- Fetch daily aggregation (already computed in SQL, retrieve via logged interface) ----
daily_sql = """
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT date_key,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 4) AS cost_per_km
FROM parsed
GROUP BY date_key
ORDER BY date_key
"""
res = db.query(daily_sql)
daily = db.frame(res)
daily['date'] = pd.to_datetime(daily['date_key'])
daily = daily.sort_values('date').reset_index(drop=True)

# ---- Hourly aggregation ----
hourly_sql = """
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) AS cost_per_km
FROM parsed
GROUP BY hour
ORDER BY hour
"""
resh = db.query(hourly_sql)
hourly = db.frame(resh)
hourly['cancel_pct'] = 100*hourly['cancellations']/hourly['bookings']
hourly['nodriver_pct'] = 100*hourly['no_driver']/hourly['bookings']
hourly['incomplete_pct'] = 100*hourly['incomplete']/hourly['bookings']

# ---- Basic stats ----
print("Daily bookings: mean=%.1f std=%.1f min=%d max=%d" % (
    daily['bookings'].mean(), daily['bookings'].std(), daily['bookings'].min(), daily['bookings'].max()))
print("\nHourly table:")
print(hourly[['hour','bookings','cancel_pct','nodriver_pct','incomplete_pct','cost_per_km']].round(2).to_string(index=False))

# Save intermediate
daily.to_csv('/work/daily_stats.csv', index=False)
hourly.to_csv('/work/hourly_stats.csv', index=False)

# Figure 1: Daily bookings time series with 7-day rolling mean
fig, ax = plt.subplots(figsize=(13, 4.5))
ax.plot(daily['date'], daily['bookings'], color='steelblue', alpha=0.55, lw=0.9, label='Daily bookings')
daily['roll7'] = daily['bookings'].rolling(7, center=True, min_periods=1).mean()
ax.plot(daily['date'], daily['roll7'], color='crimson', lw=2.2, label='7-day rolling mean')
ax.axhline(daily['bookings'].mean(), color='gray', ls='--', lw=1, label='Year mean (%.0f)' % daily['bookings'].mean())
peak_day = daily.loc[daily['bookings'].idxmax()]
trough_day = daily.loc[daily['bookings'].idxmin()]
ax.annotate('Peak %s (%d)' % (peak_day['date'].date(), peak_day['bookings']),
            xy=(peak_day['date'], peak_day['bookings']), xytext=(peak_day['date']-pd.Timedelta(days=18), peak_day['bookings']+14),
            arrowprops=dict(arrowstyle='->', color='green'), color='green')
ax.annotate('Trough %s (%d)' % (trough_day['date'].date(), trough_day['bookings']),
            xy=(trough_day['date'], trough_day['bookings']), xytext=(trough_day['date']+pd.Timedelta(days=12), trough_day['bookings']-30),
            arrowprops=dict(arrowstyle='->', color='darkorange'), color='darkorange')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_title('Daily Uber ride bookings - 2024 (peaks and troughs)')
ax.set_ylabel('Bookings per day'); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('/work/fig1_daily_bookings.png', dpi=130); plt.close(fig)

# Figure 2: Hourly bookings
fig, ax = plt.subplots(figsize=(10, 4.2))
colors = ['#d62728' if h in (9,10,11,17,18,19,20) else ('#1f77b4' if h not in (0,1,2,3,4) else '#ff7f0e') for h in hourly['hour']]
ax.bar(hourly['hour'], hourly['bookings'], color=colors)
ax.axhline(hourly['bookings'].mean(), color='gray', ls='--', lw=1)
ax.set_xticks(range(0,24)); ax.set_xlabel('Hour of day'); ax.set_ylabel('Total bookings (full year)')
ax.set_title('Hourly booking volume (peak hours red, early-morning trough orange)')
ax.grid(alpha=0.3, axis='y')
fig.tight_layout(); fig.savefig('/work/fig2_hourly_bookings.png', dpi=130); plt.close(fig)

# Figure 3: hourly cancellation / no-driver rates
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.plot(hourly['hour'], hourly['cancel_pct'], marker='o', color='crimson', label='Cancellation rate (%)')
ax.plot(hourly['hour'], hourly['nodriver_pct'], marker='s', color='steelblue', label='No driver found rate (%)')
ax.plot(hourly['hour'], hourly['incomplete_pct'], marker='^', color='green', label='Incomplete ride rate (%)')
ax.set_xticks(range(0,24)); ax.set_xlabel('Hour of day'); ax.set_ylabel('Rate (%)')
ax.set_title('Hourly ride-quality metrics')
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('/work/fig3_hourly_quality.png', dpi=130); plt.close(fig)

# Figure 4: hourly per-km cost
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.bar(hourly['hour'], hourly['cost_per_km'], color='#2ca02c')
ax.set_xticks(range(0,24)); ax.set_xlabel('Hour of day'); ax.set_ylabel('Avg ₹ per km (completed rides)')
ax.set_title('Hourly average ride cost per kilometer')
ax.grid(alpha=0.3, axis='y')
fig.tight_layout(); fig.savefig('/work/fig4_hourly_cost_km.png', dpi=130); plt.close(fig)

print("\nSaved figures.")
