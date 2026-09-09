import pandas as pd

# Company names from conversations
conv = db.frame(db.query("SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_state FROM intercom__conversation_enhanced"))
print("Conversation companies unique:", conv['all_contact_company_names'].nunique())
print(conv['all_contact_company_names'].unique())

# Company table
comp = db.frame(db.query("SELECT company_id, company_name, created_at, updated_at, all_company_tags FROM intercom__company_enhanced"))

# Check overlap
conv_companies = set(conv['all_contact_company_names'])
comp_companies = set(comp['company_name'])
print("\nOverlap between conv companies and company table:", len(conv_companies & comp_companies))
print("In conv but not in company table:", conv_companies - comp_companies)

# Check company_metrics for churn signals
metrics = db.frame(db.query("SELECT * FROM intercom__company_metrics"))
print("\ncompany_metrics missing_days distribution:", metrics['missing_days'].value_counts().head())
print("is_date_continuous distribution:", metrics['is_date_continuous'].value_counts())

# Check conversation time range
print("\nConversation created_at range:", conv['conversation_created_at'].min(), conv['conversation_created_at'].max())
print("Conversation last_updated range:", conv['conversation_last_updated_at'].max())

# Check company table created/updated ranges again - updated_at up to 2023-12-31, conversations in 2029?
# So conversations are AFTER the company table. Interesting.
print("\nCompany updated_at range:", comp['updated_at'].min(), comp['updated_at'].max())
print("Company created_at range:", comp['created_at'].min(), comp['created_at'].max())