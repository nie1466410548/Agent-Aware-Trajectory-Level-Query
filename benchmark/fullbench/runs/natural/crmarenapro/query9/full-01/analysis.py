import json, pandas as pd
from pathlib import Path
cases_path = Path('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query9/full-01/results/66b85b64822a4c2faf96518e7c618744.json')
acct_path = Path('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query9/full-01/results/08334e75d92c46fca88e6ed761c2ec8e.json')
cases = pd.DataFrame(json.loads(cases_path.read_text()))
accounts = pd.DataFrame(json.loads(acct_path.read_text()))
# Clean IDs: data has sporadic leading '#'
for col in ['id','accountid']:
    cases[col] = cases[col].astype(str).str.strip().str.lstrip('#')
accounts['Id'] = accounts['Id'].astype(str).str.strip().str.lstrip('#')
accounts['ShippingState'] = accounts['ShippingState'].astype(str).str.strip().str.upper()
for col in ['createddate','closeddate']:
    cases[col] = pd.to_datetime(cases[col], utc=True, errors='coerce')
cases['status_clean'] = cases['status'].astype(str).str.strip().str.lower()
closed = cases[cases['closeddate'].notna()].copy()
closed['hours'] = (closed['closeddate'] - closed['createddate']).dt.total_seconds()/3600
merged = closed.merge(accounts[['Id','Name','ShippingState']], left_on='accountid', right_on='Id', how='left')
print('closed cases parsed', len(merged), 'unmatched', merged['ShippingState'].isna().sum(), 'min/max created', merged.createddate.min(), merged.createddate.max(), 'min/max closed', merged.closeddate.min(), merged.closeddate.max())
print('negative durations', (merged.hours<0).sum())
anchor = pd.Timestamp('2022-10-26', tz='UTC')
windows = {
    'previous_6_complete_calendar_quarters_2021Q2_to_2022Q3': ('2021-04-01','2022-09-30 23:59:59'),
    'current_plus_prior_5_quarters_Q3_2021_to_now_Q4_2022': ('2021-07-01','2022-10-26 23:59:59'),
    'rolling_18_months': ('2021-04-26','2022-10-26 23:59:59'),
    'rolling_6_quarter_starts_calendar': ('2021-04-01','2022-10-26 23:59:59'),
}
for name,(start,end) in windows.items():
    start=pd.Timestamp(start,tz='UTC'); end=pd.Timestamp(end,tz='UTC')
    print('\n###', name, start, end)
    for basis in ['createddate','closeddate']:
        d=merged[(merged[basis]>=start)&(merged[basis]<=end)].copy()
        g=d.groupby('ShippingState').agg(n=('hours','size'), avg_hours=('hours','mean'), median_hours=('hours','median'), min_hours=('hours','min'), max_hours=('hours','max')).sort_values(['avg_hours','n'])
        print('\nBasis', basis, 'rows', len(d))
        print(g.head(15).to_string(float_format=lambda x:f'{x:.2f}'))
        print('quarter counts')
        print(d.assign(q=d[basis].dt.to_period('Q')).groupby('q').size().to_string())
