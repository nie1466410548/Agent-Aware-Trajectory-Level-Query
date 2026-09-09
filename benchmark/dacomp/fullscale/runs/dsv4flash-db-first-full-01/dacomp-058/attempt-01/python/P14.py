import pandas as pd
import numpy as np
import json

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Get full campaign health data
r = db.query("""
WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, ROUND(AVG(cost),0) AS avg_monthly_cost, ROUND(SUM(cost),0) AS total_cost,
  ROUND(AVG(roas),3) AS avg_roas, ROUND(AVG(quality_score),2) AS avg_qs,
  ROUND(AVG(impression_share),3) AS avg_is, ROUND(AVG(ctr),5) AS avg_ctr,
  ROUND(AVG(conversion_rate),5) AS avg_cvr, ROUND(AVG(cpc),2) AS avg_cpc,
  ROUND(AVG(cost_per_conversion),2) AS avg_cpa,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score
""", parameters=[])
campaigns = db.frame(r)

def risk_level(h):
    if h < 30: return 'Critical'
    if h < 36: return 'High'
    if h < 45: return 'Medium'
    return 'Low'
campaigns['risk_level'] = campaigns['health_score'].apply(risk_level)

# Get device and geo data for problematic
r = db.query("SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__device_report WHERE campaign_id IN ({}) GROUP BY campaign_id, device_type ORDER BY campaign_id, device_type".format(','.join(str(x) for x in problematic_ids)), parameters=[])
dev = db.frame(r)
r = db.query("SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__geo_report WHERE campaign_id IN ({}) GROUP BY campaign_id, geo_target ORDER BY campaign_id, cost DESC".format(','.join(str(x) for x in problematic_ids)), parameters=[])
geo = db.frame(r)

