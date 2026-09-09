import pandas as pd
import numpy as np
from scipy import stats

# Reload data
result = db.query("""
SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'
""")
df = db.frame(result)

# Test 1: Booking value differences by vehicle type (Kruskal-Wallis since not normal)
groups = [g['Booking Value'].values for _, g in df.groupby('Vehicle Type')]
kw_bv = stats.kruskal(*groups)
print(f"Kruskal-Wallis on Booking Value by Vehicle Type: stat={kw_bv.statistic:.2f}, p={kw_bv.pvalue:.4f}")

# Test 2: Fare per km by vehicle type
groups2 = [g['fare_per_km'].values for _, g in df.groupby('Vehicle Type')]
kw_fpk = stats.kruskal(*groups2)
print(f"Kruskal-Wallis on Fare per km by Vehicle Type: stat={kw_fpk.statistic:.2f}, p={kw_fpk.pvalue:.4f}")

# Test 3: Fare per km weekday vs weekend
df['is_weekend'] = df['day_of_week'].isin(['0', '6'])
weekend = df[df['is_weekend']]['Booking Value'].values
weekday = df[~df['is_weekend']]['Booking Value'].values
mw = stats.mannwhitneyu(weekend, weekday, alternative='two-sided')
print(f"Mann-Whitney on Booking Value weekend vs weekday: stat={mw.statistic:.2f}, p={mw.pvalue:.4f}")
print(f"  Weekend avg booking: {weekend.mean():.2f}, Weekday avg booking: {weekday.mean():.2f}")
print(f"  Weekend fare/km: {df[df['is_weekend']]['fare_per_km'].mean():.2f}, Weekday fare/km: {df[~df['is_weekend']]['fare_per_km'].mean():.2f}")

# Test 4: Booking value by rating band
df['rating_band'] = pd.cut(df['Driver Ratings'], bins=[3.0, 3.5, 4.0, 4.5, 5.0],
                           labels=['3.0-3.4', '3.5-3.9', '4.0-4.4', '4.5-5.0'])
groups3 = [g['Booking Value'].values for _, g in df.groupby('rating_band')]
kw_r = stats.kruskal(*groups3)
print(f"Kruskal-Wallis on Booking Value by Rating Band: stat={kw_r.statistic:.2f}, p={kw_r.pvalue:.4f}")

groups4 = [g['fare_per_km'].values for _, g in df.groupby('rating_band')]
kw_r2 = stats.kruskal(*groups4)
print(f"Kruskal-Wallis on Fare per km by Rating Band: stat={kw_r2.statistic:.2f}, p={kw_r2.pvalue:.4f}")

# Correlation between rating and fare_per_km
corr_r_fpk = df['Driver Ratings'].corr(df['fare_per_km'])
print(f"\nCorrelation Driver Ratings vs Fare per km: {corr_r_fpk:.4f}")
corr_r_bv = df['Driver Ratings'].corr(df['Booking Value'])
print(f"Correlation Driver Ratings vs Booking Value: {corr_r_bv:.4f}")

# Ratings distribution details
print("\nDriver Rating distribution:")
print(df['Driver Ratings'].value_counts().sort_index().head(10))

# Estimate of ride counts per hour: peak hours
print("\nTop 5 hours by ride volume:")
print(df.groupby('hour').size().sort_values(ascending=False).head(5))

# Realistic annual earnings model
print("\n=== Annual earnings estimation ===")
# Assume driver works 6 days/week, ~10 rides/day (avg distance 26km, ~40 min each + gaps)
avg_ride = df['Booking Value'].mean()
print(f"Average booking value per ride: ₹{avg_ride:.0f}")

for rides_per_day in [8, 10, 12]:
    for days_per_week in [5, 6]:
        annual_rides = rides_per_day * days_per_week * 52
        annual_gross = annual_rides * avg_ride
        print(f"  {rides_per_day} rides/day × {days_per_week} days/wk → {annual_rides} rides/yr → gross ₹{annual_gross:,.0f}")

# Weekend focus model: 12 rides/day weekday (lower fare) + 12 rides/day weekend (higher fare)
wkd = df[~df['is_weekend']]['Booking Value'].mean()
wke = df[df['is_weekend']]['Booking Value'].mean()
print(f"\nWeekday avg ride: ₹{wkd:.0f}, Weekend avg ride: ₹{wke:.0f}")
# Scenario: 5 weekdays x 10 rides + 2 weekend days x 10 rides
annual_mixed = (5*wkd*10 + 2*wke*10)*52
annual_all_wk = 7*wkd*10*52
annual_wknd_focus = (5*wkd*10 + 2*wke*12)*52
print(f"Scenario A (10 rides/day all days, all weekday rate): ₹{annual_all_wk:,.0f}")
print(f"Scenario B (10 rides/day, actual weekend mix): ₹{annual_mixed:,.0f}")
print(f"Scenario C (10 rides/day weekday + 12 rides/day weekend): ₹{annual_wknd_focus:,.0f}")

# Save a small table of booking value distribution by vehicle for report
vt_stats = df.groupby('Vehicle Type').agg(
    avg_booking=('Booking Value', 'mean'),
    median_booking=('Booking Value', 'median'),
    avg_fare_per_km=('fare_per_km', 'mean'),
    rides=('Booking Value', 'count')
).round(2).sort_values('avg_fare_per_km', ascending=False)
print("\nVehicle Type stats:")
print(vt_stats)