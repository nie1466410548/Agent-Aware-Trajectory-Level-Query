import pandas as pd, numpy as np, json, re

# Reload peer data
cols18 = ["Job Title","Company Name","Company Type","Industry","Salary Range","Benefits",
          "Education Requirement","Work Experience Requirement","Age Requirement","Gender Requirement",
          "Employment Type","Work Location","Job Description"]
with open('/results/S18.rows.jsonl') as f:
    peer = pd.DataFrame([json.loads(l) for l in f], columns=cols18)

print("=== EDUCATION REQUIREMENT DISTRIBUTION ===")
edu = peer['Education Requirement'].fillna('Not specified').value_counts()
print(edu.to_string())

print("\n=== WORK EXPERIENCE REQUIREMENT DISTRIBUTION ===")
exp = peer['Work Experience Requirement'].fillna('Not specified').value_counts()
print(exp.to_string())

print("\n=== AGE REQUIREMENT DISTRIBUTION ===")
age = peer['Age Requirement'].fillna('Not specified').value_counts()
print(age.to_string())

print("\n=== COMPANY TYPE DISTRIBUTION ===")
ct = peer['Company Type'].value_counts()
print(ct.to_string())

print("\n=== EMPLOYMENT TYPE ===")
et = peer['Employment Type'].value_counts()
print(et.to_string())

# Benefits analysis
all_benefits = []
benefit_items = ['五险一金','Five social insurances, housing provident fund','Commercial insurance','商业保险',
                 'Housing provident fund','住房公积金','paid annual leave','带薪年假','performance bonus','绩效奖金',
                 'year-end bonus','年终奖','professional training','专业培训','training','培训','meal allowance','餐补',
                 '交通补贴','transportation allowance','通信补贴','communication allowance','high temperature','高温补贴',
                 'holiday benefits','节日福利','regular medical check-up','定期体检','employee travel','员工旅游',
                 'flexible working hours','弹性工作']
# Check for common benefit categories
benefit_categories = {
    'Five social insurances & housing fund': ['五险一金','Five social insurances, housing provident fund','social insurances','住房'],
    'Commercial insurance': ['商业保险','Commercial insurance','commercial insurance'],
    'Paid annual leave': ['带薪年假','paid annual leave','Paid annual leave'],
    'Performance bonus': ['绩效奖金','performance bonus','Performance bonus'],
    'Year-end bonus': ['年终奖','year-end bonus','Year-end bonus'],
    'Professional training': ['专业培训','professional training','Professional training','training'],
    'Meal allowance': ['餐补','meal allowance','Meal allowance'],
    'Communication allowance': ['通信补贴','communication allowance','Communication allowance'],
    'Transportation allowance': ['交通补贴','transportation allowance'],
    'Holiday benefits': ['节日福利','holiday benefits','Holiday benefits'],
    'Regular medical checkup': ['定期体检','regular medical check','regular medical check-ups'],
    'Employee travel': ['员工旅游','employee travel','Employee travel'],
    'Flexible working hours': ['弹性工作','flexible working hours','Flexible working','flexible work arrangements'],
    'Overtime pay': ['加班','overtime pay','Overtime pay'],
}

benefit_matrix = {}
for cat, keywords in benefit_categories.items():
    count = 0
    for _, r in peer.iterrows():
        b = str(r['Benefits'])
        if any(k.lower() in b.lower() for k in keywords):
            count += 1
    benefit_matrix[cat] = count

print("\n=== BENEFIT COVERAGE AMONG 16 PEER JOBS ===")
for cat, cnt in sorted(benefit_matrix.items(), key=lambda x:-x[1]):
    print(f"{cat:40s}: {cnt}/{len(peer)}")

# Target position benefit check
target_benefits = "Commercial insurance, business trip allowance, holiday benefits, professional training, flexible working hours, employee travel, overseas opportunities, no overtime, no probation period"
target_desc = "Working hours: Monday to Friday, weekends off; except for the morning hours, the rest of the time can be arranged freely. Job requirements: 1. Age 25–50 years old; 2. Associate degree or above; 3. Personal after-tax income over 50,000 yuan in the past year; 4. At least 3 years of experience in the same industry, or at least 1 year of experience as a supervisor in the same industry. Compensation: 1. Full support from company resources; 2. Provide three insurances and one fund (housing provident fund); 3. Four promotion opportunities per year"

print("\n=== TARGET POSITION REQUIREMENTS ===")
print(f"Education: Associate degree or above")
print(f"Experience: At least 3 years in same industry or 1 year as supervisor (also: 2 years+ in table)")
print(f"Age: 25-50")
print(f"Language: None")
print(f"Gender: None")
print(f"Working hours: Mon-Fri, flexible after morning")
print(f"Benefits: Commercial insurance, business trip allowance, holiday benefits, professional training, flexible working hours, employee travel, overseas opportunities, no overtime, no probation period. Also: three insurances and one fund (housing provident fund)")