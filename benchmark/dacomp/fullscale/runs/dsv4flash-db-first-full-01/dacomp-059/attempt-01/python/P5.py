import pandas as pd
import numpy as np

def query_to_df(sql):
    result = db.query(sql)
    e = result['executions'][0]
    rows = db.rows(result)
    return pd.DataFrame(rows, columns=e['columns'])

df_ag = query_to_df("""
    WITH agg AS (
      SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type,
             SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
             SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
             SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
             SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
             CASE
               WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
               WHEN r.account_name LIKE '%Education%' THEN 'Education'
               WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
               WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
               WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
               WHEN r.account_name LIKE '%Food%' THEN 'Food'
               WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
               WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
               WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
               WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
               WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
               WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
               ELSE 'Other'
             END AS industry,
             CASE
               WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
               WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
               WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
               WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
               WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
             END AS channel,
             CASE
               WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
               WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
               WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
               WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
               WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
             END AS strategy,
             ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
      FROM google_ads__ad_group_report r
      GROUP BY r.ad_group_id
      HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
    )
    SELECT * FROM agg
""")
df_ag['is_problem'] = ((df_ag['ctr'] > 0.03587443946188341) & (df_ag['cvr'] < 0.038461538461538464)).astype(int)
print(f"Total ad groups: {len(df_ag)}, Problem: {df_ag['is_problem'].sum()}")

df_kw = query_to_df("""
    SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.clicks, k.impressions, k.conversions, k.spend
    FROM google_ads__keyword_report k
""")
df_kw = df_kw.merge(df_ag[['ad_group_id', 'is_problem', 'industry']], on='ad_group_id', how='left')
df_kw['is_problem'] = df_kw['is_problem'].fillna(0).astype(int)
print(f"Keyword rows: {len(df_kw)}, Problem kw rows: {df_kw['is_problem'].sum()}")

df_ag.to_csv('/work/df_ag.csv', index=False)
df_kw.to_csv('/work/df_kw.csv', index=False)
print("Saved.")