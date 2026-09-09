# Uber Ride Booking Analysis 2024: Peaks, Troughs & Operational Recommendations

## Executive Summary

Across the full year 2024 (150,000 bookings, 365 days), ride bookings exhibit clear **intraday peaks and troughs** driven by commuting patterns, while daily variations are modest (±5% around the mean). The most significant finding is a **45% weekend surge in per-kilometer ride cost** (43.5 ₹/km vs 29.9 ₹/km weekdays) with identical ride distances, indicating systematic dynamic pricing. Cancellation rates are remarkably stable at ~25% across all time periods, dominated by driver-side cancellations (~18% of total bookings).

---

## 1. Time-of-Day Peaks and Troughs

### Hourly Volume Profile

The hourly booking distribution reveals a clear bimodal pattern:

| Period | Hours | Bookings | % of Year | Avg Cost/km (₹) | Cancel Rate |
|--------|-------|----------|-----------|-----------------|-------------|
| **Late-night trough** | 00:00–04:59 | 6,776 | 4.5% | 33.4 | 24.7% |
| Early morning | 05:00–08:59 | 19,257 | 12.8% | 33.8 | 25.1% |
| **Morning peak** | 09:00–11:59 | 26,201 | 17.5% | 34.8 | 24.6% |
| Midday dip | 12:00–14:59 | 19,507 | 13.0% | 33.8 | 25.4% |
| Late afternoon | 15:00–16:59 | 17,835 | 11.9% | 33.3 | 25.1% |
| **Evening peak** | 17:00–20:59 | 44,118 | 29.4% | 33.6 | 25.1% |
| Late evening | 21:00–23:59 | 16,306 | 10.9% | 34.2 | 24.8% |

*Figure 1: Daily booking time series with 7-day rolling mean*  
![Daily bookings](fig1_daily_bookings.png)

*Figure 2: Hourly booking volume (peak hours in red, early-morning trough in orange)*  
![Hourly bookings](fig2_hourly_bookings.png)

**Key observations:**
- **Evening peak (17:00–20:00)** is the dominant period, accounting for nearly **30% of all bookings** in just 4 hours. Hour 18:00 is the single busiest hour (12,397 bookings).
- **Morning peak (09:00–11:00)** accounts for 17.5% of bookings. Hour 10:00 is the morning peak.
- **Late-night trough (00:00–04:59)** is the quietest period at only 4.5% of all bookings.
- Hour 13:00 (5,470 bookings) shows a notable **post-lunch dip** between the two peaks.

---

## 2. Daily Peaks and Troughs

Daily booking volumes are relatively stable (mean = 411, std = 20.6, range 355–462).

### Top 3 Peak Days

| Date | Day | Bookings | Cancel Rate | Cost/km (₹) | Notes |
|-----|-----|---------|------------|------------|-------|
| 2024-11-16 | Saturday | 462 | 19.5% | 39.3 | Weekend peak |
| 2024-05-09 | Thursday | 456 | 28.7% | 25.8 | — |
| 2024-09-18 | Wednesday | 456 | 23.9% | 29.7 | — |
| 2024-01-26 | Friday | 452 | 22.8% | 40.6 | Republic Day (India) |

### Bottom 3 Trough Days

| Date | Day | Bookings | Cancel Rate | Cost/km (₹) |
|-----|-----|---------|------------|------------|
| 2024-08-22 | Thursday | 355 | 26.5% | 29.1 |
| 2024-05-02 | Thursday | 357 | 30.3% | 29.2 |
| 2024-11-18 | Monday | 358 | 27.4% | 28.2 |

*Figure 5: Daily booking volume vs per-km cost (red = weekend)*  
![Volume vs cost](fig5_volume_vs_cost.png)

**Statistical findings:**
- No significant correlation between daily booking volume and cancellation rate (r = −0.035, p = 0.51)
- No significant correlation between daily volume and per-km cost (r = 0.061, p = 0.24)
- Monthly variation is small: bookings range 11,927–12,897; cancellation rate 24.6–25.4%

*Figure 6: Monthly trends*  
![Monthly trends](fig6_monthly_trends.png)

---

## 3. Cancellation Rate Analysis

### Overall Cancellation Profile

| Metric | % of Total |
|--------|-----------|
| Completed | 62.0% |
| **Cancelled by Driver** | **18.0%** |
| No Driver Found | 7.0% |
| Cancelled by Customer | 7.0% |
| Incomplete | 6.0% |

**Total effective cancellation rate (driver + customer): 25.0%**

### Driver vs Customer Cancellation by Hour

*Figure 9: Customer vs Driver cancellation rates by hour*  
![Cancel by type](fig9_cancel_by_type.png)

Driver cancellations (~18%) consistently dominate over customer cancellations (~7%) across all hours. This is the **single largest operational challenge**.

### Top Cancellation Reasons

**Customer-initiated cancellations:**
1. Wrong Address (2,362)
2. Change of plans (2,353)
3. Driver is not moving towards pickup (2,335)
4. Driver asked to cancel (2,295)
5. AC is not working (1,155)

**Driver-initiated cancellations:**
1. Customer related issue (6,837)
2. The customer was coughing/sick (6,751)
3. Personal & Car related issues (6,726)
4. More than permitted people (6,686)

The driver cancellation reasons are evenly distributed, suggesting systemic issues rather than a single cause.

### Cancellation Rate by Hour

*Figure 3: Hourly ride-quality metrics*  
![Hourly quality](fig3_hourly_quality.png)

Cancellation rates are **remarkably stable** across all hours (22–26%), with no meaningful spike during peak periods. This indicates that the platform's current supply allocation during peaks is sufficient to maintain service quality at baseline levels.

---

