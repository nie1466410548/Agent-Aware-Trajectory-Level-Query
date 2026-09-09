import pandas as pd, numpy as np, json, re, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':9, 'figure.dpi':110})

with open('/results/S18.rows.jsonl') as f:
    peer = pd.DataFrame([json.loads(l) for l in f], columns=["Job Title","Company Name","Company Type","Industry","Salary Range","Benefits","Education Requirement","Work Experience Requirement","Age Requirement","Gender Requirement","Employment Type","Work Location","Job Description"])

def parse_range(s):
    if s is None or (isinstance(s,float) and np.isnan(s)) or (isinstance(s,str) and s.strip()==''):
        return None
    nums = [int(x.replace(',','')) for x in re.findall(r'[\d,]+', str(s))]
    if not nums: return None
    return (nums[0], nums[1]) if len(nums)>=2 else (nums[0], nums[0])

peer['lo'] = peer['Salary Range'].apply(lambda s: parse_range(s)[0] if parse_range(s) else np.nan)
peer['hi'] = peer['Salary Range'].apply(lambda s: parse_range(s)[1] if parse_range(s) else np.nan)
peer['mid'] = (peer['lo']+peer['hi'])/2

# ---- Figure 1: Salary range comparison ----
fig, ax = plt.subplots(figsize=(9.5, 6.5))
rows = peer.sort_values('mid').copy()
y = np.arange(len(rows))
target_lo, target_hi = 30000, 50000
for i in range(len(rows)):
    r = rows.iloc[i]
    if not np.isnan(r['lo']):
        ax.barh(i, r['hi'] - r['lo'], left=r['lo'], height=0.55, color='#2c7fb8', alpha=0.75, edgecolor='k', lw=0.4)
ax.barh(-1.2, target_hi - target_lo, left=target_lo, height=0.75, color='#d73027', alpha=0.9, edgecolor='k', label='Target: 30,000–50,000 yuan/month')
labels = [str(rows.iloc[i]['Job Title'])[:48] for i in range(len(rows))] + ['TARGET: PICC Life After-sales Dept Establishment Manager']
ax.set_yticks(list(y) + [-1.2]); ax.set_yticklabels(labels, fontsize=7.5)
ax.set_xlabel('Monthly salary (yuan), headline range')
ax.set_title('Salary ranges: target vs 16 comparable Xiamen insurance-industry postings')
ax.axvline(6500, color='gray', ls='--', lw=0.8, label='Peer median 6,500')
ax.legend(fontsize=7.5, loc='lower right')
ax.set_xlim(0, 52000)
plt.tight_layout()
plt.savefig('fig1_salary_comparison.png')
plt.close()
print('fig1 done')

# ---- Figure 2: Education requirement distribution ----
fig, ax = plt.subplots(figsize=(6.5, 4.2))
edu_counts = peer['Education Requirement'].fillna('Not specified').value_counts()
edu_order = ['Bachelor\'s degree or above','College degree or above','Vocational school or above','No limit']
edu_counts = edu_counts.reindex([e for e in edu_order if e in edu_counts.index])
colors = ['#2c7fb8','#41b6c4','#a1dab4','#c7e9b4'][:len(edu_counts)]
bars = ax.barh(edu_counts.index, edu_counts.values, color=colors, edgecolor='k', lw=0.5)
for b,v in zip(bars, edu_counts.values):
    ax.text(v+0.05, b.get_y()+b.get_height()/2, str(v), va='center', fontsize=9)
ax.set_xlabel('Number of peer postings (n=16)')
ax.set_title('Education requirements among Xiamen insurance peers\n(Target: Associate degree or above)')
ax.set_xlim(0, 10.5)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('fig2_education.png')
plt.close()
print('fig2 done')

# ---- Figure 3: Benefit coverage ----
benefit_categories = {
    'Commercial insurance': ['Commercial insurance','commercial insurance','商业保险'],
    'Five social insurances & housing fund': ['五险一金','Five social insurances','social insurances','住房'],
    'Paid annual leave': ['paid annual leave','Paid annual leave','带薪年假'],
    'Performance bonus': ['performance bonus','Performance bonus','绩效奖金'],
    'Communication allowance': ['communication allowance','Communication allowance','通信补贴'],
    'Professional training': ['professional training','Professional training','专业培训','training'],
    'Meal allowance': ['meal allowance','Meal allowance','餐补'],
    'Holiday benefits': ['holiday benefits','Holiday benefits','节日福利'],
    'Regular medical checkup': ['regular medical check','Regular medical check','定期体检'],
    'Employee travel': ['employee travel','Employee travel','员工旅游'],
    'Transportation allowance': ['transportation allowance','Transportation allowance','交通补贴'],
    'Flexible working hours': ['flexible working','Flexible working','弹性工作'],
    'Year-end bonus': ['year-end bonus','Year-end bonus','年终奖'],
}
cov = {}
for cat, kws in benefit_categories.items():
    cov[cat] = sum(1 for _, r in peer.iterrows() if any(k.lower() in str(r['Benefits']).lower() for k in kws))
cov = pd.Series(cov).sort_values()
target_text = 'commercial insurance, business trip allowance, holiday benefits, professional training, flexible working hours, employee travel, overseas opportunities, no overtime, no probation period, three insurances and one fund'
target_has = {k: any(kw.lower() in target_text.lower() for kw in v) for k,v in benefit_categories.items()}

fig, ax = plt.subplots(figsize=(8, 5.2))
colors = ['#d73027' if target_has[k] else '#636363' for k in cov.index]
bars = ax.barh(cov.index, cov.values/len(peer), color=colors, edgecolor='k', lw=0.5)
for b, v, k in zip(bars, cov.values, cov.index):
    tag = ' ✓ target' if target_has[k] else ''
    ax.text(v+0.01, b.get_y()+b.get_height()/2, f'{v}/16{tag}', va='center', fontsize=8)
ax.set_xlabel('Share of 16 insurance peer postings offering benefit')
ax.set_title('Benefit-package comparison (red = offered by target posting)')
ax.set_xlim(0, 1.02)
plt.tight_layout()
plt.savefig('fig3_benefits.png')
plt.close()
print('fig3 done')

print('all figures saved to /work/')
for f in os.listdir('.'):
    if f.endswith('.png'):
        print(f, os.path.getsize(f))