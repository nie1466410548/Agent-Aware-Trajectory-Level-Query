import pandas as pd

# Load the saved analysis file
evdf = pd.read_csv('/work/event_analysis.csv')
print("Events with data in window:")
cols = ['company_name','event_at','event_type','prev_plan','new_plan','before_days','after_days','before_convs','after_convs','before_bugs','after_bugs','before_outages','after_outages','before_sla','after_sla','before_rating','after_rating']
print(evdf[cols].to_string())