## 4. Per-Kilometer Ride Cost Analysis

### The Weekend Surge Effect

The most striking finding is the **45% weekend premium** in per-km cost:

| Day | Avg Cost/km (₹) | Avg Ride Distance (km) | Avg Booking Value (₹) |
|-----|----------------|----------------------|---------------------|
| Weekday (Mon–Fri) | 29.93 | 26.0 | 449.9 |
| **Weekend (Sat–Sun)** | **43.54** | **26.0** | **655.5** |

⚠️ Ride distances are **identical on all days** (~26 km). The 45% price increase is a **systematic surge multiplier** applied uniformly across all vehicle types.

*Figure 8: Hour × Day-of-week heatmap of cost per km*  
![Cost heatmap](fig8_heatmap_cost_km.png)

The weekend cost premium is visible across every vehicle type:

| Vehicle | Weekend Cost/km (₹) | Weekday Cost/km (₹) | Markup |
|---------|-------------------|--------------------|--------|
| Auto | 43.8 | 28.8 | +52% |
| Go Mini | 44.1 | 27.9 | +58% |
| Go Sedan | 45.8 | 30.0 | +53% |
| Bike | 43.2 | 28.7 | +51% |
| Premier Sedan | 42.6 | 29.0 | +47% |
| eBike | 40.6 | 26.5 | +53% |
| Uber XL | 42.6 | 28.2 | +51% |

### Hourly Cost Variation

*Figure 4: Hourly average ride cost per kilometer*  
![Hourly cost](fig4_hourly_cost_km.png)

Hourly cost/km variation is modest (31–36 ₹/km). The highest hourly rates occur at:
- Hour 00:00 (36.1 ₹/km) — late-night premium
- Hour 09:00 (35.1 ₹/km) — morning peak
- Hour 21:00 (35.0 ₹/km) — post-evening peak

---

## 5. Operational Recommendations

### 🎯 Recommendation 1: Reduce Driver Cancellations During Peak Hours

**Problem:** Driver cancellations account for 18% of all bookings (vs 7% customer cancellations), dominating the 25% total cancellation rate. This wastes platform matching effort and frustrates customers.

**Action items:**
- Implement **peak-hour driver incentives** (bonus per completed ride during 17:00–20:00 and 09:00–11:00) to reduce driver cherry-picking
- Introduce a **driver penalty tier** for repeated cancellations after accepting rides
- Improve **pre-trip information** (customer rating, destination, trip distance) so drivers can make informed acceptance decisions rather than accepting then cancelling

**Expected impact:** Reducing driver cancellations from 18% to 12% would increase completed rides by ~9,000 per year.

### 🎯 Recommendation 2: Maintain Weekend Dynamic Pricing, Monitor for Elasticity

**Problem:** Weekend per-km cost is 45% higher with identical ride distances, yet cancellation rates are the same as weekdays (24.9% vs 25.1%). This suggests customers are price-inelastic on weekends.

**Action items:**
- Continue the weekend surge pricing strategy — it generates ~45% more revenue per ride without degrading completion rates
- Monitor for signs of demand elasticity (e.g., increasing No Driver Found rate on weekends as customers might be price-sensitive)
- Consider **time-tiered pricing within weekends** (e.g., Saturday evening premium > Sunday morning)

### 🎯 Recommendation 3: Optimize Driver Supply Allocation

**Problem:** The 4-hour evening peak (17:00–20:00) handles 29.4% of daily bookings, while the 5-hour night trough (00:00–04:59) handles only 4.5%.

**Action items:**
- **Shift driver supply** from late-night hours (00:00–05:00) to evening peak hours (17:00–20:00) and morning peak (09:00–11:00)
- Offer **time-shift incentives** for drivers who work peak hours
- Reduce driver availability during the 00:00–04:59 trough (currently 7.3% No Driver Found rate — little demand anyway)

### 🎯 Recommendation 4: Address Customer Cancellation Reasons

**Problem:** "Wrong Address" and "Change of plans" are the top customer cancellation reasons.

**Action items:**
- Implement **address verification** (geocoding confirmation) before booking confirmation
- Offer a **free 2-minute cancellation window** to reduce system friction
- Allow customers to **modify destination** post-booking (reducing the "Change of plans" trigger)

### 🎯 Recommendation 5: Prepare for Holiday Demand Surges

**Finding:** 2024-01-26 (India Republic Day, a Friday) had 452 bookings (10% above mean) with a low 22.8% cancellation rate and high 40.6 ₹/km cost.

**Action items:**
- Identify upcoming holidays (Republic Day, Diwali, etc.) and **pre-schedule driver incentives**
- Use historical data to predict demand on holiday dates and ensure adequate supply

---

## 6. Limitations

1. The dataset does not include driver availability or geographical supply data, so we cannot directly measure supply-demand imbalance.
2. The "No Driver Found" status (7%) may capture some true supply shortage but also includes system timeouts.
3. The analysis is observational; causal relationships (e.g., whether surge pricing affects cancellation rates) require controlled experiments.
4. The dataset covers the Delhi NCR region (based on pickup/drop locations); results may not generalize to other markets.

---

## 7. Conclusion

Uber's 2024 booking data reveals **strong intraday peaks** (evening 17:00–20:00 at 29.4% of volume, morning 09:00–11:00 at 17.5%) and **deep troughs** (late-night 00:00–04:59 at 4.5%). The cancellation rate is a stable 25% across all periods, dominated by driver-initiated cancellations (18% of total). The most impactful operational lever is the **45% weekend price premium** which generates significantly higher revenue per kilometer without affecting customer satisfaction metrics. By rebalancing driver supply from trough hours to peak hours and addressing the driver cancellation epidemic, the platform can improve both revenue and customer experience.