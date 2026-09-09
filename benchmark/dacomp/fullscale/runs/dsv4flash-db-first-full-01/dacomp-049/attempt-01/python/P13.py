import pandas as pd, json, re
with open('/results/S18.rows.jsonl') as f:
    peer = pd.DataFrame([json.loads(l) for l in f], columns=["Job Title","Company Name","Company Type","Industry","Salary Range","Benefits","Education Requirement","Work Experience Requirement","Age Requirement","Gender Requirement","Employment Type","Work Location","Job Description"])
print("PEER LIST FOR REPORT:")
for _, r in peer.iterrows():
    print(f"• {str(r['Job Title'])[:70]} | {str(r['Company Name'])[:50]} | Sal: {str(r['Salary Range'])[:40]} | Edu: {str(r['Education Requirement'])[:35]} | Exp: {str(r['Work Experience Requirement'])[:30]}")
print(f"\nTotal: {len(peer)} peer positions")