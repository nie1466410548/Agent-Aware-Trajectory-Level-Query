import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
result = db.query("""
SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Pickup Location",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week
FROM sheet1
WHERE "Booking Status" = 'Completed'
""")
df = db.frame(result)
df['is_weekend'] = df['day_of_week'].isin(['0', '6'])

# Compute weekend share of rides and earnings
wknd_rides = df['is_weekend'].sum()
total_rides = len(df)
wknd_earn = df[df['is_weekend']]['Booking Value'].sum()
total_earn = df['Booking Value'].sum()
print(f"Weekend rides: {wknd_rides} ({100*wknd_rides/total_rides:.1f}%)")
print(f"Weekend earnings: ₹{wknd_earn:,.0f} ({100*wknd_earn/total_earn:.1f}%)")
print(f"Weekday earnings: ₹{total_earn-wknd_earn:,.0f}")

# Summary of levers
dow_means = df.groupby('is_weekend')['Booking Value'].mean()
print(f"\nWeekday avg ride: ₹{dow_means[False]:.0f}, Weekend avg ride: ₹{dow_means[True]:.0f}")
print(f"Weekend premium: {100*(dow_means[True]/dow_means[False]-1):.1f}%")

# Location premium
loc_stats = df.groupby('Pickup Location')['fare_per_km'].mean()
loc_common = loc_stats[df.groupby('Pickup Location').size() >= 300]
top_loc = loc_common.nlargest(5).mean()
bottom_loc = loc_common.nsmallest(5).mean()
print(f"Top location fare/km (avg top5): ₹{top_loc:.2f}, Bottom (avg bottom5): ₹{bottom_loc:.2f}")
print(f"Location premium: {100*(top_loc/bottom_loc-1):.1f}%")

# Vehicle type
vt_fpk = df.groupby('Vehicle Type')['fare_per_km'].mean()
print(f"\nVehicle fare/km: Go Sedan ₹{vt_fpk['Go Sedan']:.2f} vs eBike ₹{vt_fpk['eBike']:.2f}")

# Final strategy figure
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Panel 1: Weekday vs Weekend per-ride value
ax = axes[0]
labels = ['Weekday\n(Mon-Fri)', 'Weekend\n(Sat-Sun)']
vals = [dow_means[False], dow_means[True]]
bars = ax.bar(labels, vals, color=['#4C72B0', '#C44E52'])
ax.set_ylabel('Avg Booking Value per ride (₹)')
ax.set_title(f'Day-of-week premium:\n+{100*(dow_means[True]/dow_means[False]-1):.0f}% on weekends')
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v+10, f'₹{v:.0f}', ha='center', fontweight='bold')
ax.set_ylim(0, 800)

# Panel 2: Short vs long rides per-km (flat fare finding)
ax = axes[1]
df['dist_band'] = pd.cut(df['Ride Distance'], bins=[0,5,10,20,30,50],
                         labels=['0-5','5-10','10-20','20-30','30-50'])
dist_stats = df.groupby('dist_band', observed=True).agg(
    avg_fare_per_km=('fare_per_km', 'mean'),
    avg_booking=('Booking Value', 'mean')
).reset_index()
x = np.arange(len(dist_stats))
ax2 = ax.twinx()
b1 = ax.bar(x, dist_stats['avg_fare_per_km'], alpha=0.7, color='#55A868', label='Fare per km')
ax.set_xticks(x)
ax.set_xticklabels(dist_stats['dist_band'])
ax.set_ylabel('Avg Fare per km (₹)', color='#55A868')
ax2.plot(x, dist_stats['avg_booking'], 'o--', color='#8172B3', label='Avg Booking Value')
ax2.set_ylabel('Avg Booking Value (₹)', color='#8172B3')
ax.set_title('Flat per-ride fare: short rides pay\nmuch more per km')
ax.set_xlabel('Ride Distance Band')

# Panel 3: Driver rating impact
ax = axes[2]
df['rating_band'] = pd.cut(df['Driver Ratings'], bins=[3.0, 3.5, 4.0, 4.5, 5.0],
                           labels=['3.0-3.4','3.5-3.9','4.0-4.4','4.5-5.0'])
rb = df.groupby('rating_band', observed=True)['Booking Value'].mean()
bars = ax.bar(rb.index.astype(str), rb.values, color='#DD8452')
for b, v in zip(bars, rb.values):
    ax.text(b.get_x()+b.get_width()/2, v+5, f'₹{v:.0f}', ha='center', fontsize=9)
ax.set_ylabel('Avg Booking Value per ride (₹)')
ax.set_title('Driver rating: no significant\nfare difference (p≈0.97)')
ax.set_xlabel('Driver Rating Band')
ax.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('/work/fig8_strategy_levers.png', dpi=110, bbox_inches='tight')
plt.close()

print("\nSaved fig8_strategy_levers.png")

# Final scenario summary
print("\n=== FINAL SCENARIOS (gross platform fare per driver) ===")
scenarios = {
    'Baseline: 10 rides/day, 6 days/wk, weekday rates': 10*6*52*dow_means[False],
    'Recommended: 10 rides/day, 6 days/wk, weekend+weekday mix': 10*6*52*df['Booking Value'].mean(),
    'Weekend-focused: 12 rides Sat-Sun + 8 rides weekday': (8*5*dow_means[False] + 12*2*dow_means[True])*52,
}
for k, v in scenarios.items():
    print(f"{k}: ₹{v:,.0f}")

# Also weekly-ride counts possible in a realistic day
print(f"\nNote: avg distance per ride = {df['Ride Distance'].mean():.1f} km; "
      f"at ~35km/h avg incl pickup, each ride ≈ 45-50 min, so 10-12 rides/day ≈ 8-10 hours online")