# Diagnosis per campaign
diagnoses = []
for _, row in campaigns[campaigns['campaign_id'].isin(problematic_ids)].iterrows():
    cid = row['campaign_id']
    name = row['campaign_name']
    ctype = row['campaign_type']
    bid = row['bidding_strategy']
    ind = row['industry']
    hs = row['health_score']
    rl = row['risk_level']
    ce = row['cost_eff']
    cq = row['conv_quality']
    cp = row['competitive']
    avg_roas = row['avg_roas']
    avg_qs = row['avg_qs']
    avg_is = row['avg_is']
    avg_ctr = row['avg_ctr']
    avg_cvr = row['avg_cvr']
    avg_cpc = row['avg_cpc']
    avg_cpa = row['avg_cpa']
    monthly_cost = row['avg_monthly_cost']
    
    # Core problem diagnosis
    problems = []
    if ce < 40:
        problems.append("Cost efficiency severely low (score {:.1f})".format(ce))
    if cq < 25:
        problems.append("Conversion quality critically low (score {:.1f})".format(cq))
    if cp < 20:
        problems.append("Competitiveness very weak (score {:.1f})".format(cp))
    if avg_roas < 0.6:
        problems.append("Chronic low ROAS ({:.2f}) indicates severe cost-value imbalance".format(avg_roas))
    if avg_qs < 5:
        problems.append("Low quality score ({:.1f}) suggests poor ad relevance and landing page experience".format(avg_qs))
    if avg_is < 0.35:
        problems.append("Low impression share ({:.1%}) indicates budget or rank limitations".format(avg_is))
    if avg_ctr < 0.01:
        problems.append("Very low CTR ({:.4f}) suggests poor ad copy or targeting".format(avg_ctr))
    if avg_cvr < 0.01:
        problems.append("Very low conversion rate ({:.4f}) suggests landing page or audience issues".format(avg_cvr))
    if avg_cpa > 80:
        problems.append("High cost per conversion (${:.0f}) exceeds sustainable thresholds".format(avg_cpa))
    
    core_problem = "; ".join(problems)
    
    # Device-level optimization
    dev_cid = dev[dev['campaign_id']==cid]
    dev_roas = dict(zip(dev_cid['device_type'], dev_cid['avg_roas']))
    max_roas_dev = max(dev_roas, key=dev_roas.get) if dev_roas else 'N/A'
    min_roas_dev = min(dev_roas, key=dev_roas.get) if dev_roas else 'N/A'
    
    device_rec = "Reduce budget on {} (ROAS {:.2f}); shift to {} (ROAS {:.2f})".format(
        min_roas_dev, dev_roas[min_roas_dev], max_roas_dev, dev_roas[max_roas_dev]) if dev_roas and min_roas_dev != max_roas_dev else "Maintain balanced device allocation"
    
    # Geo-level optimization
    geo_cid = geo[geo['campaign_id']==cid]
    geo_roas = dict(zip(geo_cid['geo_target'], geo_cid['avg_roas']))
    if geo_roas:
        worst_geo = min(geo_roas, key=geo_roas.get)
        best_geo = max(geo_roas, key=geo_roas.get)
        geo_rec = "Reduce spend in {} (ROAS {:.2f}); increase focus on {} (ROAS {:.2f})".format(worst_geo, geo_roas[worst_geo], best_geo, geo_roas[best_geo])
    else:
        geo_rec = "No geo data available"
    
    # Budget reallocation recommendation
    budget_rec = "Reduce monthly budget from ${:.0f} by 20-30%; reallocate to healthier campaigns. Focus on cost-efficient channels.".format(monthly_cost)
    
    # Keyword strategy (if available)
    keyword_rec = "Review and pause low-performing keywords with high CPA; add negative keywords; expand high-converting long-tail terms."
    
    # Bidding strategy
    if bid in ['Target ROAS', 'Target CPA']:
        bidding_rec = "Consider switching to {} or Enhanced CPC to regain spend control; current target-based strategy is failing to deliver ROI".format('Manual CPC' if bid in ['Target ROAS'] else 'Maximize Conversions')
    else:
        bidding_rec = "Review current {} strategy; consider lowering bids or switching to target-based bidding with realistic performance targets".format(bid)
    
    diagnoses.append({
        'Campaign ID': cid,
        'Campaign Name': name,
        'Type': ctype,
        'Bidding': bid,
        'Industry': ind,
        'Health Score': round(hs, 1),
        'Risk Level': rl,
        'Cost Eff': round(ce, 1),
        'Conv Quality': round(cq, 1),
        'Competitive': round(cp, 1),
        'Avg ROAS': round(avg_roas, 2),
        'Avg Monthly Cost': f"${monthly_cost:,.0f}",
        'Core Problem': core_problem,
        'Budget Rec': budget_rec,
        'Keyword Rec': keyword_rec,
        'Geo Rec': geo_rec,
        'Device Rec': device_rec,
        'Bidding Rec': bidding_rec
    })

diag_df = pd.DataFrame(diagnoses)
print("COMPREHENSIVE OPTIMIZATION RECOMMENDATIONS")
print("===========================================")
for _, d in diag_df.iterrows():
    print(f"\nCampaign {d['Campaign ID']}: {d['Campaign Name']}")
    print(f"  Health Score: {d['Health Score']} - {d['Risk Level']} Risk")
    print(f"  Dimensions: CostEff={d['Cost Eff']}, ConvQuality={d['Conv Quality']}, Comp={d['Competitive']}")
    print(f"  ROAS: {d['Avg ROAS']}, Avg Monthly Cost: {d['Avg Monthly Cost']}")
    print(f"  Core Problem: {d['Core Problem']}")
    print(f"  Budget: {d['Budget Rec']}")
    print(f"  Keywords: {d['Keyword Rec']}")
    print(f"  Geo: {d['Geo Rec']}")
    print(f"  Device: {d['Device Rec']}")
    print(f"  Bidding: {d['Bidding Rec']}")

# Save as JSON for reference
diag_df.to_json('work/diagnosis.json', orient='records', indent=2)
print("\n\nSaved to diagnosis.json")