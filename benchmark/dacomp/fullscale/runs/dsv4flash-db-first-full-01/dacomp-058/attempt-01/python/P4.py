import os, glob
print("exists /results:", os.path.exists('/results'))
if os.path.exists('/results'):
    print(os.listdir('/results')[:20])
# Also try to use db.query and db.frame to fetch data directly
# Test db.frame with a simple query
r = db.query("SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry, COUNT(*) n FROM google_ads__campaign_report GROUP BY campaign_id", parameters=[])
print("rows type:", type(r))
print(r.keys())
df = db.frame(r)
print(df.shape)
print(df.head())