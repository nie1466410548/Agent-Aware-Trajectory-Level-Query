import pandas as pd

# Check conversation date distribution
conv = db.frame(db.query("SELECT conversation_created_at FROM intercom__conversation_enhanced"))
conv['date'] = pd.to_datetime(conv['conversation_created_at'])
print("Conversation date range:", conv['date'].min(), conv['date'].max())
print("\nYear distribution:")
print(conv['date'].dt.year.value_counts().sort_index())
print("\nMonth distribution for 2024:")
conv_2024 = conv[conv['date'].dt.year == 2024]
print(f"Count in 2024: {len(conv_2024)}")

# Check if any conversations are in 2024
print("\nMonth distribution for all years:")
print(conv['date'].dt.year.value_counts().sort_index())

# Hmm, let me check the actual dates more carefully
print("\nAll dates sort:")
print(conv['date'].sort_values().unique()[:30])
print("...")
print(conv['date'].sort_values().unique()[-30:])