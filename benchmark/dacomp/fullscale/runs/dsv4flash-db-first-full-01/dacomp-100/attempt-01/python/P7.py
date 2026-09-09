import pandas as pd

# Get company names from conversation table
conv = db.frame(db.query("SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced"))
conv_names = set(conv['all_contact_company_names'].dropna())
print("Conversation company names count:", len(conv_names))
print("Sample:", sorted(conv_names)[:10])

# Get company names from company table
comp = db.frame(db.query("SELECT company_name FROM intercom__company_enhanced"))
comp_names = set(comp['company_name'])
print("\nCompany table names count:", len(comp_names))
print("Sample:", sorted(comp_names)[:10])

# Overlap
overlap = conv_names & comp_names
print("\nOverlap count:", len(overlap))
print("Overlap sample:", sorted(overlap)[:10])

# Companies in conv but not in company table
only_conv = conv_names - comp_names
print("\nOnly in conv:", only_conv)

# Companies in company table but not in conv
only_comp = comp_names - conv_names
print("\nOnly in company table (first 10):", sorted(only_comp)[:10])
print("Total only in company table:", len(only_comp))